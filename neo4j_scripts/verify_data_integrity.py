from rdflib import Graph, RDF
from py2neo import Graph as Neo4jGraph, Node, Relationship
from tqdm import tqdm

# Neo4j 연결 설정
neo4j_uri = "bolt://localhost:7687"
neo4j_user = "neo4j"
neo4j_password = "koyuko1870!"

# RDF 데이터 로드
rdf_file_path = "./AIrdf.ttl"
g = Graph()
g.parse(rdf_file_path, format="turtle")

# Neo4j 그래프 연결
graph = Neo4jGraph(neo4j_uri, auth=(neo4j_user, neo4j_password))

# 저장된 데이터 확인을 위한 쿼리 작성 및 실행
query = """
MATCH (n)
RETURN n
"""

result = graph.run(query)

# 결과 출력
for record in result:
    print(record)