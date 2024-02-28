import datetime
import influxdb
import modules
import os, time
from influxdb_client_3 import InfluxDBClient3, Point



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


def get_influx_client():
    token = 'redacted'
    org = "LoftusHall"
    host = "https://us-east-1-1.aws.cloud2.influxdata.com"

    client = InfluxDBClient3(host=host, token=token, org=org)
    return client


def send_influx_data(client, data):
    database = "genconhotels"
    for key in data:
        point = (
            Point("roomavailable")
            .tag("hotelname", key["hotel_name"])
            .tag("roomname", key["room_name"])
            .field("distance", key["distance_unit"])
        )
        client.write(database=database, record=point)
