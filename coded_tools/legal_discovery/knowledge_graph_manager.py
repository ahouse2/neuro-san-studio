import os

import logging
from typing import Any, Dict, List

from neo4j import GraphDatabase
from neuro_san.interfaces.coded_tool import CodedTool
from pyvis.network import Network


class KnowledgeGraphManager(CodedTool):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        uri = os.environ.get("NEO4J_URI", "bolt://localhost:7687")
        user = os.environ.get("NEO4J_USER", "neo4j")
        password = os.environ.get("NEO4J_PASSWORD", "password")
        self._fallback_graph: Dict[int, Dict[str, Any]] = {}
        self._next_id = 1
        try:
            self.driver = GraphDatabase.driver(uri, auth=(user, password))
            # Verify connection
            with self.driver.session() as session:
                session.run("RETURN 1")
        except Exception as exc:  # pragma: no cover - connection may fail in tests
            logging.warning("Neo4j unavailable, falling back to in-memory graph")
            self.driver = None
            self._exception = exc

    def close(self):
        if self.driver:
            self.driver.close()

    def run_query(self, query: str, parameters: dict = None) -> list:
        """
        Runs a Cypher query against the Neo4j database.

        :param query: The Cypher query to run.
        :param parameters: A dictionary of parameters for the query.
        :return: A list of records returned by the query.
        """
        if self.driver:
            try:
                with self.driver.session() as session:
                    result = session.run(query, parameters)
                    return [record for record in result]
            except Exception as exc:
                raise RuntimeError("Neo4j query failed") from exc
        # Minimal fallback parser for tests
        if (
            query.strip().startswith("MATCH (n) WHERE id(n) = $node_id DETACH DELETE n")
            and parameters
            and "node_id" in parameters
        ):
            self._fallback_graph.pop(parameters["node_id"], None)
            return []
        raise RuntimeError("Query not supported in fallback mode")

    def create_node(self, label: str, properties: dict) -> int:
        """
        Creates a new node in the knowledge graph.

        :param label: The label for the new node.
        :param properties: A dictionary of properties for the new node.
        :return: The ID of the newly created node.
        """
        if self.driver:
            query = f"CREATE (n:{label} $props) RETURN id(n)"
            result = self.run_query(query, {"props": properties})
            return result[0][0]

        node_id = self._next_id
        self._next_id += 1
        self._fallback_graph[node_id] = {"label": label, **properties}
        return node_id

    def create_relationship(
        self, start_node_id: int, end_node_id: int, relationship_type: str, properties: dict = None
    ):
        """
        Creates a new relationship between two nodes in the knowledge graph.

        :param start_node_id: The ID of the start node.
        :param end_node_id: The ID of the end node.
        :param relationship_type: The type of the new relationship.
        :param properties: A dictionary of properties for the new relationship.
        """
        query = (
            f"MATCH (a), (b) "
            f"WHERE id(a) = $start_node_id AND id(b) = $end_node_id "
            f"CREATE (a)-[r:{relationship_type} $props]->(b)"
        )
        if self.driver:
            self.run_query(
                query,
                {
                    "start_node_id": start_node_id,
                    "end_node_id": end_node_id,
                    "props": properties or {},
                },
            )
            return

        rel = {
            "start": start_node_id,
            "end": end_node_id,
            "type": relationship_type,
            "properties": properties or {},
        }
        self._fallback_graph.setdefault("_rels", []).append(rel)

    def get_node(self, node_id: int) -> dict:
        """
        Retrieves a node from the knowledge graph.

        :param node_id: The ID of the node to retrieve.
        :return: A dictionary representing the node.
        """
        if self.driver:
            query = "MATCH (n) WHERE id(n) = $node_id RETURN n"
            result = self.run_query(query, {"node_id": node_id})
            return dict(result[0]["n"]) if result else None

        node = self._fallback_graph.get(node_id)
        return node.copy() if node else None

    def get_relationships(self, node_id: int) -> list:
        """
        Retrieves all relationships for a given node.

        :param node_id: The ID of the node.
        :return: A list of dictionaries representing the relationships.
        """
        if self.driver:
            query = "MATCH (n)-[r]->() WHERE id(n) = $node_id RETURN r"
            result = self.run_query(query, {"node_id": node_id})
            return [dict(record["r"]) for record in result]

        rels = self._fallback_graph.get("_rels", [])
        return [r for r in rels if r["start"] == node_id]

    def export_graph(self, output_path: str = "graph.html") -> str:
        """
        Exports the entire graph as an interactive HTML file.

        :param output_path: The path to save the HTML file to.
        :return: The path to the generated HTML file.
        """
        if self.driver:
            nodes_query = "MATCH (n) RETURN id(n) as id, labels(n) as labels, properties(n) as properties"
            nodes_result = self.run_query(nodes_query)

            relationships_query = (
                "MATCH ()-[r]->() RETURN id(startNode(r)) as source, id(endNode(r)) as target, "
                "type(r) as type, properties(r) as properties"
            )
            relationships_result = self.run_query(relationships_query)
        else:
            nodes_result = [
                {"id": node_id, "labels": [data.get("label", "")], "properties": {k: v for k, v in data.items() if k != "label"}}
                for node_id, data in self._fallback_graph.items()
                if isinstance(node_id, int)
            ]
            relationships_result = self._fallback_graph.get("_rels", [])

        net = Network(notebook=True)
        for record in nodes_result:
            node_id = record["id"]
            labels = record["labels"]
            properties = record["properties"]
            title = "\\n".join([f"{k}: {v}" for k, v in properties.items()])
            net.add_node(node_id, label=labels[0], title=title)

        for record in relationships_result:
            source = record.get("source") or record.get("start")
            target = record.get("target") or record.get("end")
            rel_type = record["type"]
            properties = record.get("properties", {})
            title = "\\n".join([f"{k}: {v}" for k, v in properties.items()])
            net.add_edge(source, target, label=rel_type, title=title)

        net.save_graph(output_path)
        return output_path
