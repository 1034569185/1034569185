"""
Shortest Path Algorithms Visualization
Implements Dijkstra and Floyd algorithms with step-by-step visualization
"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches
import networkx as nx
import numpy as np
from typing import Dict, List, Tuple, Set
import os

# Create output directory
OUTPUT_DIR = "shortest_path_algorithms"
os.makedirs(OUTPUT_DIR, exist_ok=True)

class WeightedDirectedGraph:
    """
    Weighted directed graph for shortest path algorithms
    构造一个带权并连通的有向图
    """
    
    def __init__(self):
        # Graph with 5 vertices: A, B, C, D, E (exceeds minimum of 3)
        # 5个顶点：A, B, C, D, E（超过最少3个要求）
        self.vertices = ['A', 'B', 'C', 'D', 'E']
        
        # Directed edges with weights (7 edges - exceeds minimum of 4)
        # 7条有向边（超过最少4条要求）
        # Format: (from, to, weight)
        self.edges = [
            ('A', 'B', 3),
            ('A', 'C', 5),
            ('B', 'C', 2),
            ('B', 'D', 4),
            ('C', 'D', 1),
            ('C', 'E', 6),
            ('D', 'E', 2)
        ]
        
        # Build adjacency matrix
        self.n = len(self.vertices)
        self.adj_matrix = self._build_adjacency_matrix()
        
        # Vertex indices
        self.vertex_index = {v: i for i, v in enumerate(self.vertices)}
    
    def _build_adjacency_matrix(self):
        """Build adjacency matrix with infinity for no edges"""
        n = len(self.vertices)
        matrix = [[float('inf')] * n for _ in range(n)]
        
        # Diagonal is 0 (self to self)
        for i in range(n):
            matrix[i][i] = 0
        
        # Add edges
        vertex_to_idx = {v: i for i, v in enumerate(self.vertices)}
        for from_v, to_v, weight in self.edges:
            i = vertex_to_idx[from_v]
            j = vertex_to_idx[to_v]
            matrix[i][j] = weight
        
        return matrix
    
    def visualize_graph(self):
        """Visualize the directed weighted graph"""
        G = nx.DiGraph()
        G.add_nodes_from(self.vertices)
        
        # Add edges with weights
        for from_v, to_v, weight in self.edges:
            G.add_edge(from_v, to_v, weight=weight)
        
        plt.figure(figsize=(12, 8))
        
        # Use circular layout for better visibility
        pos = nx.circular_layout(G)
        
        # Draw nodes
        nx.draw_networkx_nodes(G, pos, node_color='lightblue', 
                              node_size=2000, edgecolors='black', linewidths=2.5)
        
        # Draw edges with curved arrows
        nx.draw_networkx_edges(G, pos, edge_color='darkblue', 
                              width=2.5, arrowsize=25, arrowstyle='->', 
                              connectionstyle='arc3,rad=0.1',
                              min_source_margin=15, min_target_margin=15)
        
        # Draw labels
        nx.draw_networkx_labels(G, pos, font_size=16, font_weight='bold')
        
        # Draw edge labels (weights)
        edge_labels = {(from_v, to_v): weight for from_v, to_v, weight in self.edges}
        nx.draw_networkx_edge_labels(G, pos, edge_labels, font_size=12, 
                                     font_color='red', bbox=dict(boxstyle='round,pad=0.3', 
                                     facecolor='white', edgecolor='red'))
        
        plt.title('Weighted Directed Graph for Shortest Path Algorithms\n带权有向图',
                 fontsize=16, fontweight='bold', pad=20)
        plt.axis('off')
        plt.tight_layout()
        plt.savefig(f'{OUTPUT_DIR}/graph.png', dpi=150, bbox_inches='tight')
        plt.close()
        print(f"✓ Graph visualization saved to {OUTPUT_DIR}/graph.png")
    
    def dijkstra(self, source='A'):
        """
        Dijkstra's algorithm for single-source shortest paths
        使用Dijkstra算法求单源最短路径
        
        Returns: List of steps, each containing S, V-S, distances, and paths
        """
        n = len(self.vertices)
        source_idx = self.vertex_index[source]
        
        # Initialize
        dist = [float('inf')] * n
        dist[source_idx] = 0
        
        # Previous vertex in optimal path
        prev = [None] * n
        
        # S: vertices with known shortest paths
        S = set()
        
        # V-S: vertices without known shortest paths
        V_minus_S = set(range(n))
        
        # Store all steps for visualization
        steps = []
        
        # Initial step
        steps.append({
            'iteration': 0,
            'S': S.copy(),
            'V_minus_S': V_minus_S.copy(),
            'dist': dist.copy(),
            'prev': prev.copy(),
            'added_vertex': None
        })
        
        # Main loop
        for iteration in range(n):
            # Find vertex with minimum distance in V-S
            min_dist = float('inf')
            u = None
            
            for v in V_minus_S:
                if dist[v] < min_dist:
                    min_dist = dist[v]
                    u = v
            
            if u is None or dist[u] == float('inf'):
                break
            
            # Add u to S
            S.add(u)
            V_minus_S.remove(u)
            
            # Update distances for neighbors of u
            for v in range(n):
                if self.adj_matrix[u][v] != float('inf'):
                    alt = dist[u] + self.adj_matrix[u][v]
                    if alt < dist[v]:
                        dist[v] = alt
                        prev[v] = u
            
            # Record step
            steps.append({
                'iteration': iteration + 1,
                'S': S.copy(),
                'V_minus_S': V_minus_S.copy(),
                'dist': dist.copy(),
                'prev': prev.copy(),
                'added_vertex': u
            })
        
        return steps
    
    def get_path(self, prev, target_idx):
        """Reconstruct path from prev array"""
        path = []
        current = target_idx
        
        while current is not None:
            path.append(self.vertices[current])
            current = prev[current]
        
        path.reverse()
        return ' → '.join(path) if path else 'No path'
    
    def visualize_dijkstra_steps(self, steps, source='A'):
        """Visualize all Dijkstra algorithm steps in tables"""
        n_steps = len(steps)
        
        # Create figure for all steps
        fig = plt.figure(figsize=(16, 4 * n_steps))
        
        for step_idx, step in enumerate(steps):
            ax = fig.add_subplot(n_steps, 1, step_idx + 1)
            ax.axis('off')
            
            # Title
            if step_idx == 0:
                title = f"Dijkstra Algorithm - Initial State (Source: {source})\nDijkstra算法 - 初始状态（源点：{source}）"
            else:
                added_v = self.vertices[step['added_vertex']]
                title = f"Step {step_idx}: Add vertex {added_v} to S\n步骤 {step_idx}：将顶点 {added_v} 加入 S"
            
            ax.text(0.5, 0.95, title, ha='center', va='top', 
                   fontsize=12, fontweight='bold', transform=ax.transAxes)
            
            # Prepare table data
            table_data = []
            
            # Header
            headers = ['Vertex\n顶点', 'In S?\n在S中?', 'Distance\n距离', 'Shortest Path\n最短路径']
            table_data.append(headers)
            
            # Data rows
            for i, v in enumerate(self.vertices):
                in_s = '✓' if i in step['S'] else '✗'
                
                dist = step['dist'][i]
                dist_str = str(dist) if dist != float('inf') else '∞'
                
                path = self.get_path(step['prev'], i)
                
                table_data.append([v, in_s, dist_str, path])
            
            # Create table
            table = ax.table(cellText=table_data, cellLoc='center',
                           loc='center', bbox=[0.05, 0.1, 0.9, 0.75])
            
            table.auto_set_font_size(False)
            table.set_fontsize(10)
            
            # Style header row
            for j in range(len(headers)):
                cell = table[(0, j)]
                cell.set_facecolor('#4CAF50')
                cell.set_text_props(weight='bold', color='white')
            
            # Style data rows
            for i in range(1, len(table_data)):
                vertex_idx = i - 1
                for j in range(len(headers)):
                    cell = table[(i, j)]
                    
                    # Highlight vertices in S
                    if vertex_idx in step['S']:
                        cell.set_facecolor('#E8F5E9')
                    else:
                        cell.set_facecolor('white')
                    
                    # Highlight newly added vertex
                    if step['added_vertex'] is not None and vertex_idx == step['added_vertex']:
                        cell.set_facecolor('#FFE082')
                        cell.set_text_props(weight='bold')
            
            # Add S and V-S info
            s_vertices = [self.vertices[i] for i in sorted(step['S'])]
            v_minus_s_vertices = [self.vertices[i] for i in sorted(step['V_minus_S'])]
            
            info_text = f"S = {{ {', '.join(s_vertices) if s_vertices else '∅'} }}\n"
            info_text += f"V - S = {{ {', '.join(v_minus_s_vertices) if v_minus_s_vertices else '∅'} }}"
            
            ax.text(0.5, 0.05, info_text, ha='center', va='top',
                   fontsize=10, transform=ax.transAxes,
                   bbox=dict(boxstyle='round,pad=0.5', facecolor='lightyellow'))
        
        plt.tight_layout()
        plt.savefig(f'{OUTPUT_DIR}/dijkstra_steps.png', dpi=150, bbox_inches='tight')
        plt.close()
        print(f"✓ Dijkstra steps saved to {OUTPUT_DIR}/dijkstra_steps.png")
    
    def floyd_warshall(self):
        """
        Floyd-Warshall algorithm for all-pairs shortest paths
        使用Floyd算法求所有顶点对之间的最短路径
        
        Returns: List of steps, each containing distance matrix and path matrix
        """
        n = len(self.vertices)
        
        # Initialize distance matrix (copy adjacency matrix)
        dist = [row[:] for row in self.adj_matrix]
        
        # Initialize path matrix (next vertex on shortest path)
        next_vertex = [[None] * n for _ in range(n)]
        
        # Initialize next_vertex
        for i in range(n):
            for j in range(n):
                if i != j and self.adj_matrix[i][j] != float('inf'):
                    next_vertex[i][j] = j
        
        # Store all steps
        steps = []
        
        # Initial step (k = -1, before any intermediate vertices)
        steps.append({
            'k': -1,
            'k_vertex': None,
            'dist': [row[:] for row in dist],
            'next': [row[:] for row in next_vertex]
        })
        
        # Floyd-Warshall algorithm
        for k in range(n):
            # Try using vertex k as intermediate vertex
            for i in range(n):
                for j in range(n):
                    if dist[i][k] + dist[k][j] < dist[i][j]:
                        dist[i][j] = dist[i][k] + dist[k][j]
                        next_vertex[i][j] = next_vertex[i][k]
            
            # Record step
            steps.append({
                'k': k,
                'k_vertex': self.vertices[k],
                'dist': [row[:] for row in dist],
                'next': [row[:] for row in next_vertex]
            })
        
        return steps
    
    def get_floyd_path(self, next_matrix, i, j):
        """Reconstruct path from Floyd's next matrix"""
        if next_matrix[i][j] is None:
            return "No path"
        
        path = [self.vertices[i]]
        current = i
        
        while current != j:
            current = next_matrix[current][j]
            if current is None:
                return "No path"
            path.append(self.vertices[current])
        
        return ' → '.join(path)
    
    def visualize_floyd_steps(self, steps):
        """Visualize all Floyd-Warshall algorithm steps"""
        n_steps = len(steps)
        
        # Create figure for all steps
        fig = plt.figure(figsize=(14, 6 * n_steps))
        
        for step_idx, step in enumerate(steps):
            ax = fig.add_subplot(n_steps, 1, step_idx + 1)
            ax.axis('off')
            
            # Title
            if step_idx == 0:
                title = "Floyd-Warshall Algorithm - Initial Distance Matrix\nFloyd算法 - 初始距离矩阵"
            else:
                k_v = step['k_vertex']
                title = f"Floyd-Warshall - After using vertex {k_v} as intermediate\nFloyd算法 - 使用顶点 {k_v} 作为中间顶点后"
            
            ax.text(0.5, 0.95, title, ha='center', va='top',
                   fontsize=12, fontweight='bold', transform=ax.transAxes)
            
            # Prepare distance matrix table
            dist_data = []
            header = ['From\\To\n起点\\终点'] + self.vertices
            dist_data.append(header)
            
            for i, from_v in enumerate(self.vertices):
                row = [from_v]
                for j in range(len(self.vertices)):
                    d = step['dist'][i][j]
                    if d == float('inf'):
                        row.append('∞')
                    elif d == 0:
                        row.append('0')
                    else:
                        row.append(str(int(d)))
                dist_data.append(row)
            
            # Create distance matrix table
            dist_table = ax.table(cellText=dist_data, cellLoc='center',
                                 loc='upper center', bbox=[0.05, 0.5, 0.9, 0.4])
            
            dist_table.auto_set_font_size(False)
            dist_table.set_fontsize(10)
            
            # Style header
            for j in range(len(header)):
                cell = dist_table[(0, j)]
                cell.set_facecolor('#2196F3')
                cell.set_text_props(weight='bold', color='white')
            
            # Style first column
            for i in range(1, len(dist_data)):
                cell = dist_table[(i, 0)]
                cell.set_facecolor('#2196F3')
                cell.set_text_props(weight='bold', color='white')
            
            # Highlight diagonal
            for i in range(1, len(dist_data)):
                cell = dist_table[(i, i)]
                cell.set_facecolor('#E3F2FD')
            
            # Prepare path table
            path_data = []
            path_header = ['From\\To\n起点\\终点'] + self.vertices
            path_data.append(path_header)
            
            for i, from_v in enumerate(self.vertices):
                row = [from_v]
                for j in range(len(self.vertices)):
                    if i == j:
                        row.append('-')
                    else:
                        path = self.get_floyd_path(step['next'], i, j)
                        row.append(path)
                path_data.append(row)
            
            # Create path table
            path_table = ax.table(cellText=path_data, cellLoc='left',
                                 loc='lower center', bbox=[0.05, 0.05, 0.9, 0.4])
            
            path_table.auto_set_font_size(False)
            path_table.set_fontsize(9)
            
            # Style header
            for j in range(len(path_header)):
                cell = path_table[(0, j)]
                cell.set_facecolor('#4CAF50')
                cell.set_text_props(weight='bold', color='white')
            
            # Style first column
            for i in range(1, len(path_data)):
                cell = path_table[(i, 0)]
                cell.set_facecolor('#4CAF50')
                cell.set_text_props(weight='bold', color='white')
        
        plt.tight_layout()
        plt.savefig(f'{OUTPUT_DIR}/floyd_steps.png', dpi=150, bbox_inches='tight')
        plt.close()
        print(f"✓ Floyd-Warshall steps saved to {OUTPUT_DIR}/floyd_steps.png")


