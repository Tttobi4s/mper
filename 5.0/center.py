import socket
import threading


data_secret_share = [0] * 14
lock = threading.Lock()


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_TCP, socket.TCP_NODELAY, 1)
s.setsockopt(
    socket.SOL_SOCKET,
    socket.SO_SNDBUF,
    16 * 16777216 + 10)
s.setsockopt(
    socket.SOL_SOCKET,
    socket.SO_RCVBUF,
    16 * 16777216 + 10)
s.bind(('127.0.0.1', 8001))
s.listen(10)


def receive_128(sock, addr, i):
    print(str(i) + ':Accept new connection from %s: %s...' % addr)
    data = sock.recv(16 * 16777216)
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

for i in range(14):
    t1 = threading.Thread(target=receive_128, args=(sock1, addr1, i))
    t2 = threading.Thread(target=receive_128, args=(sock2, addr2, i))
    t3 = threading.Thread(target=receive_128, args=(sock3, addr3, i))

    t1.start()
    t2.start()
    t3.start()

    t1.join()
    t2.join()
    t3.join()


# 发送秘密份额给csp
s_csp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s_csp.connect(('127.0.0.1', 8002))
for i in range(14):
    s_csp.send(data_secret_share[i].to_bytes(16 * 16777216, 'big'))

s_csp.close()
