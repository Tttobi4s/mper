import socket
import random
import numpy as np

cnt, batch = 2000000, 1000
data_p3 = np.random.randint(0, 2, cnt)

s_csp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s_center = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s_csp.connect(('127.0.0.1', 8002))
s_center.connect(('127.0.0.1', 8001))

for i in range(batch):
    tmp_center, tmp_csp = b'', b''
    batch_cnt = cnt // batch
    for j in range(batch_cnt * i, batch_cnt * i + batch_cnt):
        if data_p3[j] == 1:
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
