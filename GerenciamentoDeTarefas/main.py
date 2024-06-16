from pymongo import MongoClient

from CLI import menu

def main():
    global usuarios_collection, tarefas_collection

    # Configuração do MongoDB
    client = MongoClient('localhost', 27017)
    db = client['gerenciamento_tarefas']
    usuarios_collection = db['usuarios']
    tarefas_collection = db['tarefas']

    # Iniciar o menu
    menu()


if __name__ == "__main__":
    main()