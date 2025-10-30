from collections import deque
import random
import time

'''g: graph represented by dict of type [int, list[int]], with each key being a vertex u in g and each value the neighbors of u. 
returns traversal, dict [key, value] denoting distance start vertex is [value] distance away from vertex [key]'''
def bfs(g: dict[int, list[int]], start_key: int, goal_key: int = -1):
    visited = set()
    queue = deque([start_key])

    order = []
    distances: dict[int, int] = {start_key: 0}
    
    while queue:
        vertex = queue.popleft()
        
        if vertex not in visited:
            visited.add(vertex)
            order.append(vertex)

            current_distance = distances[vertex]

            if goal_key != -1 and goal_key == vertex:
                return order, distances

            for neighbor in g[vertex]:
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

def estimate_diameter(g: dict[int, list[int]], samples=10) -> int:
    vertices = list(g.keys())
    
    upper_bound = 0
    
    for _ in range(samples):
        start = random.choice(vertices)
        
        ecc = max(bfs(g, start)[1].values())
        
        if ecc > upper_bound:
            upper_bound = ecc
            
    return upper_bound // 2, upper_bound

# ask about formal defn for tree decomposition and to clarify this stuff
def naive_elim_ordering(g: dict[int, list[int]]):
    n = len(g)
    vertices = list(g.keys())
    ordering = []
    remaining = set(vertices)
    
    while remaining:
        v = min(remaining)
        ordering.append(v)
        remaining.remove(v)
        
        neighbors = []
        for u in g[v]:
            if u in remaining: neighbors.append(u)
            
        for i in range(len(neighbors)):
            for j in range (i+1, len(neighbors)):
                u, w = neighbors[i], neighbors[j]
                if w not in g[u] or u not in g[w]:
                    g[u].append(w)
                    g[w].append(u)
    
    return ordering

# generates tree decomposition (as dict[list[int], list[int]] similar to main graph) from elimination ordering   
# for each node v in the decomposition, v and its neighbors are added as a vertex to the graph 
def naive_tree_decomp(ordering, g: dict[int, list[int]]) -> dict[list[int], list[int]]:
    tree: dict[list[int], list[int]] = dict()
    
    for vertex in ordering:
        tree[g[vertex]] = []
        
        # non-n^2 update edges? 
        # reading suggests i should check every key k in tree such that, if k contains vertex, edge should be added between tree[g[vertex]] and tree[k]?
        

def parse_mtx(file_path: str):
    adjacency_dict: dict[int, list[int]] = {}
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

if __name__ == "__main__":
    usa_path = "include/road-road-usa/road-road-usa.mtx"
    mn_path = "include/road-minnesota/road-minnesota.mtx"

    start_time = time.time()
    graph = parse_mtx(mn_path)
    end_time = time.time()

    parse_time = end_time - start_time

    print("Graph parse time: " + str(parse_time))

    start_time = time.time()
    bfs_result = bfs(graph[0], graph[1])
    end_time = time.time()

    bfs_time = end_time - start_time

    print("BFS time: " + str(bfs_time))
    print("BFS size: " + str(len(bfs_result[0])))
    print("Graph diameter: " + str(estimate_diameter(graph[0], samples=100)))
    print("Total time: " + str(parse_time + bfs_time))