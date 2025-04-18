import socket

HOST = '0.0.0.0'
PORT = 12345

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen(1)
    conn, addr = s.accept()
    with conn:
        print('Conectado por', addr)
        with open('imagen_recibida.jpg', 'wb') as f:
            while True:
                data = conn.recv(4096)
                if not data:
                    break
                f.write(data)