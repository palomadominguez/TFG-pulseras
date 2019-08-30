# mongo.py

from flask import Flask, render_template, request, send_file
from flask import jsonify
from flask import request
from flask_pymongo import PyMongo
import shutil, os
from werkzeug import secure_filename
import time
from gevent.pywsgi import WSGIServer

from src.dao.database import Database

app = Flask(__name__)

app.config['MONGO_DBNAME'] = 'pulserasdb'
app.config['MONGO_URI'] = 'mongodb://localhost:27017/pulserasdb'
app.config['UPLOAD_FOLDER'] = './Archivos'

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

# Home
@app.route('/html/home')
def render_home():
    return render_template('home.html')

# Login
@app.route('/html/login')
def render_login():
    return render_template('login.html')

@app.route('/html/pacientes', methods=['GET'])
def show_pacientes():
    pacientes = db.get_pacientes2()
    return render_template('listaPacientes.html', pacientes=pacientes)

## Informes
@app.route('/html/informes/<idPaciente>', methods=['GET'])
def show_informes(idPaciente):
    informes = db.get_informes(idPaciente)
    return render_template('listaInforme.html', informes=informes)


@app.route('/html/upload', methods=['GET'])
def show_upload():
    pacientes = db.get_pacientes2()
    return render_template('uploadv2.html', pacientes=pacientes)

@app.route('/html/analisis', methods=['GET'])
def show_analisis():
    pacientes = db.get_pacientes2()

    return render_template('analisis.html', pacientes=pacientes)


##########################################################
#                   API
##########################################################

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


# Get los pacientes de un medico
@app.route('/api/pacientes/<idMedico>', methods=['GET'])
def get_pacientes(idMedico):
    pacientes = db.get_pacientes(idMedico)
    return jsonify(pacientes)


# Get los pacientes de la coleccion pacientes
@app.route('/api/pacientes', methods=['GET'])
def get_pacientes2():
    pacientes = db.get_pacientes2()
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


# String uploadFile(File file, String idPatient, String idDoctor):
# guarda el fichero en el servidor HDFS (en el sistema de ficheros de tu máquina),
# añadiendo una entrada en la base de datos con la ruta del fichero.

@app.route("/api/upload")
def upload_file():
    # renderiamos la plantilla "upload.html"

    return render_template('upload.html')


@app.route("/upload", methods=['POST'])
def uploader():
    if request.method == 'POST':
        # Obtenemos el input paciente
        idPaciente = request.form['idPaciente']
        # obtenemos el archivo del input "archivo"
        f = request.files['archivo']
        filename = secure_filename(f.filename)
        # Guardamos el archivo en el directorio "Archivos PDF"
        path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        # Agregamos informe a la lista de informes del paciente en la base de datos.
        pacientes = mongo.db.PacientesInformes;
        pacientes.update({"_id": int(float(idPaciente))}, {
            "$push": {"Informes": {"_idInforme": time.time(), "RutaArchivo": path, "TicketInforme": ""}}});
        # Retornamos una respuesta satisfactoria
    return render_template('uploadv2.html')


# File downloadFile(String idFile, String idPatient, String idDoctor):
# consulta la base de datos para descargar el fichero almacenado en el
# servidor HDFS (o tu máquina), dado su identificador de fichero.

@app.route('/download')
def file_downloads():
    return render_template('download.html')

@app.route('/return-files')
def return_files_tut():
    try:
        f = request.files['archivo']
        filename = secure_filename(f.filename)
        path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        return send_file(path, attachment_filename=filename)
    except Exception as e:
        return str(e)


# String analysis(String IdFile, String idPatient, Strign idDoctor):
# este será uno de los métodos principales de la API.
# Realiza el análisis del fichero (dado su identificador) y
# devuelve un ticket (una cadena de texto).

if __name__ == '__main__':
   app.run(debug=True)
