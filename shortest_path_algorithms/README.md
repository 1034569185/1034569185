# Shortest Path Algorithms Visualization

# 最短路径算法可视化

This project implements and visualizes Dijkstra's algorithm and Floyd-Warshall algorithm for finding shortest paths in a weighted directed graph.

本项目实现并可视化了Dijkstra算法和Floyd算法，用于在带权有向图中查找最短路径。

---

## Graph Structure / 图的结构

### Basic Information / 基本信息

- **Type / 类型**: Weighted Directed Graph / 带权有向图
- **Connected / 连通性**: Yes (Strongly Connected) / 是（强连通）
- **Number of Vertices / 顶点数**: 5 (A, B, C, D, E) - Exceeds minimum requirement of 3 / 超过最少3个要求
- **Number of Edges / 边数**: 7 directed edges - Exceeds minimum requirement of 4 / 7条有向边，超过最少4条要求

### Edges with Weights / 边及权重

| From<br>起点 | To<br>终点 | Weight<br>权重 |
|-------------|-----------|---------------|
| A           | B         | 3             |
| A           | C         | 5             |
| B           | C         | 2             |
| B           | D         | 4             |
| C           | D         | 1             |
| C           | E         | 6             |
| D           | E         | 2             |

### Graph Visualization / 图的可视化

The graph is visualized with:
- Blue circular nodes for vertices
- Directed edges with arrows showing direction
- Edge weights labeled in red
- Curved edges to prevent visual overlap

图的可视化包括：
- 蓝色圆形节点表示顶点
- 带箭头的有向边显示方向
- 红色标注的边权重
- 曲线边防止视觉重叠

---

## Dijkstra's Algorithm / Dijkstra算法

### Description / 算法描述

Dijkstra's algorithm finds the shortest paths from a single source vertex to all other vertices in the graph. It maintains two sets:
- **S**: Vertices with known shortest path distances
- **V - S**: Vertices without known shortest path distances

Dijkstra算法查找从单个源顶点到图中所有其他顶点的最短路径。它维护两个集合：
- **S**：已知最短路径距离的顶点
- **V - S**：未知最短路径距离的顶点

### Algorithm Steps / 算法步骤

1. **Initialization / 初始化**:
   - Set distance to source vertex = 0
   - Set distance to all other vertices = ∞
   - S = ∅ (empty set)
   - V - S = all vertices
   
   源顶点距离 = 0，其他顶点距离 = ∞，S = ∅，V - S = 所有顶点

2. **Iteration / 迭代**:
   - Find vertex u in V - S with minimum distance
   - Add u to S
   - Update distances to neighbors of u
   - Repeat until all vertices are in S
   
   在V - S中找到距离最小的顶点u，将u加入S，更新u的邻居距离，重复直到所有顶点都在S中

3. **Path Reconstruction / 路径重建**:
   - Use previous vertex information to build the shortest path
   - 使用前驱顶点信息构建最短路径

### Visualization / 可视化

The visualization shows each step of the algorithm in a table format:
- **Vertex / 顶点**: The vertex name
- **In S? / 在S中?**: Whether the vertex is in set S (✓) or not (✗)
- **Distance / 距离**: Current shortest distance from source
- **Shortest Path / 最短路径**: Current shortest path from source to this vertex

可视化以表格形式展示算法的每一步：
- **顶点**: 顶点名称
- **在S中?**: 顶点是否在集合S中（✓表示是，✗表示否）
- **距离**: 从源点到当前顶点的最短距离
- **最短路径**: 从源点到当前顶点的最短路径

**Color Coding / 颜色编码**:
- Green header / 绿色表头: Column headers
- Light green background / 浅绿色背景: Vertices already in S
- Yellow highlight / 黄色高亮: Newly added vertex in current step
- White background / 白色背景: Vertices not yet in S

### Results (Source: A) / 结果（源点：A）

| Target<br>目标 | Distance<br>距离 | Shortest Path<br>最短路径 |
|---------------|-----------------|------------------------|
| A             | 0               | A                      |
| B             | 3               | A → B                  |
| C             | 5               | A → B → C              |
| D             | 6               | A → B → C → D          |
| E             | 8               | A → B → C → D → E      |

---

## Floyd-Warshall Algorithm / Floyd算法

### Description / 算法描述

Floyd-Warshall algorithm finds the shortest paths between all pairs of vertices in the graph. It uses dynamic programming by considering intermediate vertices one by one.

Floyd算法查找图中所有顶点对之间的最短路径。它通过逐个考虑中间顶点来使用动态规划。

### Algorithm Steps / 算法步骤

1. **Initialization / 初始化**:
   - Distance matrix = Adjacency matrix
   - dist[i][i] = 0 (distance to self)
   - dist[i][j] = ∞ if no direct edge
   
   距离矩阵 = 邻接矩阵，dist[i][i] = 0（到自身的距离），无直接边时dist[i][j] = ∞

2. **Iteration / 迭代** (for each intermediate vertex k):
   - For each pair of vertices (i, j):
     - If dist[i][k] + dist[k][j] < dist[i][j]:
       - Update dist[i][j] = dist[i][k] + dist[k][j]
       - Update path to go through k
   
   对每个中间顶点k：对每对顶点(i, j)：如果dist[i][k] + dist[k][j] < dist[i][j]，则更新距离和路径

3. **Result / 结果**:
   - Final distance matrix contains shortest distances for all pairs
   - Path matrix allows reconstruction of shortest paths
   
   最终距离矩阵包含所有顶点对的最短距离，路径矩阵允许重建最短路径

### Visualization / 可视化

The visualization shows each step with two tables:

