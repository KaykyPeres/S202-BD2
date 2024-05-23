class Query:
    def __init__(self, database):
        self.db = database

    def renzo(self):
        query = "MATCH (t:Teacher) WHERE t.name = 'Renzo' RETURN t.ano_nasc AS ano_nascimento, t.cpf AS cpf"
        results = self.db.execute_query(query)
        return [(result["ano_nascimento"], result["cpf"]) for result in results]

    def starts_with_m(self):
        query = "MATCH (t:Teacher) WHERE t.name STARTS WITH 'M' RETURN t.name AS name, t.cpf AS cpf"
        results = self.db.execute_query(query)
        return [(result["name"], result["cpf"]) for result in results]

    def cities(self):
        query = "MATCH (c:City) RETURN c.name AS name_cities"
        results = self.db.execute_query(query)
        return [result["name_cities"] for result in results]

    def schools(self):
        query = "MATCH (s:School) WHERE s.number >= 150 AND s.number <= 550 RETURN s.name AS name, s.address AS endereco, s.number AS numero"
        results = self.db.execute_query(query)
        return [(result["name"], result["endereco"], result["numero"]) for result in results]

    def ano_nasc(self):
        query = "MATCH (t:Teacher) RETURN MAX(t.ano_nasc) AS mais_jovem, MIN(t.ano_nasc) AS mais_velho"
        results = self.db.execute_query(query)
        return [(result["mais_jovem"], result["mais_velho"]) for result in results]

    def population(self):
        query = "MATCH (c:City) RETURN AVG(c.population) AS media_populacao"
        results = self.db.execute_query(query)
        return [result["media_populacao"] for result in results]

    def cep(self):
        query = "MATCH (c:City) WHERE c.cep = '37540-000' RETURN REPLACE(c.name, 'a', 'A') AS city_name"
        results = self.db.execute_query(query)
        return [result["city_name"] for result in results]

    def teacher(self):
        query = "MATCH (t:Teacher) RETURN SUBSTRING(t.name, 2, 1) AS teacher"
        results = self.db.execute_query(query)
        return [result["teacher"] for result in results]