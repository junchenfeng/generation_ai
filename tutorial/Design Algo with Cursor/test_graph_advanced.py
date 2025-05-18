import unittest
from graph import Graph_Advanced
import pickle
import time
import os # Add os import

# Get the directory of the current script
script_dir = os.path.dirname(os.path.abspath(__file__))
medium_graph_path = os.path.join(script_dir, "medium_graph_300.pickle")
large_graph_path = os.path.join(script_dir, "large_graph_1000.pickle")

class TestGraphAdvanced(unittest.TestCase):
    def setUp(self):
        """
        创建测试用的图实例
        图的结构如下（全连接图）：
           1
        /  |  \
     1/    |2   \2
     /     |     \
    0 --3--|--4-- 2
     \     |     /
     5\    |3   /3
        \  |  /
           3
        """
        self.small_graph = Graph_Advanced()
        
        # 添加顶点
        for i in range(4):
            self.small_graph.add_vertex(i)
        
        # 添加边 - 全连接图
        edges = [
            (0, 1, 1),  # 0-1 权重为1
            (0, 2, 4),  # 0-2 权重为4
            (0, 3, 5),  # 0-3 权重为5
            (1, 2, 2),  # 1-2 权重为2
            (1, 3, 3),  # 1-3 权重为3
            (2, 3, 3),  # 2-3 权重为3
        ]
        
        for src, dest, weight in edges:
            self.small_graph.add_edge(src, dest, weight)

        with open(medium_graph_path, "rb") as f: # Use the new path
            self.medium_graph = pickle.load(f)
        with open(large_graph_path, "rb") as f: # Use the new path
            self.large_graph = pickle.load(f)      
              
    def test_shortest_path(self):
        # 测试从顶点0到顶点2的最短路径
        distance, path = self.small_graph.shortest_path(0, 2)
        self.assertEqual(distance, 3)  # 最短距离应该是3 (0->1->2)
        self.assertEqual(path, [0, 1, 2])  # 最短路径应该是[0,1,2]
        
        # 测试从顶点3到顶点1的最短路径
        distance, path = self.small_graph.shortest_path(3, 1)
        self.assertEqual(distance, 3)  # 最短距离应该是3 (3->1)
        self.assertEqual(path, [3, 1])  # 最短路径应该是[3,1]
        
        # 测试从顶点到自身的路径
        distance, path = self.small_graph.shortest_path(0, 0)
        self.assertEqual(distance, 0)  # 距离应该是0
        self.assertEqual(path, [0])    # 路径应该只包含起点

    def test_tsp_small(self):
        """
        测试旅行商问题(TSP)解决方案
        
        最优解应该是: 0 -> 1 -> 2 -> 3 -> 0
        总距离: 1 + 2 + 3 + 5 = 11
        """
        distance, path = self.small_graph.tsp_small_graph(0)
        self.assertEqual(distance, 11)  # 最短回路距离应为11
        self.assertTrue(path in [[0, 1, 2, 3, 0], [0, 3, 2, 1, 0]])  # 验证是否为两个最优路径之一

    def test_tsp_medium(self):
        # 读取图

        
        # 测试性能
        start_time = time.time()
        distance, path = self.medium_graph.tsp_medium_graph(0)
        end_time = time.time()
        
        execution_time = end_time - start_time
        self.assertEqual(len(path), 301, "路径长度应为301，包括返回起点的路径")
        self.assertTrue(distance<700, f"最短路径为{distance}，简单贪心算法的结果是714")  # 300个节点加上返回起点        
        # 验证时间限制
        self.assertTrue(execution_time < 0.5, f"执行时间 {execution_time:.4f} 秒超过了0.5秒限制")

    def test_tsp_large(self):
        # 测试性能
        start_time = time.time()
        distance, path = self.large_graph.tsp_large_graph(0)
        end_time = time.time()
        execution_time = end_time - start_time
        self.assertEqual(len(path), 1001, "路径长度应为1001，包括返回起点的路径") 
        self.assertTrue(distance < 1531, "最短路径不正确")     

        self.assertTrue(execution_time < 0.5, f"执行时间 {execution_time:.4f} 秒超过了0.5秒限制")


if __name__ == '__main__':
    unittest.main()