import json

from datetime import datetime

from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider
from cassandra.query import dict_factory

import redis

# This secure connect bundle is autogenerated when you download your SCB,
# if yours is different update the file name below
cloud_config = {
    'secure_connect_bundle': 'secure-connect.zip'
}

# This token JSON file is autogenerated when you download your token,
# if yours is different update the file name below
with open("token.json") as f:
    secrets = json.load(f)

CLIENT_ID = secrets["clientId"]
CLIENT_SECRET = secrets["secret"]

auth_provider = PlainTextAuthProvider(CLIENT_ID, CLIENT_SECRET)
cluster = Cluster(cloud=cloud_config, auth_provider=auth_provider)
cassandra_session = cluster.connect()
cassandra_session.row_factory = dict_factory  # Returning dict from Cassandra
cassandra_session.set_keyspace('ks')  # Change to your keyspace

redis_conn = redis.Redis(
    host="localhost", port=6379,  # Use your Redis instance host and port
    username="default",  # use your Redis user.
    password="....",  # deixei sem a senha  # use your Redis password
    decode_responses=True
)

# ------------------- !! Attention !! -------------------
#redis_conn.flushall()  # Clear Redis database


# -------------------------------------------------------

def criar_tabelas():
    cassandra_session.execute("""
    CREATE TABLE IF NOT EXISTS usuario (
        id int,
        estado text,
        cidade text,
        endereco text,
        nome text,
        email text,
        interesses list<text>,
        PRIMARY KEY ((estado, cidade), id)
    )
    """)

    cassandra_session.execute("""
    CREATE TABLE IF NOT EXISTS produto (
        id int,
        categoria text,
        nome text,
        custo int,
        preco int,
        quantidade int,
        PRIMARY KEY (categoria, id)
    )
    """)

    cassandra_session.execute("""
    CREATE TABLE IF NOT EXISTS venda (
        id int,
        dia int,
        mes int,
        ano int,
        hora text,
        valor int,
        produtos list<map<int, int>>,
        usuario map<text, text>,
        PRIMARY KEY ((dia, mes, ano), hora, id)
    )
    """)

