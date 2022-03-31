import socket
import threading
import time


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('127.0.0.1', 8002))
s.listen(10)


cnt, batch_cnt, dataspace_filter = 2000000, 1000, 0
data_secret_share = [0] * cnt
lock = threading.Lock()


def receive_1(sock, addr):
    print('Step1 :  Accept new connection from %s:%s...' % addr)
    global dataspace_filter
    lock.acquire()
    try:
        dataspace_filter = dataspace_filter ^ int.from_bytes(
            sock.recv(cnt // 8), 'big')
    finally:
        lock.release()


def receive_128(sock, addr):
    print('Step2 : Accept new connection from %s:%s...' % addr)
    batch_index = 0
    while True:
        data = sock.recv(16 * batch_cnt)
        if not data:
            break
        real_batch_cnt = len(data) // 16
        for i in range(real_batch_cnt):
            data_secret_share[batch_index * batch_cnt + i] = data_secret_share[batch_index *
                                                                               batch_cnt + i] ^ int.from_bytes(data[16 * i: 16 * i + 16], 'big')
        batch_index += 1
    sock.close()


# 传输单比特过滤
sock1, addr1 = s.accept()
t1 = threading.Thread(target=receive_1, args=(sock1, addr1))

sock2, addr2 = s.accept()
t2 = threading.Thread(target=receive_1, args=(sock2, addr2))

sock3, addr3 = s.accept()
t3 = threading.Thread(target=receive_1, args=(sock3, addr3))

start = time.time()
t1.start()
t2.start()
t3.start()

t1.join()
t2.join()
t3.join()

sock4, addr4 = s.accept()
dataspace_filter = int.from_bytes(
    sock4.recv(cnt // 8), 'big') ^ dataspace_filter
sock1.send(dataspace_filter.to_bytes(cnt // 8, 'big'))
sock2.send(dataspace_filter.to_bytes(cnt // 8, 'big'))
sock3.send(dataspace_filter.to_bytes(cnt // 8, 'big'))
dataspace_filter = bin(dataspace_filter)[2:]
dataspace_filter = "0" * (cnt - len(dataspace_filter)) + dataspace_filter
new_cnt = dataspace_filter.count("0")
print(new_cnt)
sock4.send(("%d" % new_cnt).encode('utf-8'))


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

# 计算结果
batch_index, res = 0, 0
while True:
    data = sock4.recv(16 * batch_cnt)
    if not data:
        break
    real_batch_cnt = len(data) // 16
    for i in range(real_batch_cnt):
        data_secret_share[batch_index * batch_cnt + i] = data_secret_share[batch_index *
                                                                           batch_cnt + i] ^ int.from_bytes(data[16 * i: 16 * i + 16], 'big')
        if data_secret_share[batch_index * batch_cnt + i] == 0:
            res += 1
    batch_index += 1
print(res)


end = time.time()
print(end - start)
