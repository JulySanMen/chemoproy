import socket

server_ip = "192.168.1.96"  # Cambia esto por la IP real de B

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((server_ip, 9999))

with open("perr.jpg", "rb") as f:
    client_socket.sendfile(f)

client_socket.close()
print("Imagen enviada.")