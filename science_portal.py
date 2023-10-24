import os
import json
from dotenv import load_dotenv
import pandas as pd
from pymongo import MongoClient

# Load .env
load_dotenv()

# MongoDB connection parameters
mongo_uri = os.getenv("MONGO_URI")
db_name = os.getenv("DB_NAME")
collection_name = os.getenv("COLLECTION_NAME")

# Define default values for empty fields
default_values = {

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
        "PDF": "",
        "other": ""       
	},

}

# Load data from Excel file into a pandas DataFrame
excel_file = os.getenv("EXCEL_SHEET")
df = pd.read_excel(excel_file, sheet_name="2022", header=0)


# Chose which columns wanted and rename accordingly
selected_columns = ['PMID', 'doi', 'Date', 'Title', 'Journal', 'Article Type', 'Author List', 'Filtered Author List', 'All Affiliations', 'Filtered Affiliations']
df_selected = df[selected_columns]
df_selected = df_selected.rename(columns={
    'Date': 'date',
    'Title': 'name',
    'Journal': 'journal',
    'Article Type': 'type',
	'Author List': 'authors',
    'Filtered Author List': 'filteredAuthors',
    'All Affiliations': 'affiliations',
    'Filtered Affiliations': 'filteredAffiliations' 
})

# Convert 'PMID' column to nullable integer type
df_selected['PMID'] = pd.to_numeric(df_selected['PMID'], errors='coerce').astype(pd.Int64Dtype())

# Be sure to only extract specfic types of articles and dates contain 2022
# filtered_selected_df = df_selected[
#     df_selected['type'].isin(['research-article', 'Journal Article', 'Article'])
#     & df_selected['date'].str.contains('2022')
#     & (df_selected['authors'].str.contains('Princess Margaret')
#        | df_selected['authors'].str.contains('PMC')
#        | df_selected['filteredAuthors'].str.contains('Princess Margaret')
#        | df_selected['filteredAuthors'].str.contains('PMC')
#        | df_selected['affiliations'].str.contains('Princess Margaret')
#        | df_selected['affiliations'].str.contains('PMC')
#        | df_selected['filteredAffiliations'].str.contains('Princess Margaret')
#        | df_selected['filteredAffiliations'].str.contains('PMC'))
# ]

filtered_selected_df = df_selected[
    (df_selected['type'].str.contains('research-article|Journal Article|Article', na=False))
    & (~df_selected['type'].str.contains('early-review', case=False, na=False))
    & (~df_selected['type'].str.contains('Early Access', case=False, na=False))
    & (~df_selected['type'].str.contains('brief-report', case=False, na=False))
    & (~df_selected['type'].str.contains('Review', na=False))
    & (~df_selected['type'].str.contains('Video-Audio Media', case=False, na=False))
    & (df_selected['date'].str.contains('2022', na=False))
    & ((df_selected['authors'].str.contains('Princess Margaret', na=False))
       | (df_selected['authors'].str.contains('PMC', na=False))
       | (df_selected['filteredAuthors'].str.contains('Princess Margaret', na=False))
       | (df_selected['filteredAuthors'].str.contains('PMC', na=False))
       | (df_selected['affiliations'].str.contains('Princess Margaret', na=False))
       | (df_selected['affiliations'].str.contains('PMC', na=False))
       | (df_selected['filteredAffiliations'].str.contains('Princess Margaret', na=False))
       | (df_selected['filteredAffiliations'].str.contains('PMC', na=False)))
]

# Convert 'journal' column to lowercase
filtered_selected_df['journal'] = filtered_selected_df['journal'].str.lower()

# Create the 'image' field
filtered_selected_df['image'] = filtered_selected_df['journal'].str.replace(' ', '_') + '.jpg'

unique_journals = filtered_selected_df['journal'].unique().tolist()

print(len(unique_journals))

json_output_file = "unique_journals.json"
with open(json_output_file, 'w') as f:
    json.dump(unique_journals, f)

# Convert 'PMID' column to nullable integer type in the filtered dataframe as well
filtered_selected_df['PMID'] = pd.to_numeric(filtered_selected_df['PMID'], errors='coerce').astype(pd.Int64Dtype())


print(filtered_selected_df)
print(filtered_selected_df.columns)

# Convert DataFrame to a list of dictionaries (one per row)
data = filtered_selected_df.to_dict(orient="records")

# Add default values to each document
for document in data:
    document.update(default_values)

print(len(data))
        

# Connect to MongoDB and insert
client = MongoClient(mongo_uri)
db = client[db_name]
collection = db[collection_name]

collection.insert_many(data)

client.close()

print(f"Data from '{excel_file}' has been successfully added to '{db_name}.{collection_name}'")
