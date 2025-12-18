# Minimum Spanning Tree (MST) Algorithms Visualization

[中文说明在下方 | Chinese version below]

## English Version

This project visualizes two classic algorithms for finding the Minimum Spanning Tree (MST) of a weighted undirected connected graph: **Prim's Algorithm** and **Kruskal's Algorithm**.

### Graph Structure

- **Vertices**: 5 vertices (A, B, C, D, E) - exceeds minimum requirement of 4
- **Edges**: 8 weighted edges - exceeds minimum requirement of 6
- **Graph Type**: Weighted, undirected, and connected
- **Edges with Weights**:
  - A-B: 4
  - A-C: 2
  - A-D: 7
  - B-C: 1
  - B-E: 5
  - C-D: 3
  - C-E: 8
  - D-E: 6

### Prim's Algorithm Visualization

**Algorithm Description**:
Prim's algorithm builds the MST by starting from a single vertex and repeatedly adding the minimum-weight edge that connects a vertex in the MST (set U) to a vertex outside the MST (set V-U).

**Visualization Features**:
- **Green nodes**: Vertices in U set (already in MST)
- **Yellow nodes**: Vertices in V-U set (not yet in MST)
- **Red edges**: Edges already added to MST
- **Gold dashed edges**: Current candidate edge being considered
- **Step-by-step process**: Shows 5 iterations from initial state to complete MST

**Results**:
- Starting vertex: A
- MST edges: (A,C), (C,B), (C,D), (B,E)
- Total MST weight: 11
- Steps shown: Initial state + 4 edge additions

### Kruskal's Algorithm Visualization

**Algorithm Description**:
Kruskal's algorithm builds the MST by sorting all edges by weight and adding them one by one, skipping edges that would create a cycle. Uses Union-Find data structure to detect cycles.

**Visualization Features**:
- **Different colors**: Each equivalence class (connected component) shown in a different color
- **Red thick edges**: Edges already added to MST
- **Green solid edge**: Edge being added in current step
- **Orange dashed edge**: Edge being rejected (would create cycle)
- **Equivalence classes**: Shows how vertices merge into larger components

**Results**:
- MST edges (in order of addition): (B,C), (A,C), (C,D), (B,E)
- Total MST weight: 11
- Steps shown: Initial state + processing all 8 edges (4 accepted, 4 rejected)
- Color scheme: 5 distinct colors for different equivalence classes

### Key Observations

1. **Same MST Weight**: Both algorithms produce MST with total weight 11, though edge selection order differs
2. **Prim's Algorithm**: Grows one tree from a starting vertex
3. **Kruskal's Algorithm**: Grows multiple trees (forests) that eventually merge
4. **No Chinese Characters**: All text is in English to avoid encoding issues

### Generated Files

1. **graph.png** (168 KB)
   - Original weighted undirected connected graph
   - Shows all 5 vertices and 8 weighted edges
   - Clear layout with edge weights labeled in red

2. **prim_steps.png** (720 KB)
   - Complete step-by-step visualization of Prim's algorithm
   - 5 steps showing progression from start vertex to complete MST
   - Color-coded U and V-U sets
   - Each step shows current state of MST construction

3. **kruskal_steps.png** (840 KB)
   - Complete step-by-step visualization of Kruskal's algorithm
   - 6 steps showing edge consideration and equivalence class merging
   - Color-coded equivalence classes
   - Shows both accepted and rejected edges

### Usage

```bash
cd mst_algorithms
python3 mst_visualizer.py
```

This will generate all three visualization images in the `mst_algorithms/` directory.

### Algorithm Complexity

- **Prim's Algorithm**: O(E log V) with binary heap
- **Kruskal's Algorithm**: O(E log E) = O(E log V) due to sorting

Where E = number of edges, V = number of vertices.

---

## 中文版本

本项目可视化了两个经典的最小生成树(MST)算法：**Prim算法**和**Kruskal算法**。

### 图结构

- **顶点数**：5个顶点 (A, B, C, D, E) - 超过最少4个的要求
- **边数**：8条带权边 - 超过最少6条的要求
- **图类型**：带权、无向、连通图
- **边及权重**：
  - A-B: 4
  - A-C: 2
  - A-D: 7
  - B-C: 1
  - B-E: 5
  - C-D: 3
  - C-E: 8
  - D-E: 6

### Prim算法可视化

