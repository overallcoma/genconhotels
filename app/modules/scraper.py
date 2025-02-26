import datetime
import json
import re
import requests

user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 " \
             "Safari/537.36"
user_agent_header = {
    'User-Agent': user_agent
}


def passkey_parser(html_content):
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
        'blockMap.blocks[0].checkIn': config.search_start,
        'blockMap.blocks[0].checkOut': config.search_end,
        'blockMap.blocks[0].numberOfGuests': search_numberofguests,
        'blockMap.blocks[0].numberOfRooms': search_numberofrooms,
        'blockMap.blocks[0].numberOfChildren': search_numberofchildren
    }
    return payload


def get_hotel_room_objects(config):
    base_portal_url = "https://book.passkey.com"
    housing_url_post_base = base_portal_url + "/event/" + config.event_id + "/owner/" + config.owner_id
    post_room_select_url = housing_url_post_base + "/rooms/select"
    housing_url_initial = base_portal_url + "/entry?token={}".format(config.entrytoken)
    housing_url_available_post = housing_url_post_base + "/list/hotels/available"
    response = requests.get(housing_url_initial, headers=user_agent_header)
    #print(response)
    response_cookies = response.cookies
    xsrf_token = response_cookies.get('XSRF-TOKEN')
    post_data = construct_search_post(config, xsrf_token)
    requests.post(housing_url_available_post, data='', headers=user_agent_header, cookies=response_cookies)
    response = requests.post(post_room_select_url, data=post_data, headers=user_agent_header, cookies=response_cookies)
    #print(response.text)
    try:
        hotels = passkey_parser(response.text)
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
