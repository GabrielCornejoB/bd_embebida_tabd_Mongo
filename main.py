from pymongo import MongoClient
from pymongo.errors import WriteError
from datetime import datetime
import eel

conn_str = "mongodb://localhost:27017"

enum_cuencas = ["Río Magdalena", "Río Orinoco", "Río Amazonas", "Río Sinú"]
enum_metodos = ["Arpón", "Atarraya", "Chinchorro", "Flecha", "Línea de mano"]
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

def update_schema_validation():
    try:
        client = MongoClient(conn_str)
        db = client.pescasAUNAP
    except Exception as e:
        print("Connection to DB failed:",e)
    else:
        try:
            db.command("collMod", "pescas", validator=schema_validation)
        except Exception as e:
            print("Schema validation failed:",e)
        else:
            print("Schema validation updated succesfully!")

@eel.expose
def read():
    print('read')

@eel.expose
def create():
    print('create')

@eel.expose
def update():
    print('update')

@eel.expose
def delete():
    print('delete')
