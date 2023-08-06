from datetime import datetime

from cypherdataframe.branch_maker import branches_from_labels
from cypherdataframe.config import load_config
from cypherdataframe.cypher import all_for_query_in_steps
from cypherdataframe.model.LabelNode import LabelNode
from cypherdataframe.model.Property import Property
from cypherdataframe.model.Query import Query

import os

dir_path = os.path.dirname(os.path.realpath(__file__))
_conf_path = f'{dir_path}/../conf.ini'


def cypher_query():
    material_properties = [
        Property('id', str),
        Property('createdOn', datetime)
    ]

    core_node = LabelNode('Material', material_properties)

    reference_properties = [
        Property('value', str),
        Property('createdOn', datetime)
    ]
    reference_labels = [
        'Plant',
        'PoNumber',
        'PoLine',
        'PoDeleted',
        'ReqNumber',
        'ReqLine',
        'ResNumber',
        'ResLine'
    ]
    reference_branches = branches_from_labels(
        "REFERENCED_AS", True,
        reference_labels,
        reference_properties
    )
    query = Query(core_node, reference_branches, skip=None, limit=None)
    config = load_config(_conf_path)
    df = all_for_query_in_steps(query, 100000, config)
    df.reset_index(drop=True).to_feather('./temp.feather')


if __name__ == '__main__':
    cypher_query()
