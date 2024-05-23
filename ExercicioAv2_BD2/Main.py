from Database import Database
from query import Query
from teacher_crud import TeacherCRUD
from CLI import TeacherCLI

# cria uma instância da classe Database, passando os dados de conexão com o banco de dados Neo4j
db = Database("bolt://3.235.2.20:7687", "neo4j", "liter-eddy-sponge")

# Criando uma instância da classe Query e  para interagir com o banco de dados
query_db = Query(db)
teacher_db = TeacherCRUD(db)

# QUESTAO 1
print(query_db.renzo())
print(query_db.starts_with_m())
print(query_db.cities())
print(query_db.schools())

# QUESTAO 2
print(query_db.ano_nasc())
print(query_db.population())
print(query_db.cep())
print(query_db.teacher())

# QUESTAO 3
teacherCLI = TeacherCLI(teacher_db)
teacherCLI.run()

# Fechando a conexão com o banco de dados
db.close()