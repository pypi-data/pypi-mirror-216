import unittest

from cypherdataframe.config import load_config
import os
dir_path = os.path.dirname(os.path.realpath(__file__))

_conf_path =f'{dir_path}/../conf.ini'

class ConfigTestCase(unittest.TestCase):
    def test_load_config(self):
        print()
        conf = load_config(_conf_path)
        print(conf)
        pass
