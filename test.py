# -*- coding: utf-8 -*-
"""
Created on Thu Feb 18 14:22:56 2021

@author: KRS1BBH
"""

from ImportFilter import Importfile
import pandas as pd

#nuk
Filelist=['//rt-smb-rtp1-office/data_nuk/NT311/Autosave/PFF1/CMS210M/SALNB.rcp/F36051.3/2021_2_15_17_24_1/LotResultSummaryAll.csv', '//rt-smb-rtp1-office/data_nuk/NT311/Autosave/PFF1/CMS210M/SALNB.rcp/F36051.3/2021_2_15_17_24_1/LotResultSummaryAll.csv']
product='CMS210M'
recipe='SALNB'
equipment='NuK'

data_object_nuk=pd.DataFrame()

for file in Filelist:
    file_object_nuk=Importfile(equipment,product,recipe,file)
    file_object_nuk.read_data()
    data_object_nuk=data_object_nuk.append(file_object_nuk.data)

#smv
Filelist=['//rt-smb-rtp1-office/smartview/Daten_MFW4/CMP4/C74902/AB_NW_DIF_NAE_E_S/C7490201_NW_NQ130_SAMPLE30.REC', '//rt-smb-rtp1-office/smartview/Daten_MFW4/CMP4/C74902/AB_NW_DIF_NAE_E_S/C7490202_NW_NQ130_SAMPLE30.REC']
product='CMS210M'
recipe='SAMPLE30'
equipment='SmV'

data_object_smv=pd.DataFrame()

for file in Filelist:
    file_object_smv=Importfile(equipment,product,recipe,file)
    file_object_smv.read_data()
    data_object_smv=data_object_smv.append(file_object_smv.data)
