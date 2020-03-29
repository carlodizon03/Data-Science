import pandas as pd 
import numpy as np
import json

data = pd.read_csv('Data/USvideos.csv')

#print(data)

#print(data.dtypes)

#print(data.head(10))

#print(data.tail(3))

#print(data.index)

#print(data.columns)

#print(data.to_numpy())

#print(data.describe())

#print(data.T)

#print(data['video_id'])

#print(data['trending_date'])

#rows selection
#print(data[0:2])
#pd.set_option('max_rows',5)
#pd.set_option('colheader_justify','left')
#pd.set_option('column_space',15)
#pd.set_option('display.expand_frame_repr', False)


samples = data.sample(n=10)
print(samples)
print(samples.dtypes)

new_df = pd.DataFrame(samples, columns = ['views','likes','comments_disabled','ratings_disabled','category_id'])
print(new_df)

with open('Data/US_category_id.json') as f:
    data = json.load(f)
    print("Total number of categories: {0}".format(len(data['items'])))
    categories = []
    for item in data['items']:
        categories.append(item['snippet']['title'])

print(categories)