from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()

# MongoDB connection URI
MONGO_URI = os.getenv('MONGO_URI')


client = MongoClient(MONGO_URI)

# Access your database
db = client.get_database()

# Access collections 
users_collection = db.users
uploads_collection = db.uploads
messages_collection = db.messages
