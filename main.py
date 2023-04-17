import requests
import json
import logging
from types import SimpleNamespace
import sqlite3
from utils import *
import numpy as np
import uuid

# To force an INT as an INT and not let sqlite convert to BLOB type
sqlite3.register_adapter(np.int32, int)
sqlite3.register_adapter(np.int64, int)

# Save the logs to a file
logging.basicConfig(format='%(asctime)s | %(levelname)s: %(message)s', level=logging.INFO, filename="cocktails_logs.txt")

conn = sqlite3.connect('cocktails.db')
cursor = conn.cursor()

# list of all the alphabets 
alphabet = list (map (chr, range (97,123)))

url = "https://www.thecocktaildb.com/api/json/v1/1/search.php?"

for idx, letter in enumerate(alphabet):    
    # Syntax for the endpoint taken from cocktails API documentation
    endpoint = f"f={letter}"
    logging.info(f"Searching the alphabet [{letter}], with endpoint: [{endpoint}]")
    data = make_api_call(url, endpoint)
    drinks_data = data.get("drinks")
    
    if drinks_data is None:
        logging.info(f"Skipping endpoint: [{endpoint}] as data with this endpoint is [{drinks_data}]")
        continue

    batch_id = str(uuid.uuid4())
    unprocessed_records, instructions_df, drinks_df, recipe_df = process_batch_records(conn, cursor, drinks_data, batch_id)

    dataframes_dict = {"instructions_df" : instructions_df, "drinks_df" : drinks_df, "recipe_df" : recipe_df}
    
    # loading the processed records in the sqlite database
    ret_ins, ret_drinks, ret_recipes = bulk_loading(conn, cursor, dataframes_dict, batch_id)
    
    if ret_ins != True or ret_drinks != True or ret_recipes != True:
        logging.error(f"Errors encountered: [INSTRUCTIONS TABLE: {ret_ins}, DRINKS TABLE: {ret_drinks} \
                       RECIPE TABLE: {ret_recipes}], while loading data for batch id: [{batch_id}]")
    else: 
        logging.info(f"Records for batch id: [{batch_id}] processed and loaded successfully")

conn.commit()
cursor.close()  
