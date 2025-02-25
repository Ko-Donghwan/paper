from neo4j import GraphDatabase

uri = "bolt://localhost:7687"

def check_server_status(uri):
    try:
        driver = GraphDatabase.driver(uri, auth=("neo4j", "koyuko1870!"))
        with driver.session() as session:
            result = session.run("MATCH (n) RETURN count(n)")
            print(f"Number of nodes: {result.single()[0]}")
        print("Neo4j server is running!")
    except Exception as e:
        print(f"Error connecting to Neo4j server: {e}")
    finally:
        if 'driver' in locals():
            driver.close()

check_server_status(uri)