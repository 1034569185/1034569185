#!/usr/bin/env python3
"""
Directed Weighted Graph Visualization
Creates a weighted directed graph and visualizes:
1. The directed graph itself
2. In-degree and out-degree for each vertex
3. Adjacency matrix (∞ for unreachable, 0 for self)
4. Adjacency list
5. Inverse adjacency list
6. Orthogonal linked list (十字链表)
"""

import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import networkx as nx
import numpy as np
import os
from typing import Dict, List, Tuple

class DirectedWeightedGraph:
    """Directed weighted graph implementation with comprehensive visualization."""
    
    def __init__(self):
        self.graph = nx.DiGraph()
        self.vertices = []
        self.edges = []
    
    def add_vertex(self, vertex):
        """Add a vertex to the graph."""
        if vertex not in self.vertices:
            self.vertices.append(vertex)
            self.graph.add_node(vertex)
    
    def add_edge(self, from_vertex, to_vertex, weight):
        """Add a weighted directed edge from from_vertex to to_vertex."""
        self.add_vertex(from_vertex)
        self.add_vertex(to_vertex)
        self.graph.add_edge(from_vertex, to_vertex, weight=weight)
        self.edges.append((from_vertex, to_vertex, weight))
    
    def get_degrees(self):
        """Get in-degree and out-degree for each vertex."""
        sorted_vertices = sorted(self.vertices)
        degrees = {}
        
        for vertex in sorted_vertices:
            in_degree = self.graph.in_degree(vertex)
            out_degree = self.graph.out_degree(vertex)
            degrees[vertex] = {'in': in_degree, 'out': out_degree}
        
        return degrees
    
    def get_adjacency_matrix(self):
        """Generate the adjacency matrix with ∞ for unreachable vertices."""
        sorted_vertices = sorted(self.vertices)
        n = len(sorted_vertices)
        
        # Create matrix with infinity for unreachable vertices
        matrix = np.full((n, n), np.inf, dtype=float)
        
        # Fill matrix
        for i, v1 in enumerate(sorted_vertices):
            for j, v2 in enumerate(sorted_vertices):
                if i == j:
                    # Diagonal: self to self is 0
                    matrix[i][j] = 0
                elif self.graph.has_edge(v1, v2):
                    weight = self.graph[v1][v2]['weight']
                    matrix[i][j] = weight
                # else: remains infinity (no edge)
        
        return matrix, sorted_vertices
    
    def get_adjacency_list(self):
        """Generate the adjacency list (outgoing edges)."""
        sorted_vertices = sorted(self.vertices)
        adj_list = {}
        
        for vertex in sorted_vertices:
            neighbors = []
            for neighbor in self.graph.successors(vertex):  # Outgoing edges
                weight = self.graph[vertex][neighbor]['weight']
                neighbors.append((neighbor, weight))
            # Sort neighbors by name
            neighbors.sort(key=lambda x: x[0])
            adj_list[vertex] = neighbors
        
        return adj_list
    
    def get_inverse_adjacency_list(self):
        """Generate the inverse adjacency list (incoming edges)."""
        sorted_vertices = sorted(self.vertices)
        inv_adj_list = {}
        
        for vertex in sorted_vertices:
            predecessors = []
            for predecessor in self.graph.predecessors(vertex):  # Incoming edges
                weight = self.graph[predecessor][vertex]['weight']
                predecessors.append((predecessor, weight))
            # Sort predecessors by name
            predecessors.sort(key=lambda x: x[0])
            inv_adj_list[vertex] = predecessors
        
        return inv_adj_list
    
    def visualize_directed_graph(self, output_file: str):
        """Visualize the directed weighted graph with clear arrows and curved edges."""
        plt.figure(figsize=(14, 10))
        
        # Use spring layout for better visualization
        pos = nx.spring_layout(self.graph, seed=42, k=2, iterations=50)
        
        # Define visualization parameters
        NODE_SIZE = 2000
        NODE_BORDER_WIDTH = 2.5
        EDGE_WIDTH = 2.5
        ARROW_SIZE = 25
        MARGIN = 15
        
        # Draw nodes
        nx.draw_networkx_nodes(self.graph, pos, 
                              node_color='lightblue',
                              node_size=NODE_SIZE,
                              edgecolors='black',
                              linewidths=NODE_BORDER_WIDTH)
        
        # Draw edges with curved arrows for better visibility
        # Use connectionstyle to create curved edges
        nx.draw_networkx_edges(self.graph, pos,
                              width=EDGE_WIDTH,
                              edge_color='darkblue',
                              arrows=True,
                              arrowsize=ARROW_SIZE,
                              arrowstyle='->',
                              connectionstyle='arc3,rad=0.1',  # Curved edges
                              node_size=NODE_SIZE,
                              min_source_margin=MARGIN,
                              min_target_margin=MARGIN)
        
        # Draw labels
        nx.draw_networkx_labels(self.graph, pos,
                               font_size=18,
                               font_weight='bold')
        
        # Draw edge labels (weights) with better positioning
        edge_labels = nx.get_edge_attributes(self.graph, 'weight')
        nx.draw_networkx_edge_labels(self.graph, pos,
                                     edge_labels,
                                     font_size=14,
                                     font_color='red',
                                     font_weight='bold',
                                     bbox=dict(boxstyle='round,pad=0.3', 
                                             facecolor='white', 
                                             edgecolor='none',
                                             alpha=0.7))
        
        plt.title("Directed Weighted Graph", fontsize=18, fontweight='bold', pad=20)
        plt.axis('off')
        plt.tight_layout()
        plt.savefig(output_file, dpi=150, bbox_inches='tight')
        plt.close()
        
        print(f"Saved directed graph visualization: {output_file}")
    
    def visualize_degrees(self, output_file: str):
        """Visualize in-degree and out-degree for each vertex."""
        degrees = self.get_degrees()
        
        fig, ax = plt.subplots(figsize=(12, 8))
        ax.axis('off')
        
        # Title
        ax.text(0.5, 0.95, "Vertex Degrees (In-Degree and Out-Degree)", 
               ha='center', va='top',
               fontsize=18, fontweight='bold',
               transform=ax.transAxes)
        
        # Create table
        vertices = sorted(degrees.keys())
        n = len(vertices)
        
        # Table header
        header_y = 0.85
        ax.text(0.2, header_y, "Vertex", ha='center', va='center',
               fontsize=14, fontweight='bold', transform=ax.transAxes)
        ax.text(0.5, header_y, "In-Degree", ha='center', va='center',
               fontsize=14, fontweight='bold', transform=ax.transAxes)
        ax.text(0.8, header_y, "Out-Degree", ha='center', va='center',
               fontsize=14, fontweight='bold', transform=ax.transAxes)
        
        # Draw header line
        ax.plot([0.05, 0.95], [header_y - 0.03, header_y - 0.03], 
               'k-', lw=2, transform=ax.transAxes)
        
        # Table rows
        row_height = 0.08
        for idx, vertex in enumerate(vertices):
            y_pos = header_y - 0.06 - idx * row_height
            
            # Vertex name
            ax.text(0.2, y_pos, str(vertex), ha='center', va='center',
                   fontsize=13, fontweight='bold', transform=ax.transAxes)
            
            # In-degree
            ax.text(0.5, y_pos, str(degrees[vertex]['in']), ha='center', va='center',
                   fontsize=13, transform=ax.transAxes)
            
            # Out-degree
            ax.text(0.8, y_pos, str(degrees[vertex]['out']), ha='center', va='center',
                   fontsize=13, transform=ax.transAxes)
        
        plt.tight_layout()
        plt.savefig(output_file, dpi=150, bbox_inches='tight')
        plt.close()
        
        print(f"Saved vertex degrees: {output_file}")
    
    def visualize_adjacency_matrix(self, output_file: str):
        """Visualize the adjacency matrix."""
        matrix, vertices = self.get_adjacency_matrix()
        n = len(vertices)
        
        fig, ax = plt.subplots(figsize=(10, 10))
        
        # Create a display matrix for coloring
        display_matrix = matrix.copy()
        finite_values = matrix[~np.isinf(matrix)]
        if len(finite_values) > 0:
            max_weight = np.max(finite_values)
        else:
            max_weight = 1
        display_matrix[np.isinf(display_matrix)] = max_weight + 1
        
        # Create a color map
        cmap = plt.cm.Blues
        im = ax.imshow(display_matrix, cmap=cmap, aspect='auto', vmin=0, vmax=max_weight)
        
        # Add colorbar
        cbar = plt.colorbar(im, ax=ax)
        cbar.set_label('Edge Weight', rotation=270, labelpad=20, fontsize=12)
        
        # Set ticks
        ax.set_xticks(np.arange(n))
        ax.set_yticks(np.arange(n))
        ax.set_xticklabels(vertices, fontsize=12, fontweight='bold')
        ax.set_yticklabels(vertices, fontsize=12, fontweight='bold')
        
        # Rotate the tick labels
        plt.setp(ax.get_xticklabels(), rotation=0, ha="center")
        
        # Add text annotations
        for i in range(n):
            for j in range(n):
                if np.isinf(matrix[i, j]):
                    text_str = "∞"
                    text_color = "red"
                else:
                    text_str = str(int(matrix[i, j]))
                    text_color = "black" if matrix[i, j] < max_weight/2 else "white"
                
                ax.text(j, i, text_str,
                       ha="center", va="center",
                       color=text_color,
                       fontsize=14, fontweight='bold')
        
        ax.set_title("Adjacency Matrix (Directed Graph)", fontsize=16, fontweight='bold', pad=20)
        ax.set_xlabel("To Vertex", fontsize=14, fontweight='bold')
        ax.set_ylabel("From Vertex", fontsize=14, fontweight='bold')
        
        # Add grid
        ax.set_xticks(np.arange(n)-.5, minor=True)
        ax.set_yticks(np.arange(n)-.5, minor=True)
        ax.grid(which="minor", color="black", linestyle='-', linewidth=2)
        
        plt.tight_layout()
        plt.savefig(output_file, dpi=150, bbox_inches='tight')
        plt.close()
        
        print(f"Saved adjacency matrix: {output_file}")
    
    def visualize_adjacency_list(self, output_file: str):
        """Visualize the adjacency list (outgoing edges)."""
        adj_list = self.get_adjacency_list()
        
        fig, ax = plt.subplots(figsize=(14, 8))
        ax.axis('off')
        
        # Title
        ax.text(0.5, 0.95, "Adjacency List (Outgoing Edges)", 
               ha='center', va='top',
               fontsize=18, fontweight='bold',
               transform=ax.transAxes)
        
        # Calculate positions for list visualization
        n = len(adj_list)
        y_spacing = 0.8 / (n + 1)
        
        # Draw each vertex and its adjacency list
        for idx, (vertex, neighbors) in enumerate(adj_list.items()):
            y_pos = 0.85 - idx * y_spacing
            
            # Draw vertex box
            vertex_box = plt.Rectangle((0.05, y_pos - 0.035), 0.08, 0.07,
                                       facecolor='lightblue',
                                       edgecolor='black',
                                       linewidth=2,
                                       transform=ax.transAxes)
            ax.add_patch(vertex_box)
            
            # Draw vertex label
            ax.text(0.09, y_pos, str(vertex),
                   ha='center', va='center',
                   fontsize=14, fontweight='bold',
                   transform=ax.transAxes)
            
            # Draw arrow
            ax.annotate('', xy=(0.17, y_pos), xytext=(0.14, y_pos),
                       arrowprops=dict(arrowstyle='->', lw=2, color='black'),
                       transform=ax.transAxes)
            
            # Draw neighbors
            x_offset = 0.18
            if neighbors:
                for i, (neighbor, weight) in enumerate(neighbors):
                    # Draw neighbor box
                    neighbor_box = plt.Rectangle((x_offset, y_pos - 0.035), 0.14, 0.07,
                                                facecolor='lightyellow',
                                                edgecolor='black',
                                                linewidth=1.5,
                                                transform=ax.transAxes)
                    ax.add_patch(neighbor_box)
                    
                    # Draw neighbor info (vertex, weight)
                    ax.text(x_offset + 0.07, y_pos, f"{neighbor}({weight})",
                           ha='center', va='center',
                           fontsize=11, fontweight='bold',
                           transform=ax.transAxes)
                    
                    # Draw arrow to next neighbor
                    if i < len(neighbors) - 1:
                        ax.annotate('', xy=(x_offset + 0.16, y_pos), 
                                   xytext=(x_offset + 0.145, y_pos),
                                   arrowprops=dict(arrowstyle='->', lw=1.5, color='black'),
                                   transform=ax.transAxes)
                        x_offset += 0.17
                    else:
                        # Draw NULL at the end
                        ax.text(x_offset + 0.16, y_pos, "→ NULL",
                               ha='left', va='center',
                               fontsize=10, style='italic',
                               transform=ax.transAxes)
            else:
                # No neighbors - draw NULL
                ax.text(x_offset, y_pos, "NULL",
                       ha='left', va='center',
                       fontsize=10, style='italic',
                       transform=ax.transAxes)
        
        plt.tight_layout()
        plt.savefig(output_file, dpi=150, bbox_inches='tight')
        plt.close()
        
        print(f"Saved adjacency list: {output_file}")
    
    def visualize_inverse_adjacency_list(self, output_file: str):
        """Visualize the inverse adjacency list (incoming edges)."""
        inv_adj_list = self.get_inverse_adjacency_list()
        
        fig, ax = plt.subplots(figsize=(14, 8))
        ax.axis('off')
        
        # Title
        ax.text(0.5, 0.95, "Inverse Adjacency List (Incoming Edges)", 
               ha='center', va='top',
               fontsize=18, fontweight='bold',
               transform=ax.transAxes)
        
        # Calculate positions for list visualization
        n = len(inv_adj_list)
        y_spacing = 0.8 / (n + 1)
        
        # Draw each vertex and its inverse adjacency list
        for idx, (vertex, predecessors) in enumerate(inv_adj_list.items()):
            y_pos = 0.85 - idx * y_spacing
            
            # Draw vertex box
            vertex_box = plt.Rectangle((0.05, y_pos - 0.035), 0.08, 0.07,
                                       facecolor='lightgreen',
                                       edgecolor='black',
                                       linewidth=2,
                                       transform=ax.transAxes)
            ax.add_patch(vertex_box)
            
            # Draw vertex label
            ax.text(0.09, y_pos, str(vertex),
                   ha='center', va='center',
                   fontsize=14, fontweight='bold',
                   transform=ax.transAxes)
            
            # Draw arrow
            ax.annotate('', xy=(0.17, y_pos), xytext=(0.14, y_pos),
                       arrowprops=dict(arrowstyle='->', lw=2, color='black'),
                       transform=ax.transAxes)
            
            # Draw predecessors
            x_offset = 0.18
            if predecessors:
                for i, (predecessor, weight) in enumerate(predecessors):
                    # Draw predecessor box
                    pred_box = plt.Rectangle((x_offset, y_pos - 0.035), 0.14, 0.07,
                                            facecolor='lightcoral',
                                            edgecolor='black',
                                            linewidth=1.5,
                                            transform=ax.transAxes)
                    ax.add_patch(pred_box)
                    
                    # Draw predecessor info (vertex, weight)
                    ax.text(x_offset + 0.07, y_pos, f"{predecessor}({weight})",
                           ha='center', va='center',
                           fontsize=11, fontweight='bold',
                           transform=ax.transAxes)
                    
                    # Draw arrow to next predecessor
                    if i < len(predecessors) - 1:
                        ax.annotate('', xy=(x_offset + 0.16, y_pos), 
                                   xytext=(x_offset + 0.145, y_pos),
                                   arrowprops=dict(arrowstyle='->', lw=1.5, color='black'),
                                   transform=ax.transAxes)
                        x_offset += 0.17
                    else:
                        # Draw NULL at the end
                        ax.text(x_offset + 0.16, y_pos, "→ NULL",
                               ha='left', va='center',
                               fontsize=10, style='italic',
                               transform=ax.transAxes)
            else:
                # No predecessors - draw NULL
                ax.text(x_offset, y_pos, "NULL",
                       ha='left', va='center',
                       fontsize=10, style='italic',
                       transform=ax.transAxes)
        
        plt.tight_layout()
        plt.savefig(output_file, dpi=150, bbox_inches='tight')
        plt.close()
        
        print(f"Saved inverse adjacency list: {output_file}")
    
    def visualize_orthogonal_list(self, output_file: str):
        """Visualize the orthogonal linked list (十字链表)."""
        sorted_vertices = sorted(self.vertices)
        
        fig, ax = plt.subplots(figsize=(16, 12))
        ax.axis('off')
        
        # Title
        ax.text(0.5, 0.97, "Orthogonal Linked List (十字链表)", 
               ha='center', va='top',
               fontsize=18, fontweight='bold',
               transform=ax.transAxes)
        
        # Draw description
        ax.text(0.5, 0.93, "Each vertex has: OUT edges (→) and IN edges (↓)", 
               ha='center', va='top',
               fontsize=12, style='italic',
               transform=ax.transAxes)
        
        n = len(sorted_vertices)
        cell_width = 0.8 / (n + 1)
        cell_height = 0.08
        start_x = 0.1
        start_y = 0.85
        
        # Draw vertex headers
        for idx, vertex in enumerate(sorted_vertices):
            x = start_x + (idx + 1) * cell_width
            
            # Vertex header box
            header_box = plt.Rectangle((x, start_y), cell_width * 0.8, cell_height,
                                       facecolor='lightblue',
                                       edgecolor='black',
                                       linewidth=2,
                                       transform=ax.transAxes)
            ax.add_patch(header_box)
            ax.text(x + cell_width * 0.4, start_y + cell_height/2, str(vertex),
                   ha='center', va='center',
                   fontsize=12, fontweight='bold',
                   transform=ax.transAxes)
        
        # Draw row headers and edges
        for idx, from_vertex in enumerate(sorted_vertices):
            y = start_y - (idx + 1) * (cell_height + 0.02)
            
            # Row header
            row_box = plt.Rectangle((start_x, y), cell_width * 0.8, cell_height,
                                    facecolor='lightgreen',
                                    edgecolor='black',
                                    linewidth=2,
                                    transform=ax.transAxes)
            ax.add_patch(row_box)
            ax.text(start_x + cell_width * 0.4, y + cell_height/2, str(from_vertex),
                   ha='center', va='center',
                   fontsize=12, fontweight='bold',
                   transform=ax.transAxes)
            
            # Draw edges
            for jdx, to_vertex in enumerate(sorted_vertices):
                x = start_x + (jdx + 1) * cell_width
                
                if self.graph.has_edge(from_vertex, to_vertex):
                    weight = self.graph[from_vertex][to_vertex]['weight']
                    # Edge cell
                    edge_box = plt.Rectangle((x, y), cell_width * 0.8, cell_height,
                                            facecolor='lightyellow',
                                            edgecolor='black',
                                            linewidth=1,
                                            transform=ax.transAxes)
                    ax.add_patch(edge_box)
                    ax.text(x + cell_width * 0.4, y + cell_height/2, str(int(weight)),
                           ha='center', va='center',
                           fontsize=11, fontweight='bold',
                           transform=ax.transAxes)
                elif from_vertex == to_vertex:
                    # Self loop
                    self_box = plt.Rectangle((x, y), cell_width * 0.8, cell_height,
                                            facecolor='lightgray',
                                            edgecolor='black',
                                            linewidth=1,
                                            transform=ax.transAxes)
                    ax.add_patch(self_box)
                    ax.text(x + cell_width * 0.4, y + cell_height/2, "0",
                           ha='center', va='center',
                           fontsize=11,
                           transform=ax.transAxes)
                else:
                    # No edge
                    empty_box = plt.Rectangle((x, y), cell_width * 0.8, cell_height,
                                             facecolor='white',
                                             edgecolor='gray',
                                             linewidth=0.5,
                                             linestyle='--',
                                             transform=ax.transAxes)
                    ax.add_patch(empty_box)
                    ax.text(x + cell_width * 0.4, y + cell_height/2, "∞",
                           ha='center', va='center',
                           fontsize=10, color='red',
                           transform=ax.transAxes)
        
        # Add legend
        legend_y = 0.05
        ax.text(0.1, legend_y, "Legend:", fontsize=11, fontweight='bold', transform=ax.transAxes)
        ax.text(0.25, legend_y, "Number = Edge weight", fontsize=10, transform=ax.transAxes)
        ax.text(0.5, legend_y, "0 = Self (diagonal)", fontsize=10, transform=ax.transAxes)
        ax.text(0.75, legend_y, "∞ = No edge", fontsize=10, color='red', transform=ax.transAxes)
        
        plt.tight_layout()
        plt.savefig(output_file, dpi=150, bbox_inches='tight')
        plt.close()
        
        print(f"Saved orthogonal linked list: {output_file}")
    
    def print_degrees(self):
        """Print vertex degrees to console."""
        degrees = self.get_degrees()
        
        print("\n" + "="*60)
        print("VERTEX DEGREES")
        print("="*60)
        print(f"{'Vertex':<10} {'In-Degree':<15} {'Out-Degree':<15}")
        print("-"*60)
        
        for vertex in sorted(degrees.keys()):
            print(f"{vertex:<10} {degrees[vertex]['in']:<15} {degrees[vertex]['out']:<15}")
        
        print("="*60 + "\n")
    
    def print_adjacency_matrix(self):
        """Print the adjacency matrix to console."""
        matrix, vertices = self.get_adjacency_matrix()
        
        print("\n" + "="*60)
        print("ADJACENCY MATRIX (FROM → TO)")
        print("="*60)
        
        # Print header
        print("    ", end="")
        for v in vertices:
            print(f"{v:>6}", end="")
        print()
        
        # Print matrix
        for i, v in enumerate(vertices):
            print(f"{v:>4}", end="")
            for j in range(len(vertices)):
                if np.isinf(matrix[i][j]):
                    print(f"{'∞':>6}", end="")
                else:
                    print(f"{int(matrix[i][j]):>6}", end="")
            print()
        
        print("="*60 + "\n")
    
    def print_adjacency_list(self):
        """Print the adjacency list to console."""
        adj_list = self.get_adjacency_list()
        
        print("\n" + "="*60)
        print("ADJACENCY LIST (OUTGOING EDGES)")
        print("="*60)
        
        for vertex, neighbors in adj_list.items():
            neighbors_str = " → ".join([f"{n}(w:{w})" for n, w in neighbors])
            if neighbors_str:
                print(f"{vertex} → {neighbors_str} → NULL")
            else:
                print(f"{vertex} → NULL")
        
        print("="*60 + "\n")
    
    def print_inverse_adjacency_list(self):
        """Print the inverse adjacency list to console."""
        inv_adj_list = self.get_inverse_adjacency_list()
        
        print("\n" + "="*60)
        print("INVERSE ADJACENCY LIST (INCOMING EDGES)")
        print("="*60)
        
        for vertex, predecessors in inv_adj_list.items():
            pred_str = " → ".join([f"{p}(w:{w})" for p, w in predecessors])
            if pred_str:
                print(f"{vertex} ← {pred_str} ← NULL")
            else:
                print(f"{vertex} ← NULL")
        
        print("="*60 + "\n")