def registrar_usuarios(users):
    for user in users:
        cassandra_session.execute("""
        INSERT INTO usuario (id, estado, cidade, endereco, nome, email, interesses)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (
        user['id'], user['estado'], user['cidade'], user['endereco'], user['nome'], user['email'], user['interesses']))


def registrar_produtos(products):
    for product in products:
        cassandra_session.execute("""
        INSERT INTO produto (id, categoria, nome, custo, preco, quantidade)
        VALUES (%s, %s, %s, %s, %s, %s)
        """, (
        product['id'], product['categoria'], product['nome'], int(product['custo'] * 100), int(product['preco'] * 100),
        product['quantidade']))



# Questão 1
def questao_1_a():
    rows = cassandra_session.execute("SELECT COUNT(*) FROM usuario")
    return rows[0]['count']

def test_questao_1_a():
    users = [
        {"id": 1, "estado": "Minas Gerais", "cidade": "Santa Rita do Sapucaí", "endereco": "Rua A, 45",
         "nome": "Serafim Amarantes", "email": "samarantes@g.com",
         "interesses": ["futebol", "pagode", "engraçado", "cerveja", "estética"]},
        {"id": 2, "estado": "São Paulo", "cidade": "São Bento do Sapucaí", "endereco": "Rua B, 67",
         "nome": "Tamara Borges", "email": "tam_borges@g.com",
         "interesses": ["estética", "jiujitsu", "luta", "academia", "maquiagem"]},
        {"id": 3, "estado": "Minas Gerais", "cidade": "Santa Rita do Sapucaí", "endereco": "Rua C, 84",
         "nome": "Ubiratã Carvalho", "email": "bira@g.com",
         "interesses": ["tecnologia", "hardware", "games", "culinária", "servers"]},
        {"id": 4, "estado": "Minas Gerais", "cidade": "Pouso Alegre", "endereco": "Rua D, 21",
         "nome": "Valéria Damasco", "email": "valeria_damasco@g.com",
         "interesses": ["neurociências", "comportamento", "skinner", "laboratório", "pesquisa"]}
    ]

    assert len(users) == questao_1_a(users)


def questao_1_b():
    rows = cassandra_session.execute("SELECT SUM(custo * quantidade) AS total_custo FROM produto")
    return rows[0]['total_custo'] / 100


def teste_questao_1_b():
    products = [
        {"id": 1, "categoria": "escritório", "nome": "Cadeira HM conforto", "custo": 2000.00, "preco": 3500.00,
         "quantidade": 120},
        {"id": 2, "categoria": "culinária", "nome": "Tábua de corte Hawk", "custo": 360.00, "preco": 559.90,
         "quantidade": 40},
        {"id": 3, "categoria": "tecnologia", "nome": "Notebook X", "custo": 3000.00, "preco": 4160.99,
         "quantidade": 76},
        {"id": 4, "categoria": "games", "nome": "Headset W", "custo": 265.45, "preco": 422.80, "quantidade": 88},
        {"id": 5, "categoria": "tecnologia", "nome": "Smartphone X", "custo": 2000.00, "preco": 3500.00,
         "quantidade": 120},
        {"id": 6, "categoria": "games", "nome": "Gamepad Y", "custo": 256.00, "preco": 519.99, "quantidade": 40},
        {"id": 7, "categoria": "estética", "nome": "Base Ismusquim", "custo": 50.00, "preco": 120.39, "quantidade": 76},
        {"id": 8, "categoria": "cerveja", "nome": "Gutten Bier IPA 600ml", "custo": 65.45, "preco": 122.80,
         "quantidade": 88}
    ]

    total_cost = 765559.20

    assert total_cost == questao_1_b(products)


# Questão 2
def questao_2(state):
    rows = cassandra_session.execute("SELECT * FROM usuario WHERE estado = %s", (state,))
    for row in rows:
        user_id = row['id']
        redis_conn.hset(f"user:{user_id}", mapping={
            'estado': row['estado'],
            'cidade': row['cidade'],
            'endereco': row['endereco'],
            'nome': row['nome'],
            'email': row['email'],
            'interesses': json.dumps(row['interesses'])
        })
    return [redis_conn.hgetall(f"user:{row['id']}") for row in rows]


def test_questao_2():
    state = "Minas Gerais"

    users = [
        {"id": '1', "estado": "Minas Gerais", "cidade": "Santa Rita do Sapucaí", "endereco": "Rua A, 45",
         "nome": "Serafim Amarantes", "email": "samarantes@g.com",
         "interesses": ["futebol", "pagode", "engraçado", "cerveja", "estética"]},
        {"id": '3', "estado": "Minas Gerais", "cidade": "Santa Rita do Sapucaí", "endereco": "Rua C, 84",
         "nome": "Ubiratã Carvalho", "email": "bira@g.com",
         "interesses": ["tecnologia", "hardware", "games", "culinária", "servers"]},
        {"id": '4', "estado": "Minas Gerais", "cidade": "Pouso Alegre", "endereco": "Rua D, 21",
         "nome": "Valéria Damasco", "email": "valeria_damasco@g.com",
         "interesses": ["neurociências", "comportamento", "skinner", "laboratório", "pesquisa"]}
    ]

    assert users == sorted(questao_2(state), key=lambda d: d['id'])


# Questão 3
def questao_3(user_id):
    user = redis_conn.hgetall(f"user:{user_id}")
    interesses = json.loads(user['interesses'])
    produtos_interessantes = []
    for interesse in interesses:
        rows = cassandra_session.execute("SELECT id, nome, preco FROM produto WHERE categoria = %s", (interesse,))
        produtos_interessantes.extend(rows)
    return produtos_interessantes


def test_questao_3():
    user_id = 3

    products = [
        {"id": 2, "nome": "Tábua de corte Hawk", "preco": 559.90},
        {"id": 3, "nome": "Notebook X", "preco": 4160.99},
        {"id": 4, "nome": "Headset W", "preco": 422.80},
        {"id": 5, "nome": "Smartphone X", "preco": 3500.00},
        {"id": 6, "nome": "Gamepad Y", "preco": 519.99},
        {"id": 7, "nome": "PC gamer Top", "preco": 7309.99}
    ]

    assert products == sorted(questao_3(user_id), key=lambda d: d['id'])


# Questão 4
def questao_4(user_id, cart):
    for item in cart:
        redis_conn.hset(f"cart:{user_id}:{item['id']}", mapping=item)
    return [redis_conn.hgetall(f"cart:{user_id}:{item['id']}") for item in cart]


def test_questao_4():
    user_id = 3

    cart = [
        {"id": '4', "nome": "Headset W", "preco": '422.80', "quantidade": '1'},
        {"id": '6', "categoria": "games", "nome": "Gamepad Y", "preco": '519.99', "quantidade": '2'},
    ]

    assert cart == sorted(questao_4(user_id, cart), key=lambda d: d["id"])


# Questão 5
def questao_5(user_id, date_time):
    cart_keys = redis_conn.keys(f"cart:{user_id}:*")
    cart_items = [redis_conn.hgetall(key) for key in cart_keys]
    user = redis_conn.hgetall(f"user:{user_id}")
    produtos = [{int(item['id']): int(item['quantidade'])} for item in cart_items]
    valor = sum(float(item['preco']) * int(item['quantidade']) for item in cart_items)
    venda = {
        'id': user_id,
        'dia': date_time.day,
        'mes': date_time.month,
        'ano': date_time.year,
        'hora': date_time.strftime("%H:%M"),
        'valor': int(valor * 100),
        'produtos': produtos,
        'usuario': {
            'nome': user['nome'],
            'email': user['email']
        }
    }
    cassandra_session.execute("""
    INSERT INTO venda (id, dia, mes, ano, hora, valor, produtos, usuario)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """, (venda['id'], venda['dia'], venda['mes'], venda['ano'], venda['hora'], venda['valor'], venda['produtos'], venda['usuario']))
    rows = cassandra_session.execute("""
    SELECT usuario['nome'] AS nome, hora, valor / 100 AS valor
    FROM venda
    WHERE dia = %s AND mes = %s AND ano = %s
    """, (date_time.day, date_time.month, date_time.year))
    return [dict(row) for row in rows]


def test_questao_5():
    user_id = 3
    date_time = datetime.now()

    sales = [{"usuario": 'bira@g.com', 'hora': date_time.strftime("%H:%M"), 'valor': 1462.78}]

    assert sales == questao_5(user_id, date_time)


# cassandra_session.shutdown()
# redis_conn.close()