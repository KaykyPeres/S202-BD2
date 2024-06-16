class Tarefa:
    def __init__(self, tarefa_id, descricao, status, usuario_id):
        self.tarefa_id = tarefa_id
        self.descricao = descricao
        self.status = status
        self.usuario_id = usuario_id

    def to_dict(self):
        return {
            "tarefa_id": self.tarefa_id,
            "descricao": self.descricao,
            "status": self.status,
            "usuario_id": self.usuario_id
        }