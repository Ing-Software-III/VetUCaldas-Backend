from pymongo import MongoClient
from dotenv import load_dotenv
import os
load_dotenv()
username = os.getenv("DBUSERNAME")
password = os.getenv("DBPASSWORD")
MONGO_DETAILS = "mongodb+srv://"+username+":"+password+"@cluster-vetucaldas.34etx.mongodb.net/?retryWrites=true&w=majority&appName=Cluster-VetUcaldas"
print(MONGO_DETAILS)
print()
client = MongoClient(MONGO_DETAILS)
database = client["vetucaldas"]
citas_collection = database["citas"]