from collections import deque
import time 


def bfs(g: dict[int, list[int]], start_key: int, goal_key: int = -1):
    visited = set()
    queue = deque([start_key])
    order = []
    
    while queue:
        node = queue.popleft()
        
        if node not in visited:
            visited.add(node)
            order.append(node)

            if goal_key != -1 and goal_key == node:
                return order
            
            if node in g:
                for neighbor in g[node]:
                    if neighbor not in visited:
                        queue.append(neighbor)
    
    return order

def parse_mtx(file_path: str):
    
    adjacency_dict = {}
    start_key = None
    
    with open(file_path, 'r') as file:
        for line in file:
            if not line.strip() or line.startswith('%'):
                continue
            
            split = line.strip().split()
            if len(split) >= 3:
                continue
            
            u, v = map(int, line.split())
            if start_key is None:
                start_key = u
            
            if u not in adjacency_dict:
                adjacency_dict[u] = []

            if v not in adjacency_dict:
                adjacency_dict[v] = []
                                
            adjacency_dict[u].append(v)
            adjacency_dict[v].append(u)

    # returns graph + first vertex
    return adjacency_dict, start_key

# record time to run bfs on each of the different graphs 
# find diameter of graph from bfs tree (longest path) 

if __name__ == "__main__":
    usa_path = "include/road-road-usa/road-road-usa.mtx"
    mn_path = "include/road-minnesota/road-minnesota.mtx"

    start_time = time.time()
    graph = parse_mtx(usa_path)
    end_time = time.time()

    parse_time = end_time - start_time

    print("Graph parse time: " + str(parse_time))

    start_time = time.time()
    bfs = bfs(graph[0], graph[1])
    end_time = time.time()

    bfs_time = end_time - start_time

    print("BFS time: " + str(bfs_time))
    print("BFS size: " + str(len(bfs)))
    print("Total time: " + str(parse_time + bfs_time))