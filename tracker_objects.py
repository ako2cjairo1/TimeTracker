import json
from datetime import datetime as dt
import os.path as path

datetime_format = "%d %B %Y %I:%M:%S %p"


class TimeTracker:
    def __init__(self, tracker):
        self.tracker = tracker

    def create_activities(self):
        serialized_activities = []
        for activity in self.tracker:
            serialized_activities.append(activity.serialize())
        return serialized_activities

    def get_activities_from_json(self):
        return_list = []
        if path.exists('Activities.json'):
            with open('Activities.json', 'r') as json_file:
                data = json.load(json_file)

                for activity in data["time_tracker"]:
                    return_list.append(
                        Activity(
                            name=activity["name"],
                            time_entries=self.get_time_entries_from_json(activity))
                    )
        self.tracker = return_list
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
