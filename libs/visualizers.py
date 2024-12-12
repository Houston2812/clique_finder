import networkx as nx
import matplotlib.pyplot as plt

def visualize_graph(G: nx.Graph, title: str="Graph Visualization", dims: tuple = (20, 20)):
    plt.figure(figsize=dims)
    pos = nx.spring_layout(G)
    nx.draw(G, pos, with_labels=True, node_color='lightblue', 
            node_size=500, font_size=10, font_weight='bold')
    plt.title(title)
    plt.show()

def visualize_graph_customized(G: nx.Graph, title: str="Graph Visualization", 
                   color: bool = True, 
                   node_size: int = 1000,
                   font_size: int = 12,
                   layout: str = 'spring',
                   dims: tuple = (5, 5),
                   save: bool = False):
    """
    Visualize a graph with legacy metrics displayed in the upper left corner.
    
    Args:
        G (nx.Graph): NetworkX graph object to visualize
        title (str): Title of the visualization
        color (bool): Whether to color nodes based on clique membership
        node_size (int): Size of nodes in the visualization
        font_size (int): Size of node labels
        layout (str): Layout algorithm to use ('spring', 'circular', 'random', 'shell')
        dims (tuple): Figure dimensions as (width, height)
        save (bool): Whether to save the visualization to a file
    """
    # Create a single figure for the integrated visualization
    plt.figure(figsize=dims)
    
    # Set up layout functions dictionary
    layout_funcs: dict = {
        'spring': nx.spring_layout,
        'circular': nx.circular_layout,
        'random': nx.random_layout,
        'shell': nx.shell_layout
    }
    
    layout_func = layout_funcs.get(layout, nx.spring_layout)
    pos = layout_func(G)
    
    # Handle node coloring
    colors = None
    if color:
        colors = []
        cliques = list(nx.find_cliques(G))
        cliques.sort(key=len, reverse=True)
    
        for node in G.nodes():
            for i, clique in enumerate(cliques):
                if node in clique:
                    colors.append(i)
                    break
    else:
        colors = "lightblue"

    # Draw the main graph
    nx.draw(G, pos,
            with_labels=True,
            node_color=colors,
            node_size=node_size,
            font_size=font_size,
            font_weight='bold',
            edge_color='gray',
            width=2,
            alpha=0.8)
    
    plt.title(title, fontsize=16, pad=20)

    # Calculate legacy metrics
    metrics_text = (
        f"Metrics:\n"
        f"Nodes: {G.number_of_nodes()}\n"
        f"Edges: {G.number_of_edges()}\n"
        f"Density: {nx.density(G):.3f}"
    )
    
    # Add metrics text box in the upper left corner
    # The position coordinates are in axes coordinates (0,0 is bottom left, 1,1 is top right)
    plt.text(0.02, 0.98, metrics_text,
             transform=plt.gca().transAxes,  # This ensures position is relative to the axes
             bbox=dict(facecolor='white',
                      edgecolor='gray',
                      boxstyle='round,pad=0.5',
                      alpha=0.8),
             fontsize=10,
             verticalalignment='top')

    if save:
        plt.savefig(f'graph_pictures/{title}', transparent=True, bbox_inches='tight')
    
    plt.show()