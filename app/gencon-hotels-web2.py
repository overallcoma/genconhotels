import configparser
import time
import json
import modules

try:
    configfilename = "./gchw2.cfg"
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


gchw2_config = modules.create_config_object(config)
print("Gencon-Hotels-Web2 is running")
error_count = 0
influxdbclient = modules.get_influx_client()

while True:
    try:
        hotel_room_json = modules.get_hotel_room_objects(gchw2_config)
        # print("TEST POINT 1")
        # print(hotel_room_json)
        hotel_room_objects = modules.hotel_room_parser(hotel_room_json)
        # print("TEST POINT 2")
        # print(hotel_room_objects)
        hotel_room_filtered_list = modules.filter_avail(hotel_room_objects, gchw2_config)
        # print("TEST POINT 3")
        # print(hotel_room_filtered_list)
        modules.write_file(json.dumps(hotel_room_filtered_list), gchw2_config.table_json)
        modules.write_file(json.dumps(hotel_room_objects), gchw2_config.json_output)
        modules.send_influx_data(influxdbclient, hotel_room_objects)
        modules.write_timestamp(gchw2_config)
        time.sleep(gchw2_config.check_frequency)
        error_count = 0
    except Exception as e:
        print(e)
        print("Current Error Count is {}".format(error_count))
        error_count += 1
        time.sleep(10)
        if error_count < 10:
            continue
        else:
            print("10 successive errors in a row")
            print("Exiting Application")
            exit(1)