**算法描述**：
Prim算法从单个顶点开始构建MST，每次选择连接U集合（已在MST中）和V-U集合（不在MST中）的最小权重边。

**可视化特点**：
- **绿色节点**：U集合中的顶点（已在MST中）
- **黄色节点**：V-U集合中的顶点（尚未加入MST）
- **红色边**：已添加到MST的边
- **金色虚线边**：当前正在考虑的候选边
- **分步过程**：展示从初始状态到完整MST的5次迭代

**结果**：
- 起始顶点：A
- MST边：(A,C), (C,B), (C,D), (B,E)
- MST总权重：11
- 显示步骤：初始状态 + 4次边添加

### Kruskal算法可视化

**算法描述**：
Kruskal算法按权重对所有边排序，逐个添加边，跳过会形成环的边。使用并查集数据结构检测环。

**可视化特点**：
- **不同颜色**：每个等价类（连通分量）用不同颜色显示
- **红色粗边**：已添加到MST的边
- **绿色实线边**：当前步骤中被添加的边
- **橙色虚线边**：被拒绝的边（会形成环）
- **等价类**：显示顶点如何合并成更大的分量

**结果**：
- MST边（按添加顺序）：(B,C), (A,C), (C,D), (B,E)
- MST总权重：11
- 显示步骤：初始状态 + 处理全部8条边（4条接受，4条拒绝）
- 配色方案：5种不同颜色表示不同的等价类

### 关键观察

1. **相同MST权重**：两种算法产生的MST总权重都是11，虽然边的选择顺序不同
2. **Prim算法**：从起始顶点生长一棵树
3. **Kruskal算法**：生长多棵树（森林），最终合并
4. **无中文字符**：所有文本使用英文以避免编码问题

### 生成的文件

1. **graph.png** (168 KB)
   - 原始带权无向连通图
   - 显示全部5个顶点和8条带权边
   - 清晰的布局，边权重用红色标注

2. **prim_steps.png** (720 KB)
   - Prim算法的完整分步可视化
   - 5个步骤展示从起始顶点到完整MST的过程
   - U和V-U集合用颜色区分
   - 每步显示MST构建的当前状态

3. **kruskal_steps.png** (840 KB)
   - Kruskal算法的完整分步可视化
   - 6个步骤展示边的考虑和等价类的合并
   - 等价类用颜色区分
   - 显示接受和拒绝的边

### 使用方法

```bash
cd mst_algorithms
python3 mst_visualizer.py
```

这将在 `mst_algorithms/` 目录中生成全部三个可视化图像。

### 算法复杂度

- **Prim算法**：使用二叉堆时为 O(E log V)
- **Kruskal算法**：O(E log E) = O(E log V)（由于排序）

其中 E = 边数，V = 顶点数。

---

## Technical Details

### Implementation

- **Language**: Python 3
- **Libraries**: 
  - matplotlib 3.10.8 - for visualization
  - networkx 3.6.1 - for graph data structures
  - numpy 2.3.5 - for numerical operations
- **Data Structures**:
  - Union-Find with path compression and union by rank
  - Priority queue (implicit in edge selection)
- **Visualization**: Non-interactive backend (Agg) for server-side rendering

### Code Structure

```
mst_algorithms/
├── mst_visualizer.py    # Main implementation
├── README.md            # This file
├── graph.png            # Original graph
├── prim_steps.png       # Prim's algorithm visualization
└── kruskal_steps.png    # Kruskal's algorithm visualization
```

### Features

- ✅ Graph exceeds minimum requirements (5 vertices > 4, 8 edges > 6)
- ✅ Prim's algorithm with U and V-U sets in different colors
- ✅ Kruskal's algorithm with equivalence classes in different colors
- ✅ Step-by-step visualization showing detailed process
- ✅ No Chinese characters to avoid encoding issues
- ✅ High-quality PNG images (150 DPI)
- ✅ Clear legends and annotations
- ✅ Professional color schemes
- ✅ Comprehensive bilingual documentation

---

## References

- **Prim's Algorithm**: R. C. Prim (1957). "Shortest connection networks and some generalizations"
- **Kruskal's Algorithm**: Joseph Kruskal (1956). "On the shortest spanning subtree of a graph"
- **Union-Find**: Robert Tarjan (1975). "Efficiency of a good but not linear set union algorithm"

---

*Generated by MST Visualizer - December 2025*
