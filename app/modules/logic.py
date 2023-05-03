import datetime


def string_to_bool(truefalse):
    if truefalse == "true":
        return True
    if truefalse == "false":
        return False


def all_dates_list(start, end):
    start = datetime.datetime.strptime(start, "%Y-%m-%d")
    end = datetime.datetime.strptime(end, "%Y-%m-%d")
    delta = end - start
    date_range = []
    for date in range(delta.days + 1):
        day = start + datetime.timedelta(days=date)
        day = datetime.datetime.strftime(day, "%Y, %m, %d").replace(' 0', ' ')
        date_range.append(day)
    return date_range


def write_file(data, filename):
    output_file = open(filename, "w+")
    output_file.write(data)
    output_file.close()


def write_timestamp(config):
    current_time = '{0:%Y-%m-%d %H:%M:%S}'.format(datetime.datetime.now())
    current_time = str(current_time)
    write_file(current_time, config.time_stamp_location)


def format_dateobjects_commas(inputstring):
    list_object = inputstring.split(',')
    return_list = []
    for dateobject in list_object:
        dateobject = "[" + dateobject + "]"
        dateobject = dateobject.replace('-', ',')
        return_list.append(dateobject)
    return return_list


def format_dateobjects_list_dashes(input_list):
    return_list = []
    for date in input_list:
        date = date.replace("[", "")
        date = date.replace("]", "")
        date = date.replace(",", "-")
        return_list.append(date)
    return return_list
