import pandas as pd
import logging
import uuid
import requests
from typing import List, Dict, Any


instructions_mapping = {
    "strInstructions" : "instructions_en",
    "strInstructionsES" : "instructions_es",
    "strInstructionsDE" : "instructions_de",
    "strInstructionsFR" : "instructions_fr",
    "strInstructionsIT" : "instructions_it",
    "strInstructionsZH-HANS" : "instructions_zh_hans",
    "strInstructionsZH-HANT" : "instructions_zh_hant"
}


def make_api_call(url:str, endpoint:str):
    try:
        response = requests.get(url + endpoint)
        return response.json()
    except Exception as error:
        logging.error(f"Error: [{error}] while making a call to [{url+endpoint}]")
        raise error


def get_glass_foreign_key(conn:str, cursor:str, glass_name:str) -> int:
    glass_name = glass_name.lower() # To make string values case insensitive
    cursor.execute("""SELECT id FROM glass WHERE glass_name = ?""", (glass_name,))
    response = cursor.fetchone()
    if response is not None: #read from glass table with glass name and get its row id
        last_row_id = response[0]
    else: #insert into glass table and get back last row id 
        cursor.execute('''INSERT INTO glass (glass_name) VALUES (?)''',
                    (glass_name,))
        last_row_id = cursor.lastrowid
        conn.commit()
    return last_row_id
    

def get_category_foreign_key(conn:str, cursor:str, category_name:str):
    category_name = category_name.lower()
    cursor.execute("""SELECT id FROM category WHERE category_name = ?""", (category_name,))
    response = cursor.fetchone()
    if response is not None: 
        last_row_id = response[0] 
    else: 
        cursor.execute('''INSERT INTO category (category_name) VALUES (?)''',
                    (category_name,))
        last_row_id = cursor.lastrowid
        conn.commit()
    return last_row_id


def get_alcoholic_foreign_key(conn:str, cursor:str, alcoholic_name:str):
    alcoholic_name = alcoholic_name.lower() 
    cursor.execute("""SELECT id FROM alcoholic WHERE alcohol = ?""", (alcoholic_name,))
    response = cursor.fetchone()
    if response is not None:
        last_row_id = response[0] 
    else: 
        cursor.execute('''INSERT INTO alcoholic (alcohol) VALUES (?)''',
                    (alcoholic_name,))
        last_row_id = cursor.lastrowid
        conn.commit()
    return last_row_id


def get_instructions_entry(conn:str, cursor:str, data, drink_id):
    drink_id_key_value = {"drink_id": drink_id}
    instructions_data = {key:value for key,value in data.items() if key.startswith("strInstructions")}
    instructions_data.update(drink_id_key_value)
    return instructions_data


def get_ingredient_foreign_key(conn:str, cursor:str, ingredient_name:str):
    ingredient_name = ingredient_name.lower() if ingredient_name is not None else "N/A"
    cursor.execute("""SELECT id FROM ingredients WHERE ingredient_name = ?""", (ingredient_name,))
    response = cursor.fetchone()
    if response is not None: 
        last_row_id = response[0] 
    else:  
        cursor.execute('''INSERT INTO ingredients (ingredient_name) VALUES (?)''',
                    (ingredient_name,))
        last_row_id = cursor.lastrowid
        conn.commit()
    return int(last_row_id)


def get_measure_foreign_key(conn:str, cursor:str, measure_quantity:str):
    measure_quantity = measure_quantity.lower() if measure_quantity is not None else "N/A" 
    cursor.execute("""SELECT id FROM measures WHERE measure_quantity = ?""", (measure_quantity,))
    response = cursor.fetchone()
    if response is not None:
        last_row_id = response[0] 
    else: 
        cursor.execute('''INSERT INTO measures (measure_quantity) VALUES (?)''',
                    (measure_quantity,))
        last_row_id = cursor.lastrowid
        conn.commit()
    return int(last_row_id)


def get_drink_recipe_entry(conn:str, cursor:str, ingredient_name:str, measure_quantity:str, drink_id):
    ingredient_foreign_key = get_ingredient_foreign_key(conn, cursor, ingredient_name)
    measure_foreign_key = get_measure_foreign_key(conn, cursor, measure_quantity)
    recipe_entry_json = {
        "ingredient_id" : ingredient_foreign_key,
        "measure_id" : measure_foreign_key,
        "drink_id" : drink_id
    }
    return recipe_entry_json


def get_recipe_df(conn:str, cursor:str, drinks, drink_id):
    drink_id_key_value = {"drink_id": drink_id}
    recipe_ls = []
    for i in range(1,16):
        ingredient_key = f"strIngredient{i}"
        measure_key = f"strMeasure{i}"
        ingredient_name = drinks.get(ingredient_key) 
        measure_quantity = drinks.get(measure_key) 
        if ingredient_name is not None or measure_quantity is not None:
            recipe_entry_json = get_drink_recipe_entry(conn, cursor, ingredient_name, measure_quantity, drink_id)
            recipe_entry_json.update(drink_id_key_value)
            recipe_ls.append(recipe_entry_json)
    return recipe_ls


def append_drink_id_key_value(json_record, drink_id):
    try:
        drink_id_key_value = {"drink_id": drink_id}
        return json_record.update(drink_id_key_value)
    except:
        logging.error(f"Failed to add drink id: [{drink_id}] to the json record: [{json_record}]")
        raise Exception    
    

