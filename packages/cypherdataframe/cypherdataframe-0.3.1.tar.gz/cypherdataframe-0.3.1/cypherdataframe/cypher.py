import os
from datetime import datetime
import time
import pandas as pd

from cypherdataframe.model.Config import Config
from cypherdataframe.model.Property import Property
from cypherdataframe.model.Query import Query
from py2neo import Graph

MAX_RUNS_WITHOUT_DATA = 3
MAX_EXCEPTIONS = 100
def query_to_dataframe(query: Query, config: Config) -> pd.DataFrame:
    cypher = query.to_cypher()
    print(cypher)
    graph = Graph(
        config.neo4j_url,
        auth=(config.neo4j_username, config.neo4j_password)
    )
    v = graph.run(cypher)
    print("done fetch")
    df = v.to_data_frame()
    print("converted to dataframe")
    assignment: str
    prop: Property
    for assignment, prop in query.all_properties_by_final_assigment().items():
        if assignment in df:
            if prop.datatype == datetime:
                df[assignment] = df[assignment].agg(
                    lambda x: x.to_native() if x else None
                )
            elif prop.datatype == list[datetime]:
                df[assignment] = df[assignment].agg(
                    lambda x: [y.to_native() for y in x]
                )
            elif prop.datatype == list[str]:
                pass
            elif prop.datatype == str:
                pass
            else:
                df[assignment] = df[assignment].astype(prop.datatype)

    return df.reset_index(drop=True)


def all_for_query_in_steps(
        query: Query
        , config: Config
        , step: int
        , limit: int
        , start_skip: int
):
    skip = start_skip
    len_df = 1
    df_list = []

    while (len_df > 0 and skip<(start_skip+limit)):
        print(
            f"skip: {skip}, step (query limit): {step}, " 
            f"start_skip: {start_skip}, limit (chunk limit): {limit}"
        )
        this_query = Query(
            core_node=query.core_node,
            branches=query.branches,
            skip=skip,
            limit=step,
            enforce_complete_chunks=query.enforce_complete_chunks
        )
        start_time = time.time()
        df = query_to_dataframe(this_query, config)

        len_df = df.shape[0]
        print(f"rows returned {len_df}")
        print(f"--- {(time.time() - start_time)} seconds ---")
        print()
        df_list.append(df)
        skip = skip + step
    return pd.concat(df_list).reset_index(drop=True)

def __make_meta(meta_path: str) -> None:
    df_meta = pd.DataFrame(
        columns=[
            'increment',
            'rows',
            'row_rate',
            'chunk_size',
            'start_time',
            'data_extracted_time',
            'data_stored_time',
            'extraction_time',
            'storage_time',
            'total_time'
        ]
    )
    df_meta.to_csv(meta_path, index=False)


def __add_to_meta(
    meta_path: str,
    increment: str,
    chunk_size: int,
    rows: int,
    start_time,
    data_extracted_time,
    data_stored_time,
    extraction_time,
    storage_time,
    total_time
          ) -> None:


    new_meta = {
        'increment': increment,
        'row_rate': rows/total_time,
        'rows': rows,
        'chunk_size': chunk_size,
        'start_time': start_time,
        'data_extracted_time': data_extracted_time,
        'data_stored_time': data_stored_time,
        'extraction_time': extraction_time,
        'storage_time': storage_time,
        'total_time': total_time
    }
    df_meta = pd.read_csv(meta_path)
    df_meta = pd.concat(
        [df_meta, pd.DataFrame(new_meta, index=[0])]
    )
    df_meta.to_csv(meta_path, index=False)


def __gather_to_meta(meta_path, meta_gather_path):
    df_meta = pd.read_csv(meta_path)
    df_meta.to_csv(meta_gather_path, index=False)


