import pandas as pd
import json


df = pd.read_csv('Data/USvideos.csv')

with open('Data/US_category_id.json') as f:
    data = json.load(f)
  
    categories = {}
    for item in data['items']:
        categories[item['id']] = item['snippet']['title']

for index, row in df.iterrows():
    df.loc[index, 'category_id'] = categories[str(row['category_id'])]


df.to_csv("Data/USvideos_catNames.csv")
print("done!")