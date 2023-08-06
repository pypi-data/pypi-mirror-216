import datetime
from pymongo import MongoClient
import os

class SNIIM():

    def __init__(self, product, start_date, end_date):
        self.product = product
        self.start_date = datetime.datetime.strptime(start_date, "%d/%m/%Y").strftime('%d/%m/%Y')
        self.end_date   = datetime.datetime.strptime(end_date,   "%d/%m/%Y").strftime('%d/%m/%Y')
        self.MONGO_HOST = '18.215.228.120'
        self.MONGO_PORT = 27017    
        self.MONGO_USER = 'sniim_read'  
        self.MONGO_PASSW ='sniim_read_x59m'    
        self.client = MongoClient(self._connection_string)
        self.MONGO_DB = 'sniim'                
        if product == 'fyh':
            self.db_collection = 'sniim_fyh'
        if product == 'granos':
            self.db_collection = 'sniim_granos'
        self.db = self.client[self.MONGO_DB]
        self.collection = self.db[self.db_collection]

    def get_data(self):
        result = self.collection.find({"fecha":{"$gte":self.start_date,"$lte":self.end_date}})
        return result

    @property
    def _connection_string(self):
        return "mongodb://{0}:{1}@{2}:{3}".format(self.MONGO_USER, self.MONGO_PASSW, self.MONGO_HOST, self.MONGO_PORT)
