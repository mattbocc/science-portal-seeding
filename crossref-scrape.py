import pandas as pd
import requests
import time
import json
import datetime

doi_fails = []
no_journal_or_publisher = []

def fetch_crossref_data(doi, email):
    """Fetch publication data from CrossRef API using the DOI."""
    url = f"https://api.crossref.org/works/{doi}"
    headers = {
        'User-Agent': f'Python-requests/ {requests.__version__}',
        'Mailto': email
    }
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()
        created_date = data['message']['created']['date-time'][:10]  # Extract only the date part YYYY-MM-DD

        #If journal title exists retrieve it, else create list of dois with no journals
        journal_title = data['message'].get('container-title')

        #If journal title exists retrieve it, else create list of dois with no journals
        publisher = data['message']['publisher']

        if journal_title:
            journal_title = journal_title[0]
        else:
            if publisher == '':
                no_journal_or_publisher.append(doi)
                print(f"No journal or publisher {doi}")
            journal_title = ''
        return created_date, journal_title, publisher
    except requests.RequestException as e:
        print(f"Error fetching data for DOI {doi}: {str(e)}")
        doi_fails.append(doi)
        print(doi_fails)
        return None, None, None

def update_dataframe(csv_path, output_path, email):
    """Update the DataFrame with new Date and Journal information from CrossRef."""
    df = pd.read_csv(csv_path)

    # Add initialize new columns and set their default values
    df['citations'] = 0
    df['rating'] = ""
    df['dateAdded'] = str(datetime.datetime.now())[:10]

    # Iterate over each row in the DataFrame
    for index, row in df.iterrows():
        if pd.notna(row['doi']):  # Check if DOI exists
            created_date, journal_title, publisher = fetch_crossref_data(row['doi'], email)
            if created_date and journal_title != '' and publisher:
                df.at[index, 'date'] = created_date
                df.at[index, 'journal'] = journal_title
                df.at[index, 'publisher'] = publisher
                df.at[index, 'status'] = 'Published'
            elif created_date and journal_title == '' and publisher:
                df.at[index, 'date'] = created_date
                df.at[index, 'journal'] = journal_title
                df.at[index, 'publisher'] = publisher
                df.at[index, 'status'] = 'Preprint'
                print("Preprint!")

        time.sleep(0.25)
        print(f"Updated row {index + 1}/{len(df)}")

    # # Convert journal names to titles (capitalize first letter of each 
    # df['journal'] = df['journal'].str.title()

    # Extract all unique journals into a JSON file
    unique_journals = df['journal'].unique().tolist()
    unique_journal_total = len(unique_journals)
    print(f"Total unique journals {unique_journal_total}")

    with open("./output-data/json-logs/unique_journals.json", 'w') as f:
        json.dump(unique_journals, f)

    with open("./output-data/json-logs/doi_fails.json", 'w') as f:
        json.dump(doi_fails, f)

    with open("./output-data/json-logs/no_journal.json", 'w') as f:
        json.dump(no_journal_or_publisher, f)

    # Extract journals, set to lowercase, replace spaces with underscores and add to the image slot
    lowercase_journal = df['journal'].str.lower()
    df['image'] = lowercase_journal.str.replace(' ', '_') + '.jpg'

    df.to_csv(output_path, index=False)
    print("Update complete and CSV saved.")

your_email = 'matthew.boccalon@uhn.ca'
input_csv_path = './input-data/publication-lists/UHN-publications-combined.csv'
output_csv_path = './output-data/UHN-publications-crossref-update.csv'

update_dataframe(input_csv_path, output_csv_path, your_email)
