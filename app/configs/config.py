import os
import yaml

from pydantic import BaseSettings


yaml_settings = dict()

path = os.path.abspath(os.path.dirname(__file__))
filename = "config_{}.yml".format(os.getenv("stage", "dev"))

with open(os.path.join(path, filename)) as f:
    yaml_settings.update(yaml.load(f, Loader=yaml.FullLoader))


class Config(BaseSettings):
    databases: dict = yaml_settings["databases"]

    class Config:
        env_file = "configs.yml"
        env_file_encoding = "utf-8"


config = Config()
