from flask import Flask, render_template, request
import string 
import random 
import secrets  

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('gencontra.html')

@app.route('/generar', methods=['POST'])
def generar_contraseña():
    longitud = request.form['longitud']
    longitud = int(longitud)

    # Definimos el conjunto de caracteres que se pueden usar en la contraseña
    caracteres = string.ascii_letters + string.digits + string.punctuation

    # Creamos una lista vacía para almacenar los caracteres de la contraseña
    contraseña = []

    # Añadimos al menos un carácter de cada tipo (minúscula, mayúscula, número y especial) a la contraseña
    contraseña.append(random.choice(string.ascii_lowercase))  # Añadimos una minúscula
    contraseña.append(random.choice(string.ascii_uppercase))  # Añadimos una mayúscula
    contraseña.append(random.choice(string.digits))  # Añadimos un número
    contraseña.append(random.choice(string.punctuation))  # Añadimos un carácter especial

    # Completamos la contraseña con caracteres aleatorios hasta alcanzar la longitud deseada
    while len(contraseña) < longitud:
        contraseña.append(secrets.choice(caracteres))  # Usamos secrets.choice para mayor seguridad

    # Mezclamos los caracteres de la contraseña para evitar patrones predecibles
    random.shuffle(contraseña)

    # Convertimos la lista de caracteres en una cadena
    contraseña = "".join(contraseña)

    # Renderizamos la contraseña en la plantilla HTML
    return render_template('gencontra.html', contraseña=contraseña)

if __name__ == '__main__':
    app.run(debug=True)