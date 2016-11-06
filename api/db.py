import api
from pymongo import MongoClient

# TEMPORARY CLIENT
HOST = 'localhost'
PORT = 27017
DB   = 'manglr'

def init_db():
    """ Creates client and database connections/objects """
    client     = MongoClient(HOST, PORT)
    api.DB     = client[DB]

