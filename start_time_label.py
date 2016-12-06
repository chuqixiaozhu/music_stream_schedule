import datetime

def get_time(line):
    hour = int(line[11:13])
    minute = int(line[14:16])
    second = int(line[17:19])
    the_time = datetime.time(hour, minute, second)
    return the_time

def get_start_time_label(time_str):
    t = get_time(time_str)
    MORNING = datetime.time(8, 0, 0)
    LUNCH = datetime.time(11, 0, 0)
    AFTERNOON = datetime.time(13, 0, 0)
    DINNER = datetime.time(17, 0, 0)
    EVENING = datetime.time(19, 0, 0)
    SLEEP = datetime.time(22, 0, 0)
    
    if MORNING <= t and t < LUNCH:
        return 0
    elif LUNCH <= t and t < AFTERNOON:
        return 1
    elif AFTERNOON <= t and t < DINNER:
        return 2
    elif DINNER <= t and t < EVENING:
        return 3
    elif EVENING <= t and t < SLEEP:
        return 4
    else:
        return 5

def test():
    line = '2009-05-03T13:00:00Z'
    the_time = get_time(line)
    print(the_time)
    print(the_time.hour, the_time.minute, the_time.second)
    now = datetime.time(22, 48, 25)
    print(now > the_time)
    print(get_start_time_label(line))

if __name__ == '__main__':
    test()