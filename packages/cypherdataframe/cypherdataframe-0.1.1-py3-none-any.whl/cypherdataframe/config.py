import configparser

from cypherdataframe.model.Config import Config
from dacite import from_dict


def load_config(path: str) -> Config:
    my_config = configparser.ConfigParser()
    my_config.read(path)
    return from_dict(data_class=Config, data=dict(my_config.items('DEFAULT')))

