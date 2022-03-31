import socket
import random
import numpy as np

cnt, batch = 2000000, 1000
data_p3 = np.random.randint(0, 2, cnt)

s_csp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s_center = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s_csp.connect(('127.0.0.1', 8002))
s_center.connect(('127.0.0.1', 8000))

# 传输单比特过滤
tmp_center, tmp_csp = [], []
for i in range(cnt):
    if data_p3[i] == 1:
        tmp_center.extend("0")
        tmp_csp.extend("0")
    else:
        tmp_center.extend(str(random.getrandbits(1)))
        tmp_csp.extend(str(random.getrandbits(1)))
s_center.send(int("".join(tmp_center), base=2).to_bytes(cnt // 8, 'big'))
s_csp.send(int("".join(tmp_csp), base=2).to_bytes(cnt // 8, 'big'))

dataspace = bin(int.from_bytes(s_csp.recv(cnt // 8), 'big'))[2:]
while len(dataspace) < cnt:
    dataspace = "0" + dataspace

# 传输 128 位随机比特
batch_cnt = cnt // batch
tmp_center, tmp_csp = b'', b''
for i in range(cnt):
    if dataspace[i] == '1':
        continue

    if len(tmp_center) == 16 * batch_cnt:
        s_center.send(tmp_center)
        s_csp.send(tmp_csp)
        tmp_center = b''
        tmp_csp = b''

    if data_p3[i] == 1:
        r = random.getrandbits(128)
        tmp_center = tmp_center + r.to_bytes(16, 'big')
        tmp_csp = tmp_csp + r.to_bytes(16, 'big')
    else:
        tmp_center = tmp_center + \
            random.getrandbits(128).to_bytes(16, 'big')
        tmp_csp = tmp_csp + random.getrandbits(128).to_bytes(16, 'big')

s_center.send(tmp_center)
s_csp.send(tmp_csp)

s_csp.close()
s_center.close()
