import time
from collections import deque 
import random

def bfs_with_distances(start):
    distances = {start: 0}
    queue = deque([start])
    
    while queue:
        current = queue.popleft()
        current_dist = distances[current]
        
        for neighbor in graph[current]:
            if neighbor not in distances:
                distances[neighbor] = current_dist + 1
                queue.append(neighbor)
    
    return distances

def double_sweep_eccentricity():
    if not graph:
        return 0, 0, 0
    
    nodes = list(graph.keys())
    start_node = random.choice(nodes)
    
    dist1 = bfs_with_distances(start_node)
    u = max(dist1, key=dist1.get)
    min_ecc = dist1[u]
    
    dist2 = bfs_with_distances(u)
    max_ecc = max(dist2.values())
    
    return min_ecc, max_ecc, max_ecc

def min_degree_ordering():
    """Simple min-degree elimination ordering"""
    working_graph = {node: set(neighbors) for node, neighbors in graph.items()}
    ordering = []
    
    while working_graph:
        # Find node with smallest degree
        min_degree = float('inf')
        best_node = None
        
        for node, neighbors in working_graph.items():
            degree = len(neighbors)
            if degree < min_degree:
                min_degree = degree
                best_node = node
        
        ordering.append(best_node)
        
        # Connect all neighbors (make it simplicial)
        neighbors = list(working_graph[best_node])
        for i in range(len(neighbors)):
            for j in range(i + 1, len(neighbors)):
                if neighbors[j] not in working_graph[neighbors[i]]:
                    working_graph[neighbors[i]].add(neighbors[j])
                    working_graph[neighbors[j]].add(neighbors[i])
        
        # Remove the node
        del working_graph[best_node]
        for neighbors in working_graph.values():
            neighbors.discard(best_node)
    
    return ordering

def min_fill_ordering():
    """Min-fill elimination ordering - adds fewest edges when eliminated"""
    working_graph = {node: set(neighbors) for node, neighbors in graph.items()}
    ordering = []
    
    while working_graph:
        min_fill = float('inf')
        best_node = None
        
        for node in working_graph:
            neighbors = working_graph[node]
            fill_edges = 0
            
            # Count edges needed to connect neighbors
            neighbor_list = list(neighbors)
            for i in range(len(neighbor_list)):
                for j in range(i + 1, len(neighbor_list)):
                    if neighbor_list[j] not in working_graph[neighbor_list[i]]:
                        fill_edges += 1
            
            if fill_edges < min_fill:
                min_fill = fill_edges
                best_node = node
        
        ordering.append(best_node)
        
        # Connect neighbors
        neighbors = list(working_graph[best_node])
        for i in range(len(neighbors)):
            for j in range(i + 1, len(neighbors)):
                if neighbors[j] not in working_graph[neighbors[i]]:
                    working_graph[neighbors[i]].add(neighbors[j])
                    working_graph[neighbors[j]].add(neighbors[i])
        
        # Remove node
        del working_graph[best_node]
        for neighbors in working_graph.values():
            neighbors.discard(best_node)
    
    return ordering

def calculate_treewidth(ordering):
    """Calculate treewidth from elimination ordering"""
    working_graph = {node: set(neighbors) for node, neighbors in graph.items()}
    max_clique_size = 0
    
    for node in ordering:
        if node not in working_graph:
            continue
            
        # Clique size = node + its neighbors
        clique_size = 1 + len(working_graph[node])
        max_clique_size = max(max_clique_size, clique_size)
        
        # Connect neighbors
        neighbors = list(working_graph[node])
        for i in range(len(neighbors)):
            for j in range(i + 1, len(neighbors)):
                if neighbors[j] not in working_graph[neighbors[i]]:
                    working_graph[neighbors[i]].add(neighbors[j])
                    working_graph[neighbors[j]].add(neighbors[i])
        
        # Remove node
        del working_graph[node]
        for neighbors in working_graph.values():
            neighbors.discard(node)
    
    return max_clique_size - 1  # treewidth = max clique size - 1

def random_ordering():
    """Random elimination ordering"""
    nodes = list(graph.keys())
    random.shuffle(nodes)
    return nodes

# Read graph data
graph = {}

with open("include/road-minnesota/road-minnesota.mtx", 'r') as f:
    lines = f.readlines()

for line in lines:
    if line.startswith('%') or not line.strip():
        continue
    parts = line.split()
    if len(parts) >= 2:
        u = int(parts[0])
        v = int(parts[1])
        
        if u not in graph:
            graph[u] = set()
        if v not in graph:
            graph[v] = set()
        
        graph[u].add(v)
        graph[v].add(u)

print(f"Graph has {len(graph)} nodes")

# Calculate eccentricity first
min_ecc, max_ecc, diameter = double_sweep_eccentricity()
print(f"Diameter: {diameter}")
print()

# Test different elimination orderings
methods = [
    ('Random', random_ordering),
    ('Min-Degree', min_degree_ordering),
    ('Min-Fill', min_fill_ordering)
]

for method_name, method_func in methods:
    start_time = time.time()
    
    ordering = method_func()
    treewidth = calculate_treewidth(ordering)
    
    elapsed = time.time() - start_time
    
    print(f"{method_name} Ordering:")
    print(f"  Treewidth: {treewidth}")
    print(f"  Time: {elapsed:.4f}s")
    print()