import pandas as pd

# Load the Excel files
df_2022 = pd.read_excel('./input-data/publication-lists/UHN-publications-2022.xlsm', sheet_name="2022", header=0)
df_2023 = pd.read_excel('./input-data/publication-lists/UHN-publications-2023.xlsm', sheet_name="2023", header=0)
df_2024 = pd.read_excel('./input-data/publication-lists/UHN-publications-2024.xlsm', sheet_name="2024", header=0)

print(df_2022.columns)
print(df_2023.columns)
print(df_2024.columns)

# Combine the DataFrames
df_combined = pd.concat([df_2022, df_2023, df_2024], ignore_index=True)

# Optionally, save the combined DataFrame to a new csv file
df_combined.to_csv('./input-data/publication-lists/UHN-publications-combined.csv', index=False)
