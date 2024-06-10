import redis
from datetime import datetime, timedelta
import pytest

redis_conn = redis.Redis(
    host="localhost", port=6379,
    username="default",
    password="...",
    decode_responses=True
)


def questao_1(users):
    for user in users:

        user_key = f"user:{user['id']}"

        redis_conn.hmset(user_key, {
            "nome": user["nome"],
            "email": user["email"],
            "token": f"token_{user['id']}"
        })

    return [redis_conn.hgetall(f"user:{user['id']}") for user in users]


def questao_2(interests):
    for interest in interests:
        user_key = f"interests:{interest['usuario']}"
        for topic, score in interest['interesses'].items():
            redis_conn.zadd(user_key, {topic: score})

    return [redis_conn.zrange(user_key, 0, -1, withscores=True) for interest in interests]


def questao_3(posts):
    five_hours_ago = datetime.now() - timedelta(hours=5)
    for post in posts:
        post_key = f"post:{post['id']}"

        redis_conn.hmset(post_key, post)

        redis_conn.expireat(post_key, five_hours_ago.timestamp())

    return [redis_conn.hgetall(f"post:{post['id']}") for post in posts if redis_conn.exists(f"post:{post['id']}")]


def questao_4(user_id):
    interests_key = f"interests:{user_id}"
    interests = redis_conn.zrange(interests_key, 0, -1, withscores=True)
    posts_scores = {}

    for post_key in redis_conn.scan_iter("post:*"):
        post_data = redis_conn.hgetall(post_key)
        post_keywords = post_data['palavras_chave'].split(", ")
        post_score = sum(score for keyword, score in interests if keyword in post_keywords)
        if post_score > 0:
            posts_scores[post_data['conteudo']] = post_score

    return [post for post, _ in sorted(posts_scores.items(), key=lambda item: item[1], reverse=True)]


def questao_5(user_views, user_id):
    for view in user_views:
        user_key = f"views:{view['usuario']}"
        redis_conn.sadd(user_key, *view['visualizado'])

    seen_posts = redis_conn.smembers(f"views:{user_id}")
    all_posts = [redis_conn.hgetall(key) for key in redis_conn.scan_iter("post:*")]
    unseen_posts = [post['conteudo'] for post in all_posts if post['id'] not in seen_posts]

    return unseen_posts


def test_questao_1():
    users = [
        {"id": '1', "nome": "Serafim Amarantes", "email": "samarantes@g.com"},
        {"id": '2', "nome": "Tamara Borges", "email": "tam_borges@g.com"},
        {"id": '3', "nome": "Ubiratã Carvalho", "email": "bira@g.com"},
        {"id": '4', "nome": "Valéria Damasco", "email": "valeria_damasco@g.com"}
    ]

    assert users == sorted(questao_1(users), key=lambda d: d['id'])


def test_questao_2():
    interests = [
        {"usuaruo":1, "interesses": [{"futebol":0.855}, {"pagode":0.765}, {"engraçado":0.732}, {"cerveja":0.622}, {"estética":0.519}]},
        {"usuaruo":2, "interesses": [{"estética":0.765}, {"jiujitsu":0.921}, {"luta":0.884}, {"academia":0.541}, {"maquiagem":0.658}]},
        {"usuaruo":3, "interesses": [{"tecnologia":0.999}, {"hardware":0.865}, {"games":0.745}, {"culinária":0.658}, {"servers":0.54}]},
        {"usuaruo":4, "interesses": [{"neurociências":0.865}, {"comportamento":0.844}, {"skinner":0.854}, {"laboratório":0.354}, {"pesquisa":0.428}]}
    ]

    output = [[('estética', 0.519), ('cerveja', 0.622), ('engraçado', 0.732), ('pagode', 0.765), ('futebol', 0.855)], [('laboratório', 0.354), ('pesquisa', 0.428), ('comportamento', 0.844), ('skinner', 0.854), ('neurociências', 0.865)], [('servers', 0.54), ('culinária', 0.658), ('games', 0.745), ('hardware', 0.865), ('tecnologia', 0.999)], [('academia', 0.541), ('maquiagem', 0.658), ('estética', 0.765), ('luta', 0.884), ('jiujitsu', 0.921)]]

    assert output == questao_2(interests)


def test_questao_3():

    posts = [
        {"id": '345', "autor":"news_fc@g.com", "data_hora": "2024-06-10 19:51:03", "conteudo": "Se liga nessa lista de jogadores que vão mudar de time no próximo mês!", "palavras_chave": "brasileirao, futebol, cartola, esporte" },
        {"id": '348', "autor":"gastro_pub@g.com", "data_hora": "2024-06-10 19:55:13", "conteudo": "Aprenda uma receita rápida de onion rings super crocantes.", "palavras_chave": "onion rings, receita, gastronomia, cerveja, culinária" },
        {"id": '349', "autor":"make_with_tina@g.com", "data_hora": "2024-06-10 19:56:44", "conteudo": "A dica de hoje envolve os novos delineadores da linha Rare Beauty", "palavras_chave": "maquiagem, estética, beleza, delineador" },
        {"id": '350', "autor":"samarantes@g.com", "data_hora": "2024-06-10 19:56:48", "conteudo": "Eu quando acho a chuteira que perdi na última pelada...", "palavras_chave": "pelada, futebol, cerveja, parceiros" },
        {"id": '351', "autor":"portal9@g.com", "data_hora": "2024-06-10 19:57:02", "conteudo": "No último mês pesquisadores testaram três novos medicamentos para ajudar aumentar o foco.", "palavras_chave": "neurociências, tecnologia, foco, medicamento" },
        {"id": '352', "autor":"meme_e_cia@g.com", "data_hora": "2024-06-10 19:58:33", "conteudo": "Você prefere compartilhar a nossa página agora ou daqui cinco minutos?", "palavras_chave": "entretenimento, engraçado, viral, meme" },
        {"id": '353', "autor":"rnd_hub@g.com", "data_hora": "2024-06-10 19:59:59", "conteudo": "A polêmica pesquisa de V. Damasco sobre ciência do comportamente acaba de ser publicada.", "palavras_chave": "comportamento, ciência, pesquisa, damasco" }
    ]

    assert posts == sorted(questao_3(posts), key=lambda d: d['id'])


def test_questao_4():
    user_id = 3

    output = [
        "No último mês pesquisadores testaram três novos medicamentos para ajudar aumentar o foco.",
        "Aprenda uma receita rápida de onion rings supoer crocantes.",
        "Se liga nessa lista de jogadores que vão mudar de time no próximo mês!",
        "A dica de hoje envolve os novos delineadores da linha Rare Beauty",
        "Eu quando acho a chuteira que perdi na última pelada...",
        "Você prefere compartilhar a nossa página agora ou daqui cinco minutos?",
        "A polêmica pesquisa de V. Damasco sobre ciência do comportamente acaba de ser publicada."
    ]

    assert output == questao_4(user_id)


def test_questao_5():
    user_id = 3
    user_views = [
        {"usuario":1, "visualizado": [345,350,353]},
        {"usuario":2, "visualizado": [350,351]},
        {"usuario":3, "visualizado": [345,351,352,353]},
        {"usuario":4, "visualizado": []}
    ]

    output = [
        "Aprenda uma receita rápida de onion rings supoer crocantes.",
        "A dica de hoje envolve os novos delineadores da linha Rare Beauty",
        "Eu quando acho a chuteira que perdi na última pelada..."
    ]

    assert output == questao_5(user_views, user_id)
