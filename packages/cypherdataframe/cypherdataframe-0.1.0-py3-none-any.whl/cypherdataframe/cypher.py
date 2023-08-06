from datetime import datetime

import pandas as pd

from cypherdataframe.model.Config import Config
from cypherdataframe.model.Query import Query
from py2neo import Node, Relationship, Graph, Path, Subgraph


def query_to_dataframe(query: Query, config: Config) -> pd.DataFrame:
    cypher = query.cypher_query()
    graph = Graph(
        config.neo4j_url,
        auth=(config.neo4j_username, config.neo4j_password)
    )
    v = graph.run(cypher)
    df = v.to_data_frame()
    for property in query.property_names().items():
        if property[0] in df:
            if property[1].datatype == datetime:
                df[property[0]] = df[property[0]].agg(
                    lambda x: x.to_native() if x else None
                )
            else:
                df[property[0]] = df[property[0]].astype(property[1].datatype)
    return df


def all_for_query(query: Query, limit: int, config: Config):
    skip = 0
    len_df = 1
    df_list = []
    while (len_df > 0):
        this_query = Query(
            core_node=query.core_node,
            branches=query.branches,
            skip=skip,
            limit=limit
        )
        df = query_to_dataframe(this_query, config)
        len_df = df.shape[0]
        print(skip, len_df)
        df_list.append(df)
        skip = skip + len_df
    return pd.concat(df_list)
