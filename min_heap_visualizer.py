#!/usr/bin/env python3
"""
Min-Heap Visualization Tool
Creates visualizations of min-heap building process, deletion, and insertion operations.
"""

import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import networkx as nx
from typing import List, Tuple
import os

class MinHeap:
    """Min-heap implementation with visualization capabilities."""
    
    def __init__(self):
        self.heap = []
        self.step_count = 0
    
    def parent(self, i: int) -> int:
        """Get parent index."""
        return (i - 1) // 2
    
    def left_child(self, i: int) -> int:
        """Get left child index."""
        return 2 * i + 1
    
    def right_child(self, i: int) -> int:
        """Get right child index."""
        return 2 * i + 2
    
    def heapify_up(self, i: int):
        """Move element up to maintain heap property."""
        while i > 0 and self.heap[self.parent(i)] > self.heap[i]:
            # Swap with parent
            parent_idx = self.parent(i)
            self.heap[i], self.heap[parent_idx] = self.heap[parent_idx], self.heap[i]
            i = parent_idx
    
    def heapify_down(self, i: int):
        """Move element down to maintain heap property."""
        min_idx = i
        left = self.left_child(i)
        right = self.right_child(i)
        
        if left < len(self.heap) and self.heap[left] < self.heap[min_idx]:
            min_idx = left
        
        if right < len(self.heap) and self.heap[right] < self.heap[min_idx]:
            min_idx = right
        
        if min_idx != i:
            self.heap[i], self.heap[min_idx] = self.heap[min_idx], self.heap[i]
            self.heapify_down(min_idx)
    
    def insert(self, value: int):
        """Insert a value into the heap."""
        self.heap.append(value)
        self.heapify_up(len(self.heap) - 1)
    
    def delete_min(self) -> int:
        """Remove and return the minimum element."""
        if len(self.heap) == 0:
            raise IndexError("Heap is empty")
        
        min_val = self.heap[0]
        
        # Move last element to root and heapify down
        self.heap[0] = self.heap[-1]
        self.heap.pop()
        
        if len(self.heap) > 0:
            self.heapify_down(0)
        
        return min_val
    
    def visualize(self, filename: str, title: str, highlight_nodes: List[int] = None):
        """
        Visualize the current state of the heap.
        
        Args:
            filename: Output filename for the image
            title: Title for the visualization
            highlight_nodes: List of node indices to highlight
        """
        if len(self.heap) == 0:
            return
        
        # Create a directed graph
        G = nx.DiGraph()
        
        # Add nodes
        for i in range(len(self.heap)):
            G.add_node(i, value=self.heap[i])
        
        # Add edges
        for i in range(len(self.heap)):
            left = self.left_child(i)
            right = self.right_child(i)
            
            if left < len(self.heap):
                G.add_edge(i, left)
            if right < len(self.heap):
                G.add_edge(i, right)
        
        # Calculate positions for tree layout
        pos = self._hierarchy_pos(G, 0)
        
        # Create figure
        plt.figure(figsize=(12, 8))
        
        # Draw edges
        nx.draw_networkx_edges(G, pos, edge_color='gray', arrows=False, width=2)
        
        # Prepare node colors
        node_colors = []
        for i in range(len(self.heap)):
            if highlight_nodes and i in highlight_nodes:
                node_colors.append('#ffcccc')  # Light red for highlighted
            else:
                node_colors.append('#add8e6')  # Light blue for normal
        
        # Draw nodes
        nx.draw_networkx_nodes(G, pos, node_color=node_colors, 
                              node_size=800, node_shape='o')
        
        # Draw labels (heap values)
        labels = {i: self.heap[i] for i in range(len(self.heap))}
        nx.draw_networkx_labels(G, pos, labels, font_size=14, font_weight='bold')
        
        plt.title(title, fontsize=16, fontweight='bold', pad=20)
        plt.axis('off')
        plt.tight_layout()
        
        # Save figure
        plt.savefig(filename, dpi=150, bbox_inches='tight')
        plt.close()
        
        print(f"Saved: {filename}")
    
    def _hierarchy_pos(self, G, root, width=1., vert_gap=0.2, vert_loc=0, xcenter=0.5):
        """
        Create hierarchical layout for tree visualization.
        """
        pos = {}
        
        def _pos_recursive(node, x, y, width):
            """Recursively calculate positions for tree nodes."""
            pos[node] = (x, y)
            children = list(G.neighbors(node))
            
            if children:
                # Calculate spacing for children
                dx = width / len(children)
                next_x = x - width/2 + dx/2
                
                for child in children:
                    _pos_recursive(child, next_x, y - vert_gap, dx)
                    next_x += dx
        
        _pos_recursive(root, xcenter, vert_loc, width)
        return pos


