#!/usr/bin/env python3
"""
Min-Heap Visualization Tool - Build Heap Algorithm
Uses the proper build-heap algorithm: place all elements first, then heapify from bottom-up.
Shows complete step-by-step process for all operations.
"""

import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import networkx as nx
from typing import List, Tuple
import os

class MinHeapHeapify:
    """Min-heap implementation using build-heap algorithm with detailed visualization."""
    
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
    
    def heapify_down_step(self, i: int) -> Tuple[bool, int, int]:
        """
        Perform one step of heapify down operation.
        Returns: (swapped, current_index, swapped_with_index)
        """
        min_idx = i
        left = self.left_child(i)
        right = self.right_child(i)
        
        if left < len(self.heap) and self.heap[left] < self.heap[min_idx]:
            min_idx = left
        
        if right < len(self.heap) and self.heap[right] < self.heap[min_idx]:
            min_idx = right
        
        if min_idx != i:
            self.heap[i], self.heap[min_idx] = self.heap[min_idx], self.heap[i]
            return True, i, min_idx
        
        return False, i, i
    
    def heapify_down_complete(self, i: int, output_dir: str, operation_name: str, step_counter: List[int]):
        """
        Perform complete heapify down and visualize each step.
        """
        current = i
        while True:
            swapped, from_idx, to_idx = self.heapify_down_step(current)
            
            if swapped:
                step_counter[0] += 1
                filename = os.path.join(output_dir, f"{operation_name}_step_{step_counter[0]:02d}_swap_{from_idx}_{to_idx}.png")
                title = f"{operation_name} - Step {step_counter[0]}: Swap positions {from_idx}↔{to_idx} (values {self.heap[from_idx]}↔{self.heap[to_idx]})\nHeap: {self.heap}"
                self.visualize(filename, title, highlight_nodes=[from_idx, to_idx])
                print(f"  Step {step_counter[0]}: Swapped positions {from_idx}↔{to_idx} (values {self.heap[from_idx]}↔{self.heap[to_idx]})")
                current = to_idx
            else:
                break
    
    def heapify_up_complete(self, i: int, output_dir: str, operation_name: str, step_counter: List[int]):
        """
        Perform complete heapify up and visualize each step.
        """
        current = i
        while current > 0:
            parent_idx = self.parent(current)
            
            if self.heap[parent_idx] > self.heap[current]:
                # Need to swap
                step_counter[0] += 1
                self.heap[current], self.heap[parent_idx] = self.heap[parent_idx], self.heap[current]
                
                filename = os.path.join(output_dir, f"{operation_name}_step_{step_counter[0]:02d}_swap_{parent_idx}_{current}.png")
                title = f"{operation_name} - Step {step_counter[0]}: Swap positions {parent_idx}↔{current} (values {self.heap[parent_idx]}↔{self.heap[current]})\nHeap: {self.heap}"
                self.visualize(filename, title, highlight_nodes=[parent_idx, current])
                print(f"  Step {step_counter[0]}: Swapped positions {parent_idx}↔{current} (values {self.heap[parent_idx]}↔{self.heap[current]})")
                
                current = parent_idx
            else:
                break
    
    def build_heap(self, sequence: List[int], output_dir: str):
        """
        Build heap using the proper algorithm: place all elements, then heapify from bottom-up.
        """
        print(f"\n{'='*60}")
        print(f"Building Min-Heap from sequence: {sequence}")
        print(f"Using Build-Heap Algorithm (heapify from bottom-up)")
        print(f"{'='*60}\n")
        
        # Step 1: Place all elements in array
        self.heap = sequence.copy()
        step_num = 0
        
        filename = os.path.join(output_dir, f"build_step_{step_num:02d}_initial.png")
        title = f"Step {step_num}: Initial array (not yet a heap)\nHeap: {self.heap}"
        self.visualize(filename, title)
        print(f"Step {step_num}: Initial array: {self.heap}")
        
        # Step 2: Heapify from the last non-leaf node to root
        # Last non-leaf node is at index (n//2 - 1)
        start_idx = len(self.heap) // 2 - 1
        
        print(f"\nStarting heapify from index {start_idx} (last non-leaf node) down to 0...")
        
        for i in range(start_idx, -1, -1):
            step_num += 1
            print(f"\nStep {step_num}: Heapifying subtree rooted at index {i} (value={self.heap[i]})")
            
            # Save state before heapify
            filename = os.path.join(output_dir, f"build_step_{step_num:02d}_heapify_at_{i}_before.png")
            title = f"Step {step_num}: Before heapifying at index {i} (value={self.heap[i]})\nHeap: {self.heap}"
            self.visualize(filename, title, highlight_nodes=[i])
            
            # Perform heapify and track changes
            heap_before = self.heap.copy()
            current = i
            sub_step = 0
            
            while True:
                swapped, from_idx, to_idx = self.heapify_down_step(current)
                
                if swapped:
                    sub_step += 1
                    step_num += 1
                    filename = os.path.join(output_dir, f"build_step_{step_num:02d}_heapify_at_{i}_substep_{sub_step}.png")
                    title = f"Step {step_num}: Heapify at {i} - Swap positions {from_idx}↔{to_idx} (values {self.heap[from_idx]}↔{self.heap[to_idx]})\nHeap: {self.heap}"
                    self.visualize(filename, title, highlight_nodes=[from_idx, to_idx])
                    print(f"  Swapped positions {from_idx}↔{to_idx} (values {self.heap[from_idx]}↔{self.heap[to_idx]})")
                    current = to_idx
                else:
                    if heap_before == self.heap:
                        print(f"  No swaps needed (already satisfies heap property)")
                    break
        
        print(f"\n{'='*60}")
        print(f"Final Min-Heap: {self.heap}")
        print(f"{'='*60}\n")
        
        # Save final heap
        filename = os.path.join(output_dir, f"build_step_final.png")
        title = f"Final Min-Heap after build-heap algorithm\nHeap: {self.heap}"
        self.visualize(filename, title)
    
    def delete_min(self, output_dir: str):
        """Remove minimum element and show complete adjustment process."""
        print(f"\n{'='*60}")
        print("Delete Minimum Operation")
        print(f"{'='*60}\n")
        
        if len(self.heap) == 0:
            raise IndexError("Heap is empty")
        
        step_counter = [0]
        
        # Show initial state
        filename = os.path.join(output_dir, f"delete_step_{step_counter[0]:02d}_before.png")
        title = f"Delete Min - Before: Root has minimum value {self.heap[0]}\nHeap: {self.heap}"
        self.visualize(filename, title, highlight_nodes=[0])
        print(f"Step {step_counter[0]}: Before deletion, heap: {self.heap}")
        print(f"  Minimum value to delete: {self.heap[0]}")
        
        min_val = self.heap[0]
        
        # Replace root with last element
        step_counter[0] += 1
        self.heap[0] = self.heap[-1]
        self.heap.pop()
        
        filename = os.path.join(output_dir, f"delete_step_{step_counter[0]:02d}_replace_root.png")
        title = f"Delete Min - Step {step_counter[0]}: Replaced root with last element\nHeap: {self.heap}"
        self.visualize(filename, title, highlight_nodes=[0])
        print(f"Step {step_counter[0]}: Replaced root with last element, removed last position")
        print(f"  Current heap: {self.heap}")
        
        # Heapify down from root
        if len(self.heap) > 0:
            print(f"\nNow heapifying down from root...")
            self.heapify_down_complete(0, output_dir, "delete", step_counter)
        
        # Show final state
        step_counter[0] += 1
        filename = os.path.join(output_dir, f"delete_step_{step_counter[0]:02d}_final.png")
        title = f"Delete Min - Final: Deleted {min_val}\nHeap: {self.heap}"
        self.visualize(filename, title)
        print(f"\nStep {step_counter[0]}: Final heap after deletion: {self.heap}")
        
        print(f"\n{'='*60}")
        print(f"Deleted minimum value: {min_val}")
        print(f"Final heap: {self.heap}")
        print(f"{'='*60}\n")
        
        return min_val
    
    def insert(self, value: int, output_dir: str):
        """Insert a value and show complete adjustment process."""
        print(f"\n{'='*60}")
        print(f"Insert Operation - Value: {value}")
        print(f"{'='*60}\n")
        
        step_counter = [0]
        
        # Show initial state
        filename = os.path.join(output_dir, f"insert_step_{step_counter[0]:02d}_before.png")
        title = f"Insert {value} - Before insertion\nHeap: {self.heap}"
        self.visualize(filename, title)
        print(f"Step {step_counter[0]}: Before insertion, heap: {self.heap}")
        
        # Add element to end
        step_counter[0] += 1
        self.heap.append(value)
        new_idx = len(self.heap) - 1
        
        filename = os.path.join(output_dir, f"insert_step_{step_counter[0]:02d}_append.png")
        title = f"Insert {value} - Step {step_counter[0]}: Appended to end at position {new_idx}\nHeap: {self.heap}"
        self.visualize(filename, title, highlight_nodes=[new_idx])
        print(f"Step {step_counter[0]}: Appended {value} to position {new_idx}")
        print(f"  Current heap: {self.heap}")
        
        # Heapify up from new element
        if new_idx > 0:
            print(f"\nNow heapifying up from position {new_idx}...")
            self.heapify_up_complete(new_idx, output_dir, "insert", step_counter)
        
        # Show final state
        step_counter[0] += 1
        filename = os.path.join(output_dir, f"insert_step_{step_counter[0]:02d}_final.png")
        title = f"Insert {value} - Final: Successfully inserted\nHeap: {self.heap}"
        self.visualize(filename, title)
        print(f"\nStep {step_counter[0]}: Final heap after insertion: {self.heap}")
        
        print(f"\n{'='*60}")
        print(f"Inserted value: {value}")
        print(f"Final heap: {self.heap}")
        print(f"{'='*60}\n")
    
    def visualize(self, filename: str, title: str, highlight_nodes: List[int] = None):
        """
        Visualize the current state of the heap.
        """
        if len(self.heap) == 0:
            # Create empty figure for empty heap
            plt.figure(figsize=(12, 8))
            plt.text(0.5, 0.5, 'Empty Heap', ha='center', va='center', fontsize=20)
            plt.title(title, fontsize=16, fontweight='bold', pad=20)
            plt.axis('off')
            plt.tight_layout()
            plt.savefig(filename, dpi=150, bbox_inches='tight')
            plt.close()
            print(f"Saved: {filename}")
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
        plt.figure(figsize=(14, 10))
        
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
                              node_size=1000, node_shape='o', edgecolors='black', linewidths=2)
        
        # Draw labels (heap values)
        labels = {i: self.heap[i] for i in range(len(self.heap))}
        nx.draw_networkx_labels(G, pos, labels, font_size=14, font_weight='bold')
        
        plt.title(title, fontsize=14, fontweight='bold', pad=20)
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


def main():
    """Main function to run the heap visualization."""
    # Create output directory (relative to script location)
    script_dir = os.path.dirname(os.path.abspath(__file__))
    output_dir = os.path.join(script_dir, "image_heapify")
    os.makedirs(output_dir, exist_ok=True)
    
    # Design an integer sequence with length >= 8
    sequence = [50, 30, 20, 15, 10, 8, 16, 25, 40, 35]
    
    print(f"\n{'#'*60}")
    print("MIN-HEAP VISUALIZATION - BUILD HEAP ALGORITHM")
    print(f"{'#'*60}")
    
    # Build heap with proper algorithm
    heap = MinHeapHeapify()
    heap.build_heap(sequence, output_dir)
    
    # Demonstrate deletion operation
    heap.delete_min(output_dir)
    
    # Demonstrate insertion operation
    heap.insert(15, output_dir)
    
    print(f"\nAll images saved to: {output_dir}")
    print(f"Total images generated: {len([f for f in os.listdir(output_dir) if f.endswith('.png')])}")


if __name__ == "__main__":
    main()
