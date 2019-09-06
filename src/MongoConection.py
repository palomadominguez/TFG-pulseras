from pymongo import MongoClient
import json
#import numpy as np

puerto = 27017
#puerto = 50375
hostname = 'localhost'


def ConectToMongoDB(puerto, Hostname):
    # Conexión a la base de datos
    mongoClient = MongoClient(Hostname, puerto)

    # Creamos la base de datos Pulseras
    db = mongoClient.Pulseras

    # Obtenemos una coleccion para trabajar con ella que la llamaremos archivos
    collection = db.archivos

    return collection

collection = ConectToMongoDB(puerto, hostname)

def InsertarRutaFichero(ruta_fichero):

    insert = {"fichero": ruta_fichero}

    # Insertamos la ruta del fichero en la colección
    collection.insert_one(insert)

def InsertClassify(classification, timestamp,ruta_fichero):
    query = {'fichero': ruta_fichero}

    np_array_to_list = classification.tolist()

    json_str = json.dumps(np_array_to_list)
    json_timestamp = json.dumps(timestamp.tolist())

    # Insertamos el resultado de la clasificación donde tenemos insertada la ruta de ese fichero
    collection.update(query, {'$set': {'Classify': json_str,'timeStamp':json_timestamp}}, upsert=True)