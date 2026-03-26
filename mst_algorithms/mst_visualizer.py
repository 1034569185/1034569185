#!/usr/bin/env python3
"""
Minimum Spanning Tree (MST) Algorithms Visualization
Implements Prim's and Kruskal's algorithms with step-by-step visualization.

No Chinese characters to avoid encoding issues.
"""

import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import networkx as nx
import os
from typing import List, Tuple, Set, Dict

class UnionFind:
    """Union-Find data structure for Kruskal's algorithm"""
    def __init__(self, vertices: List[str]):
        self.parent = {v: v for v in vertices}
        self.rank = {v: 0 for v in vertices}
    
    def find(self, vertex: str) -> str:
        """Find the root of the set containing vertex"""
        if self.parent[vertex] != vertex:
            self.parent[vertex] = self.find(self.parent[vertex])  # Path compression
        return self.parent[vertex]
    
    def union(self, v1: str, v2: str) -> bool:
        """Union two sets. Returns True if they were different sets."""
        root1 = self.find(v1)
        root2 = self.find(v2)
        
        if root1 == root2:
            return False
        
        # Union by rank
        if self.rank[root1] < self.rank[root2]:
            self.parent[root1] = root2
        elif self.rank[root1] > self.rank[root2]:
            self.parent[root2] = root1
        else:
            self.parent[root2] = root1
            self.rank[root1] += 1
        
        return True
    
    def get_components(self) -> Dict[str, List[str]]:
        """Get all equivalence classes (connected components)"""
        components = {}
        for vertex in self.parent:
            root = self.find(vertex)
            if root not in components:
                components[root] = []
            components[root].append(vertex)
        return components


