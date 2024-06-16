class Usuario:
    def __init__(self, usuario_id, nome, email):
        self.usuario_id = usuario_id
        self.nome = nome
        self.email = email

    def to_dict(self):
        return {
            "usuario_id": self.usuario_id,
            "nome": self.nome,
            "email": self.email
        }