#!/usr/bin/env python3
"""
Undirected Weighted Graph Visualization
Creates a weighted undirected graph and visualizes:
1. The graph itself
2. Adjacency matrix
3. Adjacency list
"""

import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import networkx as nx
import numpy as np
import os
from typing import Dict, List, Tuple

class UndirectedWeightedGraph:
    """Undirected weighted graph implementation with visualization."""
    
    def __init__(self):
        self.graph = nx.Graph()
        self.vertices = []
        self.edges = []
    
    def add_vertex(self, vertex):
        """Add a vertex to the graph."""
        if vertex not in self.vertices:
            self.vertices.append(vertex)
            self.graph.add_node(vertex)
    
    def add_edge(self, vertex1, vertex2, weight):
        """Add a weighted edge between two vertices."""
        self.add_vertex(vertex1)
        self.add_vertex(vertex2)
        self.graph.add_edge(vertex1, vertex2, weight=weight)
        self.edges.append((vertex1, vertex2, weight))
    
    def get_adjacency_matrix(self):
        """Generate the adjacency matrix."""
        # Sort vertices for consistent ordering
        sorted_vertices = sorted(self.vertices)
        n = len(sorted_vertices)
        
        # Create matrix with infinity for non-reachable vertices
        # Using float to accommodate infinity
        matrix = np.full((n, n), np.inf, dtype=float)
        
        # Fill matrix with weights
        for i, v1 in enumerate(sorted_vertices):
            for j, v2 in enumerate(sorted_vertices):
                if i == j:
                    # Diagonal: self to self is 0
                    matrix[i][j] = 0
                elif self.graph.has_edge(v1, v2):
                    weight = self.graph[v1][v2]['weight']
                    matrix[i][j] = weight
                    matrix[j][i] = weight  # Symmetric for undirected graph
                # else: remains infinity (no edge)
        
        return matrix, sorted_vertices
    
    def get_adjacency_list(self):
        """Generate the adjacency list."""
        sorted_vertices = sorted(self.vertices)
        adj_list = {}
        
        for vertex in sorted_vertices:
            neighbors = []
            for neighbor in self.graph.neighbors(vertex):
                weight = self.graph[vertex][neighbor]['weight']
                neighbors.append((neighbor, weight))
            # Sort neighbors by name
            neighbors.sort(key=lambda x: x[0])
            adj_list[vertex] = neighbors
        
        return adj_list
    
    def visualize_graph(self, output_file: str):
        """Visualize the undirected weighted graph."""
        plt.figure(figsize=(12, 10))
        
        # Use spring layout for better visualization
        pos = nx.spring_layout(self.graph, seed=42, k=2, iterations=50)
        
        # Draw nodes
        nx.draw_networkx_nodes(self.graph, pos, 
                              node_color='lightblue',
                              node_size=1500,
                              edgecolors='black',
                              linewidths=2)
        
        # Draw edges
        nx.draw_networkx_edges(self.graph, pos,
                              width=2,
                              edge_color='gray')
        
        # Draw labels
        nx.draw_networkx_labels(self.graph, pos,
                               font_size=16,
                               font_weight='bold')
        
        # Draw edge labels (weights)
        edge_labels = nx.get_edge_attributes(self.graph, 'weight')
        nx.draw_networkx_edge_labels(self.graph, pos,
                                     edge_labels,
                                     font_size=12,
                                     font_color='red',
                                     font_weight='bold')
        
        plt.title("Undirected Weighted Graph", fontsize=18, fontweight='bold', pad=20)
        plt.axis('off')
        plt.tight_layout()
        plt.savefig(output_file, dpi=150, bbox_inches='tight')
        plt.close()
        
        print(f"Saved graph visualization: {output_file}")
    
    def visualize_adjacency_matrix(self, output_file: str):
        """Visualize the adjacency matrix."""
        matrix, vertices = self.get_adjacency_matrix()
        n = len(vertices)
        
        fig, ax = plt.subplots(figsize=(10, 10))
        
        # Create a display matrix for coloring (replace inf with max+1 for color scale)
        display_matrix = matrix.copy()
        max_weight = np.max(matrix[~np.isinf(matrix)])  # Max finite weight
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
                    # Display infinity symbol for unreachable vertices
                    text_str = "∞"
                    text_color = "red"
                else:
                    # Display weight as integer
                    text_str = str(int(matrix[i, j]))
                    # Determine color based on value
                    text_color = "black" if matrix[i, j] < max_weight/2 else "white"
                
                ax.text(j, i, text_str,
                       ha="center", va="center",
                       color=text_color,
                       fontsize=14, fontweight='bold')
        
        ax.set_title("Adjacency Matrix", fontsize=16, fontweight='bold', pad=20)
        ax.set_xlabel("Vertices", fontsize=14, fontweight='bold')
        ax.set_ylabel("Vertices", fontsize=14, fontweight='bold')
        
        # Add grid
        ax.set_xticks(np.arange(n)-.5, minor=True)
        ax.set_yticks(np.arange(n)-.5, minor=True)
        ax.grid(which="minor", color="black", linestyle='-', linewidth=2)
        
        plt.tight_layout()
        plt.savefig(output_file, dpi=150, bbox_inches='tight')
        plt.close()
        
        print(f"Saved adjacency matrix: {output_file}")
    
    def visualize_adjacency_list(self, output_file: str):
        """Visualize the adjacency list."""
        adj_list = self.get_adjacency_list()
        
        fig, ax = plt.subplots(figsize=(12, 8))
        ax.axis('off')
        
        # Calculate positions for list visualization
        n = len(adj_list)
        y_spacing = 1.0 / (n + 1)
        
        # Title
        ax.text(0.5, 0.95, "Adjacency List", 
               ha='center', va='top',
               fontsize=18, fontweight='bold',
               transform=ax.transAxes)
        
        # Draw each vertex and its adjacency list
        for idx, (vertex, neighbors) in enumerate(adj_list.items()):
            y_pos = 0.88 - idx * y_spacing * 0.9
            
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
    
    def print_adjacency_matrix(self):
        """Print the adjacency matrix to console."""
        matrix, vertices = self.get_adjacency_matrix()
        
        print("\n" + "="*60)
        print("ADJACENCY MATRIX")
        print("="*60)
        
        # Print header
        print("    ", end="")
        for v in vertices:
            print(f"{v:4}", end="")
        print()
        
        # Print matrix
        for i, v in enumerate(vertices):
            print(f"{v:4}", end="")
            for j in range(len(vertices)):
                if np.isinf(matrix[i][j]):
                    print(f"{'∞':>4}", end="")
                else:
                    print(f"{int(matrix[i][j]):4}", end="")
            print()
        
        print("="*60 + "\n")
    
    def print_adjacency_list(self):
        """Print the adjacency list to console."""
        adj_list = self.get_adjacency_list()
        
        print("\n" + "="*60)
        print("ADJACENCY LIST")
        print("="*60)
        
        for vertex, neighbors in adj_list.items():
            neighbors_str = " → ".join([f"{n}(weight:{w})" for n, w in neighbors])
            if neighbors_str:
                print(f"{vertex} → {neighbors_str} → NULL")
            else:
                print(f"{vertex} → NULL")
        
        print("="*60 + "\n")


