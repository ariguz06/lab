from vertex import Vertex
from collections import deque 

def bfs(start: Vertex):
    visited = set()
    queue = deque([start])
    order = []
    
    while queue:
        node = queue.popleft()
        
        if node not in visited:
            visited.add(node)
            order.append(node.key)
            
            for neighbor in node.neighbors:
                if neighbor not in visited:
                    queue.append(neighbor)
    
    return order
                

if __name__ == "__main__":
    a = Vertex(key="a")
    b = Vertex(key="b")
    c = Vertex(key="c")
    d = Vertex(key="d")
    e = Vertex(key="e")
    
    a.neighbors = [b, c, e]
    e.neighbors = [a,b]
    c.neighbors = [a]
    b.neighbors = [c]
    
    print("BFS traversal: ", bfs(a))