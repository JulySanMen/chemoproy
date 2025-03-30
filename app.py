from flask import Flask, render_template, request
import string
import secrets  

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('gencontra.html')

@app.route('/generar', methods=['POST'])
def generar_contraseña():
    try:
        longitud = int(request.form['longitud'])
        if longitud < 4:
            return render_template('gencontra.html', error="La longitud debe ser de al menos 4 caracteres.")

        # Definir los caracteres permitidos
        caracteres = string.ascii_letters + string.digits + string.punctuation

        # Crear la contraseña asegurando al menos un carácter de cada tipo
        contraseña = [
            secrets.choice(string.ascii_lowercase),
            secrets.choice(string.ascii_uppercase),
            secrets.choice(string.digits),
            secrets.choice(string.punctuation)
        ]

        # Completar el resto de la contraseña con caracteres aleatorios
        contraseña += [secrets.choice(caracteres) for _ in range(longitud - 4)]

        # Mezclar los caracteres de la contraseña de manera segura
        secrets.SystemRandom().shuffle(contraseña)

        # Convertir la lista en una cadena
        contraseña = "".join(contraseña)

        return render_template('gencontra.html', contraseña=contraseña)
    
    except ValueError:
        return render_template('gencontra.html', error="Ingrese un número válido.")

if __name__ == '__main__':
    app.run(debug=True)
