import socket
import time
import threading
import json
import random


# 处理网络收到数据
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
    # 这里对数据进行处理
    print(data)

def recv_data(sock):
    # 接收数据
    while True:
        try:
            data = recv_sockdata(sock)
            deal_data(data) # 处理数据
        except (ConnectionResetError,ConnectionAbortedError):
            break

# 程序入口
if __name__ == '__main__':
    # 创建socket
    tcp_client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    # 目标IP 端口号
    server_addr = ('127.0.0.1',10001)
    # 连接
    try:
        tcp_client.connect(server_addr)
    except (ConnectionRefusedError,OSError):
        print("网络连接失败，请重试")

    # 启动一个线程，线程里死循环处理收到的数据
    # (target指定处理函数，args是传递给函数的参数)
    threading.Thread(target=recv_data,args=(tcp_client,)).start()

    # 发送数据的代码：
    tcp_client.sendall((json.dumps({"first_dir":"UP"})+" END").encode())

    while True:
        time.sleep(200)# 主程序不退出
