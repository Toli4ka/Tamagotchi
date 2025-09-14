
#TODO clean up the code
#TODO make the code more robust (error handling, edge cases) 
#TODO fetch second next trip

try:
    import urequests as requests
except ImportError:
    import requests

from secrets import DB_CLIENT_ID, DB_CLIENT_SECRET, LOCAL_EVA_NO, DIRECTION
from xml_parser import _parse_departures, _parse_changes
from time_utils import _now_yymmdd, _now_hour, _now_yymmddhhmm

class DeutscheBahn:
    def __init__(self):
        self.url = "https://apis.deutschebahn.com/db-api-marketplace/apis/timetables/v1"
        self.headers = {
                "DB-Client-Id": DB_CLIENT_ID,
                "DB-Api-Key": DB_CLIENT_SECRET,
                "accept": "application/xml"
            }

    def get_trips_by_hour(self, date, hour):
        """ date in format YYMMDD, hour in format HH"""
        try:
            response = requests.get(f"{self.url}/plan/{LOCAL_EVA_NO}/{date}/{hour}", headers=self.headers)
            if getattr(response, "status_code", 200) != 200:
                raise Exception("Bad HTTP status: {}".format(response.status_code))
            xml_text = response.text
        except Exception as e:
            print("Error fetching trips:", e)
            try:
                response.close()
            except Exception:
                pass
            return []
        finally:
            try:
                response.close()
            except Exception:
                pass
        return _parse_departures(xml_text)
    
    def filter_direction(self, direction, date, hour):
        planned_trips = self.get_trips_by_hour(date, hour)
        filtered_trips = []
        for trip in planned_trips:
            departure_info = trip.get("departure", "")
            planned_path = departure_info.get("planned_path", "") if departure_info else ""
            if direction in planned_path:
                filtered_trips.append(trip)
        return filtered_trips
    
    def sort_trips_by_time(self, trips):
        def sort_by_time(item):
            departure_info = item.get("departure", {})
            return departure_info.get("planned_time", "")
        trips.sort(key=sort_by_time)
        return trips
    
    def find_next_trip(self, direction):
        """
        Finds the next trip in the given direction after the current time.
        """
        date = _now_yymmdd()
        hour = _now_hour()
        time_now = _now_yymmddhhmm()
        for i in range(5):
            filtered_trips = self.filter_direction(direction, date, hour)
            sorted_trips = self.sort_trips_by_time(filtered_trips)
            for trip in sorted_trips:
                departure_info = trip.get("departure", {})
                planned_departure = departure_info.get("planned_time", "")
                if planned_departure and planned_departure > time_now:
                    print(f"Next trip to {direction}: {planned_departure}")
                    return trip
            hour = str((int(hour) + 1) % 24)                    
        print(f"No more trips to {direction} today.")
        return
    
    def get_changes(self):
        try:
            response = requests.get(f"{self.url}/fchg/{LOCAL_EVA_NO}", headers=self.headers)
            if getattr(response, "status_code", 200) != 200:
                raise Exception("Bad HTTP status: {}".format(getattr(response, "status_code", "unknown")))
            xml_text = response.text
        except Exception as e:
            print("Error fetching changes:", e)
            try:
                response.close()
            except Exception:
                pass
            return []
        finally:
            try:
                response.close()
            except Exception:
                pass
        return _parse_changes(xml_text)
    
    def lookup_trip_changes(self, trip):
        if not trip:
            return None
        stop_id = trip.get("stop_id")
        changes = self.get_changes()
        for change in changes:
            if change.get("stop_id") == stop_id:
                print(f"Changes for trip {stop_id}: {change}")
                return change
        print(f"No changes for trip {stop_id}.")
        return None

    def display_time(self, str_yymmddhhmm):
        formatted_time = "{}:{}".format(str_yymmddhhmm[6:8], str_yymmddhhmm[8:10]) if len(str_yymmddhhmm) == 10 else "Unknown"
        return formatted_time
    
    def get_trip_info(self, trip):
        if not trip:
            return "No trip info available."
        departure_info = trip.get("departure", {})
        changes = self.lookup_trip_changes(trip)
        line_number = departure_info.get("line_number", "Unknown")
        planned_time = self.display_time(departure_info.get("planned_time", ""))
        planned_platform = departure_info.get("planned_platform", "Unknown")
        if changes: 
            changed_time = changes.get("dp_changes", {}).get("changed_time")
            changed_platform = changes.get("dp_changes", {}).get("changed_platform")
            cancelled = changes.get("dp_changes", {}).get("cancelled", False)
            other_changes = changes.get("dp_changes", {}).get("other_changes", False)
        info = {"line_number": line_number,
                "planned_time": planned_time,
                "planned_platform": planned_platform,
                "changed_time": self.display_time(changed_time) if changed_time else None,
                "changed_platform": changed_platform if changed_platform else None,
                "cancelled": cancelled if changes else False,
                "other_changes": other_changes if changes else False}
        return info

if __name__ == "__main__":
    db = DeutscheBahn()
    next_trip = db.find_next_trip(DIRECTION)
    # db.lookup_trip_changes(next_trip)
    print(db.get_trip_info(next_trip))

