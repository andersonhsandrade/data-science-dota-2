from email import header
from typing import Collection
import requests
from pymongo import MongoClient
import os
import dotenv
from tqdm import tqdm
import time

def get_data(match_id):
    header = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
    url = f"https://api.opendota.com/api/matches/{match_id}"
    data = requests.get(url, headers=header).json()

    return data

def save_data(data, db_collection):
    try:
        db_collection.delete_one({"match_id": data["match_id"]})
        db_collection.insert_one(data)
    except KeyError:
        return False
    return True

def find_match_ids(mongodb_database):
    collection_history = mongodb_database['pro_match_history']
    collection_details = mongodb_database['pro_match_details']
    
    match_history = set([i["match_id"] for i in collection_history.find( {}, {"match_id": 1})])
    match_details = set([i["match_id"] for i in collection_details.find( {}, {"match_id": 1})])

    match_ids = list(match_history - match_details)

    return match_ids

def main():

    # Carrega o dotenv
    dotenv.load_dotenv(dotenv.find_dotenv())
    MONGODB_IP = os.getenv("MONGODB_IP")
    MONGODB_PORTA = int(os.getenv("MONGODB_PORT"))
        
    mongodb_client = MongoClient(MONGODB_IP, MONGODB_PORTA)
    mongodb_database = mongodb_client['dota-raw']

    for match_id in tqdm(find_match_ids(mongodb_database)):
        data = get_data(match_id)
        if save_data(data, mongodb_database['pro_match_details']):
            time.sleep(1)
        else:
            print(data)
            time.sleep(60)

if __name__ == "__main__":
    main()