# -*- coding: utf-8 -*-
"""
Created on Wed Jun 13 15:41:54 2018

@author: usuario
"""

import pandas as pd
import numpy as np
from keras.models import load_model
from collections import Counter
import time
from datetime import datetime

def runClassifier (current_batch, clf):
    current_batch=np.array(current_batch)
    pred=clf.predict(current_batch)
    print(pred)
    class_pred=np.argmax(pred, axis=1)
    print(class_pred)
    counts=Counter(class_pred)
    print(counts)
    #voting
    v=list(counts.values())
    print(v)
    k=list(counts.keys())
    print(k)
    batch_fit=k[v.index(max(v))]
    print(batch_fit)
    return batch_fit

def classify(f_name, model, time_window, stride, batch_size=6, verbose=True):
    start_computing_time = time.time()

    output_sequence=[]
    time_stamp = []
    df = pd.read_csv(f_name)
    data=df [["x", "y", "z"]].values
    timestamp = df[["timestamp"]].values
    if (verbose):
        print('Data loaded.')
    clf=load_model(model)
    if (verbose):
        print('Model loaded.')
    
    offset=0
    
    current_batch=[]
    bc=0
    while (offset+time_window)<data.shape[0]:
        current_batch.append(data[offset:(offset+time_window)])

        if len(current_batch)==batch_size:
            #print (str(bc))
            if (verbose & (bc%500==0)):
                print('Progress (batches): '+ str(bc))
            bc+=1
            output_sequence.append(runClassifier(current_batch, clf))

            dt_object = datetime.fromtimestamp(timestamp[offset+time_window])
            time_stamp.append(dt_object.strftime("%d-%b-%Y (%H:%M:%S.%f)"))

            current_batch=[]
        offset+=time_window
    if len(current_batch)>0:
        output_sequence.append(runClassifier(current_batch, clf))
        dt_object = datetime.fromtimestamp(timestamp[offset])
        time_stamp.append(dt_object.strftime("%d-%b-%Y (%H:%M:%S.%f)"))

    total_computing_time = time.time() - start_computing_time
    print("computing time:", str(total_computing_time))
    
    return np.array(output_sequence), np.array(time_stamp)

f_name = '/home/khaosdev/Documentos/Sandro/Proyecto_Spark/ML_HAR/models/cyclingmodel1.csv'
model='/home/khaosdev/AnacondaProjects/Proyecto_Pulseras/clf_11.bin'


if __name__ == '__main__': 
    outputs=classify(f_name, model, 1000, 1000)            
    print(outputs)
