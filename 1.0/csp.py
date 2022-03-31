import socket
import threading
import time

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('127.0.0.1', 8002))
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

start = time.time()

t1.start()
t2.start()
t3.start()

t1.join()
t2.join()
t3.join()

# 计算结果
sock4, addr4 = s.accept()
res = 0
batch_cnt = cnt // batch
for i in range(batch):
    data = sock4.recv(16 * batch_cnt)
    for j in range(batch_cnt):
        data_secret_share[i * batch_cnt + j] = data_secret_share[i *
                                                                 batch_cnt + j] ^ int.from_bytes(data[16 * j: 16 * j + 16], 'big')
        if data_secret_share[i * batch_cnt + j] == 0:
            res += 1

print(res)
end = time.time()
print(end - start)
