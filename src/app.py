# mongo.py

from flask import Flask, flash, redirect, render_template, request, session, abort, send_file, url_for
from flask import jsonify
from flask import request
from flask_pymongo import PyMongo
import shutil, os
from werkzeug import secure_filename
import time
import requests
import collections
import pandas as pd
import numpy as np

from gevent.pywsgi import WSGIServer

from src.dao.database import Database

app = Flask(__name__)

app.config['MONGO_DBNAME'] = 'pulserasdb'
app.config['MONGO_URI'] = 'mongodb://localhost:27017/pulserasdb'
app.config['UPLOAD_FOLDER'] = os.path.abspath("Archivos")

mongo = PyMongo(app)

db = Database("localhost", 27017)


##########################################################
#                   HTML
##########################################################

@app.route('/medicos', methods=['GET'])
def show_medicos():
    medicos = db.get_medicos()
    print(medicos)
    return render_template('upload.html', medicos=medicos)

@app.route('/download/<idPaciente>/<idInforme>', methods=['GET'])
def show_download(idPaciente, idInforme):
    informe = db.get_informe(idPaciente, idInforme)
    return render_template('upload.html', informe=informe)

# Home
@app.route('/home')
def render_home():
    return render_template('home.html')

# Login
@app.route('/login')
def render_login():
    return render_template('login.html')

@app.route('/pacientes', methods=['GET'])
def show_pacientes():
    pacientes = db.get_pacientes()
    return render_template('listaPacientes.html', pacientes=pacientes)

## Informes
@app.route('/informes/<idPaciente>', methods=['GET'])
def show_informes(idPaciente):
    informes = db.get_informes(idPaciente)
    return render_template('listaInforme.html', informes=informes)


@app.route('/upload', methods=['GET'])
def show_upload():
    pacientes = db.get_pacientes()
    return render_template('uploadFile.html', pacientes=pacientes)

@app.route('/analisis', methods=['GET'])
def show_analisis():
    pacientes = db.get_pacientes()

    return render_template('analisis.html', pacientes=pacientes)

@app.route('/graficos', methods=['GET'])
def show_grafico():
    parametros = graficar()
    pacientes = db.get_pacientes()

    return render_template('grafico.html', pacientes=pacientes,parametros=parametros)

@app.route('/resultados', methods=['GET'])
def show_resultados():
    parametros = graficar()
    return render_template('resultado.html', parametros=parametros)

##########################################################
#                   API
##########################################################

#GET usuarios
@app.route('/api/usuarios')
def get_usuarios():
    usuarios = db.get_usuarios()
    return jsonify(usuarios)

# Get todos los medicos
@app.route('/api/medicos', methods=['GET'])
def get_medicos():
    medicos = db.get_medicos()
    return jsonify(medicos)


# Get un medico
@app.route('/api/medico/<idMedico>', methods=['GET'])
def get_medico(idMedico):
    medico = db.get_medico(idMedico)
    return jsonify(medico)


# Get pacientes
@app.route('/api/pacientes', methods=['GET'])
def get_pacientes():
    pacientes = db.get_pacientes()
    return jsonify(pacientes)


# Get un paciente
@app.route('/api/paciente/<idMedico>/<idPaciente>', methods=['GET'])
def get_paciente(idMedico, idPaciente):
    paciente = db.get_paciente(idMedico, idPaciente)
    return jsonify(paciente)


@app.route('/api/informes/<idPaciente>', methods=['GET'])
def get_informes(idPaciente):
    informes = db.get_informes(idPaciente)
    return jsonify(informes)


# Get un informe
@app.route('/api/informe/<idPaciente>/<idInforme>', methods=['GET'])
def get_informe(idPaciente, idInforme):
    informe = db.get_informe(idPaciente, idInforme)
    return jsonify(informe)

# Get una ruta
@app.route('/api/ruta/<idPaciente>/<idInforme>', methods=['GET'])
def get_ruta(idPaciente, idInforme):
    ruta = db.get_ruta_informe(idPaciente, idInforme)
    return jsonify(ruta)


# POST un informe
@app.route('/api/informe/<idPaciente>/', methods=['POST'])
def post_informe(idPaciente):
    informe = db.get_informe(idPaciente)
    return jsonify(informe)

@app.route('/login', methods=['POST'])
def do_admin_login():
    if request.form['password'] == 'P123456' and request.form['username'] == 'M-123456':
        session['logged_in'] = True
    else:
        flash('wrong password!')
    return render_home()

@app.route("/api/upload")
def upload_file():
    # renderiamos la plantilla "upload.html"

    return render_template('uploadFile.html')


@app.route("/uploader", methods=['POST'])
def uploader():
    if request.method == 'POST':
        # Obtenemos el input paciente
        idPaciente = request.form['idPaciente']
        print(idPaciente)
        # obtenemos el archivo del input "archivo"
        f = request.files['archivo']
        filename = secure_filename(f.filename)
        # Guardamos el archivo en el directorio "Archivos PDF"
        path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        # Agregamos informe a la lista de informes del paciente en la base de datos.
        pacientes = mongo.db.PacientesInformes;
        pacientes.update({"_id": int(idPaciente), }, {
            "$push": {"Informes": {"_idInforme": int(time.time()), "RutaArchivo": path, "identificadorAnalisis": ""}}});
        # Retornamos una respuesta satisfactoria
    return render_template('uploadFile.html')

@app.route('/download')
def file_downloads():
    return render_template('download.html')

@app.route('/return-files')
def return_files_tut():
    try:
        ruta = request.args.get('nombre')
        path = os.path.join(app.config['UPLOAD_FOLDER'], ruta)
        return send_file(path)
    except Exception as e:
        return str(e)

@app.route('/classify', methods=['POST'])
def classify():
    if request.method == 'POST':
        idPaciente = request.form['idPaciente']
        idInforme = request.form['idInforme']

        ruta = db.get_ruta_informe(idPaciente, idInforme)

        r = requests.post(url = "http://192.168.48.222:6565/v2/run", json = [
              {
                 "task":"classify",
                 "name": "Description",
                 "data": ruta
              }
            ])
        print(r.json())
        ticket_id = r.json()['ticket_id']
        pacientes = mongo.db.PacientesInformes
        pacientes.update({"_id": int(idPaciente)}, {
            "$push": {"Informes": {"_idInforme": time.time(), "identificadorAnalisis": ticket_id}}});
        # Retornamos una respuesta satisfactoria

    return redirect(url_for('.graficar', ticket_id = ticket_id))

@app.route('/graficar', methods=['GET'])
def graficar():
    ticket_id = request.args.get('ticket_id')
    print(ticket_id)

    r = requests.get(url=f"http://192.168.48.222:6565/v2/status?ticket_id={ticket_id}")
    if(r.status_code == 200):
        r = r.json()
        if(r['state'] == "SUCCESS"):
            counter = collections.Counter(r['process_chain_list'][0]['return'])
            # Counter({1: 4, 2: 4, 3: 2, 5: 2, 4: 1})
            print(counter)
            counterValues = counter.values()
            counterValues = list(counterValues)
            counterValues = ",".join(map(str, counterValues))
        else:
            counterValues = -1
        return render_template('grafico.html', counterValues=counterValues)
    else:
        return redirect(url_for('.render_home'))

if __name__ == '__main__':
    app.secret_key = os.urandom(12)

    app.run(debug=True)
