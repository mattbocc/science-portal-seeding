#Script to extract all PM authors

import os
import certifi
from dotenv import load_dotenv
import pandas as pd
import pymongo

load_dotenv()

# Connect to mongoDB collection
client = pymongo.MongoClient(os.getenv("MONGO_URI"), tlsCAFile=certifi.where())
db = client[os.getenv("DB_NAME")]
collection = db["authors"]

# Read and load excel file
file_path = './input/UHN-PIs.xlsx'
df = pd.read_excel(file_path)

# Filter Princess Margaret PIs
filtered_df = df[df['Primary Research Institute'] == 'PM']
# Filter only by scientists
filtered_df = filtered_df[filtered_df['Primary Appointment'].str.contains('scientist', case=False)]

# Insert data into author collection
data = filtered_df.to_dict('records')
print(len(data))
result = collection.insert_many(data)

print("Data inserted with ids:", result.inserted_ids)
