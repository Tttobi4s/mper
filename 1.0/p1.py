import socket
import random
import numpy as np


cnt = 2000000 # 数据个数
data_p1 = np.random.randint(0, 2, cnt) # 数据集


# 创建socket：IPv4协议 TCP协议
s_csp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s_center = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# 建立TCP连接：IP地址 端口号
s_csp.connect(('127.0.0.1', 8002))
s_center.connect(('127.0.0.1', 8001))
# 设置缓冲区大小（字节）
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

# 用列表存储所有的随机数
tmp_center, tmp_csp = [], [] 
for i in range(cnt): 
    # 如果有该元素 发送两个相同的随机数
    if data_p1[i] == 1:
        r = random.getrandbits(128)
        tmp_csp.append(r.to_bytes(16, 'big'))
        tmp_center.append(r.to_bytes(16, 'big'))
    # 如果没有该元素 发送两个不同的随机数
    else:
        tmp_csp.append(random.getrandbits(128).to_bytes(16, 'big'))
        tmp_center.append(random.getrandbits(128).to_bytes(16, 'big'))
# 一次性发送
s_csp.send(b''.join(tmp_csp))
s_center.send(b''.join(tmp_center))


# 断开连接
s_csp.close()
s_center.close()
