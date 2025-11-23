from collections import deque
import random
import time

from src.graph import Graph
from src.tree_decomp import TreeDecomp


if __name__ == "__main__":
    usa_path = "include/road-road-usa/road-road-usa.mtx"
    mn_path = "include/road-minnesota/road-minnesota.mtx"
    us_48_path = "include/road-usroads-48/road-usroads-48.mtx"

    start_time = time.time()
    # mn_graph = Graph(file_path=mn_path)
    # usa_graph = Graph(file_path=usa_path)
    usa_48_graph = Graph(file_path=us_48_path)

    end_time = time.time()

    parse_time = end_time - start_time

    print("Graph parse time: " + str(parse_time))

    start_time = time.time()
    bfs_result = usa_48_graph.bfs(17)
    end_time = time.time()

    bfs_time = end_time - start_time

    print("BFS time: " + str(bfs_time))
    print("BFS size: " + str(len(bfs_result[0])))
    print("Graph diameter (lower, upper): " + str(usa_48_graph.estimate_diameter(samples=10)))
    print("Total time: " + str(parse_time + bfs_time))

    start_time = time.time()

    mn_mtx = parse_mtx("include/road-minnesota/road-minnesota.mtx")
    graph = generate_graph(mn_mtx)
    
    start_key = list(graph.keys())[0]
    bfs_result = bfs(graph[start_key])

    end_time = time.time()

    elapsed_time = end_time - start_time
    print(f"Total execution time: {elapsed_time: .4f} seconds")
    print(f"BFS found {len(bfs_result)} nodes")