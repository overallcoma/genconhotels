import datetime
import influxdb
import modules


def get_lowest_inventory(hotel_room_object, config):
    inventory = []
    for key in hotel_room_object:
        if key in modules.format_dateobjects_list_dashes(config.event_dates):
            if hotel_room_object[key] == "WL":
                inventory.append(0)
            else:
                inventory.append(int(hotel_room_object[key]))
    return min(inventory)


def hotel_json_to_points(hotel_room_json, config):
    db_insert_list = []
    for hotel_room in hotel_room_json:
        body = {
                "measurement": "inventory",
                "tags": {
                    "hotel_name": hotel_room["hotel_name"],
                    "room_type": hotel_room["room_name"]
                },
                "time": datetime.datetime.now(),
                "fields": {
                    "value": get_lowest_inventory(hotel_room, config)
                }
            }
        db_insert_list.append(body)
    return db_insert_list


def influxdb_client(config):
    client = influxdb.InfluxDBClient(host=config.db_host, port=config.db_port, username=config.db_username,
                                     password=config.db_password, database=config.db_name)
    return client


def influxdb_insert(json_object, config):
    data_to_write = hotel_json_to_points(json_object, config)
    db_client = influxdb_client(config)
    db_client.write_points(data_to_write)
    db_client.close()
