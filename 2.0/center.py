import socket
import threading
from typing import final


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('127.0.0.1', 8000))
s.listen(10)


cnt, batch, dataspace_filter = 2000000, 1000, 0
data_secret_share = [0] * cnt
lock = threading.Lock()


def receive_1(sock, addr):
    print('Step1 :  Accept new connection from %s:%s...' % addr)
    global dataspace_filter
    lock.acquire()
    try:
        dataspace_filter = dataspace_filter ^ int.from_bytes(sock.recv(cnt // 8), 'big')
    finally:
        lock.release()


def receive_128(sock, addr):
    print('Step2 : Accept new connection from %s:%s...' % addr)
    batch_cnt = cnt // batch
    for i in range(batch):
        data = sock.recv(16 * batch_cnt)
        if not data:
            break
        for j in range(batch_cnt):
            data_secret_share[i * batch_cnt + j] = data_secret_share[i *
                                                                     batch_cnt + j] ^ int.from_bytes(data[16 * j: 16 * j + 16], 'big')
    sock.close()


# 传输单比特过滤
sock1, addr1 = s.accept()
t1 = threading.Thread(target=receive_1, args=(sock1, addr1))

sock2, addr2 = s.accept()
t2 = threading.Thread(target=receive_1, args=(sock2, addr2))

sock3, addr3 = s.accept()
t3 = threading.Thread(target=receive_1, args=(sock3, addr3))

t1.start()
t2.start()
t3.start()

t1.join()
t2.join()
t3.join()

s_csp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s_csp.connect(('127.0.0.1', 8002))
s_csp.send(dataspace_filter.to_bytes(cnt // 8, 'big'))

# 传输 128 位随机比特
t4 = threading.Thread(target=receive_128, args=(sock1, addr1))

t5 = threading.Thread(target=receive_128, args=(sock2, addr2))

t6 = threading.Thread(target=receive_128, args=(sock3, addr3))

t4.start()
t5.start()
t6.start()

t4.join()
t5.join()
t6.join()


# 发送秘密份额给csp
for i in range(batch):
    batch_cnt = cnt // batch
    tmp = b''
    for j in range(batch_cnt * i, batch_cnt * i + batch_cnt):
        tmp = tmp + data_secret_share[j].to_bytes(16, 'big')
    s_csp.send(tmp)

s_csp.close()
