# -*- coding: utf-8 -*-
"""
Created on Thu Feb 18 14:22:56 2021

@author: KRS1BBH
"""

from ImportFilter import Importfile
import pandas as pd
import os, glob
#get path of directory script is executed from
dirname = os.path.dirname(__file__)

#nuk
Filelist=[dirname+'/testdata/NuK/LotResultSummaryAll.csv']
product='test'
recipe='test'
equipment='NuK'

data_object_nuk=pd.DataFrame()

for file in Filelist:
    file_object_nuk=Importfile(equipment,product,recipe,file)
    file_object_nuk.read_data()
    data_object_nuk=data_object_nuk.append(file_object_nuk.data)

#smv
Filelist=[dirname+"/testdata/SmV/TEST.REC"]
product='test'
recipe='test'
equipment='SmV'

data_object_smv=pd.DataFrame()

for file in Filelist:
    file_object_smv=Importfile(equipment,product,recipe,file)
    file_object_smv.read_data()
    data_object_smv=data_object_smv.append(file_object_smv.data, ignore_index=True)
    
#elli
Filelist=[dirname+"/testdata/Elli/test.txt"]
product='test'
recipe='test'
equipment='Elli'

data_object_elli=pd.DataFrame()

for file in Filelist:
    file_object_elli=Importfile(equipment,product,recipe,file)
    file_object_elli.read_data()
    data_object_elli=data_object_elli.append(file_object_elli.data)
