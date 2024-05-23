class SimpleCLI:
    def __init__(self):
        self.commands = {}

    def add_command(self, name, function):
        self.commands[name] = function

    def run(self):
        while True:
            command = input("Enter a command: ")
            if command == "quit":
                print("Goodbye!")
                break
            elif command in self.commands:
                self.commands[command]()
            else:
                print("Invalid command. Try again.")


class TeacherCLI(SimpleCLI):
    def __init__(self, teacher_model):
        super().__init__()
        self.teacher_model = teacher_model
        self.add_command("create", self.create_teacher)
        self.add_command("read", self.read_teacher)
        self.add_command("update", self.update_teacher)
        self.add_command("delete", self.delete_teacher)

    def create_teacher(self):
        name = input("Enter the name: ")
        ano_nasc = int(input("Enter the year of birth: "))
        cpf = input("Enter the cpf: ")
        self.teacher_model.create(name, ano_nasc, cpf)

    def read_teacher(self):
        name = input("Enter the name: ")
        teacher = self.teacher_model.read(name)
        if teacher:
            _properties = teacher[0]._properties
            ano_nasc = _properties.get('ano_nasc')
            cpf = _properties.get('cpf')
            name = _properties.get('name')
            if ano_nasc:
                print(f"Ano de Nascimento: {ano_nasc}")
            if cpf:
                print(f"CPF: {cpf}")
            if name:
                print(f"Nome: {name}")

    def update_teacher(self):
        name = input("Enter the name: ")
        new_cpf = input("Enter the new cpf: ")
        self.teacher_model.update(name, new_cpf)

    def delete_teacher(self):
        name = input("Enter the name: ")
        self.teacher_model.delete(name)

    def run(self):
        print("Welcome to the book CLI!")
        print("Available commands: create, read, update, delete, quit")
        super().run()
