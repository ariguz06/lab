from collections import deque
import time

'''g: graph represented by dict of type [int, list[int]], with each key being a vertex u in g and each value the neighbors of u'''
def bfs(g: dict[int, list[int]], start_key: int, goal_key: int = -1) -> ([int], dict[int, int]):
    visited = set()
    queue = deque([start_key])

    order = []
    distances: dict[int, int] = {start_key: 0}
    
    while queue:
        node = queue.popleft()
        
        if node not in visited:
            visited.add(node)
            order.append(node)

            current_distance = distances[node]

            if goal_key != -1 and goal_key == node:
                return order, distances

            for neighbor in g[node]:
                if neighbor not in visited:
                    distances[neighbor] = current_distance + 1
                    queue.append(neighbor)
    
    return order, distances


def diameter(g: dict[int, list[int]], sample_size=100) -> int:
    d = 0
    vertices = list(g.keys())

    for i in range(min(len(g), sample_size)):

        start_vertex = vertices[i]

        dists = bfs(g=g, start_key=start_vertex)[1]

        if max(dists.values()) > d:
            d = max(dists.values())

    return d


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
    bfs_result = bfs(graph[0], graph[1])
    end_time = time.time()

    bfs_time = end_time - start_time

    print("BFS time: " + str(bfs_time))
    print("BFS size: " + str(len(bfs_result[0])))
    print("Graph diameter: " + str(diameter(graph[0], 1)))
    print("Total time: " + str(parse_time + bfs_time))