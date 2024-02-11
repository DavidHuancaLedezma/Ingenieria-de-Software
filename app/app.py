from flask import Flask, render_template, url_for, request, redirect, flash
from flask_sqlalchemy import SQLAlchemy
import base64
from datetime import datetime
import time

app = Flask(__name__)

elector_interactuando = []
corte_interactuando = []

app.config['SQLALCHEMY_DATABASE_URI'] = \
    '{SGBD}://{usuario}:{clave}@{servidor}/{database}'.format(
        SGBD = 'mysql+mysqlconnector',
        usuario = 'pythonES',
        clave = 'Unodostres123',
        servidor = 'pythonES.mysql.pythonanywhere-services.com',
        database = 'pythonES$verano2023'
    )
db = SQLAlchemy(app)

class Elector(db.Model):
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    ci = db.Column(db.Integer)
    nombre = db.Column(db.String(60))
    foto = db.Column(db.LargeBinary)
    fechaN = db.Column(db.Date)
    genero = db.Column(db.String(50))
    estado = db.Column(db.String(50))

class Corte_electoral(db.Model):
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    ci = db.Column(db.Integer)
    nombre = db.Column(db.String(60))
    fechaN = db.Column(db.Date)
    genero = db.Column(db.String(50))

class Voto(db.Model):
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    candidato_elegido = db.Column(db.String(60))
    cantidad_votos = db.Column(db.Integer)




@app.route('/')
def index():
    db.create_all()
    return render_template('inico_elector.html')


@app.route('/iniciar_sesion', methods=['POST'])
def iniciar_sesion():
    ci = request.form['ci']
    contra = request.form['contra']
    try:
        fechaN = datetime.strptime(contra, '%Y-%m-%d')
        elector = Elector.query.filter_by(ci=ci).filter_by(fechaN=fechaN).first()
        if elector is not None:
            foto = base64.b64encode(elector.foto).decode('utf-8')
            elector_interactuando.append(elector)
            return render_template('Datos_personales.html',elector=elector,foto=foto)
        else:
            return render_template('mensaje_error_elector.html') # reemplazar con mensaje contra incorrecta
    except ValueError:
        return render_template('mensaje_error_elector.html')  # reemplazar con mensaje contra incorrecta


@app.route('/regresar_al_inicio', methods=['POST'])
def regresar_al_inicio():
    elector_interactuando.pop(0)
    return render_template('inico_elector.html')


@app.route("/emitir_voto", methods=['POST'])
def emitir_voto():
    elector = elector_interactuando[0]
    if elector.estado == 'Habilitado':
        return render_template('emitir_voto.html')
    elif elector.estado == 'Inactivo':
        return render_template('mensaje_inactivo.html')

@app.route("/voto_ya_realizado", methods=['POST'])
def voto_ya_realizado():
    time.sleep(8)
    elector_interactuando.pop(0)
    return render_template('inico_elector.html')

@app.route('/procesar_voto', methods=['POST'])
def procesar_voto():
    selected_candidate = request.form.get('voto')
    #return f'Este es el  error.-{selected_candidate}'
    if selected_candidate:
        candidato = Voto.query.filter_by(candidato_elegido=selected_candidate).first()
        candidato.cantidad_votos = candidato.cantidad_votos + 1
        db.session.commit()
        elector_actual = elector_interactuando.pop(0)
        elector = Elector.query.filter_by(ci=elector_actual.ci).first()
        elector.estado = 'Inactivo'
        db.session.commit()
        return render_template('inico_elector.html')



@app.route('/login_corte_electoral')
def login_corte_electoral():
    return render_template('login_corte_electoral.html')

@app.route('/login_elector')
def login_elector():
    return render_template('inico_elector.html')

@app.route('/ingresar_a_resultados', methods=['POST'])
def ingresar_a_resultados():
    #validar cuenta Corte Electoral
    ci = request.form['ci']
    contra = request.form['contra']
    try:
        fechaN = datetime.strptime(contra, '%Y-%m-%d')
        corte = Corte_electoral.query.filter_by(ci=ci).filter_by(fechaN=fechaN).first()
        if corte is not None:

            corte_interactuando.append(corte)
            porcentaje_votos = {}
            votos_conseguidos = {}

            votos = Voto.query.all()
            total = 0
            for i in votos:
                total = total + i.cantidad_votos

            for i in votos:
                porcentaje = (i.cantidad_votos/total) * 100
                numero_redondeado = round(porcentaje, 2)
                votos_conseguidos[i.candidato_elegido] = i.cantidad_votos
                porcentaje_votos[i.candidato_elegido] = numero_redondeado

            return render_template('resultados.html',corte=corte,votos_conseguidos=votos_conseguidos,porcentaje_votos=porcentaje_votos,total=total)
        else:
            return render_template('mensaje_error_corte.html') # reemplazar con mensaje contra incorrecta
    except ValueError:
        return render_template('mensaje_error_corte.html')  # reemplazar con mensaje contra incorrecta

@app.route('/salir_de_resultados', methods=['POST'])
def salir_de_resultados():
    corte_interactuando.pop(0)
    return render_template('inico_elector.html')


@app.route('/contraseña_incorrecta_elector', methods=['POST'])
def contraseña_incorrecta_elector():
    time.sleep(5)
    return render_template('inico_elector.html')


@app.route('/contraseña_incorrecta_corte', methods=['POST'])
def contraseña_incorrecta_corte():
    time.sleep(5)
    return render_template('login_corte_electoral.html')

