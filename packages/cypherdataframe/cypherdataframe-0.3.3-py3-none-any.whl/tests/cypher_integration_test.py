import unittest

from cypherdataframe.config import load_config
from cypherdataframe.cypher import query_to_dataframe
import os
dir_path = os.path.dirname(os.path.realpath(__file__))

_conf_path =f'{dir_path}/../conf.ini'



def i_test_query_to_dataframe(query_material_1):
    conf = load_config(_conf_path)
    df = query_to_dataframe(query_material_1,conf)
    print()
    print(df)
    print(df.dtypes)
