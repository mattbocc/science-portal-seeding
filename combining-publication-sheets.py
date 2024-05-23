import pandas as pd
import json

# Load the Excel files
df_2022 = pd.read_excel('./input-data/publication-lists/UHN-publications-2022.xlsm', sheet_name="2022", header=0)
df_2023 = pd.read_excel('./input-data/publication-lists/UHN-publications-2023.xlsm', sheet_name="2023", header=0)
df_2024 = pd.read_excel('./input-data/publication-lists/UHN-publications-2024.xlsm', sheet_name="2024", header=0)

print(df_2022.columns)
print(df_2023.columns)
print(df_2024.columns)

# Combine the DataFrames
df_combined = pd.concat([df_2022, df_2023, df_2024], ignore_index=True)

# Chose which columns are wanted and rename accordingly
selected_columns = ['PMID', 'doi', 'Date', 'Title', 'Journal', 'Article Type', 'Author List', 'Filtered Author List', 'All Affiliations']
df_selected = df_combined[selected_columns]
df_selected = df_selected.rename(columns={
    'Date': 'date',
    'Title': 'name',
    'Journal': 'journal',
    'Article Type': 'type',
	'Author List': 'authors',
    'Filtered Author List': 'filteredAuthors',
    'All Affiliations': 'affiliations',
})

df_selected['PMID'] = pd.to_numeric(df_selected['PMID'], errors='coerce').astype(pd.Int64Dtype())

#Filter dataframe based on type and affiliation criteria
filtered_selected_df = df_selected[
    (
        (df_selected['type'].str.contains('research-article', case=False, na=False))
        | (df_selected['type'].str.contains('Article', case=False, na=False))
    )
    & (~df_selected['type'].str.contains('early-review', case=False, na=False))
    & (~df_selected['type'].str.contains('Early Access', case=False, na=False))
    & (~df_selected['type'].str.contains('brief-report', case=False, na=False))
    & (~df_selected['type'].str.contains('Review', case=False, na=False))
    & (~df_selected['type'].str.contains('Preprint', case=False, na=False))
    & (~df_selected['type'].str.contains('Video-Audio Media', case=False, na=False))
    & 
    (
        (df_selected['affiliations'].str.contains('Princess Margaret', case=False, na=False))
        | (df_selected['affiliations'].str.contains('PMC', case=False, na=False))
    )
]

filtered_selected_df['affiliations'] = filtered_selected_df['affiliations'].str.replace('/', '')


# Save the combined DataFrame to a new csv file
filtered_selected_df.to_csv('./input-data/publication-lists/UHN-publications-combined.csv', index=False)
