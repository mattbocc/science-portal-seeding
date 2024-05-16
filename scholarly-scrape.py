import pandas as pd
from scholarly import scholarly

# Load the CSV data
df = pd.read_csv('path_to_your_csv.csv')

def update_publication_details(row):
    try:
        # Search for the publication on Google Scholar by DOI
        search_publication = scholarly.search_single_pub(row['doi'])
        if search_publication:
            # Update the date and journal name if available
            row['Date'] = search_publication.get('pub_year', row['Date'])
            row['Journal'] = search_publication.get('journal', row['Journal'])
    except Exception as e:
        print(f"Failed to update for DOI {row['doi']}: {str(e)}")
    return row

# Apply the function to each row in the DataFrame
df = df.apply(update_publication_details, axis=1)

# Save the updated DataFrame to a new CSV file
df.to_csv('updated_publications.csv', index=False)
