import socket
import threading
import json

def recv_sockdata(the_socket):
    total_data = ""
    while True:
        data = the_socket.recv(1024).decode()
        if "END" in data:
            total_data += data[:data.index("END")]
            break
        total_data += data
    return total_data

def deal_data(data):
    # 对数据进行处理
    print(data)

def do_server(sock,addr):
    # 处理客户端连接
    print("收到来自客户端{}的连接：".format(addr))
    # 发送数据：
    sock.sendall((json.dumps({"msg":"welcome connect to server"})+" END").encode())
    # 在一个死循环中接收数据并处理
    while True:
        try:
            recv_data = recv_sockdata(sock)
            deal_data(recv_data) # 处理数据
        except (ConnectionResetError,ConnectionAbortedError):
            break

if __name__ == '__main__':
    HOST = ''
    PORT = 10001
    #创建Socket
    tcpSocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    #绑定地址
    tcpSocket.bind((HOST,PORT))
    #监听端口，传入的参数指定等待连接的最大数量
    tcpSocket.listen(16)
    threads = [] # 线程数组，每一个线程维护一个客户端连接
    #服务器程序通过一个永久循环来接受来自客户端的连接
    while True:
        print('Waiting for connection...')
        # 接受一个新连接:
        sock,addr = tcpSocket.accept()
        # 创建新线程来处理TCP连接:每个连接都必须创建新线程（或进程）来处理，
        #否则，单线程在处理连接的过程中，无法接受其他客户端的连接：
        th = threading.Thread(target=do_server,args=(sock,addr))
        th.start()
        threads.append(th)
