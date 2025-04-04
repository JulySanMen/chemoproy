import socket
import os

HOST = '0.0.0.0'
PORT = 4444

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    print(f"Esperando conexión en {HOST}:{PORT}...")

    while True:
        conn, addr = s.accept()
        with conn:
            print(f"Conexión de {addr}")
            data = conn.recv(4096)
            log_name = f"log_{addr[0].replace('.', '_')}.txt"
            with open(log_name, "a") as f:
                f.write(data.decode(errors="ignore"))
            print("Datos guardados en", log_name)
