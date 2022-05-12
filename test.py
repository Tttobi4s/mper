from hashlib import md5
import numpy as np
from functools import reduce

# np.random.seed(100)

# md5 哈希函数
i = 10
m = md5(str(100).encode("utf-8")).hexdigest()
m = (32 - len(m)) * "0" + m
print(len(m))
print(m)
print(int(m[-4:],base=16))

# 随机数
data_p1 = np.random.randint(0, pow(2, 24), pow(2,20), dtype=np.int64)
print(len(data_p1))
data_p2 = np.random.randint(0, pow(2, 24), pow(2,20), dtype=np.int64)
print(len(data_p2))
data_p3 = np.random.randint(0, pow(2, 24), pow(2,20), dtype=np.int64)
print(len(data_p3))
print(len(reduce(np.intersect1d,[data_p1,data_p2,data_p3])))

print("123".index("1",0))