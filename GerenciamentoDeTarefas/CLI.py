from classes.Tarefa import Tarefa
from classes.Usuario import Usuario
from TarefaCRUD import criar_tarefa, ler_tarefa, atualizar_tarefa, deletar_tarefa
from UsuarioCRUD import criar_usuario, ler_usuario, atualizar_usuario, deletar_usuario

def menu():
    while True:
        print("1. Criar Usuario")
        print("2. Ler Usuario")
        print("3. Atualizar Usuario")
        print("4. Deletar Usuario")
        print("5. Criar Tarefa")
        print("6. Ler Tarefa")
        print("7. Atualizar Tarefa")
        print("8. Deletar Tarefa")
        print("9. Sair")

        escolha = input("Escolha uma opçao: ")

        if escolha == "1":
            usuario_id = input("ID do Usuario: ")
            nome = input("Nome do Usuario: ")
            email = input("Email do Usuario: ")
            usuario = Usuario(usuario_id, nome, email)
            criar_usuario(usuario)
            print("Usuario criado!")
        elif escolha == "2":
            usuario_id = input("ID do Usuario: ")
            usuario = ler_usuario(usuario_id)
            print(usuario)
            print("                                                       ")
        elif escolha == "3":
            usuario_id = input("ID do Usuario: ")
            nome = input("Nome do Usuario: ")
            email = input("Email do Usuario: ")
            dados_atualizados = {"nome": nome, "email": email}
            atualizar_usuario(usuario_id, dados_atualizados)
            print("Usuario atualizado!")
        elif escolha == "4":
            usuario_id = input("ID do Usuario: ")
            deletar_usuario(usuario_id)
            print("Usuario deletado do banco de dados!")
        elif escolha == "5":
            tarefa_id = input("ID da Tarefa: ")
            descricao = input("Descriçao da Tarefa: ")
            status = input("Status da Tarefa: ")
            usuario_id = input("ID do Usuario: ")
            tarefa = Tarefa(tarefa_id, descricao, status, usuario_id)
            criar_tarefa(tarefa)
            print("Nova tarefa adicionada")
        elif escolha == "6":
            tarefa_id = input("ID da Tarefa: ")
            tarefa = ler_tarefa(tarefa_id)
            print(tarefa)
            print("                                                       ")
        elif escolha == "7":
            tarefa_id = input("ID da Tarefa: ")
            descricao = input("Descriçao da Tarefa: ")
            status = input("Status da Tarefa: ")
            dados_atualizados = {"descricao": descricao, "status": status}
            atualizar_tarefa(tarefa_id, dados_atualizados)
            print("Tarefa atualizada!")
        elif escolha == "8":
            tarefa_id = input("ID da Tarefa: ")
            deletar_tarefa(tarefa_id)
            print("Tarefa concluida com sucesso!")
            print("Mais uma pra conta !")
        elif escolha == "9":
            break
        else:
            print("Opção invalida. Tente novamente.")

if __name__ == "__main__":
    menu()