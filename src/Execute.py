#import har.code.MongoConection as mongo
#import har.code.classify as classify

import classify as classify
import sys
import pandas as pd
import numpy as np
np.set_printoptions(threshold=sys.maxsize)
from keras.models import load_model
from collections import Counter
import time
from datetime import datetime

#Ruta del fichero CSV a clasificar
#f_name = '/home/khaosdev/Documentos/Sandro/Proyecto_Spark/ML_HAR/models/cyclingmodel1.csv'
#Ruta del Modelo
#model='/home/khaosdev/AnacondaProjects/Proyecto_Pulseras/clf_11.bin'

#f_name = '/Users/Paloma/MEGA/4ANO/TFG/models/1__020144_2016-12-12_13-07-57_Carmen_Aguilera_Garcia_6_meses.csv'
f_name = '/Users/Paloma/MEGA/4ANO/TFG/models/cyclingmodel1.csv'

model = '/Users/Paloma/MEGA/4ANO/TFG/clf_11.bin'

def execute_analysis(filename: str, model):
    classification, timestamp = classify.classify(filename, model, 1000, 1000)
    return classification, timestamp

if __name__ == '__main__':

    # #Insertamos la ruta del fichero en MongoDB
    # mongo.InsertarRutaFichero(f_name)
    # #Clasificamos el fichero
    # classification, timestamp = classify.classify(f_name, model, 1000, 1000)
    # print(classification)
    # # Insertamos la clasificacion en la base de datos de mongodb junto a la ruta del fichero insertada previamente
    # mongo.InsertClassify(classification, timestamp, f_name)
    classification, timestamp = classify.classify(f_name, model, 1000, 1000)
    file = open('testfile.csv', 'w')
    print("aqui empieza")
    print(str(classification))
    file.write(str(classification))
    file.close()

