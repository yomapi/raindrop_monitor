import os
import yaml

yaml_settings = dict()
path = os.path.abspath(os.path.dirname(__file__))
filename = "config_real.yml"

with open(os.path.join(path, filename)) as f:
    yaml_settings.update(yaml.load(f, Loader=yaml.FullLoader))


class Config:
    seoul_api: dict = yaml_settings["seoul_api"]


config = Config()
