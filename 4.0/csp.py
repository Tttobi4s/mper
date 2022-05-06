import socket
import threading
import time


data_secret_share = [0] * 8
lock = threading.Lock()


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_TCP, socket.TCP_NODELAY, 1)
s.setsockopt(
    socket.SOL_SOCKET,
    socket.SO_SNDBUF,
    16 * 65536 + 10)
s.setsockopt(
    socket.SOL_SOCKET,
    socket.SO_RCVBUF,
    16 * 65536 + 10)
s.bind(('127.0.0.1', 8002))
s.listen(10)


def receive_128(sock, addr, i):
    print(str(i) + ':Accept new connection from %s: %s...' % addr)
    data = sock.recv(16 * 65536)
    lock.acquire()
    global data_secret_share
    try:
        data_secret_share[i] = data_secret_share[i] ^ int.from_bytes(
            data, 'big')
    finally:
        lock.release()


# 传输 128 位随机比特
sock1, addr1 = s.accept()
sock2, addr2 = s.accept()
sock3, addr3 = s.accept()

for i in range(8):
    t1 = threading.Thread(target=receive_128, args=(sock1, addr1, i))
    t2 = threading.Thread(target=receive_128, args=(sock2, addr2, i))
    t3 = threading.Thread(target=receive_128, args=(sock3, addr3, i))

    t1.start()
    t2.start()
    t3.start()

    t1.join()
    t2.join()
    t3.join()

# 计算结果
sock4, addr4 = s.accept()
res = []
for i in range(8):
    data = sock4.recv(16 * 65536)
    data_secret_share[i] = data_secret_share[i] ^ int.from_bytes(data, 'big')
    sock1.send(data_secret_share[i].to_bytes(16 * 65536, 'big'))
