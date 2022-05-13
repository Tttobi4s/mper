import socket
import random
import numpy as np
from hashlib import md5

np.random.seed(100)
data_p1 = np.random.randint(0, pow(2, 24), pow(2, 20), dtype=np.int64)


s_csp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s_center = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s_csp.connect(('127.0.0.1', 8002))
s_center.connect(('127.0.0.1', 8001))
s_csp.setsockopt(
    socket.SOL_SOCKET,
    socket.SO_SNDBUF,
    16 * 1048576 + 10)
s_csp.setsockopt(
    socket.SOL_SOCKET,
    socket.SO_RCVBUF,
    16 * 1048576 + 10)
s_center.setsockopt(
    socket.SOL_SOCKET,
    socket.SO_SNDBUF,
    16 * 1048576 + 10)
s_center.setsockopt(
    socket.SOL_SOCKET,
    socket.SO_RCVBUF,
    16 * 1048576 + 10)


md5_data_p1 = []
for ele in data_p1:
    m = md5(str(ele).encode("utf-8")).hexdigest()
    m = (32 - len(m)) * "0" + m
    md5_data_p1.append(m)


for i in range(9):
    tmp_data = 1048576 * [0]
    for m in md5_data_p1:
        tmp_data[int(m[3 * i : 3 * i + 5], base=16)] = 1

    tmp_center, tmp_csp = [], []
    for j in range(1048576):
        if tmp_data[j] == 1:
            r = random.getrandbits(128)
            tmp_csp.append(r.to_bytes(16, 'big'))
            tmp_center.append(r.to_bytes(16, 'big'))
        else:
            tmp_csp.append(random.getrandbits(128).to_bytes(16, 'big'))
            tmp_center.append(random.getrandbits(128).to_bytes(16, 'big'))
    s_csp.send(b''.join(tmp_csp))
    s_center.send(b''.join(tmp_center))

s_center.close()

# 验证数据集
res = []
for i in range(9):
    data = s_csp.recv(16 * 1048576)
    str_sec = bin(int.from_bytes(data, 'big'))[2:]
    str_sec = (128 * 1048576 - len(str_sec)) * "0" + str_sec
    tmp_res = [0] * 1048576
    for j in range(1048576):
        if str_sec[128 * j: 128 * j + 128] == 128 * "0":
            tmp_res[j] = 1
    res.append(tmp_res)

cnt = 0
for m in md5_data_p1:
    for i in range(9):
        if res[i][int(m[3 * i: 3 * i + 5], base=16)] == 0:
            break
        if i == 8:
            cnt += 1
print(cnt)

s_csp.close()
