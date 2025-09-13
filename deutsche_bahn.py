
#TODO make a request to fetch the changes
#TODO implement the changes in the next trip info
#TODO make the code more robust (error handling, edge cases) 

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
        print(trips)
        return trips
    
    def find_next_trip(self, direction):
        """
        Finds the next trip in the given direction after the current time.
        """
        date = _now_yymmdd()
        hour = "14"
        time_now = "2509131440"
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

if __name__ == "__main__":
    db = DeutscheBahn()
    # test = db.get_trips_by_hour("250912", "16")
    # filtered = db.filter_direction("Wächterhof", "250912", "16")
    # print(test)
    # print(filtered)
    # db.get_changes()
    next_trip = db.find_next_trip(DIRECTION)
    db.lookup_trip_changes(next_trip)