1. **Distance Matrix (adj) / 距离矩阵**:
   - Shows shortest distances between all vertex pairs
   - Diagonal is 0 (self to self)
   - ∞ indicates no path exists (yet)
   - Updated after considering each intermediate vertex

2. **Path Table / 路径表**:
   - Shows the actual shortest path between each pair of vertices
   - Format: Start → Intermediate → ... → End
   - "-" indicates same vertex (diagonal)

可视化展示每一步的两个表格：
1. **距离矩阵**：显示所有顶点对之间的最短距离
2. **路径表**：显示每对顶点之间的实际最短路径

**Color Coding / 颜色编码**:
- Blue header / 蓝色表头: Distance matrix headers
- Light blue diagonal / 浅蓝色对角线: Self-distances (always 0)
- Green header / 绿色表头: Path table headers

### Final Results / 最终结果

**Final Distance Matrix / 最终距离矩阵**:

```
     A    B    C    D    E
A    0    3    5    6    8
B    ∞    0    2    3    5
C    ∞    ∞    0    1    3
D    ∞    ∞    ∞    0    2
E    ∞    ∞    ∞    ∞    0
```

**Sample Shortest Paths / 示例最短路径**:

| From<br>起点 | To<br>终点 | Distance<br>距离 | Path<br>路径 |
|-------------|-----------|-----------------|-------------|
| A           | E         | 8               | A → B → C → D → E |
| B           | E         | 5               | B → C → D → E |
| C           | E         | 3               | C → D → E |
| A           | D         | 6               | A → B → C → D |
| B           | D         | 3               | B → C → D |

---

## How to Run / 如何运行

### Requirements / 环境要求

```bash
pip3 install matplotlib networkx numpy
```

### Execute / 执行

```bash
cd shortest_path_algorithms
python3 shortest_paths.py
```

### Output / 输出

The program generates 3 visualization files:

程序生成3个可视化文件：

1. **graph.png** - Weighted directed graph visualization / 带权有向图可视化
2. **dijkstra_steps.png** - Step-by-step Dijkstra algorithm execution / Dijkstra算法逐步执行
3. **floyd_steps.png** - Step-by-step Floyd-Warshall algorithm execution / Floyd算法逐步执行

---

## File Structure / 文件结构

```
shortest_path_algorithms/
├── shortest_paths.py          # Main program / 主程序
├── README.md                  # This file / 本文件
├── graph.png                  # Graph visualization / 图的可视化
├── dijkstra_steps.png         # Dijkstra algorithm steps / Dijkstra算法步骤
└── floyd_steps.png            # Floyd-Warshall algorithm steps / Floyd算法步骤
```

---

## Algorithm Comparison / 算法比较

| Feature<br>特性 | Dijkstra | Floyd-Warshall |
|----------------|----------|----------------|
| Purpose<br>目的 | Single-source shortest paths<br>单源最短路径 | All-pairs shortest paths<br>所有顶点对最短路径 |
| Time Complexity<br>时间复杂度 | O(V²) or O((V+E)logV)<br>O(V²) 或 O((V+E)logV) | O(V³) |
| Space Complexity<br>空间复杂度 | O(V)<br>O(V) | O(V²) |
| Handles Negative Weights<br>处理负权重 | No<br>不支持 | Yes (but not negative cycles)<br>支持（但不支持负环） |
| Output<br>输出 | Distances from one source<br>从一个源点到所有顶点的距离 | Distances between all pairs<br>所有顶点对之间的距离 |
| Best Use Case<br>最佳使用场景 | Finding paths from one specific vertex<br>从特定顶点查找路径 | Need all shortest paths<br>需要所有最短路径 |

---

## Key Concepts / 关键概念

### Dijkstra's Algorithm / Dijkstra算法

- **Greedy approach / 贪心法**: Always selects the closest unvisited vertex
- **Relaxation / 松弛**: Updates distances when a shorter path is found
- **Set S / 集合S**: Represents vertices with finalized shortest distances
- **Priority / 优先级**: Vertices are processed in order of increasing distance from source

### Floyd-Warshall Algorithm / Floyd算法

- **Dynamic programming / 动态规划**: Builds solution from smaller subproblems
- **Intermediate vertices / 中间顶点**: Considers each vertex as potential intermediate point
- **All-pairs / 所有顶点对**: Computes shortest paths between every pair simultaneously
- **Matrix updates / 矩阵更新**: Each iteration updates the entire distance matrix

---

## Summary / 总结

This project successfully implements:

本项目成功实现了：

✅ A weighted directed graph with 5 vertices and 7 edges (exceeds minimum requirements)

✅ 带权有向图，5个顶点、7条边（超过最低要求）

✅ Dijkstra's algorithm with step-by-step visualization showing S and V-S sets

✅ Dijkstra算法，逐步可视化显示S和V-S集合

✅ Floyd-Warshall algorithm with step-by-step visualization showing distance matrix updates

✅ Floyd算法，逐步可视化显示距离矩阵更新

✅ Detailed tables showing intermediate steps, distances, and paths

✅ 详细表格显示中间步骤、距离和路径

✅ All visualizations saved in the shortest_path_algorithms/ directory

✅ 所有可视化保存在shortest_path_algorithms/目录中

Both algorithms correctly compute shortest paths and demonstrate different approaches to solving the shortest path problem.

两种算法都正确计算了最短路径，并展示了解决最短路径问题的不同方法。

---

## References / 参考资料

- Dijkstra, E. W. (1959). "A note on two problems in connexion with graphs"
- Floyd, Robert W. (1962). "Algorithm 97: Shortest Path"
- Warshall, Stephen (1962). "A Theorem on Boolean Matrices"
- Introduction to Algorithms (CLRS) - Chapter 24 & 25

---

## License / 许可证

This project is created for educational purposes.

本项目为教育目的创建。
