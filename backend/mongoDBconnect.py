import os
from mongoengine import connect

def mongoDBconnection():
    try:
        mongo_uri = os.environ.get('MONGO_URI')
        if not mongo_uri:
            raise ValueError("MONGO_URI environment variable not set")
        connect(host=mongo_uri)
        print("Connected to MongoDB successfully")
    except Exception as e:
        print(f"Error connecting to MongoDB: {e}") 

