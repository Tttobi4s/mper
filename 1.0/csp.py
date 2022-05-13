import socket
import threading


cnt = 2000000  # 数据个数
data_secret_share = 0
lock = threading.Lock() # 锁


# 创建socket：IPv4协议 TCP协议
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# 设置缓冲区大小（字节）
s.setsockopt(socket.SOL_TCP, socket.TCP_NODELAY, 1)
s.setsockopt(
    socket.SOL_SOCKET,
    socket.SO_SNDBUF,
    16 * cnt + 10)
s.setsockopt(
    socket.SOL_SOCKET,
    socket.SO_RCVBUF,
    16 * cnt + 10)
# 绑定监听的地址和端口号
s.bind(('127.0.0.1', 8002))
# 监听端口 等待连接最大数量为 10
s.listen(10)


def receive_128(sock, addr):
    print('Accept new connection from %s:%s...' % addr)
    # 接收所有的随机数
    data = sock.recv(16 * cnt)
    lock.acquire()
    global data_secret_share
    try:
        data_secret_share = data_secret_share ^ int.from_bytes(data,'big')
    finally:
        lock.release()
    sock.close()


sock1, addr1 = s.accept()  # 接收一个来自客户端的连接
t1 = threading.Thread(target=receive_128, args=(sock1, addr1))  # 创建线程处理TCP连接
sock2, addr2 = s.accept()
t2 = threading.Thread(target=receive_128, args=(sock2, addr2))
sock3, addr3 = s.accept()  
t3 = threading.Thread(target=receive_128, args=(sock3, addr3))

t1.start()
t2.start()
t3.start()

t1.join()
t2.join()
t3.join()


# 计算结果
sock_center, addr_center = s.accept()
data = sock_center.recv(16 * cnt)
data_secret_share = data_secret_share ^ int.from_bytes(data, 'big')
str_res = bin(data_secret_share)[2:]
str_res = (128 * cnt - len(str_res)) * "0" + str_res
print(str_res.count("0" * 128))