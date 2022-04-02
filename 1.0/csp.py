import socket
import threading
import time


cnt = 2000000
data_secret_share = 0
lock = threading.Lock()


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_TCP, socket.TCP_NODELAY, 1)
s.setsockopt(
    socket.SOL_SOCKET,
    socket.SO_SNDBUF,
    16 * cnt + 10)
s.setsockopt(
    socket.SOL_SOCKET,
    socket.SO_RCVBUF,
    16 * cnt + 10)
s.bind(('127.0.0.1', 8002))
s.listen(10)


def receive_128(sock, addr):
    print('Accept new connection from %s:%s...' % addr)
    data = sock.recv(16 * cnt)
    lock.acquire()
    global data_secret_share
    try:
        data_secret_share = data_secret_share ^ int.from_bytes(data,'big')
    finally:
        lock.release()
    sock.close()


# 传输 128 位随机比特
sock1,addr1 = s.accept()
t1 = threading.Thread(target=receive_128, args=(sock1, addr1))

sock2,addr2 = s.accept()
t2 = threading.Thread(target=receive_128, args=(sock2, addr2))

sock3,addr3 = s.accept()
t3 = threading.Thread(target=receive_128, args=(sock3, addr3))

t1.start()
t2.start()
t3.start()

t1.join()
t2.join()
t3.join()

# 计算结果
sock4, addr4 = s.accept()
data = sock4.recv(16 * cnt)
data_secret_share = data_secret_share ^ int.from_bytes(data,'big')
print(bin(data_secret_share)[2:].count("0" * 128))


print(time.time())
