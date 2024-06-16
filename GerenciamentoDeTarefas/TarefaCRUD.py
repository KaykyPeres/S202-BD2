from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client['gerenciamento_tarefas']
usuario_collection = db['usuario']
tarefas_collection = db['tarefas']

def criar_tarefa(tarefa):
    tarefas_collection.insert_one(tarefa.to_dict())

def ler_tarefa(tarefa_id):
    return tarefas_collection.find_one({"tarefa_id": tarefa_id})

def atualizar_tarefa(tarefa_id, dados_atualizados):
    tarefas_collection.update_one({"tarefa_id": tarefa_id}, {"$set": dados_atualizados})

def deletar_tarefa(tarefa_id):
    tarefas_collection.delete_one({"tarefa_id": tarefa_id})