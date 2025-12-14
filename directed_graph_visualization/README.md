# Directed Weighted Graph Visualization / 有向带权图可视化

## 概述 / Overview

本项目实现了一个有向带权图的构建和可视化，包括：
1. 有向图的可视化
2. 每个顶点的入度和出度
3. 邻接矩阵
4. 邻接表
5. 逆邻接表
6. 十字链表

This project implements a directed weighted graph with comprehensive visualizations including:
1. Directed graph visualization
2. In-degree and out-degree for each vertex
3. Adjacency matrix
4. Adjacency list
5. Inverse adjacency list
6. Orthogonal linked list

---

## 图的结构 / Graph Structure

### 顶点 / Vertices
图包含 **5个顶点**：A, B, C, D, E

The graph contains **5 vertices**: A, B, C, D, E

### 有向边 / Directed Edges
图包含 **8条有向边**（满足不少于5条边的要求）：

The graph contains **8 directed edges** (meeting the requirement of at least 5 edges):

| 有向边 / Directed Edge | 权重 / Weight |
|------------------------|---------------|
| A → B                  | 3             |
| A → C                  | 5             |
| B → C                  | 2             |
| B → D                  | 4             |
| C → D                  | 1             |
| C → E                  | 6             |
| D → E                  | 3             |
| E → A                  | 2             |

---

## 顶点度数 / Vertex Degrees

每个顶点的入度和出度：

In-degree and out-degree for each vertex:

| 顶点 / Vertex | 入度 / In-Degree | 出度 / Out-Degree |
|---------------|------------------|-------------------|
| A             | 1                | 2                 |
| B             | 1                | 2                 |
| C             | 2                | 2                 |
| D             | 2                | 1                 |
| E             | 2                | 1                 |

**说明 / Explanation:**
- **入度 (In-Degree)**: 指向该顶点的边的数量 / Number of edges pointing to the vertex
- **出度 (Out-Degree)**: 从该顶点出发的边的数量 / Number of edges originating from the vertex

---

## 邻接矩阵 / Adjacency Matrix

邻接矩阵是一个 5×5 的矩阵，其中元素 matrix[i][j] 表示从顶点 i 到顶点 j 的边的权重。

The adjacency matrix is a 5×5 matrix where element matrix[i][j] represents the weight of the edge from vertex i to vertex j.

```
FROM\TO    A     B     C     D     E
   A       0     3     5     ∞     ∞
   B       ∞     0     2     4     ∞
   C       ∞     ∞     0     1     6
   D       ∞     ∞     ∞     0     3
   E       2     ∞     ∞     ∞     0
```

**特点 / Characteristics:**
- **对角线**: 自己到自己为 0 / Diagonal: self to self is 0
- **有向边**: 矩阵不对称（有向图的特点）/ Directed edges: matrix is not symmetric (characteristic of directed graphs)
- **权重**: 有边的位置显示权重 / Weights: positions with edges show weights
- **不可达**: 用 ∞ 表示没有直接边 / Unreachable: ∞ represents no direct edge

---

## 邻接表 / Adjacency List (Outgoing Edges)

邻接表表示每个顶点的**出边**（从该顶点出发的边）。

The adjacency list represents the **outgoing edges** from each vertex.

```
A → B(w:3) → C(w:5) → NULL
B → C(w:2) → D(w:4) → NULL
C → D(w:1) → E(w:6) → NULL
D → E(w:3) → NULL
E → A(w:2) → NULL
```

**说明 / Explanation:**
- 每行显示一个顶点及其所有出边的目标顶点和权重 / Each row shows a vertex and all its outgoing edge targets with weights
- w: 表示权重 / w: represents weight
- NULL 表示链表结束 / NULL indicates end of linked list

---

## 逆邻接表 / Inverse Adjacency List (Incoming Edges)

逆邻接表表示每个顶点的**入边**（指向该顶点的边）。

The inverse adjacency list represents the **incoming edges** to each vertex.

```
A ← E(w:2) ← NULL
B ← A(w:3) ← NULL
C ← A(w:5) ← B(w:2) ← NULL
D ← B(w:4) ← C(w:1) ← NULL
E ← C(w:6) ← D(w:3) ← NULL
```

**说明 / Explanation:**
- 每行显示一个顶点及其所有入边的来源顶点和权重 / Each row shows a vertex and all its incoming edge sources with weights
- 箭头方向表示边的方向（← 表示指向当前顶点）/ Arrow direction shows edge direction (← points to current vertex)
- w: 表示权重 / w: represents weight

---

## 十字链表 / Orthogonal Linked List

十字链表是有向图的一种存储结构，同时存储每个顶点的出边和入边信息。

The orthogonal linked list is a storage structure for directed graphs that stores both outgoing and incoming edge information for each vertex.

**结构特点 / Structure Characteristics:**
- 行表示**出边**（从该顶点出发）/ Rows represent **outgoing edges** (from the vertex)
- 列表示**入边**（到达该顶点）/ Columns represent **incoming edges** (to the vertex)
- 每个位置显示边的权重或状态 / Each position shows edge weight or status

**图例 / Legend:**
- **数字**: 边的权重 / Number: edge weight
- **0**: 对角线（自己到自己）/ Diagonal (self to self)
- **∞**: 没有边（不可达）/ No edge (unreachable)

---

## 生成的图片 / Generated Images

### 1. directed_graph.png - 有向图可视化 / Directed Graph Visualization
显示所有顶点和有向边，边上标注了权重（红色数字），箭头显示方向。

Shows all vertices and directed edges with weights labeled in red and arrows showing direction.

### 2. vertex_degrees.png - 顶点度数 / Vertex Degrees
以表格形式显示每个顶点的入度和出度。

