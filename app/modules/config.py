class Configuration(object):
    event_id = ""


gch_config = Configuration()


def create_config_object(config):
    gch_config.event_id = (config["event"])["event-id"]
    gch_config.owner_id = (config["event"])["owner-id"]
    gch_config.token = (config["account"])["token"]
    gch_config.frequency = int((config["search"])["frequency"])
    gch_config.tuesday = (config["event"])["tuesday"]
    gch_config.wednesday = (config["event"])["wednesday"]
    gch_config.thursday = (config["event"])["thursday"]
    gch_config.friday = (config["event"])["friday"]
    gch_config.saturday = (config["event"])["saturday"]
    gch_config.sunday = (config["event"])["sunday"]
    gch_config.json_output = (config["web"])["formatted"]
    gch_config.timestamp = (config["web"])["timestamp"]
    return gch_config
