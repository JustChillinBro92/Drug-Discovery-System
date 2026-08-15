from neo4j import GraphDatabase

from . import graph_queries

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
        
    def initialize_schema(self):

        with self.driver.session() as session:

            session.run(
                graph_queries.CREATE_COMPOUND_CONSTRAINT
            )

            session.run(
                graph_queries.CREATE_PROTEIN_CONSTRAINT
            )

            session.run(
                graph_queries.CREATE_DISEASE_CONSTRAINT
            )

            session.run(
                graph_queries.CREATE_PAPER_CONSTRAINT
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