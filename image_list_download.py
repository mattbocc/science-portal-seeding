from icrawler.builtin import GoogleImageCrawler
import json
import time
import random
import os

with open('output-data/json-logs/unique_journals.json', 'r') as f:
    unique_journals = json.load(f)
    
filters = dict(
    date=((2024, 1, 1), (2025, 1, 1))
)

no_directory = []



for idx, journal in enumerate(unique_journals, start=1):
    print(f"Processing journal {idx}/{len(unique_journals)}: {journal}")
    try:
        google_Crawler = GoogleImageCrawler(storage={'root_dir': f'journal-images/{journal}'})
        google_Crawler.crawl(keyword=f'{journal}', filters=filters, max_num=5)
    except Exception as e:
        print(f"Error crawling for journal {journal}: {e}")
    time.sleep(random.randint(1, 2))

# Renaming the files
for journal in unique_journals:
    directory = f'journal-images/{journal}'
    if not os.path.exists(directory):
        print(f"Directory not found for journal {journal}, skipping...")
        no_directory.append(journal)
        continue
    for count, filename in enumerate(os.listdir(directory), 1):
        if filename.endswith(".jpg") or filename.endswith(".png"):
            journal_name = journal.replace(" ", "_")
            extension = filename.split(".")[-1]
            os.rename(os.path.join(directory, filename),
                      os.path.join(directory, f"{journal_name}{count}.{extension}"))
            
print(no_directory)
print("Script completed.")
