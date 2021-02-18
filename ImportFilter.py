# -*- coding: utf-8 -*-
"""
Created on Thu Feb 18 08:27:59 2021

@author: KRS1BBH
"""

import pandas as pd

class Importfile:
    
    def __init__(self, equipment='', product='', recipe='', path_data=''):
        """
        

        Parameters
        ----------
        equipment : TYPE
            DESCRIPTION.
        product : TYPE
            DESCRIPTION.
        recipe : TYPE
            DESCRIPTION.
        path_data : TYPE
            DESCRIPTION.

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
        

        Parameters
        ----------
        path_out : TYPE, optional
            DESCRIPTION. The default is ''.

        Returns
        -------
        None.

        """
        
        self.data.to_excel(path_out+self.product+"_"+self.recipe+"_"+self.equipment+"_data.xlsx", index=False, sheet_name='imported data')

    
    def read_data(self):
        """
        

        Parameters
        ----------
        delimiter : TYPE, optional
            DESCRIPTION. The default is ','.
        decimal : TYPE, optional
            DESCRIPTION. The default is '.'.
        header : TYPE, optional
            DESCRIPTION. The default is 0.

        Returns
        -------
        None.

        """
        if self.equipment=='NuK':
            self._read_nuk_data()
            self._process_raw_data_nuk()
        if self.equipment=='SmV':
            self._read_smv_data()
            self._process_raw_data_smv()
        else: 
            return self
        self.data.dropna(axis=1, how='all',inplace=True)
        self.data['product']=self.product
        self.data['recipe']=self.recipe
        self.data['equipment']=self.equipment
        self.data['file']=self.path_data
    
    def _read_nuk_data(self):
        self.data=pd.read_csv(self.path_data, delimiter=',', decimal='.', header=0)
    
    def _read_smv_data(self):
        self.data=pd.read_csv(self.path_data, delimiter="\t", skiprows=54, header=None,na_values='-', names=['MP', 'Position','Membrandicke','Kavernentiefe','qual','bin'], dtype={'Position':'object','d1':'float64','d2':'float64','Qual':'float64'})
    
    def _process_raw_data_smv(self):
        header=pd.read_csv(self.path_data, delimiter='=|/',engine='python', decimal='.', nrows=23, comment='[', header=None, encoding='latin-1', index_col=False);
        for i in range(len(header[0])):
            self.data[header[0][i]]=header[1][i]
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

