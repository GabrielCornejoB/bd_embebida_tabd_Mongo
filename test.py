from pymongo import MongoClient
from pymongo.errors import WriteError
from datetime import datetime
from numpy import array_equal
from bson.objectid import ObjectId

conn_str = "mongodb://localhost:27017"
pescas_keys = ['cuenca', 'metodo', 'fecha', 'peso_total_pesca']
pescas_keys.sort()

try:
    client = MongoClient(conn_str)
except Exception as e:
    print("Conexión con mongo falló:",e)

db = client.pescasAUNAP

enum_cuencas = [x['cuenca'] for x in list(db['cuencas'].find({}, {'_id': 0, 'cuenca': 1}))]
print(enum_cuencas)
enum_metodos = [x['metodo'] for x in list(db['metodos'].find({}, {'_id': 0, 'metodo': 1}))]
print(enum_metodos)

def append_to_enum(enum_name, new_val):
    if enum_name == "enum_cuencas":
        global enum_cuencas
        enum_cuencas.append(new_val)
    elif enum_name == "enum_metodos":
        global enum_metodos
        enum_metodos.append(new_val)

def update_enum(enum_name, old_val, new_val):
    if enum_name == "enum_cuencas":
        global enum_cuencas
        enum_cuencas = [new_val if x == old_val else x for x in enum_cuencas]
    elif enum_name == "enum_metodos":
        global enum_metodos
        enum_metodos = [new_val if x == old_val else x for x in enum_metodos]

def update_schema_validation():  
    try:
        global enum_cuencas
        global enum_metodos
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
        print("Schema validation failed:",e)
    else:
        print("Schema validation updated succesfully!")

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
        if collection_name == "cuencas":
            append_to_enum("enum_cuencas", data_dict['cuenca'])
            update_schema_validation()

    except WriteError as e:
        err_desc = str(e).split("'description': ",1)[1]
        print("Error al insertar los datos:", err_desc.split("'", 2)[1])
    except Exception as e:
        print(e)

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

def update(_id, data_dict, collection_name):
    try:
        if collection_name not in cols:
            raise Exception("Nombre de colección no valido")
        dict_keys = list(data_dict.keys())
        dict_keys.sort()
        if (collection_name == "pescas" and not array_equal(dict_keys, pescas_keys)) or (collection_name == "cuencas" and not array_equal(list(data_dict.keys()), ['cuenca'])) or (collection_name == "metodos" and not array_equal(list(data_dict.keys()), ['metodo'])):
            raise Exception("Llaves del documento a ingresar no validas")

        _id = ObjectId(_id)

        col = db[collection_name]
        old_doc = col.find_one({'_id': _id})
        if old_doc:
            update_json = {
                "$set": data_dict
            }
            if collection_name != "pescas":
                if collection_name == "cuencas":
                    update_enum("enum_cuencas", old_doc['cuenca'], data_dict['cuenca'])
                    update_schema_validation()
                    db['pescas'].update_many({'cuenca': old_doc['cuenca']},{ "$set": { 'cuenca': data_dict['cuenca']}})
                elif collection_name == "metodos":
                    update_enum("enum_metodos", old_doc['metodo'], data_dict['metodo'])
                    update_schema_validation()
                    db['pescas'].update_many({'metodo': old_doc['metodo']},{ "$set": { 'metodo': data_dict['metodo']}})
            col.find_one_and_update({'_id': _id}, update_json)

    except Exception as e:
        print(e)

# def delete(_id, collection_name):


update("63644453cadd66da5dae5f01", {"cuenca": "Río Magdalena"}, "cuencas")