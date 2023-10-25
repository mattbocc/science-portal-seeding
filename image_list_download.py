from icrawler.builtin import GoogleImageCrawler
import json
import time
import random
import os

with open('unique_journals.json', 'r') as f:
    unique_journals = json.load(f)

# filters = dict(
#     size='large',
# )

for idx, journal in enumerate(unique_journals, start=1):
    google_Crawler = GoogleImageCrawler(storage={'root_dir': f'journal_images/{journal}'})
    google_Crawler.crawl(keyword=f'{journal} journal', max_num=5)
    time.sleep(random.randint(4, 10))

# Renaming the files
for journal in unique_journals:
    directory = f'journal_images/{journal}'
    for count, filename in enumerate(os.listdir(directory), 1):
        if filename.endswith(".jpg") or filename.endswith(".png"):
            journal_name = journal.replace(" ", "_")
            extension = filename.split(".")[-1]
            os.rename(os.path.join(directory, filename),
                      os.path.join(directory, f"{journal_name}{count}.{extension}")
            )
