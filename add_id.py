import pandas as pd
import csv 
from itertools import groupby
import numpy as np

def add_id():

    with open('train_labels_new2.csv') as imp:
        reader = csv.reader(imp)
        examples= pd.read_csv(imp, encoding='unicode_escape')
        filename = examples["filename"].values
        
        #No need to use `insert(), `append()` simply use `+` to concatenate two lists.
        
        grouped = [list(g) for k, g in groupby(filename.tolist())]
        examples['ID']=np.repeat(range(len(grouped)),[len(x) for x in grouped])+1
        examples.to_csv("train_labels_new2.csv")
    
    with open('test_labels_new2.csv') as imp:
        reader = csv.reader(imp)
        examples= pd.read_csv(imp, encoding='unicode_escape')
        filename = examples["filename"].values
            
        grouped = [list(g) for k, g in groupby(filename.tolist())]
        examples['ID']=np.repeat(range(len(grouped)),[len(x) for x in grouped])+1
        examples.to_csv("test_labels_new2.csv")


add_id()








