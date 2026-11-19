import ssl

import certifi
from neo4j import GraphDatabase

from . import graph_queries

class Neo4jClient:
    def __init__(
        self,
        uri: str,
        username: str,
        password: str,
        ca_bundle: str | None = None
    ):
        config = {}
        driver_uri = uri

        if uri.lower().startswith("neo4j+s://"):
            bundle = ca_bundle or certifi.where()
            ssl_context = ssl.create_default_context(cafile=bundle)
            driver_uri = "neo4j://" + uri[len("neo4j+s://"):]
            config["encrypted"] = True
            config["ssl_context"] = ssl_context
        elif uri.lower().startswith("bolt+s://"):
            bundle = ca_bundle or certifi.where()
            ssl_context = ssl.create_default_context(cafile=bundle)
            driver_uri = "bolt://" + uri[len("bolt+s://"):]
            config["encrypted"] = True
            config["ssl_context"] = ssl_context

        self.driver = GraphDatabase.driver(
            driver_uri,
            auth=(username, password),
            **config
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
                graph_queries.CREATE_SIDE_EFFECT_CONSTRAINT
            )
            session.run(
                graph_queries.CREATE_DISEASE_CONSTRAINT
            )
            # session.run(
            #     graph_queries.CREATE_PAPER_CONSTRAINT
            # )
        


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