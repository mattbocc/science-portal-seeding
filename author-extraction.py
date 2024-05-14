import os
import pandas as pd
from dotenv import load_dotenv

load_dotenv()
#Extract authors from PI list

input_file = os.getenv("AUTHOR_SHEET")

data = pd.read_csv(f'/input-data/{input_file}')
    
filtered_data = data[data['Primary Research Institute'] == 'PM']
    
filtered_data.to_csv('/Users/mattbocc/uhn/science-portal-seeding/output-data', index=False)

