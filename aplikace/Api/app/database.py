from ctypes import sizeof
from distutils.command.config import config
from multiprocessing import connection
from posixpath import split
from matplotlib.pyplot import connect
import mysql.connector
import json
import pandas as pd
from sqlalchemy.types import Float, Integer

class DBconnect():
    def __init__(self,filepath=None,dictionary=None):
        self.__config=self.__load_configuration(filepath)
        self._connection=self.__db_con(self.__config['database'])
        self._dictionary=dictionary

    def __load_configuration(self,filepath=None):
        #filepath = filepath or "Api/app/configs/configuration.json" # local tests without docker
        filepath = filepath or "/app/configs/configuration.json" #Removed api - because docker filesystem
        with open(filepath,'r') as f:        
            config=json.load(f)
        return config

    def __db_con(self,db_config):
        connection=mysql.connector.connect(
            host=db_config["host"],
            port=db_config["port"],
            database=db_config["db_name"],
            user=db_config["user"],
            password=db_config["password"],
            charset=db_config["charset"],
            use_unicode=True
        )
        if connection.is_connected():
            print("Succesfully connected to database")
            return connection
        else:
            print("Cannot connect do database")

class SelectMethods(DBconnect):
    def process(self):
        self.__with_columns=True
        sql=self.prepare_sql(self._dictionary)
        self.__cursor=self._connection.cursor()
        self.__cursor.execute(sql)
        self.__myresult = self.__cursor.fetchall()
        self.__data=self.list_to_df(self._dictionary)
        return self.__data
        
    def prepare_sql(self,dictionary):
        if 'columns' in dictionary:
            sql="SELECT {} FROM {}".format("".join(dictionary["columns"]),dictionary['table_name'])
        else:
            sql="SELECT * FROM {}".format(dictionary['table_name'])    
            self.__with_columns=False        
        return sql


    def list_to_df(self,dictionary):
        if self.__with_columns==False:
            pass
        else:               
            columns=self._dictionary['columns']
            columns=list(columns.split(","))
        df=pd.DataFrame(self.__myresult)
        print("df")
        print(df)
        return df
        #return df.to_json(indent=2,orient='values') # can change different orient

    def save_to_csv(self,df,dataPath,filename):
        df.to_csv(dataPath+filename,index=False)
    
    def return_data(self):
        return self.__data

class InsertMethods(DBconnect):
    def process(self):
        self.insert_to_db(self._dictionary)
        return "Uspesne ulozeno do databaze"

    def insert_to_db(self,dictionary):
        print("inser to db")
        con = self._connection
        data = pd.DataFrame(dictionary['values'])
        print(type(data["sig"][1]))
        #data.to_sql(name={'signals':['PS_sig']['sig']['DAS_sig']},con=con,if_exists= 'append',index= False, method= 'multi')
                    #,dtype={"PS_sig":Integer(), "sig":Integer(),"DAS_sig":Integer()})
        for i in range(0,len(data)):
            self.__sql="INSERT INTO signals (PS_sig, sig,DAS_sig) VALUES ({},{},{})".format(data["PS_sig"][i],data["sig"][i],data["DAS_sig"][i])
            self.__cursor=self._connection.cursor()
            print(self.__sql)
            self.__cursor.execute(self.__sql)
            self._connection.commit()

        
    def prepare_sql_data(self,dictionary): # For one record
        types=["%s" for x in range(len(dictionary['field_names'].split(",")))]
        sql="INSERT INTO {} ({}) VALUES ({})".format(dictionary['table_name'],",".join(dictionary['field_names'].split(",")),','.join(map(str, types)))
        return sql

    def load_data(filepath):
        df=pd.read_csv(filepath)
        return df
    



