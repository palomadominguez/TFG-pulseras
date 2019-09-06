# mongo.py

from flask import Flask,flash, redirect, render_template, request, session, abort, send_file
from flask import jsonify
from flask import request
from flask_pymongo import PyMongo
import shutil, os
from werkzeug import secure_filename
import time
import requests
import collections


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

# String uploadFile(File file, String idPatient, String idDoctor):
# guarda el fichero en el servidor HDFS (en el sistema de ficheros de tu máquina),
# añadiendo una entrada en la base de datos con la ruta del fichero.

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
        pacientes.update({"_id": int(idPaciente)}, {
            "$push": {"Informes": {"_idInforme": time.time(), "RutaArchivo": path, "identificadorAnalisis": ""}}});
        # Retornamos una respuesta satisfactoria
    return render_template('uploadFile.html')


# File downloadFile(String idFile, String idPatient, String idDoctor):
# consulta la base de datos para descargar el fichero almacenado en el
# servidor HDFS (o tu máquina), dado su identificador de fichero.

@app.route('/download')
def file_downloads():
    return render_template('download.html')

@app.route('/return-files')
def return_files_tut():
    try:
        print("Aqui llego")
        f = request.files['archivo']
        print(f)
        filename = secure_filename(f.filename)
        path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        return send_file(path, attachment_filename=filename)
    except Exception as e:
        return str(e)


# String analysis(String IdFile, String idPatient, Strign idDoctor):
# este será uno de los métodos principales de la API.
# Realiza el análisis del fichero (dado su identificador) y
# devuelve un ticket (una cadena de texto).
@app.route('/classify')
def classify(idPaciente, idInforme):

    informe = get_informe(idPaciente, idInforme);
    ruta = informe['RutaArchivo'];

    r = requests.post(url = "http://192.168.48.222:6565/v2/run", json = [
          {
             "name":"classify",
             "path":ruta
          },
        ] )

    return jsonify(r.json())

@app.route('/returnclassify/<identificadorClasificacion>', methods=['GET'])
def return_classify(identificadorClasificacion):
    # consulta en BD como va la clasificacion
    # devuelve el resultado
    r = requests.get(url=f"http://192.168.48.222:6565/v2/status?ticket_id={identificadorClasificacion}")
    return jsonify(r.json())


@app.route('/graficar', methods=['GET'])
def graficar():
    a = [8, 0, 4, 8, 8, 4, 0, 8, 8, 8, 6, 6, 7, 7, 0, 8, 7, 7, 7, 8, 8, 8, 8, 8, 8, 1, 1, 1, 0, 1, 0, 0, 1,
         0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 6, 6, 10]
    counter = collections.Counter(a)
    # Counter({1: 4, 2: 4, 3: 2, 5: 2, 4: 1})
    counterValues = counter.values()
    return render_template('grafico.html', counterValues=counterValues)

if __name__ == '__main__':
    app.secret_key = os.urandom(12)

    app.run(debug=True)