class MSTVisualizer:
    """Visualize Minimum Spanning Tree algorithms"""
    
    def __init__(self):
        # Create output directory
        self.output_dir = "mst_algorithms"
        os.makedirs(self.output_dir, exist_ok=True)
        
        # Define graph: 5 vertices, 8 edges (exceeds requirements: >=4 vertices, >=6 edges)
        self.vertices = ['A', 'B', 'C', 'D', 'E']
        self.edges = [
            ('A', 'B', 4),
            ('A', 'C', 2),
            ('A', 'D', 7),
            ('B', 'C', 1),
            ('B', 'E', 5),
            ('C', 'D', 3),
            ('C', 'E', 8),
            ('D', 'E', 6)
        ]
        
        # Create networkx graph
        self.G = nx.Graph()
        self.G.add_nodes_from(self.vertices)
        for u, v, w in self.edges:
            self.G.add_edge(u, v, weight=w)
        
        # Fixed layout for consistency
        self.pos = nx.spring_layout(self.G, seed=42, k=2)
        
        # Color schemes
        self.COLOR_U_SET = '#90EE90'  # Light green for U set (Prim)
        self.COLOR_V_MINUS_U = '#FFE4B5'  # Light yellow for V-U set (Prim)
        self.COLOR_MST_EDGE = '#FF6B6B'  # Red for MST edges
        self.COLOR_CANDIDATE_EDGE = '#FFD700'  # Gold for candidate edges
        self.COLOR_DEFAULT_EDGE = '#CCCCCC'  # Gray for default edges
        
        # Kruskal color palette for equivalence classes
        self.KRUSKAL_COLORS = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#FFA07A', '#98D8C8']
    
    def draw_graph_base(self, ax, title: str):
        """Draw the base graph"""
        # Draw all edges in gray
        nx.draw_networkx_edges(
            self.G, self.pos, ax=ax,
            edge_color=self.COLOR_DEFAULT_EDGE,
            width=2, alpha=0.6
        )
        
        # Draw all nodes
        nx.draw_networkx_nodes(
            self.G, self.pos, ax=ax,
            node_color='lightblue',
            node_size=2000,
            edgecolors='black',
            linewidths=2.5
        )
        
        # Draw labels
        nx.draw_networkx_labels(
            self.G, self.pos, ax=ax,
            font_size=16,
            font_weight='bold'
        )
        
        # Draw edge weights
        edge_labels = {(u, v): w for u, v, w in self.edges}
        nx.draw_networkx_edge_labels(
            self.G, self.pos, edge_labels, ax=ax,
            font_size=12,
            font_color='red',
            font_weight='bold'
        )
        
        ax.set_title(title, fontsize=18, fontweight='bold', pad=20)
        ax.axis('off')
    
    def visualize_graph(self):
        """Visualize the original weighted undirected graph"""
        fig, ax = plt.subplots(figsize=(12, 10))
        self.draw_graph_base(ax, "Weighted Undirected Connected Graph")
        
        # Add info text
        info_text = f"Vertices: {len(self.vertices)}, Edges: {len(self.edges)}\n"
        info_text += "All edges are weighted and graph is connected"
        plt.text(0.5, 0.02, info_text, 
                 ha='center', va='bottom',
                 transform=fig.transFigure,
                 fontsize=12, style='italic')
        
        plt.tight_layout()
        plt.savefig(f'{self.output_dir}/graph.png', dpi=150, bbox_inches='tight')
        plt.close()
        print(f"Saved: {self.output_dir}/graph.png")
    
    def prim_algorithm(self):
        """Prim's algorithm with step-by-step visualization"""
        # Start from vertex A
        start_vertex = 'A'
        U = {start_vertex}  # Vertices in MST
        V_minus_U = set(self.vertices) - U  # Vertices not in MST
        mst_edges = []
        total_weight = 0
        
        steps = []
        
        # Initial state
        steps.append({
            'U': U.copy(),
            'V_minus_U': V_minus_U.copy(),
            'mst_edges': [],
            'candidate_edge': None,
            'step_num': 0,
            'description': f"Initial: Start from vertex {start_vertex}"
        })
        
        step_num = 1
        while V_minus_U:
            # Find minimum edge connecting U to V-U
            min_edge = None
            min_weight = float('inf')
            
            for u in U:
                for v in V_minus_U:
                    if self.G.has_edge(u, v):
                        weight = self.G[u][v]['weight']
                        if weight < min_weight:
                            min_weight = weight
                            min_edge = (u, v, weight)
            
            if min_edge:
                u, v, weight = min_edge
                mst_edges.append(min_edge)
                total_weight += weight
                U.add(v)
                V_minus_U.remove(v)
                
                steps.append({
                    'U': U.copy(),
                    'V_minus_U': V_minus_U.copy(),
                    'mst_edges': mst_edges.copy(),
                    'candidate_edge': min_edge,
                    'step_num': step_num,
                    'description': f"Add edge ({u},{v}) weight={weight} to MST"
                })
                step_num += 1
        
        # Visualize all steps
        self._visualize_prim_steps(steps, total_weight)
    
    def _visualize_prim_steps(self, steps: List[Dict], total_weight: int):
        """Create visualization for all Prim's algorithm steps"""
        num_steps = len(steps)
        rows = (num_steps + 1) // 2
        cols = 2
        
        fig = plt.figure(figsize=(24, 12 * rows))
        
        for idx, step in enumerate(steps):
            ax = fig.add_subplot(rows, cols, idx + 1)
            
            # Draw edges
            # First, draw all edges in default color
            for u, v, w in self.edges:
                nx.draw_networkx_edges(
                    self.G, self.pos, [(u, v)], ax=ax,
                    edge_color=self.COLOR_DEFAULT_EDGE,
                    width=2, alpha=0.3
                )
            
            # Draw MST edges in red
            for u, v, w in step['mst_edges']:
                nx.draw_networkx_edges(
                    self.G, self.pos, [(u, v)], ax=ax,
                    edge_color=self.COLOR_MST_EDGE,
                    width=4, alpha=1.0
                )
            
            # Highlight candidate edge in gold
            if step['candidate_edge']:
                u, v, w = step['candidate_edge']
                nx.draw_networkx_edges(
                    self.G, self.pos, [(u, v)], ax=ax,
                    edge_color=self.COLOR_CANDIDATE_EDGE,
                    width=5, alpha=1.0,
                    style='dashed'
                )
            
            # Draw nodes colored by set membership
            node_colors = []
            for node in self.vertices:
                if node in step['U']:
                    node_colors.append(self.COLOR_U_SET)  # Green for U
                else:
                    node_colors.append(self.COLOR_V_MINUS_U)  # Yellow for V-U
            
            nx.draw_networkx_nodes(
                self.G, self.pos, ax=ax,
                node_color=node_colors,
                node_size=2000,
                edgecolors='black',
                linewidths=2.5
            )
            
            # Draw labels
            nx.draw_networkx_labels(
                self.G, self.pos, ax=ax,
                font_size=14,
                font_weight='bold'
            )
            
            # Draw edge weights
            edge_labels = {(u, v): w for u, v, w in self.edges}
            nx.draw_networkx_edge_labels(
                self.G, self.pos, edge_labels, ax=ax,
                font_size=10,
                font_color='red',
                font_weight='bold'
            )
            
            # Title
            title = f"Step {step['step_num']}: {step['description']}\n"
            title += f"U (green) = {{{', '.join(sorted(step['U']))}}}\n"
            title += f"V-U (yellow) = {{{', '.join(sorted(step['V_minus_U']))}}}"
            ax.set_title(title, fontsize=13, fontweight='bold', pad=15)
            ax.axis('off')
            
            # Create legend
            legend_elements = [
                mpatches.Patch(color=self.COLOR_U_SET, label='U set (in MST)'),
                mpatches.Patch(color=self.COLOR_V_MINUS_U, label='V-U set (not in MST)'),
                plt.Line2D([0], [0], color=self.COLOR_MST_EDGE, linewidth=4, label='MST edge'),
                plt.Line2D([0], [0], color=self.COLOR_CANDIDATE_EDGE, linewidth=5, 
                          linestyle='--', label='Candidate edge')
            ]
            ax.legend(handles=legend_elements, loc='upper right', fontsize=9)
        
        # Add overall title
        fig.suptitle(f"Prim's Algorithm - Total MST Weight: {total_weight}", 
                    fontsize=20, fontweight='bold', y=0.995)
        
        plt.tight_layout()
        plt.savefig(f'{self.output_dir}/prim_steps.png', dpi=150, bbox_inches='tight')
        plt.close()
        print(f"Saved: {self.output_dir}/prim_steps.png ({num_steps} steps)")
    
    def kruskal_algorithm(self):
        """Kruskal's algorithm with step-by-step visualization"""
        # Sort edges by weight
        sorted_edges = sorted(self.edges, key=lambda x: x[2])
        
        uf = UnionFind(self.vertices)
        mst_edges = []
        total_weight = 0
        
        steps = []
        
        # Initial state
        initial_components = uf.get_components()
        steps.append({
            'components': initial_components,
            'mst_edges': [],
            'current_edge': None,
            'edge_added': False,
            'step_num': 0,
            'description': "Initial: Each vertex is its own equivalence class"
        })
        
        step_num = 1
        for u, v, weight in sorted_edges:
            current_edge = (u, v, weight)
            edge_added = False
            
            # Check if adding this edge would create a cycle
            if uf.union(u, v):
                mst_edges.append(current_edge)
                total_weight += weight
                edge_added = True
                description = f"Add edge ({u},{v}) weight={weight}. Merge classes."
            else:
                description = f"Skip edge ({u},{v}) weight={weight}. Would create cycle."
            
            components = uf.get_components()
            steps.append({
                'components': components,
                'mst_edges': mst_edges.copy(),
                'current_edge': current_edge,
                'edge_added': edge_added,
                'step_num': step_num,
                'description': description
            })
            step_num += 1
            
            # Stop if MST is complete
            if len(mst_edges) == len(self.vertices) - 1:
                break
        
        # Visualize all steps
        self._visualize_kruskal_steps(steps, total_weight)
    
    def _visualize_kruskal_steps(self, steps: List[Dict], total_weight: int):
        """Create visualization for all Kruskal's algorithm steps"""
        num_steps = len(steps)
        rows = (num_steps + 1) // 2
        cols = 2
        
        fig = plt.figure(figsize=(24, 12 * rows))
        
        for idx, step in enumerate(steps):
            ax = fig.add_subplot(rows, cols, idx + 1)
            
            # Assign colors to equivalence classes
            components = step['components']
            color_map = {}
            for color_idx, (root, vertices) in enumerate(components.items()):
                color = self.KRUSKAL_COLORS[color_idx % len(self.KRUSKAL_COLORS)]
                for vertex in vertices:
                    color_map[vertex] = color
            
            # Draw edges
            # First, draw all edges in default color
            for u, v, w in self.edges:
                nx.draw_networkx_edges(
                    self.G, self.pos, [(u, v)], ax=ax,
                    edge_color=self.COLOR_DEFAULT_EDGE,
                    width=2, alpha=0.3
                )
            
            # Draw MST edges in thick red
            for u, v, w in step['mst_edges']:
                nx.draw_networkx_edges(
                    self.G, self.pos, [(u, v)], ax=ax,
                    edge_color=self.COLOR_MST_EDGE,
                    width=4, alpha=1.0
                )
            
            # Highlight current edge being considered
            if step['current_edge']:
                u, v, w = step['current_edge']
                if step['edge_added']:
                    # Green for added edge
                    edge_color = '#00FF00'
                    style = 'solid'
                else:
                    # Orange for rejected edge
                    edge_color = '#FFA500'
                    style = 'dashed'
                
                nx.draw_networkx_edges(
                    self.G, self.pos, [(u, v)], ax=ax,
                    edge_color=edge_color,
                    width=5, alpha=0.9,
                    style=style
                )
            
            # Draw nodes colored by equivalence class
            node_colors = [color_map[node] for node in self.vertices]
            
            nx.draw_networkx_nodes(
                self.G, self.pos, ax=ax,
                node_color=node_colors,
                node_size=2000,
                edgecolors='black',
                linewidths=2.5
            )
            
            # Draw labels
            nx.draw_networkx_labels(
                self.G, self.pos, ax=ax,
                font_size=14,
                font_weight='bold'
            )
            
            # Draw edge weights
            edge_labels = {(u, v): w for u, v, w in self.edges}
            nx.draw_networkx_edge_labels(
                self.G, self.pos, edge_labels, ax=ax,
                font_size=10,
                font_color='red',
                font_weight='bold'
            )
            
            # Title with equivalence classes
            title = f"Step {step['step_num']}: {step['description']}\n"
            title += "Equivalence Classes (same color = same class):\n"
            for root, vertices in components.items():
                title += f"{{{', '.join(sorted(vertices))}}}  "
            
            ax.set_title(title, fontsize=12, fontweight='bold', pad=15)
            ax.axis('off')
            
            # Create legend for equivalence classes
            legend_elements = [
                plt.Line2D([0], [0], color=self.COLOR_MST_EDGE, linewidth=4, label='MST edge'),
            ]
            for color_idx, (root, vertices) in enumerate(components.items()):
                color = self.KRUSKAL_COLORS[color_idx % len(self.KRUSKAL_COLORS)]
                label = f"Class: {{{', '.join(sorted(vertices))}}}"
                legend_elements.append(mpatches.Patch(color=color, label=label))
            
            ax.legend(handles=legend_elements, loc='upper right', fontsize=8)
        
        # Add overall title
        fig.suptitle(f"Kruskal's Algorithm - Total MST Weight: {total_weight}", 
                    fontsize=20, fontweight='bold', y=0.995)
        
        plt.tight_layout()
        plt.savefig(f'{self.output_dir}/kruskal_steps.png', dpi=150, bbox_inches='tight')
        plt.close()
        print(f"Saved: {self.output_dir}/kruskal_steps.png ({num_steps} steps)")
    
    def run(self):
        """Run all visualizations"""
        print("Generating MST Algorithm Visualizations...")
        print(f"Graph: {len(self.vertices)} vertices, {len(self.edges)} edges")
        print()
        
        # 1. Visualize the original graph
        print("1. Creating graph visualization...")
        self.visualize_graph()
        
        # 2. Run Prim's algorithm
        print("2. Running Prim's algorithm...")
        self.prim_algorithm()
        
        # 3. Run Kruskal's algorithm
        print("3. Running Kruskal's algorithm...")
        self.kruskal_algorithm()
        
        print()
        print("=" * 60)
        print("All visualizations completed successfully!")
        print(f"Output directory: {self.output_dir}/")
        print("Generated files:")
        print("  - graph.png (original graph)")
        print("  - prim_steps.png (Prim's algorithm steps)")
        print("  - kruskal_steps.png (Kruskal's algorithm steps)")
        print("=" * 60)


if __name__ == "__main__":
    visualizer = MSTVisualizer()
    visualizer.run()
