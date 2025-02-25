from rdflib import Graph, RDF
from py2neo import Graph as Neo4jGraph, Node, Relationship
from tqdm import tqdm

# Neo4j 연결 설정
neo4j_uri = "bolt://localhost:7687"
neo4j_user = "neo4j"
neo4j_password = "koyuko1870!"

# RDF 데이터 로드
rdf_file_path = "../model_data.ttl"
g = Graph()
g.parse(rdf_file_path, format="turtle")

# Neo4j 그래프 연결
graph = Neo4jGraph(neo4j_uri, auth=(neo4j_user, neo4j_password))

# RDF 트리플을 Neo4j로 저장
nodes_cache = {}  # 노드 캐시
triples = list(g)

for subj, pred, obj in tqdm(triples, desc="Processing RDF triples", unit="triple"):
    # 서브젝트 노드 생성
    if str(subj) not in nodes_cache:
        node_labels = set()  # 노드 라벨을 담는 집합
        for _, p, o in g.triples((subj, RDF.type, None)):
            node_labels.add(str(o).split("/")[-1])  # 타입에서 마지막 부분 추출

        # 라벨이 없는 경우 기본 라벨로 설정
        if not node_labels:
            node_labels.add("Resource")

        # 노드 생성
        subject_node = Node(*node_labels, uri=str(subj))  # 라벨 추가
        nodes_cache[str(subj)] = subject_node
        graph.merge(subject_node, list(node_labels)[0], "uri")  # 첫 번째 라벨로 병합

    subject_node = nodes_cache[str(subj)]

    # koai:name 및 rdf:type 처리
    if str(pred) == "http://www.w3.org/1999/02/22-rdf-syntax-ns#type":
        # rdf:type 정보를 노드의 라벨로 처리
        node_type = str(obj).split("/")[-1]
        if node_type not in subject_node.labels:
            subject_node.add_label(node_type)
        graph.push(subject_node)
        continue
    elif str(pred).endswith("name"):
        # koai:name을 속성으로 추가
        subject_node["name"] = str(obj)
        graph.push(subject_node)
        continue

    # 오브젝트 노드 생성
    if str(obj) not in nodes_cache:
        object_labels = set()  # 오브젝트 라벨을 담는 집합
        for _, p, o in g.triples((obj, RDF.type, None)):
            object_labels.add(str(o).split("/")[-1])  # 타입에서 마지막 부분 추출
        # 라벨이 없는 경우 기본 라벨로 설정
        if not object_labels:
            object_labels.add("Resource")

        # 노드 생성
        object_node = Node(*object_labels, uri=str(obj))  # 라벨 추가
        nodes_cache[str(obj)] = object_node
        graph.merge(object_node, list(object_labels)[0], "uri")  # 첫 번째 라벨로 병합
    else:
        object_node = nodes_cache[str(obj)]

    # 서브젝트와 오브젝트 사이의 관계 생성
    relationship_name = str(pred).split("/")[-1]  # 관계 이름 추출
    relationship = Relationship(subject_node, relationship_name, object_node)
    graph.merge(relationship)