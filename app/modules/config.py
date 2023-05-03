from .logic import format_dateobjects_commas


class Configuration(object):
    event_id = ""
    owner_id = ""


gchw2_config = Configuration()


def create_config_object(config):
    gchw2_config.event_id = (config["target-config"])["event-id"]
    gchw2_config.owner_id = (config["target-config"])["owner-id"]
    gchw2_config.entrytoken = (config["account-config"])["entry-token"]
    gchw2_config.check_frequency = int((config["account-config"])["check-frequency"])
    gchw2_config.search_start = (config["search-config"])["search-start"]
    gchw2_config.search_end = (config["search-config"])["search-end"]
    gchw2_config.event_dates = format_dateobjects_commas((config["search-config"])["event-dates"])
    gchw2_config.event_before = format_dateobjects_commas((config["search-config"])["event-before"])
    gchw2_config.event_after = format_dateobjects_commas((config["search-config"])["event-after"])
    gchw2_config.json_output = (config["web-config"])["json-output"]
    gchw2_config.table_json = (config["web-config"])["table-json"]
    gchw2_config.time_stamp_location = (config["web-config"])["time-stamp-location"]
    gchw2_config.db_name = (config["db-config"])["db-name"]
    gchw2_config.db_host = (config["db-config"])["db-host"]
    gchw2_config.db_port = (config["db-config"])["db-port"]
    gchw2_config.db_username = (config["db-config"])["db-username"]
    gchw2_config.db_password = (config["db-config"])["db-password"]
    return gchw2_config
