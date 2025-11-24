# Min-Heap Build-Heap Algorithm Visualization

## 概述 / Overview

本项目使用正确的**建堆算法**（Build-Heap Algorithm）实现小顶堆的可视化。与逐个插入不同，建堆算法先将所有元素放入数组，然后从最后一个非叶子节点开始向前调整（heapify），更高效且更符合标准算法。

This project implements min-heap visualization using the proper **Build-Heap Algorithm**. Unlike inserting elements one by one, this algorithm places all elements in an array first, then heapifies from the last non-leaf node backwards - more efficient and standard.

## 文件结构 / File Structure

```
.
├── min_heap_heapify.py          # 建堆算法实现 / Build-heap implementation
├── image_heapify/               # 图片输出目录 / Image output directory
│   ├── build_step_*.png        # 建堆过程图片 / Heap building steps
│   ├── delete_step_*.png       # 删除操作图片 / Deletion operation steps
│   └── insert_step_*.png       # 插入操作图片 / Insertion operation steps
├── min_heap_visualizer.py      # 旧实现（逐个插入）/ Old implementation (insert one-by-one)
└── image/                       # 旧实现图片 / Old implementation images
```

## 算法说明 / Algorithm Description

### 建堆过程 / Heap Building Process

1. **初始化**：将所有元素放入数组
   - Initial: Place all elements in array
   
2. **找到最后一个非叶子节点**：索引为 `n//2 - 1`
   - Find last non-leaf node: index `n//2 - 1`
   
3. **从后向前调整**：对每个非叶子节点执行 heapify-down
   - Heapify backwards: perform heapify-down on each non-leaf node
   
4. **完成**：所有节点满足堆性质
   - Complete: all nodes satisfy heap property

### 使用的序列 / Sequence Used

**序列 / Sequence**: `[50, 30, 20, 15, 10, 8, 16, 25, 40, 35]`

- 长度 / Length: 10 个元素 / elements
- 最后一个非叶子节点 / Last non-leaf node: 索引 4 / index 4 (值 / value 10)

## 生成的图片 / Generated Images

### 1. 建堆过程 / Heap Building (11 images)

- `build_step_00_initial.png` - 初始数组（尚未成堆）/ Initial array (not yet a heap)
- `build_step_01_heapify_at_4_before.png` - 开始调整索引4 / Start heapifying at index 4
- `build_step_02_heapify_at_3_before.png` - 调整索引3 / Heapify at index 3
- `build_step_03_heapify_at_2_before.png` - 调整索引2（开始）/ Heapify at index 2 (start)
- `build_step_04_heapify_at_2_substep_1.png` - 索引2调整（交换2↔5）/ Index 2 adjustment (swap 2↔5)
- `build_step_05_heapify_at_1_before.png` - 调整索引1（开始）/ Heapify at index 1 (start)
- `build_step_06_heapify_at_1_substep_1.png` - 索引1调整（交换1↔4）/ Index 1 adjustment (swap 1↔4)
- `build_step_07_heapify_at_0_before.png` - 调整索引0（开始）/ Heapify at index 0 (start)
- `build_step_08_heapify_at_0_substep_1.png` - 索引0调整步骤1（交换0↔2）/ Index 0 step 1 (swap 0↔2)
- `build_step_09_heapify_at_0_substep_2.png` - 索引0调整步骤2（交换2↔6）/ Index 0 step 2 (swap 2↔6)
- `build_step_final.png` - 最终小顶堆 / Final min-heap

**最终堆 / Final Heap**: `[8, 10, 16, 15, 30, 20, 50, 25, 40, 35]`

### 2. 删除操作 / Deletion Operation (6 images)

删除最小元素（根节点）并显示完整调整过程：
Delete minimum element (root) and show complete adjustment process:

- `delete_step_00_before.png` - 删除前状态 / Before deletion
- `delete_step_01_replace_root.png` - 用最后元素替换根节点 / Replace root with last element
- `delete_step_02_swap_0_1.png` - 调整步骤1：交换位置0↔1 / Step 1: swap 0↔1
- `delete_step_03_swap_1_3.png` - 调整步骤2：交换位置1↔3 / Step 2: swap 1↔3
- `delete_step_04_swap_3_7.png` - 调整步骤3：交换位置3↔7 / Step 3: swap 3↔7
- `delete_step_05_final.png` - 删除后最终状态 / Final state after deletion

**结果 / Result**: 删除了8 / Deleted 8，最终堆 / Final heap: `[10, 15, 16, 25, 30, 20, 50, 35, 40]`

### 3. 插入操作 / Insertion Operation (4 images)

插入新元素并显示完整调整过程：
Insert new element and show complete adjustment process:

- `insert_step_00_before.png` - 插入前状态 / Before insertion
- `insert_step_01_append.png` - 将元素添加到末尾 / Append element to end
- `insert_step_02_swap_4_9.png` - 向上调整：交换位置4↔9 / Heapify up: swap 4↔9
- `insert_step_03_final.png` - 插入后最终状态 / Final state after insertion

**结果 / Result**: 插入了15 / Inserted 15，最终堆 / Final heap: `[10, 15, 16, 25, 15, 20, 50, 35, 40, 30]`

## 关键改进 / Key Improvements

相比之前的实现：
Compared to previous implementation:

1. ✅ **正确的建堆算法** / Correct build-heap algorithm
   - 先放入所有元素，再从后向前调整 / Place all elements first, then heapify backwards
   - 时间复杂度 O(n) vs O(n log n) / Time complexity O(n) vs O(n log n)

2. ✅ **完整的调整过程** / Complete adjustment process
   - 显示删除操作的每一步交换 / Shows every swap in deletion
   - 显示插入操作的每一步交换 / Shows every swap in insertion

3. ✅ **分离的输出目录** / Separate output directory
   - 新结果在 `image_heapify/` / New results in `image_heapify/`
   - 旧结果保留在 `image/` / Old results kept in `image/`

4. ✅ **更详细的可视化** / More detailed visualization
   - 高亮显示交换的节点 / Highlighted swapping nodes
   - 每个子步骤都有图片 / Image for each substep

## 运行方法 / How to Run

### 环境要求 / Requirements

```bash
pip3 install matplotlib networkx
```

### 执行程序 / Execute

```bash
python3 min_heap_heapify.py
```

程序将：
The program will:
- 创建 `image_heapify/` 目录 / Create `image_heapify/` directory
- 生成21张可视化图片 / Generate 21 visualization images
- 在控制台输出详细步骤 / Print detailed steps to console

## 算法复杂度 / Algorithm Complexity

- **建堆 / Build Heap**: O(n) - 比逐个插入的 O(n log n) 更高效 / More efficient than O(n log n) for inserting one by one
- **插入 / Insert**: O(log n) - 需要向上调整 / Requires heapify up
- **删除最小值 / Delete Min**: O(log n) - 需要向下调整 / Requires heapify down

## 总结 / Summary

本实现展示了：
This implementation demonstrates:

✅ 标准的建堆算法（从后向前heapify）
✅ Standard build-heap algorithm (heapify backwards)

✅ 完整的操作调整过程可视化
✅ Complete visualization of operation adjustments

✅ 21张详细的步骤图片
✅ 21 detailed step-by-step images

✅ 与之前实现分离的新目录
✅ New directory separate from previous implementation
