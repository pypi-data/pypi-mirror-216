import datetime
import mysql.connector
from pymongo import MongoClient
import os

class SNIIM():

    def __init__(self, product, start_date, end_date, dbms):
        self.product = product
        self.start_date = start_date
        self.end_date   = end_date
        if dbms=='mysql':
            self.MYSQL_HOST = os.environ.get('MYSQL_HOST')
            self.MYSQL_PORT = os.environ.get('MYSQL_PORT')
            self.MYSQL_USER = os.environ.get('MYSQL_USER')
            self.MYSQL_PASSW= os.environ.get('MYSQL_PASSWORD')
            self.MYSQL_DB = os.environ.get('MYSQL_DATABASE')
            self.dbms=dbms
        if dbms=='mongo':
            self.MONGO_HOST = os.environ.get('MONGO_HOST')
            self.MONGO_PORT = os.environ.get('MONGO_PORT')
            self.MONGO_USER = os.environ.get('MONGO_USER')
            self.MONGO_PASSW = os.environ.get('MONGO_PASSWORD')
            self.dbms=dbms

            self.client = MongoClient(self._connection_string)

            #if os.environ.get('CONNECT_WITH_USER', 'False') == 'True':
            #    self.client = "mongodb://{0}:{1}@{2}:{3}".format(self.MONGO_USER, self.MONGO_PASSW, self.MONGO_HOST, self.MONGO_PORT)
            #else:
            #    self.client = "mongodb://{0}:{1}".format(self.MONGO_HOST, self.MONGO_PORT)


            self.MONGO_DB = os.environ.get('MONGO_DATABASE')
            if product == 'fyh':
                self.db_collection = 'sniim_fyh'
            if product == 'granos':
                self.db_collection = 'sniim_granos'
            self.db = self.client[self.MONGO_DB]
            self.collection = self.db[self.db_collection]


    def get_data(self):
        start_date = self.start_date
        end_date   = self.end_date
        dbms       = self.dbms
        if self.product == 'granos':
            result = self.db_con('sniim_granos', start_date, end_date, dbms)
        if self.product == 'fyh':
            result = self.db_con('sniim_fyh', start_date, end_date, dbms)
        return result

    def db_con(self, product, start_date, end_date, dbms):
        if dbms == 'mysql':
            mydb = mysql.connector.connect(host=self.MYSQL_HOST, user=self.MYSQL_USER, password=self.MYSQL_PASSW, port=self.MYSQL_PORT, database=self.MYSQL_DB)
            mycursor = mydb.cursor(dictionary=True)
            mycursor.execute("SELECT * FROM "+ str(product) + " WHERE fecha BETWEEN '" + str(start_date) + "' AND '" + str(end_date) + "' ")
            return mycursor.fetchall()
        if dbms == 'mongo':
            start_date = datetime.datetime.strptime(start_date, "%Y-%m-%d")
            start_date = start_date.strftime('%d/%m/%Y')
            end_date = datetime.datetime.strptime(end_date, "%Y-%m-%d")
            end_date = end_date.strftime('%d/%m/%Y')
            return self.collection.find({"fecha":{"$gte":start_date,"$lte":end_date}})
    
    @property
    def _connection_string(self):
        if os.environ.get('CONNECT_WITH_USER', 'False') == 'True':
            return "mongodb://{0}:{1}@{2}:{3}".format(self.MONGO_USER, self.MONGO_PASSW, self.MONGO_HOST, self.MONGO_PORT)
        else:
            return "mongodb://{0}:{1}".format(self.MONGO_HOST, self.MONGO_PORT)
