import os
from dotenv import load_dotenv
import pandas as pd
from pymongo import MongoClient

# Load environment variables from .env
load_dotenv()

# Define MongoDB connection parameters
mongo_uri = os.getenv("MONGO_URI")
db_name = os.getenv("DB_NAME")
collection_name = os.getenv("COLLECTION_NAME")

# Define default values for empty fields
default_values = {
    
    "doiLink": "",
    "rating": "",
    "citations": "",
    "status": "",
    "repoLinks": {
        "codeOcean": "",
		"github": "",
        "dggap": "",
        "GEO": "",
        "EGA": "",
        "protocols": "",
        "other": ""       
	},

}

# Load data from Excel file into a pandas DataFrame
excel_file = os.getenv("EXCEL_SHEET")
df = pd.read_excel(excel_file, sheet_name="2022", header=0)


# Chose which columns wanted and rename accordingly
selected_columns = ['PMID', 'doi', 'Date', 'Title', 'Journal', 'Article Type', 'Author List']
df_selected = df[selected_columns]
df_selected = df_selected.rename(columns={
    'Date': 'date',
    'Title': 'name',
    'Journal': 'journal',
    'Article Type': 'type',
	'Author List': 'authors'   
})

# Be sure to only extract specfic types of articles and dates contain 2022
filtered_selected_df = df_selected[df_selected['type'].isin(['research-article', 'Journal Article', 'Article']) & df_selected['date'].str.contains('2022')]

print(filtered_selected_df)
print(filtered_selected_df.columns)

# Convert DataFrame to a list of dictionaries (one per row)
data = filtered_selected_df.to_dict(orient="records")

# Add default values to each document
for document in data:
    document.update(default_values)

print(data)
        

# Connect to MongoDB
client = MongoClient(mongo_uri)
db = client[db_name]
collection = db[collection_name]

# Insert data into MongoDB collection
# collection.insert_many(data)

# # Close MongoDB connection
# client.close()

# print(f"Data from '{excel_file}' has been successfully added to '{db_name}.{collection_name}' with empty fields.")
