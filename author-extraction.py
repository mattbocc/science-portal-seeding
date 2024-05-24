import os
import pandas as pd
from dotenv import load_dotenv

load_dotenv()
#Extract authors from PI list

input_file = os.getenv("AUTHOR_SHEET")
data = pd.read_csv(f'./input-data/{input_file}', encoding='ISO-8859-1')
    
filtered_data = data[data['Primary Research Institute'] == 'PM']
filtered_data = data[data['Primary Appointment'].str.contains('scientist', case=False)]
    
filtered_data.to_csv(f'./output-data/authors.csv', index=False)

