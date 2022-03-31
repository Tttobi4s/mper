import socket
import threading

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('127.0.0.1', 8000))
s.listen(10)

cnt, batch = 2000000, 1000
data_secret_share = [0] * cnt

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


# 发送秘密份额给csp
s_csp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s_csp.connect(('127.0.0.1', 8002))
for i in range(batch):
    batch_cnt = cnt // batch
    tmp = b''
    for j in range(batch_cnt * i, batch_cnt * i + batch_cnt):
        tmp = tmp + data_secret_share[j].to_bytes(16, 'big')
    s_csp.send(tmp)

s_csp.close()
