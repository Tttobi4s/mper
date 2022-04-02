import socket
import random
import numpy as np
import time


cnt = 2000000
data_p3 = np.random.randint(0, 2, cnt)


s_csp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s_center = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s_csp.connect(('127.0.0.1', 8002))
s_center.connect(('127.0.0.1', 8001))
s_csp.setsockopt(
    socket.SOL_SOCKET,
    socket.SO_SNDBUF,
    16 * cnt + 10)
s_csp.setsockopt(
    socket.SOL_SOCKET,
    socket.SO_RCVBUF,
    16 * cnt + 10)
s_center.setsockopt(
    socket.SOL_SOCKET,
    socket.SO_SNDBUF,
    16 * cnt + 10)
s_center.setsockopt(
    socket.SOL_SOCKET,
    socket.SO_RCVBUF,
    16 * cnt + 10)

print(time.time())
tmp_center, tmp_csp = [], []
for i in range(cnt):
    if data_p3[i] == 1:
        r = random.getrandbits(128)
        tmp_csp.append(r.to_bytes(16, 'big'))
        tmp_center.append(r.to_bytes(16, 'big'))
    else:
        tmp_csp.append(random.getrandbits(128).to_bytes(16, 'big'))
        tmp_center.append(random.getrandbits(128).to_bytes(16, 'big'))
print(time.time())
s_csp.send(b''.join(tmp_csp))
s_center.send(b''.join(tmp_center))


s_csp.close()
s_center.close()
