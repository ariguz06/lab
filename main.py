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
"""
Distance preserved vertex eilimination (algoirithm 2)
H: current weighted graph as adjacency dict: H[u][w] = weight(u,w)
v: vertext to eliminate

Adds/updates shortest edges between neighbors of v
Removes v from H
"""
def dp_vertex_elim(H: dict[int, dict[int, int]], v: int):
    if v not in H:
        return
    
    neighbors = list(H[v].keys())

    #for all pairs (u,w) in N(v), add/relact shortcut edge u-w
    for i in range(len(neighbors)):
        u = neighbors[i]
        for j in range(i + 1, len(neighbors)):
            w = neighbors[j]

            new_w = H[v][u] + H[v][w]  #adds weight(u,v) and weight(v,w)

            #if edge (u,w) doesnt exist or fond shorter path, update
            if w not in H[u] or new_w < H[u][w]:
                H[u][w] = new_w
                H[w][u] = new_w
    
    #removes v from H
    for u in neighbors:
        if v in H[u]:
            del H[u][v]
    del H[v]


"""
Implementation of Algorithm 3: DPTreeDecomposition(G(V,E)) for an unweighted, undirected graph given as an adjacency list

Input: original adjacency list (unweighted, undirected)
Outputs:
    bags: dict[int, list[int]]
        X(v) for each center vertex c (bag: [V] + neighbors at elimination time)
    lambdas: dict[int, list[int]]
        lambda-array for each v, aligned with bags[v], where lambdas[v][j] = distance from v to bags[v][j]
        For j == 0, this is always 0 (distance from v to itself)
    parent: dict[int, int | None]
        Parent center of X(v) in the tree decomposition or None if root
    phi: dict[int, int]
        Elimination order index phi(v): the i used in Algorithm 3
"""
def naive_dp_tree_decomposition(g: dict[int, list[int]]):
    
    #Copying G into weighted form H with initial weight 1 for each edge
    H: dict[int, dict[int,int]] = {}

    for u, nbrs in g.items():
        if u not in H:
            H[u] = {}
        for v in nbrs:
            if v not in H:
                H[v] = {}

            if v not in H[u] or H[u][v] > 1:
                H[u][v] = 1
                H[v][u] = 1
    
    #initializing containers
    bags: dict[int, list[int]] = {}
    lambdas: dict[int, list[int]] = {}
    phi: dict[int, int] = {}

    #copy vertex set to avoid issues when mutating H
    vertices = list(H.keys())
    n = len(vertices)

    #main eliminatiin loop
    for i in range(1, n + 1):
        #pick vertext with smallest degree in H
        v = min(H.keys(), key=lambda u: len(H[u]))

        #create star X(v) = {v} U N(v, H)
        neighbors = list(H[v].keys())
        bag = [v] + neighbors

        lam = [0]
        for u in neighbors:
            lam.append(H[v][u])

        bags[v] = bag
        lambdas[v] = lam
        phi[v] = i

        #eliminate v with DPVertextElimination
        dp_vertex_elim(H, v)


    #Assign parents. Parent of X(v) is X(u) where u in X(v)\{v} has smallest phi(u)
    parent: dict[int, int | None] = {v: None for v in bags.keys()}

    for v, bag in bags.items():
        if len(bag) > 1:
            candidates = [u for u in bag if u != v]
            #All candidates should have phi[u] already set
            u_parent = min(candidates, key=lambda x:phi[x])
            parent[v] = u_parent
        else: 
            parent[v] = None    # Leaf or possible root

    #Sort vertices in each bag in decreasing order of phi and keep lambdas aligned with bags
    for v in bags.keys():
        bag = bags[v]
        lam = lambdas[v]
        paired = list(zip(bag, lam))
        #sort be decreasing phi; -1 if not in phi (shouldnt happen)
        #paired.sort(key=lambda p: -phi.get(p[0], -1))

        bags[v] = [p[0] for p in paired]
        lambdas[v] = [p[1] for p in paired]
    
    return bags, lambdas, parent, phi

"""
Builds X(v).anc for each v (top-down pass)
anc[v] is the list of centers on the path root -> v
"""
def build_ancestors(bags, parent):
    anc = {}
    #Root has parent[v] == None. Can be multiple roots, we handle all
    def get_anc(v):
        if v in anc:
            return anc[v]
        if parent[v] is None:
            anc[v] = [v]
        else:
            anc[v] = get_anc(parent[v]) + [v]
        return anc[v]
    
    for v in bags.keys():
        get_anc(v)
    
    return anc
