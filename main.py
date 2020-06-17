import TimeTracker as tt


if __name__ == "__main__":
    # create instance of handler
    # set interval time to check frequency of active application
    # in seconds, default is 30 if not provided
    tth = tt.TimeTrackerHandler(15)

    # start the time tracking
    tth.run_time_tracker()
