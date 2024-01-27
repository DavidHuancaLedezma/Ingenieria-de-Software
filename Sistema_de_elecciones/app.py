from flask import Flask, render_template, url_for, request, redirect
from elector import Elector

electores = [
    Elector(72324,'Jose Jose Quispe Colque','2002/23/12','Hombre',True),
    Elector(23451,'Abigail Nayra Pacheco Basoalto','2000/28/12','Mujer',True),
    Elector(23124,'Ariana Wara Luz','1999/04/20','Mujer',True)
]

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('inico_elector.html')

@app.route('/iniciar_sesion', methods=['POST'])
def iniciar_sesion():

    ci = int(request.form['ci'])
    contra = request.form['contra']
    existe = False

    for datos in electores:
        if datos.get_ci() == ci and datos.get_fecha_nacimiento() == contra:
            existe = True
            return render_template('Datos_personales.html',elector=datos)

    if existe == False:
        return f'Ci: {ci} y contra {contra} incorrectos'


@app.route("/Volver a la pantalla de inicio", methods=['POST'])
def regresar_al_inicio():
    return render_template('inico_elector.html')

if __name__ == '__main__':
    app.run(debug=True, port=5000)