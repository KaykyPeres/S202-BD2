from pymongo import MongoClient


client = MongoClient('localhost', 27017)
db = client['gerenciamento_tarefas']
usuario_collection = db['usuario']
tarefas_collection = db['tarefas']

def criar_usuario(usuario):
    usuario_collection.insert_one(usuario.to_dict())

def ler_usuario(usuario_id):
    return usuario_collection.find_one({"usuario_id": usuario_id})

def atualizar_usuario(usuario_id, dados_atualizados):
    usuario_collection.update_one({"usuario_id": usuario_id}, {"$set": dados_atualizados})

def deletar_usuario(usuario_id):
    usuario_collection.delete_one({"usuario_id": usuario_id})