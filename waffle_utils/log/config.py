import json
import logging
import logging.config
import os

with open("waffle_utils/log/.log_conf.json") as json_file:
    conf = json.load(json_file)
    os.makedirs(os.path.split(conf["handlers"]["file"]["filename"])[0], exist_ok=True)
    logging.config.dictConfig(conf)

logger = logging.getLogger(__name__)
