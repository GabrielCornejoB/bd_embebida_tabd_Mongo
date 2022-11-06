from pymongo import MongoClient
from pymongo.errors import WriteError
from datetime import datetime
from numpy import array_equal

pescas_keys = ['cuenca', 'metodo', 'fecha', 'peso_total_pesca']
pescas_keys.sort()

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
        dict_keys = list(data_dict.keys())
        dict_keys.sort()
        if (collection_name == "pescas" and not array_equal(dict_keys, pescas_keys)) or (collection_name == "cuencas" and not array_equal(list(data_dict.keys()), ['cuenca'])) or (collection_name == "metodos" and not array_equal(list(data_dict.keys()), ['metodo'])):
            raise Exception("Llaves del documento a ingresar no validas")
            
        col = db[collection_name]
        col.insert_one(data_dict)
    except WriteError as e:
        err_desc = str(e).split("'description': ",1)[1]
        print("Error al insertar los datos:", err_desc.split("'", 2)[1])
    except Exception as e:
        print(e)

pesca_test = {
    "cuenca": "Río Sinú",
    "fecha": datetime(2022, 1, 9, 5, 0),
    "metodo": "Línea de mano",
    "peso_total_pesca": 12.12
}

create(pesca_test, "pescas")

def read(collection_name):
    try:
        if collection_name not in cols:
            raise Exception("Nombre de colección no valido")

        col = db[collection_name]
        documents = col.find()
    except Exception as e:
        print(e)
    else:
        for doc in documents:
            print(doc, "\n")

# read("pescas")