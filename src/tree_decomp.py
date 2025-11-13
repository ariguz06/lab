from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from graph import Graph


class TreeDecomp:
    """
    Tree decomposition class where bags are Graph instances.
    Uses adjacency dict to represent the tree structure.
    """

    def __init__(self):
        # Adjacency dict: Graph -> list of neighbor Graphs
        # Using 'any' at runtime to avoid circular import
        self.adj: dict = {}
        # Root of the tree decomposition
        self.root: Graph | None = None
        # Track all bags in the decomposition
        self.bags: set = set()

    def add_bag(self, bag):
        """
        Add a bag to the tree decomposition.

        Args:
            bag: Either a Graph instance or adjacency dict to create a Graph from
        """
        if isinstance(bag, dict):
            from src.graph import Graph
            bag = Graph(adjacency_dict=bag)

        if bag not in self.bags:
            self.bags.add(bag)
            self.adj[bag] = []

    def add_edge(self, u, v):
        """
        Add an edge between two bags in the tree decomposition.
        The first vertex v of the first edge added becomes the root.

        Args:
            u: First bag (Graph instance or adjacency dict)
            v: Second bag (Graph instance or adjacency dict)
        """
        # Convert to Graph instances if needed
        if isinstance(u, dict):
            from graph import Graph
            u = Graph(adjacency_dict=u)
        if isinstance(v, dict):
            from graph import Graph
            v = Graph(adjacency_dict=v)

        # Ensure both bags exist
        self.add_bag(u)
        self.add_bag(v)

        # Set root to v if this is the first edge
        if self.root is None:
            self.root = v

        # Add bidirectional edge
        if v not in self.adj[u]:
            self.adj[u].append(v)
        if u not in self.adj[v]:
            self.adj[v].append(u)

    def get_neighbors(self, bag):
        """Get all neighbor bags of a given bag."""
        return self.adj.get(bag, [])

    def get_root(self):
        """Get the root of the tree decomposition."""
        return self.root

    def num_bags(self):
        """Get the number of bags in the decomposition."""
        return len(self.bags)

    def tree_width(self):
        """
        Calculate the tree width of the decomposition.
        Tree width = max(|bag| - 1) over all bags.
        """
        if not self.bags:
            return -1

        max_bag_size = 0
        for bag in self.bags:
            bag_size = len(list(bag.g.values())[0]) + 1 # denotes values in each bag, and the vertex they are adjacent to (hence +1)
            max_bag_size = max(max_bag_size, bag_size)

        return max_bag_size - 1

    def __str__(self):
        """String representation of the tree decomposition."""
        lines = [f"TreeDecomp with {self.num_bags()} bags"]
        if self.root:
            lines.append(f"Root bag has {len(self.root.g)} vertices")
        lines.append(f"Treewidth: {self.tree_width()}")
        return "\n".join(lines)