def all_for_query_in_chunks(
        query: Query
        , config: Config
        , step: int
        , chunk_size: int
        , save_directory: str
        , table_name_root: str
        , max_total_chunks: int
        , gather_to_dir: str
) -> None:
    meta_path = f'{save_directory}/meta.csv'
    meta_gather_dir = f'{gather_to_dir}_meta'
    meta_gather_path = f'{meta_gather_dir}/{table_name_root}_meta.csv'
    if not os.path.isdir(meta_gather_dir):
        os.makedirs(meta_gather_dir)

    if not os.path.isdir(save_directory):
        os.makedirs(save_directory)

    if not os.path.isfile(meta_path):
        __make_meta(meta_path)


    process_start_time = time.time()
    df_meta = pd.read_csv(meta_path)


    if df_meta.shape[0] > 0:
        if 'gather' not in df_meta['increment'].values.tolist():
            start_chunk = df_meta['increment'].max() + 1
            total_rows = df_meta['rows'].sum()
        else:
            print("Already Gathered")
            print()
            return None
    else:
        total_rows = 0
        start_chunk = 1

    exceptions = 0
    inc_chunk = 0
    runs_without_data = 0

    while True:
        try:
            chunk_start_time = time.time()
            current_chunk = start_chunk + inc_chunk

            if current_chunk > max_total_chunks:
                break
            print()
            print(
                f"Chunk: {current_chunk} "
                f"Rows So Far: {total_rows} "
                f"Time: {time.strftime('%H:%M:%S', time.localtime())}")

            df = all_for_query_in_steps(
                query
                , config
                , step=step
                , limit=chunk_size
                , start_skip=total_rows
            )



        except Exception as e:
            print(f"Whoops {exceptions} waiting 10 s")
            print(e)
            time.sleep(10)
            exceptions = exceptions + 1
            if exceptions >= MAX_EXCEPTIONS:
                print(f"Exceptions: {exceptions} "
                      f"exceeded max: {MAX_EXCEPTIONS}")
                print("Process Abandoned")
                return None
            else:
                continue

        data_extracted_time = time.time()
        df.to_csv(
            f"{save_directory}/{table_name_root}_{current_chunk}.csv",
            index=False
        )
        data_stored_time = time.time()

        __add_to_meta(
            meta_path,
            increment=current_chunk,
            rows=df.shape[0],
            chunk_size=chunk_size,
            start_time=datetime.fromtimestamp(chunk_start_time, tz=None),
            data_extracted_time=datetime.fromtimestamp(data_extracted_time, tz=None),
            data_stored_time=datetime.fromtimestamp(data_stored_time, tz=None),
            extraction_time=(data_extracted_time - chunk_start_time) / 60,
            storage_time=(data_stored_time - data_extracted_time) / 60,
            total_time=(data_stored_time - chunk_start_time) /60
        )
        total_rows += df.shape[0]
        if df.shape[0] < 1:
            runs_without_data += 1
        else:
            runs_without_data = 0

        if df.shape[0] < chunk_size and query.enforce_complete_chunks:
            print(f"Incomplete chunk with enforce_complete_chunks turned on")
            print("Chunk Done")
            break

        if runs_without_data == MAX_RUNS_WITHOUT_DATA:
            print(f"Consecutive runs_without_data: {runs_without_data} "
                  f"exceeded max: {MAX_RUNS_WITHOUT_DATA}")
            print("Chunk Done")
            break


        inc_chunk += 1

    start_gather_time = time.time()

    gather_chunks_from_dir(
        gather_to_dir=gather_to_dir,
        read_directory=save_directory,
        table_name_root=table_name_root
    )
    __add_to_meta(
        meta_path,
        increment="gather",
        rows=0,
        chunk_size=0,
        start_time=datetime.fromtimestamp(start_gather_time, tz=None),
        data_extracted_time=None,
        data_stored_time=None,
        extraction_time=0,
        storage_time=0,
        total_time=(time.time() - start_gather_time) /60
    )

    __add_to_meta(
        meta_path,
        increment="process_total",
        rows=0,
        chunk_size=0,
        start_time=datetime.fromtimestamp(process_start_time, tz=None),
        data_extracted_time=None,
        data_stored_time=None,
        extraction_time=0,
        storage_time=0,
        total_time=(time.time() - process_start_time) / 60
    )
    __gather_to_meta(meta_path, meta_gather_path)


def gather_chunks_from_dir(gather_to_dir: str, read_directory: str, table_name_root: str):
    if os.path.isdir(read_directory):
        df_list = []
        for file_name in os.listdir(read_directory):
            file_size = os.path.getsize(f"{read_directory}/{file_name}")
            if "csv" in file_name \
                    and "-gathered.csv" not in file_name \
                    and "meta.csv" not in file_name \
                    and file_size > 10:
                df_list.append(pd.read_csv(f"{read_directory}/{file_name}"))
        if len(df_list) > 0:
            df = pd.concat(df_list).reset_index(drop=True)
            if not os.path.isdir(gather_to_dir):
                os.makedirs(gather_to_dir)

            df.to_csv(
                f"{gather_to_dir}/{table_name_root}-gathered.csv",
                index=False
            )
