from flask import Flask, render_template, request
import string
import secrets  

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('gencontra.html')

@app.route('/generar', methods=['POST'])
def generar_contraseñas():
    try:
        longitud = int(request.form['longitud'])
        cantidad = int(request.form['cantidad'])

        if longitud < 8:
            return render_template('gencontra.html', error="La longitud debe ser de al menos 8 caracteres.")
        if cantidad < 1:
            return render_template('gencontra.html', error="Debes generar al menos 1 contraseña.")

        caracteres = string.ascii_letters + string.digits + string.punctuation
        contraseñas = []

        for _ in range(cantidad):
            contraseña = [
                secrets.choice(string.ascii_lowercase),
                secrets.choice(string.ascii_uppercase),
                secrets.choice(string.digits),
                secrets.choice(string.punctuation)
            ]
            contraseña += [secrets.choice(caracteres) for _ in range(longitud - 4)]
            secrets.SystemRandom().shuffle(contraseña)
            contraseñas.append("".join(contraseña))

        return render_template('gencontra.html', contraseñas=contraseñas)

    except ValueError:
        return render_template('gencontra.html', error="Ingrese valores numéricos válidos.")

if __name__ == '__main__':
    app.run(debug=True)
