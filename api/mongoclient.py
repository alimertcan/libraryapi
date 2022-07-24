import pymongo
import os

url_mongo = "mongodb://localhost:27017"  #os.getenv('MONGO_URL')



class MongoClient:
    __instance = None

    @staticmethod
    def get_instance():
        if MongoClient.__instance == None:
            MongoClient()
        return MongoClient.__instance

    def __init__(self):
        """ Virtually private constructor. """
        if MongoClient.__instance != None:
            raise Exception("This class is a singleton!")
        else:
            MongoClient.__instance = pymongo.MongoClient(url_mongo, connect=False, serverSelectionTimeoutMS=2000)