def build_heap_with_visualization(sequence: List[int], output_dir: str):
    """
    Build a min-heap from a sequence and visualize each step.
    
    Args:
        sequence: List of integers to build heap from
        output_dir: Directory to save visualization images
    """
    heap = MinHeap()
    
    print(f"\n{'='*60}")
    print(f"Building Min-Heap from sequence: {sequence}")
    print(f"{'='*60}\n")
    
    # Insert elements one by one and visualize
    for idx, value in enumerate(sequence):
        heap.insert(value)
        step_num = idx + 1
        filename = os.path.join(output_dir, f"step_{step_num:02d}_insert_{value}.png")
        title = f"Step {step_num}: Insert {value} - Heap: {heap.heap}"
        heap.visualize(filename, title)
        print(f"Step {step_num}: Inserted {value}, Heap: {heap.heap}")
    
    print(f"\n{'='*60}")
    print(f"Final Min-Heap: {heap.heap}")
    print(f"{'='*60}\n")
    
    return heap


def demonstrate_operations(heap: MinHeap, output_dir: str, insert_value: int = 15):
    """
    Demonstrate deletion and insertion operations on the heap.
    
    Args:
        heap: The min-heap to operate on
        output_dir: Directory to save visualization images
        insert_value: Value to insert in the insertion operation (default: 15)
    """
    print(f"\n{'='*60}")
    print("Demonstrating Operations")
    print(f"{'='*60}\n")
    
    # Deletion operation
    print("Before deletion:", heap.heap)
    deleted_value = heap.delete_min()
    print(f"Deleted minimum value: {deleted_value}")
    print("After deletion:", heap.heap)
    
    heap.visualize(
        os.path.join(output_dir, "operation_1_delete.png"),
        f"After Deletion (removed {deleted_value}) - Heap: {heap.heap}"
    )
    
    # Insertion operation
    print(f"\nInserting new value: {insert_value}")
    heap.insert(insert_value)
    print("After insertion:", heap.heap)
    
    heap.visualize(
        os.path.join(output_dir, "operation_2_insert.png"),
        f"After Insertion (added {insert_value}) - Heap: {heap.heap}"
    )
    
    print(f"\n{'='*60}")
    print("Operations completed!")
    print(f"{'='*60}\n")


def main():
    """Main function to run the heap visualization."""
    # Create output directory (relative to script location)
    script_dir = os.path.dirname(os.path.abspath(__file__))
    output_dir = os.path.join(script_dir, "image")
    os.makedirs(output_dir, exist_ok=True)
    
    # Design an integer sequence with length >= 8
    # Using a sequence that will demonstrate heap building clearly
    sequence = [50, 30, 20, 15, 10, 8, 16, 25, 40, 35]
    
    print(f"\n{'#'*60}")
    print("MIN-HEAP VISUALIZATION PROGRAM")
    print(f"{'#'*60}")
    
    # Build heap with visualization
    heap = build_heap_with_visualization(sequence, output_dir)
    
    # Demonstrate operations
    demonstrate_operations(heap, output_dir)
    
    print(f"\nAll images saved to: {output_dir}")
    print(f"Total images generated: {len([f for f in os.listdir(output_dir) if f.endswith('.png')])}")


if __name__ == "__main__":
    main()