def main():
    """Main function to create and visualize the graph."""
    
    # Create output directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    output_dir = script_dir
    
    print("\n" + "#"*60)
    print("UNDIRECTED WEIGHTED GRAPH VISUALIZATION")
    print("#"*60 + "\n")
    
    # Create the graph
    graph = UndirectedWeightedGraph()
    
    # Define the graph structure (at least 4 vertices, at least 6 edges)
    # Using 6 vertices and 10 edges for a more interesting graph
    edges = [
        ('A', 'B', 4),
        ('A', 'C', 2),
        ('A', 'D', 7),
        ('B', 'C', 1),
        ('B', 'E', 5),
        ('C', 'D', 3),
        ('C', 'E', 8),
        ('D', 'E', 6),
        ('E', 'F', 2),
        ('D', 'F', 4)
    ]
    
    print("Building graph with:")
    print(f"  Vertices: A, B, C, D, E, F (6 vertices)")
    print(f"  Edges: {len(edges)} edges")
    print("\nEdges with weights:")
    for v1, v2, w in edges:
        print(f"  {v1} -- {v2} : weight = {w}")
        graph.add_edge(v1, v2, w)
    
    # Print graph info
    print(f"\nGraph created successfully!")
    print(f"  Total vertices: {len(graph.vertices)}")
    print(f"  Total edges: {len(graph.edges)}")
    
    # Print adjacency matrix
    graph.print_adjacency_matrix()
    
    # Print adjacency list
    graph.print_adjacency_list()
    
    # Generate visualizations
    print("Generating visualizations...")
    
    # 1. Graph visualization
    graph.visualize_graph(os.path.join(output_dir, "graph.png"))
    
    # 2. Adjacency matrix
    graph.visualize_adjacency_matrix(os.path.join(output_dir, "adjacency_matrix.png"))
    
    # 3. Adjacency list
    graph.visualize_adjacency_list(os.path.join(output_dir, "adjacency_list.png"))
    
    print("\n" + "="*60)
    print("All visualizations completed!")
    print(f"Output directory: {output_dir}")
    print("="*60 + "\n")


if __name__ == "__main__":
    main()
