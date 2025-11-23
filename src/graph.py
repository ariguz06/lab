import math
from collections import deque
import random
from src.tree_decomp import TreeDecomp

class Graph:
    
    def __init__(self, adjacency_dict: dict[int, list[int]]=None, file_path=None):

        self._hash = None
        self.pos: list[int] = []
        self.dis: list[int] = []
        
        # Used for H2H
        self.root: int = 0

        if adjacency_dict:
            self.g: dict[int, list[int]] = adjacency_dict
            self.start_key = next(iter(adjacency_dict.keys()))
        elif file_path:
            self.g, self.start_key = self.parse_mtx(file_path)
        else:
            self.g = {}
            self.start_key = None
            
        self.edges = self.get_edges(adj=self.g)
            
    def __eq__(self, other):
        if not isinstance(other, Graph): return False
        return self.g == other.g
    
    def __hash__(self):
        if self._hash is None:
            frozen_adj = tuple(
                (v, frozenset(neigh)) for v, neigh in self.g.items()
            )
            self._hash = hash(frozen_adj)
        return self._hash


    @staticmethod
    def get_edges(adj: dict[int, list[int]]) -> set[tuple]:
        edges = set()
        
        for k, v in adj.items():
            for vertex in v:
                edges.add((k, vertex))
        
        return edges

    @staticmethod
    def min_degree(h: dict[int, list[int]]) -> int:
        min_k = list(h.keys())[0]
        for k, v in h.items():
            if len(v) < len(h[min_k]):
                min_k = k
        
        return min_k

    @staticmethod
    def parse_mtx(file_path: str):
        adjacency_dict = {}
        start_key = None

        with open(file_path, 'r') as file:
            for line in file:
                if not line.strip() or line.startswith('%'):
                    continue

                parts = line.strip().split()
                if len(parts) != 2:
                    continue

                u, v = map(int, parts)
                if start_key is None:
                    start_key = u

                adjacency_dict.setdefault(u, []).append(v)
                adjacency_dict.setdefault(v, []).append(u)

        return adjacency_dict, start_key

    def bfs(self, start_key: int, goal_key: int = -1):
        visited = set()
        queue = deque([start_key])
        order = []
        distances = {start_key: 0}

        while queue:
            vertex = queue.popleft()
            if vertex not in visited:
                visited.add(vertex)
                order.append(vertex)

                current_distance = distances[vertex]

                if goal_key != -1 and goal_key == vertex:
                    return order, distances

                for neighbor in self.g[vertex]:
                    if neighbor not in visited:
                        distances[neighbor] = current_distance + 1
                        queue.append(neighbor)

        return order, distances
    
    '''Returns adjacency dict consisting of vertex and its neighbors as vertices, edges from vertex to its neighbors as edges'''
    @staticmethod
    def star(adj: dict[int, list[int]], vertex: int) -> dict[int, list[int]]:
        if not vertex in adj:
            return {}
        
        return {vertex: adj[vertex]}

    def neighbors(self, vertex: int) -> list[int]:
        return self.star(self.g, vertex)

    def diameter(self, sample_size=100):
        d = 0
        vertices = list(self.g.keys())

        for i in range(min(len(vertices), sample_size)):
            start_vertex = vertices[i]
            dists = self.bfs(start_vertex)[1]
            d = max(d, max(dists.values()))
        return d
    
    def estimate_diameter(self, samples=10):
        vertices = list(self.g.keys())
        
        upper_bound = math.inf
        lower_bound = 0

        for _ in range(samples):
            start = random.choice(vertices)
            ecc = max(self.bfs(start)[1].values())
            
            lower_bound = max(lower_bound, ecc)
            upper_bound = min(upper_bound, ecc * 2)

        return lower_bound, upper_bound
    
    """
    Algorithm 2 Distance Preserving Vertex Elimination
        - Eliminates vertex v from weight graph H, preserves shortest-path distances
        - H is dict of dicts. H[u][w] is weight between u and w
    """
    def dp_elim(self, H, v):
        if v not in H:
            return
        
        neighbors = list(H[v].keys())

        # For every pair of neighbors (u, w)
        for i in range(len(neighbors)):
            u = neighbors[i]
            for j in range(i + 1, len(neighbors)):
                w = neighbors[j]

                # New distance going through v
                new_dist = H[v][u] + H[v][w]

                # Update if no edge or shorter path found
                if w not in H[u] or new_dist < H[u][w]:
                    H[u][w] = new_dist
                    H[w][u] = new_dist

        # Remove v and its incident edges
        for u in neighbors:
            if v in H[u]:
                del H[u][v]
        del H[v]

    """
    Algorithm 3 DP Tree Decomposition
        - g is adjancency list dict[int, list[int]]
        - Returns bags[v], lambdas[v], parent[v], and phi[v]
            bags[v] represents X(v) = {v} U N(v)
            lambdas[v] represents lambda-array of distances from v to each vertex in bags[v]
            parent[v] represents the parent center in the DP-tree
            phi[v] represents the elimination order index 
    """
    def naive_dp_tree_decomp(self, g: dict[int, list[int]]):

        # Build weighted graph H with weight 1 on every edge
        H = {}
        for u in g:
            H[u] = {}
            for w in g[u]:
                H[u][w] = 1

        bags = {}
        lambdas = {}
        phi = {}

        rem_vertices = list(H.keys())
        num_vertices = len(rem_vertices)

        # Eliminate vertices one-by-one
        for i in range(1, num_vertices + 1):
            smallest_degree_vertex = None
            smallest_degree = float('inf')

            # Find min-degree vertex in current H
            for x in H.keys():
                degree_x = len(H[x])
                if degree_x < smallest_degree:
                    smallest_degree = degree_x
                    smallest_degree_vertex = x
            
            v = smallest_degree_vertex

            # Build bag X(v)
            neighbors_of_v = list(H[v].keys())
            bag = [v]
            for u in neighbors_of_v:
                bag.append(u)
            bags[v] = bag

            # Build lambda(v)
            lam = []
            lam.append(0)
            for u in neighbors_of_v:
                lam.append(H[v][u])
            lambdas[v] = lam

            # Record elimination order
            phi[v] = i

            # Distance-preserving elimination
            self.dp_elim(H, v)

        # Compute parent[v]
        parent = {}
        for v in bags:
            bag_v = bags[v]

            candidates = []
            for x in bag_v:
                # only consider x != v and x that has a phi(x)
                if x != v and x in phi:
                    candidates.append(x)

            if len(candidates) == 0:
                parent[v] = None
            else:
                best_parent = candidates[0]
                for x in candidates:
                    if phi[x] < phi[best_parent]:
                        best_parent = x
                parent[v] = best_parent
        
        return bags, lambdas, parent, phi

    """
    Ancestor chains for Algorithm 5
        - For every center v, builds its chain of ancestors from the root
    """
    def build_ancestors(self, bags, parent):
        anc = {}

        def helper(v):
            if v in anc:
                return anc[v]
            if parent[v] is None:
                anc[v] = [v]
            else:
                anc[v] = helper(parent[v]) + [v]
            return anc[v]
        
        for v in bags:
            helper(v)

        return anc

    """
    Algorithm 5: H2H Index Construction
        - Produces anc[v], pos[v], and dis[v]
            anc[v] represents the ancestor chain of v's center
            pos[v] represents the positions of bag vertices in anc[v]
            dis[v] represents the distance array of anc[v]
    """
    def naive_H2H(self, bags, lambdas, parent, phi):
        anc = self.build_ancestors(bags, parent)
        pos = {}
        dis = {}

        vertices_in_order = sorted(phi.keys(), key=lambda x: phi[x])

        for v in vertices_in_order:
            bag_v = bags[v]
            lam_v = lambdas[v]
            chain_v = anc[v]

            # Build pos[v]
            pos_list = []
            for x in bag_v:
                if x not in chain_v:
                    raise ValueError(f"Vertex {x} not found in ancestor chain of {v}")
                position = chain_v.index(x)
                pos_list.append(position)
            pos[v] = pos_list

            # Build dis[v]
            L = len(chain_v)
            dis_list = [float('inf')] * L
            dis_list[L - 1] = 0  # distance from v to itself

            for i in range(L - 1):
                best_distance = float('inf')

                for j in range(len(bag_v)):
                    x_j = bag_v[j]
                    lam_xj = lam_v[j]
                    pos_xj = pos_list[j]

                    if pos_xj > i:
                        if (x_j in dis) and (i < len(dis[x_j])):
                            temp_distance = dis[x_j][i]
                        else:
                            temp_distance = float('inf')
                    else:
                        ancestor_i = chain_v[i]
                        if (ancestor_i in dis) and (pos_xj < len(dis[ancestor_i])):
                            temp_distance = dis[ancestor_i][pos_xj]
                        else:
                            temp_distance = float('inf')
                    
                    total = lam_xj + temp_distance
                    if total < best_distance:
                        best_distance = total

                dis_list[i] = best_distance

            dis[v] = dis_list

        return anc, pos, dis