Displays in-degree and out-degree for each vertex in table format.

### 3. adjacency_matrix.png - 邻接矩阵可视化 / Adjacency Matrix Visualization
使用热力图显示邻接矩阵，颜色深度表示权重大小，∞ 用红色显示。

Displays the adjacency matrix as a heatmap with color intensity representing weight magnitude, ∞ shown in red.

### 4. adjacency_list.png - 邻接表可视化 / Adjacency List Visualization
用框图和箭头显示邻接表的链表结构（出边）。

Shows the linked list structure of the adjacency list (outgoing edges) using boxes and arrows.

### 5. inverse_adjacency_list.png - 逆邻接表可视化 / Inverse Adjacency List Visualization
用框图和箭头显示逆邻接表的链表结构（入边）。

Shows the linked list structure of the inverse adjacency list (incoming edges) using boxes and arrows.

### 6. orthogonal_list.png - 十字链表可视化 / Orthogonal Linked List Visualization
以矩阵形式显示十字链表结构，同时表示出边和入边。

Displays the orthogonal linked list structure in matrix form, representing both outgoing and incoming edges.

---

## 如何运行 / How to Run

### 环境要求 / Requirements

```bash
pip3 install matplotlib networkx numpy
```

### 执行程序 / Execute

```bash
cd directed_graph_visualization
python3 directed_weighted_graph.py
```

程序将自动生成6张可视化图片。

The program will automatically generate 6 visualization images.

---

## 文件结构 / File Structure

```
directed_graph_visualization/
├── directed_weighted_graph.py      # 主程序 / Main program
├── README.md                       # 本文件 / This file
├── directed_graph.png              # 有向图可视化 / Directed graph visualization
├── vertex_degrees.png              # 顶点度数 / Vertex degrees
├── adjacency_matrix.png            # 邻接矩阵 / Adjacency matrix
├── adjacency_list.png              # 邻接表 / Adjacency list
├── inverse_adjacency_list.png      # 逆邻接表 / Inverse adjacency list
└── orthogonal_list.png             # 十字链表 / Orthogonal linked list
```

---

## 有向图的特性 / Directed Graph Properties

- **类型 / Type**: 有向图 / Directed Graph
- **是否带权 / Weighted**: 是 / Yes
- **顶点数 / Number of Vertices**: 5
- **边数 / Number of Edges**: 8
- **是否强连通 / Strongly Connected**: 否 / No（存在环，但不是所有顶点都能互相到达 / Contains cycles but not all vertices are mutually reachable）

---

## 有向图与无向图的区别 / Differences from Undirected Graphs

| 特性 / Feature | 有向图 / Directed | 无向图 / Undirected |
|----------------|-------------------|---------------------|
| 边的方向 / Edge Direction | 有方向 / Has direction | 无方向 / No direction |
| 邻接矩阵 / Adjacency Matrix | 不对称 / Not symmetric | 对称 / Symmetric |
| 度数 / Degree | 分入度和出度 / In-degree and out-degree | 只有度数 / Only degree |
| 边的表示 / Edge Representation | A→B 和 B→A 是不同的边 / A→B and B→A are different | A-B 就是 B-A / A-B is same as B-A |

---

## 应用场景 / Applications

有向带权图可以用于建模：
- 交通网络（单行道）/ Transportation networks (one-way streets)
- 任务调度（依赖关系）/ Task scheduling (dependencies)
- 网页链接关系 / Web page link relationships
- 社交网络（关注关系）/ Social networks (follow relationships)
- 状态转换 / State transitions

Directed weighted graphs can model:
- Transportation networks with one-way roads
- Task scheduling with dependencies
- Web page link structures
- Social network follow relationships
- State transition systems

---

## 算法复杂度 / Algorithm Complexity

### 空间复杂度 / Space Complexity
- **邻接矩阵 / Adjacency Matrix**: O(V²) - V 是顶点数 / V is the number of vertices
- **邻接表 / Adjacency List**: O(V + E) - E 是边数 / E is the number of edges
- **逆邻接表 / Inverse Adjacency List**: O(V + E)
- **十字链表 / Orthogonal List**: O(V + E)

### 时间复杂度 / Time Complexity
- **查找边 / Find edge**:
  - 邻接矩阵 / Matrix: O(1)
  - 邻接表 / List: O(out-degree)
- **获取所有出边 / Get all outgoing edges**:
  - 邻接矩阵 / Matrix: O(V)
  - 邻接表 / List: O(out-degree)
- **获取所有入边 / Get all incoming edges**:
  - 邻接矩阵 / Matrix: O(V)
  - 逆邻接表 / Inverse list: O(in-degree)

---

## 总结 / Summary

本项目成功实现了：
✅ 构建了包含5个顶点、8条有向边的带权有向图
✅ 生成了有向图的可视化（带方向箭头）
✅ 计算并显示了每个顶点的入度和出度
✅ 生成了邻接矩阵及其可视化（∞表示不可达，0表示自己到自己）
✅ 生成了邻接表及其可视化（出边）
✅ 生成了逆邻接表及其可视化（入边）
✅ 生成了十字链表及其可视化
✅ 所有文件保存在独立的 directed_graph_visualization 文件夹中

This project successfully implements:
✅ A directed weighted graph with 5 vertices and 8 directed edges
✅ Directed graph visualization with directional arrows
✅ Calculation and display of in-degree and out-degree for each vertex
✅ Adjacency matrix and its visualization (∞ for unreachable, 0 for self)
✅ Adjacency list and its visualization (outgoing edges)
✅ Inverse adjacency list and its visualization (incoming edges)
✅ Orthogonal linked list and its visualization
✅ All files saved in separate directed_graph_visualization folder
