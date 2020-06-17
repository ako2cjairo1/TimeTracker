import json
import win32gui
from datetime import datetime as dt
import os.path as path
import time
from json.decoder import JSONDecodeError

datetime_format = "%d %B %Y %I:%M:%S %p"


class TimeTracker:
    def __init__(self):
        self.tracker_list = []

    def create_activities(self):
        serialized_activities = []
        for activity in self.tracker_list:
            serialized_activities.append(activity.serialize())
        return serialized_activities

    def get_activities_from_json(self):
        return_list = []
        if path.exists('Activities.json'):
            try:
                with open('Activities.json', 'r', encoding="utf-8") as json_file:
                    data = json.load(json_file)

                    for activity in data["time_tracker"]:
                        return_list.append(
                            Activity(
                                name=activity["name"],
                                time_entries=self.get_time_entries_from_json(activity)))
            except JSONDecodeError:
                return self.tracker_list

        self.tracker_list = return_list
        return return_list

    def get_time_entries_from_json(self, data):
        time_entry = []
        for entry in data["time_entries"]:
            time_entry.append(
                TimeEntry(
                    start_time=dt.strptime(
                        entry["start_time"], datetime_format),
                    end_time=dt.strptime(entry["end_time"], datetime_format))
            )
        self.time_entries = time_entry
        return time_entry

    def serialize(self):
        return {
            "time_tracker": self.create_activities()
        }


class Activity:
    def __init__(self, name, time_entries):
        self.name = name
        self.time_entries = time_entries

    def create_time_entries(self):
        serialized_time_entries = []
        for te in self.time_entries:
            serialized_time_entries.append(te.serialize())
        return serialized_time_entries

    def serialize(self):
        return {
            "name": self.name,
            "time_entries": self.create_time_entries()
        }


class TimeEntry:
    def __init__(self, start_time, end_time):
        self.start_time = start_time
        self.end_time = end_time
        total_time = end_time - start_time
        self.days = str(total_time.days)
        self.hours = str((total_time.days * 24) + (total_time.seconds // 3600))
        self.minutes = str((total_time.seconds % 3600) // 60)
        self.seconds = str(total_time.seconds % 60)

    def serialize(self):
        return {
            "start_time": self.start_time.strftime(datetime_format),
            "end_time": self.end_time.strftime(datetime_format),
            "days": self.days,
            "hours": self.hours,
            "minutes": self.minutes,
            "seconds": self.seconds
        }


tracker_model = TimeTracker()


class TimeTrackerHandler:
    def __init__(self, interval):
        self.INTERVAL_TIME = interval

    def get_active_window_name(self):
        window = win32gui.GetForegroundWindow()
        app_window_name = str(win32gui.GetWindowText(window)).split("-")

        return app_window_name[0].strip().upper() if len(app_window_name) == 1 else app_window_name[-1].strip().upper()

    def write_updates_to_json(self):
        with open('Activities.json', 'w', encoding='utf-8') as json_file:
            json.dump(tracker_model.serialize(), json_file, indent=4)

    def create_time_entry(self, app_name, start_time, end_time):
        new_time_entry = TimeEntry(start_time, end_time)

        tracker_model.get_activities_from_json()
        name_exists = False

        for activity in tracker_model.tracker_list:
            if app_name.strip().lower() == activity.name.strip().lower():
                activity.time_entries.append(new_time_entry)
                name_exists = True

        if not name_exists:
            new_activity = Activity(app_name, [new_time_entry])
            tracker_model.tracker_list.append(new_activity)

        self.write_updates_to_json()

    def run_time_tracker(self):
        active_window = self.get_active_window_name()
        start_time = dt.now()

        try:
            print("Time Tracker Activated...")
            while True:
                new_active_window = self.get_active_window_name()

                if active_window != new_active_window:
                    end_time = dt.now()

                    # create a time entry in json file
                    self.create_time_entry(active_window, start_time, end_time)

                    # set new active application name and start the timer
                    active_window = new_active_window
                    start_time = dt.now()
                    print(active_window)

                # check newly active windows/application every 30 second
                time.sleep(self.INTERVAL_TIME)

        except KeyboardInterrupt:
            # ensures to capture the time log of last active window
            self.create_time_entry(active_window, start_time, dt.now())
            print("Updated successfully after interrupted.")
