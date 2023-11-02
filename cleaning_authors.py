from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()

client = MongoClient(os.getenv("MONGO_URI"))
db = client[os.getenv("DB_NAME")]
collection = db[os.getenv("COLLECTION_NAME")]

def clean_author_names(author_string):
    # Split the author string by semicolon
    authors = author_string.split(';')
    cleaned_authors = []
    
    for author in authors:
        # Split each author by comma and strip any whitespace
        names = author.split(',')
        if len(names) > 1:
            last_name = names[0].strip()
            cleaned_authors.append(last_name)
        else:
            # If there's no comma, just use the whole name
            cleaned_authors.append(names[0].strip())
            
    # Join the cleaned last names with a semicolon
    return '; '.join(cleaned_authors)

# Iterate through the documents in the collection
for document in collection.find():
    # Clean the 'authors' field
    cleaned_authors = clean_author_names(document['authors'])
    
    # Update the document with the cleaned 'authors' field
    collection.update_one(
        {'_id': document['_id']},
        {'$set': {'authors': cleaned_authors}}
    )
    print(cleaned_authors)

print('Author names cleaned successfully.')
