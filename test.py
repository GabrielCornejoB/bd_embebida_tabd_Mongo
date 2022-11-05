from pymongo import MongoClient
from pymongo.errors import WriteError
from datetime import datetime

conn_str = "mongodb://localhost:27017"
try:
    client = MongoClient(conn_str)
except Exception as e:
    print("Conexión con mongo falló:",e)

db = client.pescasAUNAP
collections = db.list_collection_names()
print(collections)

pesca_test = {
    "cuenca": "0000njkr",
    "metodo": "Atarraya",
    "fecha": datetime.now(),
    "peso_total_pesca": 3.1
}
try:
    db.pescas.insert_one(pesca_test)
except WriteError as e:
    err_desc = str(e).split("'description': ",1)[1]
    print(err_desc.split("'", 2)[1])
else:
    print("Exito!")