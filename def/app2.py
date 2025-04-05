from pynput.keyboard import Listener

def on_press(key):
    print(f'Tecla presionada: {key}')

with Listener(on_press=on_press) as listener:
    listener.join()
