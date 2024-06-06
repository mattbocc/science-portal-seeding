import os
from dotenv import load_dotenv
from scholarly import scholarly
import certifi
import pymongo
import random
import time
import json

load_dotenv()

# MongoDB connection parameters
client = pymongo.MongoClient(os.getenv("MONGO_URI"), tlsCAFile=certifi.where())
db_name = client[os.getenv("DB_NAME")]
collection = db_name[os.getenv("PUBLICATION_COLLECTION")]

no_scholar_list = []

# Iterate through each document in the collection
for document in collection.find():
    name = document.get('name', '')
    doi = document.get('doi', '')
    
    try:
        # Search for the publication on Google Scholar by doi
        search_publication = scholarly.search_single_pub(doi)
        
        if search_publication is not None:
            # Get the number of citations
            num_citations = int(search_publication.get('num_citations', 0))

            if num_citations != 0:
                # Update the 'citations' field in the document
                collection.update_one(
                    {"_id": document["_id"]},
                    {"$set": {"citations": num_citations}}
                )
                print(f'{name} entered {num_citations}')
            else:
                print(f"No citations found for publication '{name}'.")
        else:
            print(f"Publication '{name}' not found on Google Scholar.")
    except:
        no_scholar_list.append(name)
        print(f'Cannot get citations for {name} publication')
    
    time.sleep(random.randint(8, 20))

client.close()

# Write no_scholar_list to a JSON file
with open('no_scholar_list.json', 'w') as json_file:
    json.dump(no_scholar_list, json_file)