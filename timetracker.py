import json
import time
import win32gui
from datetime import datetime as dt
from tracker_objects import *

trackerObj = TimeTracker([])


def get_active_window_name():
    window = win32gui.GetForegroundWindow()
    app_window_name = str(win32gui.GetWindowText(window)).split("-")
    # print(app_window_name)
    return app_window_name[0].strip().upper() if len(app_window_name) == 1 else app_window_name[-1].strip().upper()


def write_updates_to_json():
    with open('Activities.json', 'w', encoding='utf-8') as json_file:
        json.dump(trackerObj.serialize(), json_file, indent=4)


def create_time_entry(app_name, start_time, end_time):
    new_time_entry = TimeEntry(start_time, end_time)

    trackerObj.get_activities_from_json()
    name_exists = False
    for activity in trackerObj.tracker:
        if app_name.strip().lower() == activity.name.strip().lower():
            activity.time_entries.append(new_time_entry)
            name_exists = True

    if not name_exists:
        new_activity = Activity(app_name, [new_time_entry])
        trackerObj.tracker.append(new_activity)

    write_updates_to_json()


if __name__ == "__main__":
    active_window = get_active_window_name()
    start_time = dt.now()

    try:
        while True:
            new_active_window = get_active_window_name()

            if active_window != new_active_window:
                end_time = dt.now()
                # create a time entry in json file
                create_time_entry(active_window, start_time, end_time)
                # set new active application name and start the timer
                active_window = new_active_window
                start_time = dt.now()
                print(active_window)

            # check newly active windows/application every 1 second
            time.sleep(1)
    except KeyboardInterrupt:
        # ensures to capture the time log of last active window
        create_time_entry(active_window, start_time, dt.now())
        print("Updated successfully after interrupted.")
