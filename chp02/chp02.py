from pylab import *
import numpy as np;
import pandas as pd;
import matplotlib.pyplot as plt;

from collections import defaultdict
from collections import Counter
from pandas import DataFrame, Series
import json

path = 'usagov_bitly_data2012-03-16-1331923249.txt'
records = [json.loads(line) for line in open(path)]
print records[0]
print records[0]['tz']

time_zones = [rec['tz'] for rec in records if 'tz' in rec]
print time_zones[:10]


def get_counts(sequence):
    counts = {}
    for x in sequence:
        if x in counts:
            counts[x] += 1
        else:
            counts[x] = 1
    return counts


def get_counts2(sequence):
    counts = defaultdict(int)
    for x in sequence:
        counts[x] += 1
    return counts;


counts = get_counts2(time_zones)


def top_counts(count_dict, n=10):
    value_key_paris = [(count, tz) for tz, count in count_dict.items()]
    value_key_paris.sort()
    return value_key_paris[-n:]


print top_counts(counts)

counts = Counter(time_zones)
print counts.most_common(10)

frame = DataFrame(records)
print frame['tz'].value_counts()[:10]

clean_tz = frame['tz'].fillna('Missing')
clean_tz[clean_tz == ''] = 'Unknown'
tz_counts = clean_tz.value_counts()
print tz_counts[:10]
tz_counts[:10].plot(kind='barh', rot=0)

frame['a'][1]

results = Series([x.split()[0] for x in frame.a.dropna()])

results[:5]

results.value_counts()[:8]

cframe = frame[frame.a.notnull()]

operating_system = np.where(cframe['a'].str.contains('Windows'), 'Windows', 'Not Windows')
operating_system[:5]

by_tz_os = cframe.groupby(['tz', operating_system])
agg_counts = by_tz_os.size().unstack().fillna(0)

indexer = agg_counts.sum(1).argsort()
