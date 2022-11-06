from pymongo import MongoClient
from pymongo.errors import WriteError
from datetime import datetime

conn_str = "mongodb://localhost:27017"
try:
    client = MongoClient(conn_str)
except Exception as e:
    print("Conexión con mongo falló:",e)

db = client.pescasAUNAP

cols = db.list_collection_names()

def create(data_dict, collection_name):
    try:
        if collection_name not in cols:
            raise Exception("Nombre de colección no valido")

        col = db[collection_name]
        col.insert_one(data_dict)
    except WriteError as e:
        err_desc = str(e).split("'description': ",1)[1]
        print("Error al insertar los datos:", err_desc.split("'", 2)[1])
    except Exception as e:
        print(e)

pesca_test = {
    "cuenca": "Río Sinú",
    "metodo": "Atarraya",
    "fecha": datetime.now(),
    "peso_total_pesca": 30.65
}

create(pesca_test, 'pescas')