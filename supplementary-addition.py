import pandas as pd
import os
import pymongo
import certifi
import json
from dotenv import load_dotenv

load_dotenv()

# MongoDB connection parameters
client = pymongo.MongoClient(os.getenv("MONGO_URI"), tlsCAFile=certifi.where())
db_name = client[os.getenv("DB_NAME")]
collection = db_name[os.getenv("PUBLICATION_COLLECTION")]

df = pd.read_excel('./input-data/UHNPublication_scrapped_results.xlsx', sheet_name="Results_June4", header=0)


for document in collection.find():
	name = document.get('name', '')




