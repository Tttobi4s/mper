import socket
import threading
import time

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('127.0.0.1', 8002))
s.listen(10)

cnt, batch = 2000000, 1000
data_secret_share = [0] * cnt
dataspace = 0


def receive_1(sock, addr):
    print('Step1 :  Accept new connection from %s:%s...' % addr)
    global dataspace
    dataspace = dataspace ^ int.from_bytes(sock.recv(cnt // 8), 'big')


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

start = time.time()
t1.start()
t2.start()
t3.start()

t1.join()
t2.join()
t3.join()

sock4, addr4 = s.accept()
dataspace = int.from_bytes(sock4.recv(cnt // 8), 'big') ^ dataspace
sock1.send(dataspace.to_bytes(cnt // 8,'big'))
sock2.send(dataspace.to_bytes(cnt // 8,'big'))
sock3.send(dataspace.to_bytes(cnt // 8,'big'))
dataspace = bin(dataspace)[2:]
if len(dataspace) < cnt:
    dataspace = "0" * (cnt - len(dataspace)) + dataspace

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
batch_cnt = cnt // batch
res = 0
real_cnt = dataspace.count("0")
print(real_cnt)
for i in range(batch):
    data = sock4.recv(16 * batch_cnt)
    for j in range(batch_cnt):
        data_secret_share[i * batch_cnt + j] = data_secret_share[i *
                                                                 batch_cnt + j] ^ int.from_bytes(data[16 * j: 16 * j + 16], 'big')
        if data_secret_share[i * batch_cnt + j] == 0 and (i * batch_cnt + j) < real_cnt:
            res += 1

print(res)
end = time.time()
print(end - start)
