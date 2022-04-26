import requests
from pymongo import MongoClient
import dotenv
import os
import time
import argparse


def get_matches_batch(min_match_id=None):
    ''' Captura lista de partidas pro players. 
    '''
    url = "https://api.opendota.com/api/proMatches"

    if min_match_id != None:
        url += f"?less_than_match_id={min_match_id}"

    data = requests.get(url).json()

    return data

def save_matches(data, db_collection):
    '''Salva lista de partidas no banco de dados.'''
    db_collection.insert_many(data)
    return True

def get_oldest_matches(db_collection):
    min_match_id = db_collection.find_one(sort=[('match_id',1)])['match_id']
    while True:
        data = get_matches_batch(min_match_id)
        data = [i for i in data if 'match_id' in i]
        
        if len(data) == 0:
            break

        save_matches(data, db_collection)
        min_match_id = min([i['match_id'] for i in data])
        time.sleep(1)
    
    print("Finalizado captura de partidas antigas.")

def get_newest_matches(db_collection):
    max_match_id = db_collection.find_one(sort=[('match_id',-1)])['match_id']
    data = get_matches_batch()
    while True:
        try:
            max_match_index = [i['match_id'] for i in data].index(max_match_id)
            if max_match_index == 0:
                print("Não foi encontrado novas partidas.")
                break
            data_new = data[0:max_match_index]
            save_matches(data_new, db_collection)
            break
        except:
            save_matches(data, db_collection)

            data = get_matches_batch(data[99]['match_id'])
    
    print("Finalizado captura de partidas novas.")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--how", choices=['oldest', 'newest'])
    args = parser.parse_args()


    # Carrega o dotenv
    dotenv.load_dotenv(dotenv.find_dotenv())
    MONGODB_IP = os.getenv("MONGODB_IP")
    MONGODB_PORTA = int(os.getenv("MONGODB_PORT"))
        

    mongodb_client = MongoClient(MONGODB_IP, MONGODB_PORTA)
    mongodb_database = mongodb_client['dota-raw']


#data = get_matches_batch()
#save_matches(data, mongodb_database['pro_match_history'])
    if args.how == "oldest":
        get_oldest_matches(mongodb_database['pro_match_history'])
    elif args.how == "newest":
        get_newest_matches(mongodb_database['pro_match_history'])

if __name__ == "__main__":
    main()