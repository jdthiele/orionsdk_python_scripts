import sys
import re
from datetime import datetime, timedelta

# validate dates
def val_date(date_input):
    try: 
      date = datetime.strptime(date_input, '%Y-%m-%d-%H-%M')
    except ValueError:
        raise ValueError("Incorrect date format, should be YYYY-MM-DD-hh-mm")
    #date = datetime.strptime(date_input, '%Y-%m-%d-%H-%M')
    now = datetime.now()
    if date < now:
        print('You entered a date in the past. the dates provided need to be in the future. Exitting')
        sys.exit(3)
    return date


# calculate duration
def calc_dur(date_input, duration):
    if date_input == "now":
        start = datetime.now()
    else:
        start = date_input
    dur_num = int(re.sub("\D", "", duration))
    if duration.endswith('d'):
        stop_date = start + timedelta(days=dur_num)
    elif duration.endswith('h'):
        stop_date = start + timedelta(hours=dur_num)
    else:
        print("you entered an incorrect duration unit, use either 'd' (days) or 'h' (hours)")
        sys.exit(4)
    return stop_date