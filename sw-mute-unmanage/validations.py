import datetime

# validate start time
def val_start(start):
    year, month, day, hour, minute = map(int,start.split('-'))
    startdate = datetime.date(year, month, day, hour, minute)
    return startdate


# validate end time