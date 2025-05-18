import random
from itertools import combinations

class Graph:
    def __init__(self, directed=False):
        """
        初始化图。

        参数：
        - directed (bool): 指定图是否为有向图。默认为 False（无向图）。

        属性：
        - graph (dict): 用于存储顶点及其相邻顶点（带权重）的字典。
        - directed (bool): 表示图是否为有向图。
        """
        self.graph = {}
        self.directed = directed
    
    def add_vertex(self, vertex):
        """
        向图中添加顶点。

        参数：
        - vertex: 要添加的顶点。必须是可哈希类型。

        确保每个顶点在图字典中都表示为一个键，其值为空字典。
        """
        if not isinstance(vertex, (int, str, tuple)):
            raise ValueError("Vertex must be a hashable type.")
        if vertex not in self.graph:
            self.graph[vertex] = {}
    
    def add_edge(self, src, dest, weight):
        """
        从起始顶点(src)到目标顶点(dest)添加一条带权重的边。如果是无向图，则同时添加从目标顶点到起始顶点的边。

        参数：
        - src: 起始顶点
        - dest: 目标顶点
        - weight: 边的权重
        
        防止添加重复的边，并确保两个顶点都存在于图中。
        """
        if src not in self.graph or dest not in self.graph:
            raise KeyError("Both vertices must exist in the graph.")
        if dest not in self.graph[src]:  # Check to prevent duplicate edges
            self.graph[src][dest] = weight
        if not self.directed and src not in self.graph[dest]:
            self.graph[dest][src] = weight
    
    def remove_edge(self, src, dest):
        """
        从起始顶点到目标顶点删除一条边。如果是无向图，则同时删除从目标顶点到起始顶点的边。

        参数：
        - src: 起始顶点
        - dest: 目标顶点
        """
        if src in self.graph and dest in self.graph[src]:
            del self.graph[src][dest]
        if not self.directed:
            if dest in self.graph and src in self.graph[dest]:
                del self.graph[dest][src]
    
    def remove_vertex(self, vertex):
        """
        移除一个顶点及其所有连接的边。

        参数：
        - vertex: 要移除的顶点
        """
        if vertex in self.graph:
            # 从其他顶点移除到该顶点的边
            for adj in list(self.graph):
                if vertex in self.graph[adj]:
                    del self.graph[adj][vertex]
            # 移除该顶点本身
            del self.graph[vertex]
    
    def get_adjacent_vertices(self, vertex):
        """
        获取指定顶点的相邻顶点列表。

        参数：
        - vertex: 要获取相邻顶点的顶点

        返回：
        - 相邻顶点列表。如果顶点不存在，则返回空列表。
        """
        return list(self.graph.get(vertex, {}).keys())

    def _get_edge_weight(self, src, dest):
        """
        获取从起始顶点到目标顶点的边的权重。

        参数：
        - src: 起始顶点
        - dest: 目标顶点

        返回：
        - 边的权重。如果边不存在，则返回无穷大。
        """
        return self.graph[src].get(dest, float('inf'))
    
    def __str__(self):
        """
        提供图的邻接表的字符串表示，方便打印和调试。

        返回：
        - 图字典的字符串表示。
        """
        return str(self.graph)

   
def generate_graph(nodes, edges=None, complete=False, weight_bounds=(1,600), seed=None):
    """
    生成一个具有指定参数的图，允许完全图和非完全图。
    
    该函数创建一个具有指定节点和边的图，并提供创建完全图和指定边权重范围的选项。它使用Graph_Advanced类来创建和操作图。

    参数：
    - nodes (int): 图中的节点数。必须是正整数。
    - edges (int, optional): 为图中的每个节点添加的边数。如果`complete`设置为True，则忽略此参数。默认为None。
    - complete (bool, optional): 如果设置为True，则生成一个完全图，其中每个不同的顶点通过唯一的边连接。默认为False。
    - weight_bounds (tuple, optional): 一个指定边随机权重范围的下限和上限（包括）的元组。默认为(1, 600)。
    - seed (int, optional): 用于确保可重复性的随机数生成器种子。默认为None。

    抛出：
    - ValueError: 如果`edges`不是None且`complete`设置为True，因为完全图不需要指定边数。

    返回：
    - Graph_Advanced: 一个表示生成的图的Graph_Advanced类实例，顶点标签从0开始。

    示例：
    - 生成一个包含5个节点的完全图：
        generate_graph(5, complete=True)
    
    - 生成一个包含5个节点且每个节点有2条边的非完全图：
        generate_graph(5, edges=2)
    
    注意：
    - 该函数假设存在一个具有添加顶点(`add_vertex`)和边(`add_edge`)方法以及获取相邻顶点(`get_adjacent_vertices`)方法的Graph_Advanced类。
    """
    random.seed(seed)
    graph = Graph_Advanced()
    if edges is not None and complete:
        raise ValueError("edges must be None if complete is set to True")
    if not complete and edges > nodes:
        raise ValueError("number of edges must be less than number of nodes")
    

    for i in range(nodes):
        graph.add_vertex(i)
    if complete:
        for i in range(nodes):
            for j in range(i+1,nodes):
                weight = random.randint(weight_bounds[0], weight_bounds[1])
                graph.add_edge(i,j,weight)
    else:
        for i in range(nodes):
            for _ in range(edges):
                j = random.randint(0, nodes - 1)
                while (j == i or j in graph.get_adjacent_vertices(i)) and len(graph.get_adjacent_vertices(i)) < nodes - 1:  # Ensure the edge is not a loop or a duplicate
                    j = random.randint(0, nodes - 1)
                weight = random.randint(weight_bounds[0], weight_bounds[1])
                if len(graph.graph[i]) < edges and len(graph.graph[j]) < edges:
                    graph.add_edge(i, j, weight)
    return graph

class Graph_Advanced(Graph):

    def shortest_path(self, start, end) -> tuple[float, list]: 
        """
        计算从起始顶点到目标顶点的最短路径。
        参数：
        - start: 起始顶点
        - end: 目标顶点
        
        返回：
        - 一个包含最短路径距离和路径顶点列表的元组。
        """
        # 代码写这里
        return 0,[]
    
    def tsp_small_graph(self, start_vertex) -> tuple[float, list]:
        """
        解决小（~10节点）完全图的旅行商问题，从指定节点开始。
        任务要求[!]: 需要找到最优路径。预期图最多有10个节点。必须在0.5秒内运行。
        
        参数：
        - start_vertex: 起始节点
        
        返回：
        - 一个包含总距离和路径顶点列表的元组。
        """
        # 代码写这里
        
        return 0, []


    def tsp_large_graph(self, start) -> tuple[float, list]: 
        """
        解决大（~1000节点）完全图的旅行商问题，从指定节点开始。
        任务要求[!]: 不需要找到最优路径。必须在0.5秒内运行。
        
        参数：
        - start: 起始节点
        
        返回：
        - 一个包含总距离和路径顶点列表的元组。
        """
        # 代码写这里
        return 0, []
        

    def tsp_medium_graph(self, start_vertex) -> tuple[float, list]:
        """
        解决中型（~300节点）完全图的旅行商问题，从指定节点开始。
        任务要求[!]: 需要找到相对较优的路径，结果应该优于简单贪心算法。必须在0.5秒内运行。
        
        参数：
        - start_vertex: 起始节点
        - time_limit: 最大允许时间（秒）

        返回：
        - 一个包含总距离和路径顶点列表的元组。
        """
        # 代码写这里
        return 0, []
            
        