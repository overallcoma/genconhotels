import html
import modules


def hotel_room_parser(hotel_json_list):
    hotel_list = []
    for hotel in hotel_json_list:
        hotel_name = html.unescape(hotel["name"])
        hotel_id = hotel["id"]
        hotel_distance = hotel["distanceFromEvent"]
        hotel_distance_unit = hotel["distanceUnit"]

        for block in hotel["blocks"]:
            room_name = html.unescape(block["name"])
            room_id = block["id"]
            room_rate = block["averageRate"]

            hotel_room_object = {"hotel_name": hotel_name, "hotel_id": hotel_id, "distance": hotel_distance,
                                 "distance_unit": hotel_distance_unit, "room_name": room_name, "room_id": room_id,
                                 "room_rate": room_rate}

            for day in block["inventory"]:
                date = day["date"]
                date = "{}-{}-{}".format(date[0], date[1], date[2])
                if day["available"] == day["wlAvailable"] and day["wlAvailable"] > 0:
                    available = "WL"
                else:
                    available = "Y"
                hotel_room_object[date] = available
            hotel_list.append(hotel_room_object)
    return hotel_list


def filter_avail(hotel_json, config):
    available_rooms = []
    for hotel_room in hotel_json:
        room_show = True
        for key in hotel_room:
            if key in modules.format_dateobjects_list_dashes(config.event_dates):
                if not room_show:
                    break
                if hotel_room[key] == 0:
                    room_show = False
        if room_show:
            available_rooms.append(hotel_room)
    return available_rooms
