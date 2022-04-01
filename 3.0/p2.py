import socket
import random
import numpy as np


cnt, batch_cnt = 2000000, 1000
data_p2 = np.random.randint(0, 2, cnt)


s_csp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s_center = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s_csp.connect(('127.0.0.1', 8002))
s_center.connect(('127.0.0.1', 8001))


# 传输单比特过滤
tmp_center_1, tmp_csp_1 = [], []
r2str = {0: "000", 1: "001", 2: "010", 3: "011",
         4: "100", 5: "101", 6: "110", 7: "111"}
for i in range(cnt):
    if data_p2[i] == 1:
        r = random.getrandbits(3)
        tmp_center_1.append(r2str[r])
        tmp_csp_1.append(r2str[r])
    else:
        tmp_center_1.append(r2str[random.getrandbits(3)])
        tmp_csp_1.append(r2str[random.getrandbits(3)])
s_center.send(int("".join(tmp_center_1), base=2).to_bytes((3 * cnt) // 8, 'big'))
s_csp.send(int("".join(tmp_csp_1), base=2).to_bytes((3 * cnt) // 8, 'big'))

dataspace_filter = bin(int.from_bytes(s_csp.recv(cnt // 8), 'big'))[2:]
dataspace_filter = "0" * (cnt - len(dataspace_filter)) + dataspace_filter


# 传输 128 位随机比特
tmp_center_128, tmp_csp_128 = [], []
for i in range(cnt):
    if dataspace_filter[i] == '1':
        continue
    if len(tmp_center_128) == batch_cnt:
        s_center.send(b''.join(tmp_center_128))
        s_csp.send(b''.join(tmp_csp_128))
        tmp_center_128.clear()
        tmp_csp_128.clear()
    if data_p2[i] == 1:
        r = random.getrandbits(128)
        tmp_center_128.append(r.to_bytes(16, 'big'))
        tmp_csp_128.append(r.to_bytes(16, 'big'))
    else:
        tmp_center_128.append(random.getrandbits(128).to_bytes(16, 'big'))
        tmp_csp_128.append(random.getrandbits(128).to_bytes(16, 'big'))
s_center.send(b''.join(tmp_center_128))
s_csp.send(b''.join(tmp_csp_128))


s_csp.close()
s_center.close()