def get_drinks_record(conn:str, cursor:str, drink):
    drink_name = drink.get("strDrink")
    alternate_drink_name = drink.get("strDrinkAlternate") 
    drink_id = int(drink.get("idDrink"))
    glass = drink.get("strGlass")
    category = drink.get("strCategory")
    alcohol = drink.get("strAlcoholic")
    date_modified = drink.get("dateModified")
    glass_key = get_glass_foreign_key(conn, cursor, glass)
    category_key = get_category_foreign_key(conn, cursor, category)
    alcoholic_key = get_alcoholic_foreign_key(conn, cursor, alcohol)
    return { 
        "drink_name" : drink_name,
        "alternate_drink_name" : alternate_drink_name,
        "date_modified" : date_modified,
        "glass_id" :  glass_key,
        "category_id" : category_key,
        "alcoholic_id" : alcoholic_key,
        "id" : drink_id
        }


def instructions_json_to_df(records):
    instructions_df = pd.DataFrame.from_records(records)
    instructions_df.rename(columns=instructions_mapping, inplace=True)
    return instructions_df


def drinks_json_to_df(records):
    drinks_df = pd.DataFrame.from_records(records)
    drinks_df = drinks_df[["drink_name", "alternate_drink_name", "date_modified", "glass_id", "category_id", "alcoholic_id", "id"]]
    return drinks_df    


def recipes_json_to_df(records):
    recipes_df = pd.DataFrame.from_records(records)
    recipes_df = recipes_df[["ingredient_id", "measure_id", "drink_id"]]
    return recipes_df    


def bulk_load_to_drinks(conn:str, cursor:str, dataframe):
    try:
        cursor.executemany('''INSERT INTO drinks (drink_name, alternate_drink_name, date_modified, glass_id, category_id, alcoholic_id, id)
                     VALUES (?, ?, ?, ?, ?, ?, ?)''', dataframe.to_records(index=False))
        conn.commit()
        return True
    except Exception as error:
        return error   


def bulk_load_to_instructions(conn:str, cursor:str, dataframe):
    try:
        cursor.executemany('''INSERT INTO instructions (instructions_en, instructions_es, instructions_de, instructions_fr, instructions_it, instructions_zh_hans, instructions_zh_hant, drink_id)
                     VALUES (?, ?, ?, ?, ?, ?, ?, ?)''', dataframe.to_records(index=False))
        conn.commit()
        return True
    except Exception as error:
        return error


def bulk_load_to_recipes(conn:str, cursor:str, dataframe):
    try:
        cursor.executemany('''INSERT INTO drink_recipe (ingredient_id, measure_id, drink_id)
                     VALUES (?, ?, ?)''', dataframe.to_records(index=False))
        conn.commit()
        return True
    except Exception as error:
        return error


def process_batch_records(conn:str, cursor:str, drinks_data, batch_id:str):
    logging.info(f"batch id : [{batch_id}] processing [{len(drinks_data)}] number of records.")
    drinks_ls = []
    instructions_ls = []
    recipes_ls = []
    unprocessed_records = []
    for drink in drinks_data:
        instructions_de = drink.get("strInstructionsDE")
        drink_name = drink.get("strDrink")
        drink_id = drink.get("idDrink")
        logging.info(f"Processing drink: [{drink_name}] with drink id: [{drink_id}] and batch id: [{batch_id}]")
        if instructions_de == None:
            logging.info(f"Skipping drink: [{drink_name}] with drink id: [{drink_id}] with batch id: [{batch_id}] because instructions in DE: [{instructions_de}]")
            unprocessed_records.append(drink)
            continue

        elif instructions_de:
            # Room for improvement: validate the record, something like the following
            #is_vaidated = validate_json_record(record)
            instructions_record = get_instructions_entry(conn, cursor, drink, drink_id) 
            instructions_ls.append(instructions_record)
            drinks_record = get_drinks_record(conn, cursor, drink)
            drinks_ls.append(drinks_record)
            recipe_records = get_recipe_df(conn, cursor, drink, drink_id)
            recipes_ls.extend(recipe_records)
        
        # Convert the record in pandas dataframes for batch loading in the database using execute_many command
        instructions_df = instructions_json_to_df(instructions_ls)
        drinks_df = drinks_json_to_df(drinks_ls)
        recipe_df = recipes_json_to_df(recipes_ls)
  
    logging.info(f"Successfully processed [{len(drinks_data)}] number of records with batch id: [{batch_id}]")
    return unprocessed_records, instructions_df, drinks_df, recipe_df
    

def bulk_loading(conn:str, cursor:str, dataframes:dict, batch_id:str):
    logging.info(f"Loading data for batch id: [{batch_id}]") 

    # loading the data for the batch into the sqlite database
    instructions_df = dataframes.get("instructions_df")
    drinks_df = dataframes.get("drinks_df")
    recipe_df = dataframes.get("recipe_df")
    ret_ins = bulk_load_to_instructions(conn, cursor, instructions_df)
    ret_drinks = bulk_load_to_drinks(conn, cursor, drinks_df)
    ret_recipes = bulk_load_to_recipes(conn, cursor, recipe_df)

    return ret_ins, ret_drinks, ret_recipes