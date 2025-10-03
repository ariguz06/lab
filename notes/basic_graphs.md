spanning tree: contains all the vertices of G but is acyclic, can be produced by search algorithms (as seen in 250)

"whatever first search"
    put any vertex in bag
    while the bag is not empty 
        take first element (p, v) from bag
        if v is unmarked
            mark v as visited
            for each edge __vw__
                put w into the bag

stack bag: DFS O(V + E)
queue: BFS O(V + E)
priority queue/heap: "Best first" O(V + ElogE) for weighted graphs 

10/9 goal 

parse file 
create adjacency matrix 
modify + run bfs algorithm
