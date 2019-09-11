import pymongo
from pandas._libs import json

myclient = pymongo.MongoClient("mongodb://localhost:27017/")

mydb = myclient["pulserasdb"]

#check database
print(myclient.list_database_names())

mycol = mydb["MedicoPacientes"]

medicoPacientes = "/Users/Paloma/MEGA/4ANO/TFG/BD-Pulseras/ColeccionMedicoPacientes.json"

print("\nLos datos ingresados son:")
print("Base de datos: " + str(mydb))
print("Coleccion: " + str(mycol))
print("Ruta del archivo .json: " + str(medicoPacientes))

# Abriendo el archivo con la funcion open()
f = open(str(medicoPacientes), 'r')



