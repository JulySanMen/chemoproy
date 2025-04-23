from flask import Flask, render_template, request, redirect, url_for
import socket
import os

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
            data = s.recv(BUFFER_SIZE)
            return data.decode(errors="ignore")
    except Exception as e:
        return f"Error: {str(e)}"

@app.route("/")
def index():
    return render_template("indexpro.html")

@app.route("/connect", methods=["POST"])
def connect():
    ip = request.form.get("ip")
    response = send_command(ip, "PING")
    return render_template("indexpro.html", ip=ip, response=response)

@app.route("/start", methods=["POST"])
def start():
    ip = request.form.get("ip")
    response = send_command(ip, "START")
    return render_template("indexpro.html", ip=ip, response=response)

@app.route("/view_logs", methods=["POST"])
def view_logs():
    ip = request.form.get("ip")
    response = send_command(ip, "GET_LOG")
    return render_template("indexpro.html", ip=ip, log=response)

@app.route("/delete", methods=["POST"])
def delete():
    ip = request.form.get("ip")
    response = send_command(ip, "DELETE_ALL")
    return render_template("indexpro.html", ip=ip, response=response)

if __name__ == "__main__":
    app.run(debug=True)
