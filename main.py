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

def delete_from_enum(enum_name, val):
    if enum_name == "enum_cuencas":
        global enum_cuencas
        enum_cuencas.remove(val)
    elif enum_name == "enum_metodos":
        global enum_metodos
        enum_metodos.remove(val)
   

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
            client.close()
            return jsonize("[ERR]Schema validation failed:" + str(e))    
        client.close()
    
@eel.expose
def read(collection_name):
    try:
        client = MongoClient(conn_str)
        db = client.pescasAUNAP
    except Exception as e:
        client.close()
        return jsonize("[ERR]Conexión con mongo falló:" + str(e))

    try:
        if collection_name not in cols:
            return jsonize("[ERR]Nombre de colección no valido")

        col = db[collection_name]
        documents = col.find()

    except Exception as e:
        client.close()
        return jsonize("[ERR]" + str(e))
    else:
        l_docs = []
        for doc in documents:
            l_docs.append(doc)
        client.close()
        return jsonize(l_docs)

@eel.expose
def create(data_dict, collection_name):
    try:
        client = MongoClient(conn_str)
        db = client.pescasAUNAP
    except Exception as e:
        return jsonize("[ERR]Conexión con mongo falló:" + str(e))

    try:
        if collection_name not in cols:
            return jsonize("[ERR]Nombre de colección no valido")
        dict_keys = list(data_dict.keys())
        dict_keys.sort()
        if (collection_name == "pescas" and not array_equal(dict_keys, pescas_keys)) or (collection_name == "cuencas" and not array_equal(list(data_dict.keys()), ['cuenca'])) or (collection_name == "metodos" and not array_equal(list(data_dict.keys()), ['metodo'])):
            return jsonize("[ERR]Llaves del documento a ingresar no validas")

        if collection_name == "cuencas":
            append_to_enum("enum_cuencas", data_dict['cuenca'])
            update_schema_validation()
        elif collection_name == "metodos":
            append_to_enum("enum_metodos", data_dict['metodo'])
            update_schema_validation()

        col = db[collection_name]
        if collection_name == "pescas":
            data_dict['fecha'] = datetime.strptime(data_dict['fecha'], "%Y-%m-%d")
            data_dict['peso_total_pesca'] = float(data_dict['peso_total_pesca'])
        col.insert_one(data_dict)
        
    except WriteError as e:
        client.close()
        err_desc = str(e).split("'description': ",1)[1]
        return jsonize("[ERR]" + err_desc.split("'", 2)[1])
    except Exception as e:
        client.close()
        return jsonize("[ERR]" + str(e))
    else:
        client.close()
        with open("logs.txt", 'a', encoding='utf-8') as logs:
            logs.write("[" + str(datetime.now())[0:16] + "]\tCREATE on " + collection_name + ", args:" + str(data_dict) + "<br>\n")
        return jsonize("[MSG]Operación realizada con exito :)")


@eel.expose
def update(_id, data_dict, collection_name):
    try:
        client = MongoClient(conn_str)
        db = client.pescasAUNAP
    except Exception as e:
        return jsonize("[ERR]Conexión con mongo falló:" + str(e))

    try:
        if collection_name not in cols:
            return jsonize("[ERR]Nombre de colección no valido")
        dict_keys = list(data_dict.keys())
        dict_keys.sort()
        if (collection_name == "pescas" and not array_equal(dict_keys, pescas_keys)) or (collection_name == "cuencas" and not array_equal(list(data_dict.keys()), ['cuenca'])) or (collection_name == "metodos" and not array_equal(list(data_dict.keys()), ['metodo'])):
            return jsonize("[ERR]Llaves del documento a ingresar no validas")

        _id = ObjectId(_id)

        col = db[collection_name]
        old_doc = col.find_one({'_id': _id})
        if old_doc:
            if collection_name == "pescas":
                data_dict['fecha'] = datetime.strptime(data_dict['fecha'], "%Y-%m-%d")
                data_dict['peso_total_pesca'] = float(data_dict['peso_total_pesca'])

            update_json = {
                "$set": data_dict
            }
            col.find_one_and_update({'_id': _id}, update_json)

            if collection_name != "pescas":
                if collection_name == "cuencas":
                    update_enum("enum_cuencas", old_doc['cuenca'], data_dict['cuenca'])
                    update_schema_validation()
                    db['pescas'].update_many({'cuenca': old_doc['cuenca']},{ "$set": { 'cuenca': data_dict['cuenca']}})
                elif collection_name == "metodos":
                    update_enum("enum_metodos", old_doc['metodo'], data_dict['metodo'])
                    update_schema_validation()
                    db['pescas'].update_many({'metodo': old_doc['metodo']},{ "$set": { 'metodo': data_dict['metodo']}})        
    except WriteError as e:
        err_desc = str(e).split("'description': ",1)[1]
        return jsonize("[ERR]" + err_desc.split("'", 2)[1])
    except Exception as e:
        return jsonize("[ERR]" + str(e))
    else:
        with open("logs.txt", 'a', encoding='utf-8') as logs:
            logs.write("[" + str(datetime.now())[0:16] + "]\tUPDATE on " + collection_name + ", id: " + str(_id) + ", args: " + str(data_dict) + "<br>\n")
        return jsonize("[MSG]Operación realizada con exito :)")

@eel.expose
def delete(_id, collection_name):
    try:
        client = MongoClient(conn_str)
        db = client.pescasAUNAP
    except Exception as e:
        return jsonize("[ERR]Conexión con mongo falló:" + str(e))

    try:
        if collection_name not in cols:
            return jsonize("[ERR]Nombre de colección no valido")
        col = db[collection_name]
        _id = ObjectId(_id)
        old_doc = col.find_one({'_id': _id})
        is_related = True

        if collection_name != "pescas":
            if collection_name == "cuencas":
                cuencas_count = db['pescas'].count_documents({"cuenca": old_doc['cuenca']})
                if cuencas_count == 0:
                    is_related = False
                    delete_from_enum("enum_cuencas", old_doc['cuenca'])
                    update_schema_validation()
            if collection_name == "metodos":
                metodos_count = db['pescas'].count_documents({'metodo': old_doc['metodo']})
                if metodos_count == 0:
                    is_related = False
                    delete_from_enum("enum_metodos", old_doc['metodo'])
                    update_schema_validation()
        else:
            is_related = False
        if not is_related:
            col.find_one_and_delete({"_id": _id})
        else:
            return jsonize("[ERR]El doc se encuentra en uso en la colección Pescas")
    except Exception as e:
        return jsonize("[ERR:]" + str(e))
    else:
        with open("logs.txt", 'a', encoding='utf-8') as logs:
            logs.write("[" + str(datetime.now())[0:16] + "]\tDELETE on " + collection_name + ", (id: " + str(_id) + ")<br>\n")
        return jsonize("[MSG]Operación realizada con exito :)")

@eel.expose
def get_logs():
    logs =  open("logs.txt", 'r', encoding='utf-8')
    data = logs.read()
    logs.close()
    return jsonize(data)

eel.start("index.html", cmdline_args=['--start-fullscreen'])