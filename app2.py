import socket

# Crear un socket RAW para capturar paquetes
sniffer = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_IP)

# Escuchar en la interfaz de red (reemplazar con la adecuada)
sniffer.bind(("0.0.0.0", 0))

# Habilitar el modo promiscuo (solo en Windows, para Linux se usa `tcpdump`)
sniffer.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)

print("[*] Escuchando paquetes...")

while True:
    paquete, addr = sniffer.recvfrom(65535)  # Recibir paquetes
    print(f"Paquete recibido desde {addr}: {paquete[:20]}")  # Mostrar primeros bytes
