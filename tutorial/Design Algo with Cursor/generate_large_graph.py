import pickle
from graph import generate_graph

if __name__ == "__main__":
    num_nodes = 300
    graph = generate_graph(
        nodes=num_nodes,
        complete=True,
        weight_bounds=(1, 100),
        seed=42  # 可选：设置随机种子以确保可重现性
    )
    
    # 保存到文件
    filename = "medium_graph_300.pickle"
    print(f"正在将图保存到 {filename}...")
    with open(filename, "wb") as f:
        pickle.dump(graph, f)
    
    print("完成！")
    
    # 打印图的基本信息
    n_vertices = len(graph.graph)
    n_edges = sum(len(edges) for edges in graph.graph.values()) // 2
    print(f"图的统计信息:")
    print(f"节点数量: {n_vertices}")
    print(f"边的数量: {n_edges}") 