def main():
    """Main function to run all visualizations"""
    print("=" * 60)
    print("Shortest Path Algorithms Visualization")
    print("最短路径算法可视化")
    print("=" * 60)
    print()
    
    # Create graph
    print("Creating weighted directed graph...")
    print("创建带权有向图...")
    graph = WeightedDirectedGraph()
    
    print(f"Vertices: {graph.vertices}")
    print(f"Number of edges: {len(graph.edges)}")
    print("Edges:")
    for from_v, to_v, weight in graph.edges:
        print(f"  {from_v} → {to_v} (weight: {weight})")
    print()
    
    # Visualize graph
    print("Visualizing graph...")
    graph.visualize_graph()
    print()
    
    # Dijkstra's algorithm
    print("Running Dijkstra's algorithm (source: A)...")
    print("运行Dijkstra算法（源点：A）...")
    dijkstra_steps = graph.dijkstra(source='A')
    print(f"Number of steps: {len(dijkstra_steps)}")
    
    # Visualize Dijkstra steps
    print("Visualizing Dijkstra algorithm steps...")
    graph.visualize_dijkstra_steps(dijkstra_steps, source='A')
    print()
    
    # Floyd-Warshall algorithm
    print("Running Floyd-Warshall algorithm...")
    print("运行Floyd算法...")
    floyd_steps = graph.floyd_warshall()
    print(f"Number of steps: {len(floyd_steps)}")
    
    # Visualize Floyd steps
    print("Visualizing Floyd-Warshall algorithm steps...")
    graph.visualize_floyd_steps(floyd_steps)
    print()
    
    print("=" * 60)
    print("All visualizations completed!")
    print("所有可视化已完成！")
    print(f"Files saved in '{OUTPUT_DIR}/' directory")
    print("=" * 60)


if __name__ == "__main__":
    main()
