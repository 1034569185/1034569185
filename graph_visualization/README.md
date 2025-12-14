# Undirected Weighted Graph Visualization / 无向带权图可视化

## 概述 / Overview

本项目实现了一个无向带权图的构建和可视化，包括：
1. 图的可视化
2. 邻接矩阵
3. 邻接表

This project implements an undirected weighted graph with visualizations including:
1. Graph visualization
2. Adjacency matrix
3. Adjacency list

---

## 图的结构 / Graph Structure

### 顶点 / Vertices
图包含 **6个顶点**：A, B, C, D, E, F

The graph contains **6 vertices**: A, B, C, D, E, F

### 边 / Edges
图包含 **10条边**（满足不少于6条边的要求）：

The graph contains **10 edges** (meeting the requirement of at least 6 edges):

| 边 / Edge | 权重 / Weight |
|-----------|---------------|
| A - B     | 4             |
| A - C     | 2             |
| A - D     | 7             |
| B - C     | 1             |
| B - E     | 5             |
| C - D     | 3             |
| C - E     | 8             |
| D - E     | 6             |
| E - F     | 2             |
| D - F     | 4             |

---

## 邻接矩阵 / Adjacency Matrix

邻接矩阵是一个 6×6 的矩阵，其中元素 matrix[i][j] 表示顶点 i 和顶点 j 之间边的权重。如果两个顶点之间没有边，则值为 0。

The adjacency matrix is a 6×6 matrix where element matrix[i][j] represents the weight of the edge between vertex i and vertex j. If there is no edge, the value is 0.

```
     A   B   C   D   E   F   
A    0   4   2   7   0   0
B    4   0   1   0   5   0
C    2   1   0   3   8   0
D    7   0   3   0   6   4
E    0   5   8   6   0   2
F    0   0   0   4   2   0
```

**特点 / Characteristics:**
- 对称矩阵（因为是无向图）/ Symmetric matrix (because it's an undirected graph)
- 主对角线全为 0（没有自环）/ Main diagonal is all 0 (no self-loops)
- 非零元素表示边的权重 / Non-zero elements represent edge weights

---

## 邻接表 / Adjacency List

邻接表用链表的形式表示每个顶点的相邻顶点及其边的权重。

The adjacency list represents each vertex's adjacent vertices and edge weights in linked list form.

```
A → B(weight:4) → C(weight:2) → D(weight:7) → NULL
B → A(weight:4) → C(weight:1) → E(weight:5) → NULL
C → A(weight:2) → B(weight:1) → D(weight:3) → E(weight:8) → NULL
D → A(weight:7) → C(weight:3) → E(weight:6) → F(weight:4) → NULL
E → B(weight:5) → C(weight:8) → D(weight:6) → F(weight:2) → NULL
F → D(weight:4) → E(weight:2) → NULL
```

**说明 / Explanation:**
- 每行表示一个顶点及其所有邻居 / Each row shows a vertex and all its neighbors
- 括号中的数字是边的权重 / Numbers in parentheses are edge weights
- NULL 表示链表结束 / NULL indicates end of linked list

---

## 生成的图片 / Generated Images

### 1. graph.png - 图的可视化 / Graph Visualization
显示所有顶点和边，边上标注了权重（红色数字）。

Shows all vertices and edges with weights labeled in red.

### 2. adjacency_matrix.png - 邻接矩阵可视化 / Adjacency Matrix Visualization
使用热力图显示邻接矩阵，颜色深度表示权重大小。

Displays the adjacency matrix as a heatmap where color intensity represents weight magnitude.

### 3. adjacency_list.png - 邻接表可视化 / Adjacency List Visualization
用框图和箭头显示邻接表的链表结构。

Shows the linked list structure of the adjacency list using boxes and arrows.

---

## 如何运行 / How to Run

### 环境要求 / Requirements

```bash
pip3 install matplotlib networkx numpy
```

### 执行程序 / Execute

```bash
cd graph_visualization
python3 undirected_weighted_graph.py
```

程序将自动生成三张可视化图片。

The program will automatically generate three visualization images.

---

## 文件结构 / File Structure

```
graph_visualization/
├── undirected_weighted_graph.py    # 主程序 / Main program
├── README.md                       # 本文件 / This file
├── graph.png                       # 图的可视化 / Graph visualization
├── adjacency_matrix.png            # 邻接矩阵 / Adjacency matrix
└── adjacency_list.png              # 邻接表 / Adjacency list
```

---

## 图的特性 / Graph Properties

- **类型 / Type**: 无向图 / Undirected Graph
- **是否带权 / Weighted**: 是 / Yes
- **顶点数 / Number of Vertices**: 6
- **边数 / Number of Edges**: 10
- **是否连通 / Connected**: 是 / Yes（所有顶点都可以互相到达 / All vertices are reachable from each other）

---

## 图的应用 / Graph Applications

无向带权图可以用于建模：
- 交通网络（城市间的距离）
- 社交网络（关系强度）
- 计算机网络（链路成本）
- 地图导航（路径长度）

Undirected weighted graphs can model:
- Transportation networks (distances between cities)
- Social networks (relationship strength)
- Computer networks (link costs)
- Map navigation (path lengths)

---

## 算法复杂度 / Algorithm Complexity

### 空间复杂度 / Space Complexity
- **邻接矩阵 / Adjacency Matrix**: O(V²) - V 是顶点数 / V is the number of vertices
- **邻接表 / Adjacency List**: O(V + E) - E 是边数 / E is the number of edges

### 时间复杂度 / Time Complexity
- **检查边是否存在 / Check edge existence**:
  - 邻接矩阵 / Matrix: O(1)
  - 邻接表 / List: O(V)
- **获取所有邻居 / Get all neighbors**:
  - 邻接矩阵 / Matrix: O(V)
  - 邻接表 / List: O(degree(V))

---

## 总结 / Summary

本项目成功实现了：
✅ 构建了包含6个顶点、10条边的无向带权图
✅ 生成了图的可视化
✅ 生成了邻接矩阵及其可视化
✅ 生成了邻接表及其可视化
✅ 所有文件保存在独立的 graph_visualization 文件夹中

This project successfully implements:
✅ An undirected weighted graph with 6 vertices and 10 edges
✅ Graph visualization
✅ Adjacency matrix and its visualization
✅ Adjacency list and its visualization
✅ All files saved in separate graph_visualization folder
