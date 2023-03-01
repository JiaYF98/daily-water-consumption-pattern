"""
通过K-means算法去除记录有很大误差的天数
"""
from itertools import chain

import numpy as np
import pandas as pd

d = {'a': [1, 2, 3], 'b': None, 'c': [4, 5, 6]}
temp_label = pd.DataFrame(data=d)
a = temp_label.columns[1]
b = temp_label.loc[1]

means = temp_label.mean().fillna(0)
t = np.reshape(means.to_numpy(), (means.size, 1))
print(means)

