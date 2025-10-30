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

10/19 tree decomp notes 

Recall: the treewidth of a graph of is the size of its largest bag of all possible tree decomps (obtained by decomposition) minus one

the width of a tree decomp is its largest bag 

NP-hard and other (constraint satisfaction) problems can be represented as graphs 

    NP-hard refers to problems from which all NP problems (NP meaning solution can be verified in polynomial time) can be derived. NP-hard problems may or may not be in the class NP (if they are they are called NP-complete)

    Finding treewidth of a graph itself is an NP-hard problem. Is that NP complete? Do complexity classes matter?
    
If these graphs have bounded treewidth, polynomial algorithms exist for them (with dynamic programming)

Ex: coloring problem w/ undirected edges 

A->B, A->C, B->C, C->D

To solve the problem based on its decomposition, get d^n where d := number of possible colors, n := number of vertices, for each bag 

The bag containing A,B,C has 6 valid solutions, because A cannot = B, A cannot = C, B cannot = C

The bag containing C, D has 6 possible solutions as C cannot = D

To proceed, the solutions for first bag are joined with second bag solutions in which C has the same vertex color. Using tree decomposition in this case only requires 36 comparisons, as opposed to the 81 without. Thus, the NP-hard problem has been reduced. 


A set of strongly connected vertices is a _clique_. A vertex is _simplicial_ if its neighbors form a clique. An edge connecting two non-adjacent vertices is called a chord. The graph is triangulated if there exists a chord in every cycle of length larger than 3. 

Broad algorithm: Given an elimination ordering of nodes, the triangulation H of graph G, if H=G initially, can be found this way:
    
    Eliminate next vertex in the ordering by making it into a simplicial, i.e. adding edges to make all of its neighbors connected 


__Genetic Algorithms__

Genetic algorithms (reinforcement learning?) 

__Questions to ask Hector__:

If decomposing a tree is NP-hard itself?, what is the advantage of doing this for NP-hard problems? Examples seem to overlook this

"An ordering of nodes σ(1, 2, . . . , n) of V is called a perfect elimination ordering for G if for any i ∈ {1, 2, . . . , n}, σ(i) is a simplicial vertex in G[σ(i), . . . , σ(n)]", what does this notation mean? Entire paragraph makes no sense (translation issues?)
