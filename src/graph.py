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
    
    # Returns list of edges to then be added to h_adj in tree decomposition 
    def triangulate_neighbors(self, adj: dict[int, list[int]], vertex: int) -> dict[int, list[int]]:
        h_adj = adj
        
        neighbors = adj[vertex]
        edges = self.edges
        l = len(neighbors)
        
        for i in range(l):
            for j in range(l):
                u = neighbors[i]
                w = neighbors[j]
                
                if i != j and (u, w) not in edges:
                    # h_adj [u] must exist (i.e. it is not None), as it the edge (u, vertex) exists
                    # likewise for h_adj [w]
                    h_adj[u].append(w)
                    h_adj[w].append(u)
                    
                # should we consider edge weights here?
        
        return h_adj
    
    def dp_tree_decomp(self) -> TreeDecomp:
        h_adj = self.g
        td = TreeDecomp()
        ordering: dict[int, int] = {}
        
        count = 0

        for i in range(len(h_adj)):
            min_degree: int = self.min_degree(h=h_adj)
            star_min_deg = self.star(h_adj, min_degree)
            td.add_bag(star_min_deg, min_degree)
            
            h_adj = self.triangulate_neighbors(h_adj, min_degree)
            ordering[min_degree] = i
            
            if(count % 1000 == 0): print(count)
            count += 1
            
        for v in self.g:
            star_v: dict[int, list[int]] = self.star(self.g, v)
            if len(list(star_v.values())[0]) > 1:
                
                # finds vertex in X(v) \ {v} with smallest ordering value
                ordering_exclude_v = {vertex: value for vertex, value in ordering.items() if vertex != v}
                min_ordering_vertex = min(ordering_exclude_v, key=ordering_exclude_v.get)

                star_u = self.star(self.g, min_ordering_vertex)

                # root can be last u vertex added (or any node, really)
                td.add_edge(Graph(adjacency_dict=star_v), min_ordering_vertex, Graph(adjacency_dict=star_u), v)
                        
        # addl for loop here for reassigning edge weights
        
        return td

    @staticmethod
    def dict_to_list(adj: dict[int, list[int]]) -> list[int]:
        to_ret = [list(adj.keys())[0]]
        for value in adj.values():
            for v in value:
                to_ret.append(v)

        return to_ret

    # Hierarchical 2-hop indexing
    def h_two_h(self, tg):

        call_stack = [tg.root]
        h2h = []
        visited = set()

        # implement algorithm 1
        # find graph of ~100k vertices
        # make tables similar to figure 11

        while call_stack:
            c_bag: Graph = call_stack.pop()

            xv_list: list[int] = self.dict_to_list(c_bag.g) # assume X(v) \in V(Tg) = (x_1,x_2...x_|v|)

            anc_list = tg.anc(c_bag)

            for i in range(len(xv_list)-1):
                pass
                # c_bag.pos.append(anc_list.index(xv_list[i])) #X(v).pos_i = index of x_i in X(v).anc

            for i in range(len(anc_list) - 2):
                c_bag.dis.append(1)
                # add

            if len(c_bag.dis) == 0:
                c_bag.dis.append(0)
            else:
                c_bag.dis[len(anc_list)] = 0

            h2h.append((c_bag.dis, c_bag.pos))

            visited.add(c_bag)

            for neighbor in tg.get_neighbors(c_bag):
                if not neighbor in visited:
                    call_stack.append(neighbor)

        return h2h