from neo4j import GraphDatabase

# Neo4j 드라이버 설정
uri = "bolt://localhost:7687"  # 또는 적절한 Neo4j URI
driver = GraphDatabase.driver(uri, auth=("neo4j", "koyuko1870!"))

def delete_nodes_in_batches(tx, limit):
    # Cypher 쿼리: 한 번에 지정한 수의 노드를 삭제
    query = f""" 
    MATCH (n)
    WITH n LIMIT {limit}
    DETACH DELETE n
    RETURN count(n)
    """
    result = tx.run(query)
    count = result.single()[0]  # 삭제된 노드 수 반환
    return count

def delete_all_nodes_in_batches(limit=10):
    with driver.session() as session:
        while True:
            # 세션을 열고 트랜잭션 실행
            deleted_count = session.write_transaction(delete_nodes_in_batches, limit)
            if deleted_count == 0:
                # 더 이상 삭제할 노드가 없을 때 중지
                print("모든 노드 삭제 완료.")
                break
            else:
                print(f"{deleted_count}개의 노드가 삭제되었습니다.")

# 한 번에 200개의 노드를 삭제하도록 실행
delete_all_nodes_in_batches(limit=10)

# 드라이버 종료
driver.close()