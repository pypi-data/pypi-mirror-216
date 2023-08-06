import pandas as pd
import json
import re
import urllib.request as request
from pathlib import Path


def UP(species):
    url = 'http://rest.kegg.jp/conv/%s/uniprot'
    response = request.urlopen(url % species).read().decode('utf-8')
    response = response.rstrip().rsplit('\n')
    entrez = []
    uniprot = []
    for resp in response:
        uniprot.append(resp.rsplit()[0])
        entrez.append(resp.rsplit()[1])
    d = {}
    for key, value in zip(entrez, uniprot):
        if key not in d:
            d[key] = [value]
        else:
            d[key].append(value)
    return d

file = Path('all_tests/trouble/hsa04261.tsv')
df = pd.read_csv(file, delimiter = '\t')
conv = UP('hsa')
df['match1'] = df['entry1'].str.extract(r'(-[0-9]+)')
df['match2'] = df['entry2'].str.extract(r'(-[0-9]+)')
df['entry1'] = df['entry1'].str.replace(r'(-[0-9]+)', '', regex=True)
df['entry2'] = df['entry2'].str.replace(r'(-[0-9]+)', '', regex=True)
df['entry1'] = df['entry1'].map(conv)
df['entry2'] = df['entry2'].map(conv)
df1 = df.dropna()
for index, row in df1.iterrows():
    df1.loc[index, 'entry1'] = [x.replace('up:', '') + row['match1'] for x in row['entry1']]
    df1.loc[index, 'entry2'] = [y.replace('up:', '') + row['match2'] for y in row['entry2']]
df_out = df1.explode('entry1', ignore_index = True).explode('entry2', ignore_index = True)
df_out.drop(['match1', 'match2'], axis = 1, inplace = True)
df_out.to_csv('up_%s' % file.name, sep = '\t', index = False)

graphics = Path('all_tests/trouble/hsa04261_graphics.txt')
pos = open(graphics)
d = json.loads(pos.read())
up_dict = {}
for key, items in d.items():
    pattern = re.search(r'(-[0-9]+)', key)
    new_keys = re.sub(r'(-[0-9]+)', '', key)
    try:
        uplist = conv[new_keys]
        new_up = [up + pattern.group() for up in uplist]
        up_dict[str(new_up)] = items
        for up in new_up:
            up_dict[up.replace('up:', '')] = items
    except KeyError:
        pass
with open('up_{}'.format(graphics.name), 'w') as outfile:
    outfile.write(json.dumps(up_dict))
#%%
df1 = pd.read_csv('up_hsa/up_hsa04261.tsv', sep = '\t')
df2 = pd.read_csv('up_hsa04261.tsv', sep = '\t')
df3 = pd.concat([df1, df2]).drop_duplicates(keep = False)
df3.to_csv('corupted.tsv', sep = '\t')