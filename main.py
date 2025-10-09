import time
from vertex import Vertex
from collections import deque 

def bfs(start: Vertex):
    visited = set()
    queue = deque([start])
    order = []
    
    while queue:
        node = queue.popleft()
        
        if node not in visited:
            visited.add(node)
            order.append(node.key)
            
            for neighbor in node.neighbors:
                if neighbor not in visited:
                    queue.append(neighbor)
    
    return order

'''
parses .mtx file and returns adjacency matrix 
'''
def parse_mtx(file_path: str, start_line: int = 16):
    
    adjacency_matrix = {}
    
    with open(file_path, 'r') as file:
        for line in file:
            if not line.strip() or line.startswith('%'):
                continue
            
            split = line.strip().split()
            if len(split) == 3:
                continue
            
            u, v = map(int, line.split())
            
            if u not in adjacency_matrix:
                adjacency_matrix[u] = {}
                
            adjacency_matrix[u][v] = 1
    
    return adjacency_matrix


def generate_graph(adjacency_matrix: dict):
    seen = {}
    
    for u, v in adjacency_matrix.items():
        if not u in seen:
            print(u)
            seen[u] = Vertex(key=str(u))
        
        seen[u].neighbors.append(Vertex(key=str(v)))
    
    return seen
            

if __name__ == "__main__":
    start_time = time.time()

    mn_mtx = parse_mtx("include/road-minnesota/road-minnesota.mtx")
    graph = generate_graph(mn_mtx)
    
    start_key = list(graph.keys())[0]
    bfs_result = bfs(graph[start_key])

    end_time = time.time()

    elapsed_time = end_time - start_time
    print(f"Total execution time: {elapsed_time: .4f} seconds")
    print(f"BFS found {len(bfs_result)} nodes")