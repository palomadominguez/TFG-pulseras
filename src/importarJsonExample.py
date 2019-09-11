from pymongo import *
import json

puerto = 27017
#puerto = 50375
hostname = 'localhost'

print("\nSe conectara al Servidor de Base de Datos Local.")
conexion = MongoClient(hostname, puerto)  # La conexion sera local

# Variable de referencia de la base de datos.
ndb = raw_input("\nIngrese el nombre de la base de datos: ")
db = conexion[ndb]  # Conexion a la db

# Variable de referencia a la coleccion que se usara.
col = raw_input("\nIngrese el nombre de la coleccion a usar: ")
coleccion = db[col]

# Variable que contendra la ruta del archivo .json
archivo = raw_input("\nIngrese la ruta del archivo que contiene los datos: ")

print("\nLos datos ingresados son:")
print("Base de datos: " + str(db))
print("Coleccion: " + str(coleccion))
print("Ruta del archivo .json: " + str(archivo))

respuesta = raw_input("\nEstos datos son correctos? (s/n): ")

if respuesta == "s":
    # Abriendo el archivo con la funcion open()
    f = open(str(archivo), 'r')

    # Recorriendo las lineas del archivo
    for linea in f:
        # Insertando los registros en la DB
        dic = json.loads(linea)  # Crea los diccionarios a partir del string linea
        coleccion.insert(dic)

    # Cerramos el archivo
    f.close()
    print
    "\nSe han importado los datos exitosamente!"

else:
    print
    "\nAccion Cancelada."