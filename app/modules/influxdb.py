import datetime
import influxdb
import modules


def hotel_json_to_points(hotel_room_json):
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
                    "value": 1
                }
            }
        db_insert_list.append(body)
    return db_insert_list


def get_influx_client(config):
    client = influxdb.InfluxDBClient(
        config.db_host,
        config.db_port,
        config.db_username,
        config.db_password,
        config.db_name
    )
    return client


def send_influx_data(client, data):
    data = hotel_json_to_points(data)
    client.write_points(data)
