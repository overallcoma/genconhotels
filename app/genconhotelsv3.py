import configparser
import datetime
import json
import modules
import time

try:
    configfilename = "./config.ini"
    config = configparser.ConfigParser()
except Exception as e:
    print("Unable to load config file - please verify it exists")
    print(e)
    exit(1)

try:
    config.read(configfilename)
except Exception as e:
    print("Unable to read config file")
    print(e)
    exit(1)

gch_config = modules.create_config_object(config)
print("genconhotels3 is running")
error_count = 0
loop_count = 0

while True:
    try:
        dict_hotels = modules.get_hotelobjects(gch_config)
        modules.write_file(json.dumps(dict_hotels), gch_config.json_output)
        modules.write_timestamp(gch_config)
        time.sleep(gch_config.frequency)
        loop_count += 1
        if loop_count >= 100:
            loop_count = 0
            loop_time = str(datetime.datetime.now())
            print(loop_time + " - 100 successful loops")
    except Exception as e:
        print('ERROR OCCURRED')
        print(e)
        error_count += 1
        if error_count < 10:
            continue
        else:
            print("10 successive errors in a row")
            print("Exiting Application")
            exit(1)