"""
Produces:
    anc[v] = ancestor chain
    pos[v] = position of each element of X(v) insice anc[v]
    dis[v] = distance array for shortest-path indexing
"""
def naive_H2H(bags, lambdas, parent, phi):
    anc = build_ancestors(bags, parent)
    pos = {}
    dis = {}

    #verticies in increasing phi (root to leaves) because parents have smaller phi than children
    verticies_ordered = sorted(phi.keys(), key=lambda x: phi[x])

    for v in verticies_ordered:
        bag = bags[v]
        lam = lambdas[v]
        anc_v = anc[v]

        #Build pos[v]
        pos_v = []
        for x in bag:
            if x in anc_v:
                pos_v.append(anc_v.index(x))
            else:
                pos_v.append(len(anc_v) - 1) #shouldnt happen in valid DP decomposition
        pos[v] = pos_v

        #Build dis[v]: dis[v][i] = shortest distance from v to anc[v][i]
        L = len(anc_v)
        dis_v = [float('inf')] * L

        dis_v[L-1] = 0  #last element in anc[v] is v itself

        for i in range(L-1):
            best = float('inf')

            for j in range(len(bag)):
                x_j = bag[j]
                lam_j = lam[j]
                pos_j = pos_v[j]

                #Case 1: pos_j > i -> dis(x_j, anc[i]) = dis[x_j][i]
                if pos_j > i:
                    if x_j in dis and i < len(dis[x_j]):
                        dist_xj_anci = dis[x_j][i]
                    else:
                        dist_xj_anci = float('inf')
                #Case 2: pos_j <= i -> dis(x_j, anc[i]) = dis[anc[i]][pos_j]
                else:
                    a = anc_v[i]
                    if a in dis and pos_j < len(dis[a]):
                        dist_xj_anci = dis[a][pos_j]
                    else:
                        dist_xj_anci = float('inf')
                
                candidate = lam_j + dist_xj_anci
                if candidate < best:
                    best = candidate

            dis_v[i] = best

        dis[v] = dis_v

    return anc, pos, dis



if __name__ == "__main__":
    usa_path = "include/road-road-usa/road-road-usa.mtx"
    mn_path = "include/road-minnesota/road-minnesota.mtx"

    start_time = time.time()
    graph, start_vertex = parse_mtx(mn_path)
    end_time = time.time()

    parse_time = end_time - start_time

    print("Graph parse time: " + str(parse_time))

    start_time = time.time()
    bfs_result = bfs(graph, start_vertex)
    end_time = time.time()

    bfs_time = end_time - start_time

    print("BFS time: " + str(bfs_time))
    print("BFS size: " + str(len(bfs_result[0])))
    print("Graph diameter: " + str(estimate_diameter(graph, samples=100)))

    td_start = time.time()
    bags, lambdas, parent, phi = naive_dp_tree_decomposition(graph)
    anc, pos, dis = naive_H2H(bags, lambdas, parent, phi)
    td_end = time.time()

    print("DP Tree Decomposition time: ", td_end - td_start)
    print("Number of bags: ", len(bags))

    if start_vertex in bags:
        print("bag[start]      =", bags[start_vertex])
        print("lambda[start]   =", lambdas[start_vertex])
        print("anc[start]      =", anc[start_vertex])
        print("pos[start]      =", pos[start_vertex])
        print("dis[start]      =", dis[start_vertex])
    else:
        print("Start vertex not found in bags (this means it was eliminated but not stored).")

    # Compute depth of the DP decomposition tree
    tree_depth = max(len(anc[v]) for v in anc)
    print("\nDP-tree max depth:", tree_depth)

    # Maximum dis-array length (largest ancestor chain)
    max_dis_len = max(len(dis[v]) for v in dis)
    print("Max dis[v] array length:", max_dis_len)

    # Maximum bag size (width-related signal)
    max_bag = max(len(bags[v]) for v in bags)
    print("Max bag size:", max_bag)

    # Maximum lambda size
    max_lambda = max(len(lambdas[v]) for v in lambdas)
    print("Max lambda size:", max_lambda)

