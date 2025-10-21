try:
    import urequests as requests
except ImportError:
    import requests
import utime
import ntptime
from secrets import DB_CLIENT_ID, DB_CLIENT_SECRET, LOCAL_EVA_NO, DIRECTION

class TrainFetcher:
    def __init__(self):
        self.url = "https://apis.deutschebahn.com/db-api-marketplace/apis/timetables/v1"
        self.headers = {
            "DB-Client-Id": DB_CLIENT_ID,
            "DB-Api-Key": DB_CLIENT_SECRET,
            "accept": "application/xml"
        }
    
    def _get_current_time(self):
        """Get current time with proper German timezone handling"""
        try:
            ntptime.settime()
        except Exception as e:
            print(f"NTP sync failed: {e}")
            # Fallback: use local time if NTP fails
            pass
        utc_time = utime.localtime()
        y, m, d, hh, mm, ss, wd, yd = utc_time
        
        # Determine if we're in daylight saving time (CEST) or standard time (CET)
        # DST in Germany: last Sunday in March to last Sunday in October
        offset_hours = self._get_german_timezone_offset(y, m, d, hh)
        
        # Apply timezone offset
        hh = (hh + offset_hours) % 24
        if hh < offset_hours and offset_hours > 0:
            d += 1
        
        return f"{y % 100:02d}{m:02d}{d:02d}{hh:02d}{mm:02d}"

    def _get_german_timezone_offset(self, year, month, day, hour):
        """Calculate German timezone offset (CET/CEST) from UTC"""
        # Standard time (CET): UTC+1
        # Daylight saving time (CEST): UTC+2
        
        # DST starts on last Sunday in March at 02:00 CET (01:00 UTC)
        # DST ends on last Sunday in October at 03:00 CEST (01:00 UTC)
        
        # Before March or after October: CET (UTC+1)
        if month < 3 or month > 10:
            return 1
        
        # April to September: CEST (UTC+2)
        if month > 3 and month < 10:
            return 2
        
        # March: Check if we're past the last Sunday
        if month == 3:
            last_sunday_march = self._get_last_sunday_of_month(year, 3)
            if day > last_sunday_march:
                return 2
            elif day == last_sunday_march and hour >= 1:  # 01:00 UTC = 02:00 CET
                return 2
            else:
                return 1
        
        # October: Check if we're before the last Sunday
        if month == 10:
            last_sunday_october = self._get_last_sunday_of_month(year, 10)
            if day < last_sunday_october:
                return 2
            elif day == last_sunday_october and hour < 1:  # Before 01:00 UTC = 03:00 CEST
                return 2
            else:
                return 1
        
        return 1  # Default to CET

    def _get_last_sunday_of_month(self, year, month):
        """Get the day number of the last Sunday in a given month"""
        # Get the last day of the month
        if month == 12:
            next_month_first = utime.mktime((year + 1, 1, 1, 0, 0, 0, 0, 0))
        else:
            next_month_first = utime.mktime((year, month + 1, 1, 0, 0, 0, 0, 0))
        
        # Go back one day to get last day of current month
        last_day_timestamp = next_month_first - 86400  # 24 * 60 * 60 seconds
        last_day_struct = utime.localtime(last_day_timestamp)
        last_day = last_day_struct[2]
        last_weekday = last_day_struct[6]  # 0=Monday, 6=Sunday
        
        # Calculate days to subtract to get to last Sunday
        days_back = last_weekday if last_weekday != 6 else 0
        if last_weekday == 6:  # If last day is Sunday
            return last_day
        else:  # Go back to find last Sunday
            return last_day - (last_weekday + 1)
    
    def _fetch_xml(self, date_str, hour_str):
        """Fetch XML data for specific date/hour"""
        try:
            response = requests.get(
                f"{self.url}/plan/{LOCAL_EVA_NO}/{date_str}/{hour_str}", 
                headers=self.headers,
                timeout=5
            )
            
            if getattr(response, "status_code", 200) != 200:
                response.close()
                return None
            
            xml = response.text
            response.close()
            return xml
            
        except Exception as e:
            print(f"API Error: {e}")
            try:
                response.close()
            except:
                pass
            return None
    
    def _fetch_changes_xml(self):
        """Fetch changes XML data"""
        try:
            response = requests.get(
                f"{self.url}/fchg/{LOCAL_EVA_NO}", 
                headers=self.headers,
                timeout=5
            )
            
            if getattr(response, "status_code", 200) != 200:
                response.close()
                return None
            
            xml = response.text
            response.close()
            return xml
            
        except Exception as e:
            print(f"Changes API Error: {e}")
            try:
                response.close()
            except:
                pass
            return None
    
    def _parse_trains_from_xml(self, xml, current_time):
        """Parse all trains from XML that match direction and are in future"""
        trains = []
        
        pos = 0
        s_start = 0
        while True:
            # Find next <s> tag (station stop)
            s_start = xml.find('<s ', s_start)
            if s_start == -1:
                break
                
            s_end = xml.find('</s>', s_start)
            if s_end == -1:
                break
                
            section = xml[s_start:s_end + 4]  # Include </s>
            
            # Extract train info
            train_info = self._extract_train_info(section, current_time)
            if train_info:
                direction_path = train_info['direction']
                # print(f"Train at {train_info['actual_time']} P{train_info['platform']} -> {direction_path}")
                # Check if DIRECTION is in the route
                if DIRECTION in direction_path:
                    trains.append(train_info)
            s_start = s_end + 1
        
        return trains
    
    def _extract_train_info(self, section, current_time):
        """Extract train information from XML section"""
        # Extract stop_id
        id_start = section.find('id="') + 4
        id_end = section.find('"', id_start)
        stop_id = section[id_start:id_end]
        
        # Find departure tag
        dp_pos = section.find('<dp ')
        if dp_pos == -1:
            return None

        # Find the end of the <dp ...> tag (self-closing or not)
        dp_tag_end = section.find('>', dp_pos)
        dp_tag = section[dp_pos:dp_tag_end]

        # Extract time, line, platform, and ppth from <dp ...>
        def extract_attr(tag, attr):
            start = tag.find(f'{attr}="')
            if start == -1:
                return ""
            start += len(attr) + 2
            end = tag.find('"', start)
            return tag[start:end]

        train_time = extract_attr(dp_tag, "pt")
        line = extract_attr(dp_tag, "l")
        platform = extract_attr(dp_tag, "pp")
        direction_extracted = extract_attr(dp_tag, "ppth")
        
        # Check if train is in future
        if train_time <= current_time:
            return None
        
        return {
            "line": line,
            "time": train_time,
            "platform": platform,
            "stop_id": stop_id,
            "direction": direction_extracted,  # Add for debugging
            "display_time": f"{train_time[6:8]}:{train_time[8:10]}",
            "scheduled_time": f"{train_time[6:8]}:{train_time[8:10]}",
            "actual_time": f"{train_time[6:8]}:{train_time[8:10]}",
            "delay_minutes": 0,
            "cancelled": False,
            "platform_changed": False
        }
    
    def _apply_changes_to_train(self, train_info, changes_xml):
        """Apply changes from changes XML to train info"""
        if not changes_xml:
            return train_info
        
        stop_id = train_info["stop_id"]
        stop_pattern = f'<s id="{stop_id}"'
        s_start = changes_xml.find(stop_pattern)
        
        if s_start == -1:
            return train_info  # No changes found
        
        s_end = changes_xml.find('</s>', s_start)
        if s_end == -1:
            return train_info
        
        section = changes_xml[s_start:s_end]
        
        # Find departure changes
        dp_pos = section.find('<dp ')
        if dp_pos == -1:
            return train_info
        
        dp_end = section.find('/>', dp_pos)
        if dp_end == -1:
            return train_info
        
        dp_tag = section[dp_pos:dp_end]
        
        # Check for cancellation
        if 'clt=' in dp_tag:
            train_info["cancelled"] = True
            train_info["actual_time"] = "CANCELLED" # TODO: Something that will fit in 8 chars
            return train_info
        
        # Check for time change (delay)
        ct_start = dp_tag.find('ct="')
        if ct_start != -1:
            ct_start += 4
            ct_end = dp_tag.find('"', ct_start)
            new_time = dp_tag[ct_start:ct_end]
            
            if len(new_time) == 10:
                train_info["actual_time"] = f"{new_time[6:8]}:{new_time[8:10]}"
                
                # Calculate delay
                original_hhmm = int(train_info["time"][6:8]) * 60 + int(train_info["time"][8:10])
                new_hhmm = int(new_time[6:8]) * 60 + int(new_time[8:10])
                delay = new_hhmm - original_hhmm
                
                if delay > 0:
                    train_info["delay_minutes"] = delay
        
        # Check for platform change
        cp_start = dp_tag.find('cp="')
        if cp_start != -1:
            cp_start += 4
            cp_end = dp_tag.find('"', cp_start)
            new_platform = dp_tag[cp_start:cp_end]
            train_info["platform"] = new_platform
            train_info["platform_changed"] = True
        
        return train_info
    
    def get_next_trains(self, count=2):
        """Get next trains (default 2)"""
        current_time = self._get_current_time()
        # print(f"Looking for trains after: {current_time[6:8]}:{current_time[8:10]}")
        # print(f"Looking for direction: '{DIRECTION}'")
        
        all_trains = []
        
        # Get current time parts for API calls
        yy, mm, dd, hh = current_time[:2], current_time[2:4], current_time[4:6], int(current_time[6:8])
        
        # Search current and next hours
        for hour_offset in range(3):
            search_hour = (hh + hour_offset) % 24
            date_str = f"{yy}{mm}{dd}"
            hour_str = f"{search_hour:02d}"
            
            print(f"Searching hour: {hour_str}")
            xml = self._fetch_xml(date_str, hour_str)
            if xml:
                trains_in_hour = self._parse_trains_from_xml(xml, current_time)
                all_trains.extend(trains_in_hour)
                
                # Stop if we have enough trains
                if len(all_trains) >= count:
                    break
            else:
                print(f"No XML data for hour {hour_str}")
        
        if not all_trains:
            return []
        
        # Sort by time and take requested count
        all_trains.sort(key=lambda x: x['time'])
        next_trains = all_trains[:count]
        
        # Apply changes to all trains
        changes_xml = self._fetch_changes_xml()
        for train in next_trains:
            self._apply_changes_to_train(train, changes_xml)
        
        return next_trains
    
    def get_next_train(self):
        """Get only the next train"""
        trains = self.get_next_trains(1)
        return trains[0] if trains else None
    
    def format_train_display(self, train_info):
        """Format train info for display"""
        if not train_info:
            return "No trains"
        
        time = train_info["actual_time"]
        platform = train_info["platform"]
        direction = train_info.get("direction", "?")
        
        if train_info["cancelled"]:
            return f"CANCELLED"
        else:
            return f"{time} P{platform} -> {direction}"
    
    def format_trains_display(self, trains):
        """Format multiple trains for display"""
        if not trains:
            return "No trains"
        
        result = []
        for train in trains:
            result.append(self.format_train_display(train))
        
        return "\n".join(result)

# Usage functions
def get_train_info():
    """Get next train as dictionary"""
    fetcher = TrainFetcher()
    return fetcher.get_next_train()

def get_trains_info(count=2):
    """Get next trains as list of dictionaries"""
    fetcher = TrainFetcher()
    return fetcher.get_next_trains(count)

def get_train_display():
    """Get formatted train display string"""
    fetcher = TrainFetcher()
    train = fetcher.get_next_train()
    return fetcher.format_train_display(train)

if __name__ == "__main__":
    fetcher = TrainFetcher()
    
    # Get train info as dictionaries
    print("=== TRAIN DICTIONARIES ===")
    trains = fetcher.get_next_trains(2)
    # for i, train in enumerate(trains):
    #     print(f"Train {i+1}: {train}")
    
    # print("\n=== FORMATTED DISPLAY ===")
    print(fetcher.format_trains_display(trains))