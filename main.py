from pymongo import MongoClient
from pymongo.errors import WriteError
from datetime import datetime
from numpy import array_equal
from bson.objectid import ObjectId
import eel
import json

conn_str = "mongodb://localhost:27017"
pescas_keys = ['cuenca', 'metodo', 'fecha', 'peso_total_pesca']
pescas_keys.sort()

try:
    init_client = MongoClient(conn_str)
except Exception as e:
    print("Conección inicial con Mongo falló:",e)

init_db = init_client.pescasAUNAP
enum_cuencas = [x['cuenca'] for x in list(init_db['cuencas'].find({}, {'_id': 0, 'cuenca': 1}))]
enum_metodos = [x['metodo'] for x in list(init_db['metodos'].find({}, {'_id': 0, 'metodo': 1}))]
cols = init_db.list_collection_names()
init_client.close()

eel.init("web")

def jsonize(text):
    return json.dumps(text, ensure_ascii=False, default=str).encode('utf-8').decode()

def update_schema_validation():
    try:
        client = MongoClient(conn_str)
        db = client.pescasAUNAP
    except Exception as e:
        client.close()
        return jsonize("[ERR]Connection to DB failed:" + str(e))
    else:
        try:
            schema_validation = { 
            "$jsonSchema": { 
                "bsonType": "object", 
                "required": ["_id", "cuenca", "metodo", "fecha", "peso_total_pesca"], 
                "properties": { 
                    "_id": { "bsonType": "objectId" }, 
                    "cuenca": { 
                        "enum": enum_cuencas, 
                        "description": "El nombre de la cuenca ingresado no es valido" 
                    }, 
                    "metodo": { 
                        "enum": enum_metodos, 
                        "description": "El nombre del método de pesca ingresado no es valido" 
                    }, 
                    "fecha": { 
                        "bsonType": "date", 
                        "description": "El campo fecha debe enviarse en formato AAAA/MM/DD" 
                    }, 
                    "peso_total_pesca": { 
                        "bsonType": "double", 
                        "minimum": 0.1, 
                        "description": "El peso de la pesca debe ser un número decimal y debe valer mínimo 0.1" 
                    }
                }, 
                "additionalProperties": False 
            } 
        }
            db.command("collMod", "pescas", validator=schema_validation)
        except Exception as e:
            return jsonize("[ERR]Schema validation failed:" + str(e))
        client.close()
    
@eel.expose
def read(collection_name):
    try:
        client = MongoClient(conn_str)
        db = client.pescasAUNAP
    except Exception as e:
        return "[ERR]Conexión con mongo falló:" + str(e)

    try:
        if collection_name not in cols:
            return "[ERR]Nombre de colección no valido"

        col = db[collection_name]
        documents = col.find()
    except Exception as e:
        return "[ERR]" + str(e)
    else:
        l_docs = []
        for doc in documents:
            l_docs.append(doc)
        return jsonize(l_docs)

@eel.expose
def create():
    print('create')

@eel.expose
def update():
    print('update')

@eel.expose
def delete():
    print('delete')


eel.start("index.html", cmdline_args=['--start-fullscreen'])