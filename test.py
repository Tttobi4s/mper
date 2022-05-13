import numpy as np
from functools import reduce


# 随机数
np.random.seed(100)
data_p1 = np.random.randint(0, pow(2, 24), pow(2,20), dtype=np.int64)
np.random.seed(101)
data_p2 = np.random.randint(0, pow(2, 24), pow(2,20), dtype=np.int64)
np.random.seed(102)
data_p3 = np.random.randint(0, pow(2, 24), pow(2,20), dtype=np.int64)
print(reduce(np.intersect1d,[data_p1,data_p2,data_p3]))
print(len(reduce(np.intersect1d,[data_p1,data_p2,data_p3])))