def main():
    """Main function to create and visualize the directed graph."""
    
    # Create output directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    output_dir = script_dir
    
    print("\n" + "#"*60)
    print("DIRECTED WEIGHTED GRAPH VISUALIZATION")
    print("#"*60 + "\n")
    
    # Create the directed graph
    graph = DirectedWeightedGraph()
    
    # Define the directed graph structure (at least 4 vertices, at least 5 edges)
    # Using 5 vertices and 8 directed edges
    edges = [
        ('A', 'B', 3),
        ('A', 'C', 5),
        ('B', 'C', 2),
        ('B', 'D', 4),
        ('C', 'D', 1),
        ('C', 'E', 6),
        ('D', 'E', 3),
        ('E', 'A', 2),
    ]
    
    print("Building directed graph with:")
    print(f"  Vertices: A, B, C, D, E (5 vertices)")
    print(f"  Directed Edges: {len(edges)} edges")
    print("\nDirected Edges with weights:")
    for from_v, to_v, w in edges:
        print(f"  {from_v} → {to_v} : weight = {w}")
        graph.add_edge(from_v, to_v, w)
    
    # Print graph info
    print(f"\nDirected graph created successfully!")
    print(f"  Total vertices: {len(graph.vertices)}")
    print(f"  Total directed edges: {len(graph.edges)}")
    
    # Print vertex degrees
    graph.print_degrees()
    
    # Print adjacency matrix
    graph.print_adjacency_matrix()
    
    # Print adjacency list
    graph.print_adjacency_list()
    
    # Print inverse adjacency list
    graph.print_inverse_adjacency_list()
    
    # Generate visualizations
    print("Generating visualizations...")
    
    # 1. Directed graph visualization
    graph.visualize_directed_graph(os.path.join(output_dir, "directed_graph.png"))
    
    # 2. Vertex degrees
    graph.visualize_degrees(os.path.join(output_dir, "vertex_degrees.png"))
    
    # 3. Adjacency matrix
    graph.visualize_adjacency_matrix(os.path.join(output_dir, "adjacency_matrix.png"))
    
    # 4. Adjacency list
    graph.visualize_adjacency_list(os.path.join(output_dir, "adjacency_list.png"))
    
    # 5. Inverse adjacency list
    graph.visualize_inverse_adjacency_list(os.path.join(output_dir, "inverse_adjacency_list.png"))
    
    # 6. Orthogonal linked list
    graph.visualize_orthogonal_list(os.path.join(output_dir, "orthogonal_list.png"))
    
    print("\n" + "="*60)
    print("All visualizations completed!")
    print(f"Output directory: {output_dir}")
    print("="*60 + "\n")


if __name__ == "__main__":
    main()
