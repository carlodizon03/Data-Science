import pandas as pd 
import numpy as np
import json
import pprint
from scipy import stats
from collections import  Counter
from scipy.stats import entropy
data = pd.read_csv('Data/USvideos.csv')



samples = data.sample(n=10)


new_df = pd.DataFrame(samples, columns = ['views','likes','comments_disabled','ratings_disabled','category_id'])
print(new_df)

with open('Data/US_category_id.json') as f:
    data = json.load(f)
  
    categories = {}
    for item in data['items']:
        categories[item['id']] = item['snippet']['title']



num_attrib = pd.DataFrame(new_df, columns = ['views', 'likes'])

print(num_attrib.corr(method = 'pearson'))


crosstab = pd.crosstab(new_df['comments_disabled'],new_df['ratings_disabled'])
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



pd_target_attr_category_id = Counter(new_df['category_id'])
print(pd_target_attr_category_id)
print(len(pd_target_attr_category_id))
p = []
for key,val in pd_target_attr_category_id.items():
    p.append(val/10)
print(p)
entropy_target_attr_category_id = entropy(p,base=2)
print(entropy_target_attr_category_id)
ct = pd.crosstab(new_df['views'],new_df['category_id'])
print(ct)
print(max(ct.count()))
num_view_labels = max(ct.count())
view_level_Pds = []
for view_label in range(num_view_labels):
    temp = []
    for label,content in ct.iteritems():
        print(label,content[view_label])
        temp.append(content[view_label]/len(pd_target_attr_category_id))
    view_level_Pds.append(temp)

print(view_level_Pds)

#category_vs_views entropy
entropy_category_vs_views = []
for arr in view_level_Pds:
    entropy_category_vs_views.append(entropy(arr,base=2))

print(entropy_category_vs_views)

#information gain
view_levels = Counter(new_df['views'])

sum_views_entropy  = 0
idx = 0
for key,val in view_levels.items():
    print("{0}: {1}/10".format(key,val))
    sum_views_entropy = sum_views_entropy+(val/10)*entropy_category_vs_views[idx]
    idx = idx+1
print("sum_views_entropy = {0}".format(sum_views_entropy))
print("information gain = {0}-{1}".format(entropy_target_attr_category_id,sum_views_entropy))
information_gain = entropy_target_attr_category_id-sum_views_entropy
print("information gain = {0})".format(information_gain))