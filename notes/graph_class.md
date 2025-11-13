```class Graph```

__Properties__:

```self.adj: dict[int, list[int]]``` 
way to represent adjacency, can be a dict that maps a vertex (key of type ```int```) to its neighbors (value of type ```list[int]```)

```self.file: str```
the path to the .mtx graph file

__Methods__:

```__init__(file: str)```
Constructor that takes ```file```, the path to the .mtx graph file desired, and parses it to populate ```self.adj``` (copy code from ```parse_mtx``` method)

```from_dict(adj: dict[int, list[int]]) -> Graph```
Returns a new ```Graph``` object such that ```self.adj=adj```. In other words, initializes a graph directly with an adjacency dict without parsing a file. 

```min_degree() -> int```
Returns the vertex with smallest degree (number of neighbors). Can be obtained by iterating over ```adj``` and keeping track of shortest list of neighbors. 

```bfs(start_vertex: int, goal_vertex: int = -1) -> (order: list[int], distances: dict[int, int])```
BFS method with the same logic as current ```bfs``` function, operating on ```self.adj```. Returns order of traversal and the distance from ```start_vertex``` to each vertex. Stops traversal if ```goal_vertex``` is reached. 

```star(vertex: int) -> Graph```
Returns a new ```Graph``` object containing ```vertex```, its neighbors, and the edges from ```vertex``` to each of its neighbors. Can be obtained trivially using ```self.adj``` and ```self.from_dict```.  E.g. if ```vertex = 5``` and ```self.adj = [5: [1,2,3], 1: [2, 3], 3: [4]]```, ```neighbors_of(5)``` returns ```[5: [1,2,3]]```

```get_edges() -> list[(int, int)]```
Gets edges of graph from ```self.adj```. Returns a list of 2-tuples denoting edges.

```estimate_diameter(sample_size: int) -> int```
Estimates the diameter of graph using triangle inequality. Copy logic from existing method.

```symmetric_diff(vertex: int) -> Graph```
Defined in algorithm 2 in seed paper. Necessary for tree decomposition. Assume φ(u,v) = 1 for any edge (u, v) because our graphs are unweighted.
<br><br>
```class TreeDecomp```

Refer to https://gist.github.com/pat-mart/e5a4a33759da841b4e26e3ef8ce85ac5 (ChatGPT generated)
