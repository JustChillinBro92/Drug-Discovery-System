from neo4j import GraphDatabase


class Neo4jClient:
    def __init__(
        self,
        uri: str,
        username: str,
        password: str
    ):
        self.driver = GraphDatabase.driver(
            uri,
            auth=(username, password)
        )


    def execute_query(
        self,
        query: str,
        parameters: dict | None = None
    ):
        with self.driver.session() as session:

            return session.run(
                query,
                parameters or {}
            ).data()


    def close(self):
        self.driver.close()


neo4j_client = None