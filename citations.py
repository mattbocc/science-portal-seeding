import os
from dotenv import load_dotenv
from scholarly import scholarly
import pymongo

# MongoDB connection parameters
client = pymongo.MongoClient(os.getenv("MONGO_URI"))
db_name = client[os.getenv("DB_NAME")]
collection = db_name[os.getenv("COLLECTION_NAME")]

# Iterate through each document in the collection
for document in collection.find():
    name = document.get('name', '')
    
    # Search for the publication on Google Scholar
    search_publication = scholarly.search_single_pub(name)
    
    if search_publication:
        # Get the number of citations
        num_citations = search_publication.get('num_citations', 0)
        
        # Update the 'citations' field in the document
        collection.update_one(
            {"_id": document["_id"]},
            {"$set": {"citations": num_citations}}
        )
    else:
        print(f"Publication '{name}' not found on Google Scholar.")

client.close()
