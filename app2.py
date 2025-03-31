from flask import Flask, render_template
from flask_socketio import SocketIO
from scapy.all import sniff

app = Flask(__name__)
socketio = SocketIO(app)

@app.route('/')
def index():
    return render_template('index.html')

def capturar_paquetes(paquete):
    # Extraer información del paquete
    data = {
        "origen": paquete.src if hasattr(paquete, 'src') else "Desconocido",
        "destino": paquete.dst if hasattr(paquete, 'dst') else "Desconocido",
        "protocolo": paquete.proto if hasattr(paquete, 'proto') else "Desconocido"
    }
    socketio.emit('nuevo_paquete', data)  # Enviar paquete al frontend en tiempo real

@socketio.on('iniciar_sniffer')
def iniciar_sniffer():
    sniff(prn=capturar_paquetes, store=False)  # Capturar paquetes en tiempo real

if __name__ == '__main__':
    socketio.run(app, debug=True)
