# Min-Heap Visualization

This project demonstrates the construction and operations of a min-heap data structure with visual representations.

## Overview

The project includes:
- A Python script (`min_heap_visualizer.py`) that builds a min-heap and generates visualizations
- A folder (`image/`) containing all generated visualization images

## Sequence Used

The integer sequence used for building the heap: **[50, 30, 20, 15, 10, 8, 16, 25, 40, 35]**

This sequence has a length of 10 elements (≥ 8 as required).

## Generated Images

### Heap Building Process (10 steps)
1. `step_01_insert_50.png` - Insert 50 (first element)
2. `step_02_insert_30.png` - Insert 30
3. `step_03_insert_20.png` - Insert 20
4. `step_04_insert_15.png` - Insert 15
5. `step_05_insert_10.png` - Insert 10
6. `step_06_insert_8.png` - Insert 8
7. `step_07_insert_16.png` - Insert 16
8. `step_08_insert_25.png` - Insert 25
9. `step_09_insert_40.png` - Insert 40
10. `step_10_insert_35.png` - Insert 35 (final heap)

**Final Min-Heap:** [8, 15, 10, 25, 20, 30, 16, 50, 40, 35]

### Operations
1. `operation_1_delete.png` - Delete minimum element (removed 8)
   - Result: [10, 15, 16, 25, 20, 30, 35, 50, 40]

2. `operation_2_insert.png` - Insert element 15
   - Result: [10, 15, 16, 25, 15, 30, 35, 50, 40, 20]

## How to Run

To regenerate the visualizations:

```bash
python3 min_heap_visualizer.py
```

## Requirements

- Python 3.x
- matplotlib
- networkx

Install dependencies:
```bash
pip3 install matplotlib networkx
```

## Min-Heap Properties

A min-heap is a complete binary tree where:
- The value of each node is less than or equal to the values of its children
- The minimum element is always at the root
- It's commonly used for priority queue implementations

The visualizations show how elements are inserted and how the heap property is maintained through heapify operations.
