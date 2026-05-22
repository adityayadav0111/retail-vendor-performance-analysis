## importing libraries
import pandas as pd
import os
from sqlalchemy import create_engine
import logging
import time

## logging in data
logging.basicConfig(
    filename="logs/ingestion_db.log",
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s",
    filemode="a"
)

engine = create_engine('sqlite:///inventory.db')

## ingestion in db
def ingest_db(df, table_name, engine, mode):
    """this function will ingest the dataframe into database table"""
    df.to_sql(table_name,con=engine,if_exists=mode,index=False)

## data load from source
def load_raw_data():
    """this function will load the CSVs as dataframe and ingest in db"""
    start = time.time()
    url = r"C:/Users/Arvind/Downloads/Vendor Performance/source-files/data"
    for file in os.listdir(url):
        if file.endswith('.csv'):
            logging.info(f'Ingesting {file} in db')
            first_chunk = True
            try:
                for chunk in pd.read_csv(url + "/" + file,chunksize=50000,low_memory=False):

                    mode = 'replace' if first_chunk else 'append'

                    ingest_db(chunk,file[:-4],engine,mode)
                    first_chunk = False
                logging.info(f'{file} loaded successfully')

            except Exception as e:

                logging.error(f'Error loading {file}: {e}')

    end = time.time()
    total_time = (end - start) / 60
    logging.info(f"{'*'*10} Ingestion Completed {'*'*10}")
    logging.info(f'Total Time Taken {total_time:.2f} minutes')


if __name__ == "__main__":
    load_raw_data()