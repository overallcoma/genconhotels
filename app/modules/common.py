import datetime


def write_file(data, filename):
    output_file = open(filename, "w")
    output_file.write(data)
    output_file.close()


def write_timestamp(config):
    current_time = '{0:%Y-%m-%d %H:%M:%S}'.format(datetime.datetime.now())
    current_time = str(current_time)
    write_file(current_time, config.timestamp)


