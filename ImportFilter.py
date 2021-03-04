# -*- coding: utf-8 -*-
"""
Created on Thu Feb 18 08:27:59 2021

@author: KRS1BBH
"""

import pandas as pd
import collections
import numpy as np

class Importfile:
    
    def __init__(self, equipment='', product='', recipe='', path_data=''):
        """
        Initialization of the Importfile class.

        Parameters
        ----------
        equipment : STRING
            Describes equipment from which the data comes. The default is ''.
            Implemented to far:
                - NuK - Rudolph n&k equipment
                - SmV - SmartView equipment
        product : STRING
            Product which the data were recorded of. The default is ''.
        recipe : STRING
            Manufactoring recipe of process flow. The default is ''.
        path_data : STRING
            Related data path. The default is ''.

        Returns
        -------
        None.

        """
        
        self.path_data=path_data
        self.data=pd.DataFrame();
        self.equipment=equipment
        self.product=product
        self.recipe=recipe
               
    def export(self, path_out = ''):
        """
        Export of class objects data into excel file in given path.

        Parameters
        ----------
        path_out : STRING, optional
            Export path in which excel file is saved. The default is ''.

        Returns
        -------
        None.

        """
        
        self.data.to_excel(path_out+self.product+"_"+self.recipe+"_"+self.equipment+"_data.xlsx", index=False, sheet_name='imported data')

    
    def read_data(self):
        """
        Reads data depending on equipment type and saves it into objects data.

        Returns
        -------
        TYPE
            DESCRIPTION.

        """
        if self.equipment=='NuK':
            self._read_nuk_data()
            self._process_raw_data_nuk()
        if self.equipment=='SmV':
            self._read_smv_data()
            self._process_raw_data_smv()
        if self.equipment=='Elli':
            self._read_elli_data()
            #self._process_raw_data_elli()
        else: 
            return self
        self.data.dropna(axis=1, how='all',inplace=True)
        self.data['product']=self.product
        self.data['recipe']=self.recipe
        self.data['equipment']=self.equipment
        self.data['file']=self.path_data
    
    def _read_nuk_data(self):
        """
        Data import for NuK equipment.

        Returns
        -------
        None.

        """
        self.data=pd.read_csv(self.path_data, delimiter=',', decimal='.', header=0)
    
    def _read_smv_data(self):
        """
        Data import for SmV equipment.

        Returns
        -------
        None.

        """
        
        self.data=pd.read_csv(self.path_data, delimiter="\t", skiprows=54, header=None,na_values='-', names=['MP', 'Position','Membrandicke','Kavernentiefe','qual','bin'], dtype={'Position':'object','d1':'float64','d2':'float64','Qual':'float64'})

    def _read_elli_data(self):
        """
        Data import for Elli equipment.

        Returns
        -------
        None.

        """
        #open file
        with open(self.path_data) as f:
            lines = f.readlines()
            
        #find beginning and end of each measurement
        points_measured=[int(lines[k].split(':')[1].strip()) for k in range(len(lines)) if 'Points Measured' in lines[k]]
        start=[k for k in range(len(lines)) if str(lines[k])[0:5]=="Point" and str(lines[k])[0:6]!="Points"]
        header_start=[k for k in range(len(lines)) if 'Wafer Number' in lines[k]]
        header_end=[k for k in range(len(lines)) if 'Points Measured' in lines[k]]
        
        #loop through the measurements
        for m in range(len(start)):
            
            #get column names and give duplicate names a counter
            names=lines[start[m]].split()
            names_col=[]
            dupl_cols=[item for item, count in collections.Counter(names).items() if count > 1]
            n=1
            k=1
            for i in range(len(names)):
                if names[i] in dupl_cols:
                    names_col.append(names[i]+'_'+str(n))
                    if k == len(dupl_cols):
                        n=n+1
                        k=1
                    k=k+1
                else:
                    names_col.append(names[i])
                    
            #transform lines into Dataframe and name columns
            df_wafer=pd.DataFrame(lines[start[m]+1:start[m]+points_measured[m]+1])
            df_wafer_2=df_wafer[0].str.replace('nm','').str.lstrip().str.rstrip().str.split('\s+', expand=True).replace('N/A',np.nan)
            df_wafer_2.columns=names_col
            
            #convert all columns into float
            for column in df_wafer_2.columns:
                df_wafer_2[column]=df_wafer_2[column].astype('float32')
           
            #add header information
            for o in range(header_start[m],header_end[m]):
                df_wafer_2[lines[o].split(':')[0].strip()]=lines[o].split(':')[1].strip()
            
            #add 'wafer_id'
            if len(df_wafer_2['Wafer Number'][0])<2:
                df_wafer_2['wafer_id']=df_wafer_2['Lot ID'][0].split('.')[0]+'-0'+df_wafer_2['Wafer Number'][0]
            else:
                df_wafer_2['wafer_id']=df_wafer_2['Lot ID'][0].split('.')[0]+'-'+df_wafer_2['Wafer Number'][0]
            
            #append wafer data 
            if m==0:           
                df_file=df_wafer_2
            else:
                df_file=df_file.append(df_wafer_2)
                
        #add general header information
        for h in range(header_start[0]):
            df_file[lines[h].split(':')[0].strip()]=lines[h].split(':')[1].strip()
            

        df_file['R_(mm)']=(df_file['X']**2+df_file['Y']**2)**0.5
        
        self.data=df_file

    
    def _process_raw_data_smv(self):
        """
        Transfer of header information into separate columns and creation of standard columns "m_date", "lot_id", "wafer_id", "product", and "recipe".
        There is also a couple of operations in there:
            - Calculate measurement position from col, row, DieSizeX, and DieSizeY as well as a radius r
            - Transfer "StartTime" into datetime format
            - Transfer wafer id into standard format XXXXXX-YY            
        
        Returns
        -------
        None.

        """
        #extract header from file
        header=pd.read_csv(self.path_data, delimiter='=|/',engine='python', decimal='.', nrows=23, comment='[', header=None, encoding='latin-1', index_col=False);
        #convert header information in individual columns
        for i in range(len(header[0])):
            self.data[header[0][i]]=header[1][i]
        #create and calculate columns described above
        self.data = self.data.rename(index=str, columns={"BatchID":"lot_id"})
        self.data['wafer_id']=header.iloc[13,1][:-2]+'-'+header.iloc[13,1][-2:]
        self.data.drop(columns='WaferID',inplace=True)
        new = self.data['Position'].str.split("/", n=1, expand=True)
        self.data['col']=new[0].astype('float32')
        self.data['row']=new[1].astype('float32')
        self.data['x']=new[0].astype('float32')*self.data['DieSizeX'].astype('float32')/1000
        self.data['y']=new[1].astype('float32')*self.data['DieSizeY'].astype('float32')/1000
        self.data['r']=(self.data['x']**2+self.data['y']**2)**0.5
        self.data['m_date'] = pd.to_datetime(self.data['StartTime'])
        self.data.drop(columns=['Position'], inplace=True)
        
    def _process_raw_data_nuk(self):
        """
        Creation of standard columns "m_date", "lot_id", "wafer_id", "product", and "recipe".
        There is also a couple of operations in there:
            - Calculate radius r from x and y
            - Transfer "DateTime" into datetime format
            - Transfer wafer id into standard format XXXXXX-YY  

        Returns
        -------
        None.

        """
        new = self.data['Position'].str.split(",|=", n=4, expand=True)
        self.data['x']=new[1].astype('float')*10
        self.data['y']=new[3].astype('float')*10  
        self.data['r']=(self.data['x']**2+self.data['y']**2)**0.5
        self.data.drop(columns=['Position'], inplace=True)
        self.data.drop(columns=['User Coords'], inplace=True)
        self.data['m_date'] = pd.to_datetime(self.data['DateTime'])
        self.data.drop(columns=['DateTime'], inplace=True)
        self.data = self.data.rename(index=str, columns={"LotID":"lot_id"}) 
        self.data['wafer_id']=self.data['SampleID'].apply(lambda row: str(row)[2:8]+'-'+str(row)[8:10] if len(str(row))==10 else str(row)[2:8]+'-0'+str(row)[8:9])
  
        
    def __repr__(self):
        
        """
        "magic" method to adjust output when class object is called

        Returns
        -------
         - first five rows of data table
         - shape
         - filepath

        """
        
        print(self.data.head())
        return "shape: {}\nfilepath: {}".format(self.data.shape, self.path_data)

