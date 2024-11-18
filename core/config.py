from pymongo import MongoClient

MONGO_DETAILS = "mongodb+srv://albert1701920351:E8T7mtKYhFLbDMXY@cluster-vetucaldas.34etx.mongodb.net/?retryWrites=true&w=majority&appName=Cluster-VetUcaldas"

client = MongoClient(MONGO_DETAILS)
database = client["vetucaldas"]
citas_collection = database["citas"]