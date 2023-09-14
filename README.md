# science-portal-seeding
This script will parse through the UHN publication excel spreadsheet and extract publications with article types: research-articles, journal articles, and articles. The script then compiles this data into a JSON with required fields that is directly added to a mongo collection of choice defined in your enironment file.

pip dependencies needed are python-dotenv, pandas, pymongo, and openpyxl(dependency for another package):

pip install python-dotenv pandas pymongo openpyxl

