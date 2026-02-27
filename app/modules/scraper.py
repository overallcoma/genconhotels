import datetime
import html
import json
from .common import write_file
import re
import requests

user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/145.0.0.0 " \
    "Safari/537.36"
user_agent_header = {
    'User-Agent': user_agent
}

def passkey_parse(html_content):
    parsed_content = re.findall('<script id="last-search-results" type="application/json">(.*?)</script>',
                                html_content)[0]
    parsed_content = json.loads(parsed_content)
    return parsed_content


def construct_search_post(config, xsrf_token):
    search_hotel_id = 0
    search_block_hotelid = 0
    search_block_id = 0
    search_numberofguests = 1
    search_numberofrooms = 1
    search_numberofchildren = 0
    payload = {
        'hotelId': search_hotel_id,
        '_csrf': xsrf_token,
        'blockMap.blocks[0].hotelId': search_block_hotelid,
        'blockMap.blocks[0].blockId': search_block_id,
        'blockMap.blocks[0].checkIn': config.wednesday,
        'blockMap.blocks[0].checkOut': config.sunday,
        'blockMap.blocks[0].numberOfGuests': search_numberofguests,
        'blockMap.blocks[0].numberOfRooms': search_numberofrooms,
        'blockMap.blocks[0].numberOfChildren': search_numberofchildren
    }
    return payload


def filter_hotelobjects(dictlist_hotels):
    filter_return = []
    for dict_hotel in dictlist_hotels:
        if dict_hotel['blocks']:
            for block in dict_hotel['blocks']:
                room = {
                    'hotel_name': dict_hotel['name'],
                    'distance': round(dict_hotel['distanceFromEvent'],2),
                    'room_name': block['name'],
                    'rate': block['averageRate'],
                }
                for date_entry in block['inventory']:
                    if date_entry['date'] == [2026,7,29] and date_entry['available'] != 0:
                        if date_entry['wlAvailable'] < date_entry["available"]:
                            room['wednesday'] = 'Open'
                        elif date_entry['wlAvailable'] >= date_entry["available"]:
                            room['wednesday'] = 'WL'
                    if date_entry['date'] == [2026,7,30] and date_entry['available'] != 0:
                        if date_entry['wlAvailable'] < date_entry["available"]:
                            room['thursday'] = 'Open'
                        elif date_entry['wlAvailable'] >= date_entry["available"]:
                            room['thursday'] = 'WL'
                    if date_entry['date'] == [2026,7,31] and date_entry['available'] != 0:
                        if date_entry['wlAvailable'] < date_entry["available"]:
                            room['friday'] = 'Open'
                        elif date_entry['wlAvailable'] >= date_entry["available"]:
                            room['friday'] = 'WL'
                    if date_entry['date'] == [2026,8,1] and date_entry['available'] != 0:
                        if date_entry['wlAvailable'] < date_entry["available"]:
                            room['saturday'] = 'Open'
                        elif date_entry['wlAvailable'] >= date_entry["available"]:
                            room['saturday'] = 'WL'
                filter_return.append(room)
    return filter_return


def distance_type(dictlist_hotels):
    skywalk_hotels = [
        'The Westin Indianapolis',
        'Indianapolis Marriott Downtown',
        'JW Marriott Indianapolis',
        'Omni Severin Hotel',
        'Fairfield Inn &amp; Suites Indianapolis Downtown',
        'Le Meridien Indianapolis',
        'Embassy Suites Indianapolis Downtown',
        'Hyatt Regency Indianapolis',
        'Crowne Plaza Indianapolis Downtown Union Station',
        'Conrad Indianapolis',
        'Courtyard by Marriott Downtown Indianapolis',
        'SpringHill Suites Indianapolis Downtown'
    ]
    for hotel in dictlist_hotels:
        if hotel['hotel_name'] in skywalk_hotels:
            hotel['skywalk'] = 1
            hotel['downtown'] = 0
        else:
            hotel['skywalk'] = 0
        if hotel['hotel_name'] not in skywalk_hotels:
            if hotel['distance'] <= 1:
                hotel['downtown'] = 1
            else:
                hotel['downtown'] = 0
    return(dictlist_hotels)


def roomname_unescapehtml(dictlist_rooms):
    for room in dictlist_rooms:
        room['room_name'] = html.unescape(room['room_name'])
    return(dictlist_rooms)


def get_hotelobjects(config):
    base_portal_url = "https://book.passkey.com"
    housing_url_post_base = base_portal_url + "/event/" + config.event_id + "/owner/" + config.owner_id
    post_room_select_url = housing_url_post_base + "/rooms/select"
    housing_url_initial = base_portal_url + "/entry?token={}".format(config.token)
    housing_url_available_post = housing_url_post_base + "/list/hotels/available"
    response = requests.get(housing_url_initial, headers=user_agent_header)
    response_cookies = response.cookies
    xsrf_token = response_cookies.get('XSRF-TOKEN')
    post_data = construct_search_post(config, xsrf_token)
    requests.post(housing_url_available_post, data='', headers=user_agent_header, cookies=response_cookies)
    response = requests.post(post_room_select_url, data=post_data, headers=user_agent_header, cookies=response_cookies)
    try:
        hotels = passkey_parse(response.text)
        #write_file(json.dumps(hotels), 'testout.txt')
        hotels = filter_hotelobjects(hotels)
        #write_file(json.dumps(hotels), 'testout2.txt')
        hotels = distance_type(hotels)
        hotels = roomname_unescapehtml(hotels)

    except TypeError:
        current_time = str(datetime.datetime.now())
        print(current_time + " - Error Scraping Page - Continuing Script")
        print("This is an expected occasional error - do not worry")
        return []
    except Exception as i:
        current_time = str(datetime.datetime.now())
        print(current_time + " - Error Scraping Page - Continuing Script")
        print("This is not an expected error - report this for repair")
        print(i)
        return []
    if hotels:
        return hotels
    else:
        return []