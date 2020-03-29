import pandas as pd 
import numpy as np
import json
import pprint
from scipy import stats

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
#print(samples)
#print(samples.dtypes)

new_df = pd.DataFrame(samples, columns = ['views','likes','comments_disabled','ratings_disabled','category_id'])
print(new_df)

with open('Data/US_category_id.json') as f:
    data = json.load(f)
    #print(data['items'][0])
    #print("Total number of categories: {0}".format(len(data['items'])))

    categories = {}
    for item in data['items']:
        categories[item['id']] = item['snippet']['title']
        #categories.append(item['snippet']['title'])


#pprint.pprint(categories)

num_attrib = pd.DataFrame(new_df, columns = ['views', 'likes'])

print(num_attrib.corr(method = 'pearson'))


crosstab = pd.crosstab(new_df['comments_disabled'],new_df['category_id'])
print(crosstab)
chi2,p_value,dof,freqs = stats.chi2_contingency(crosstab)
print(chi2)
#chi2 tells the discrepancies between the expected and the actual result
#since we've got 0 or pretty low result, it means that there are no or low correlation between these two categories 


def normalize(col):
    min = np.min(col)
    max = np.max(col)
    range = max - min

    return [(item - min) / range for item in col]


new_df['views'], new_df['likes'] = normalize(new_df['views']), normalize(new_df['likes'])

print(new_df)

new_df['views'], new_df['likes']  = pd.cut(new_df['views'],3, labels=["Low","Medium","High"]),  pd.cut(new_df['likes'],3, labels=["Low","Medium","High"])
print(new_df)
