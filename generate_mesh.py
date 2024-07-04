import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial import Delaunay

def generate_mesh(nodes, shape="grid", randomize_triangles=False, randomize_vertices=False):
    """Generates 2D meshes (grid or circular) with optional randomization.

    Args:
        nodes: Number of nodes in the mesh (grid: side length, circle: points on circumference)
        shape: Type of mesh ("grid" or "circle")
        randomize_triangles: Shuffle triangle indices (True/False)
        randomize_vertices: Shuffle vertex coordinates (True/False)

    Returns:
        vertices: (n, 2) array of vertex coordinates
        triangles: (m, 3) array of triangle indices
    """
    
    if shape == "grid":
        x = y = np.linspace(0, 1, nodes)
        X, Y = np.meshgrid(x, y)
        vertices = np.c_[X.ravel(), Y.ravel()]

        triangles = []
        for i in range(nodes - 1):
            for j in range(nodes - 1):
                idx = [i * nodes + j, (i + 1) * nodes + j, i * nodes + j + 1, (i + 1) * nodes + j + 1]
                triangles.extend([idx[:3], idx[1:]])
        triangles = np.array(triangles)

    elif shape == "circle":
        angles = np.linspace(0, 2 * np.pi, nodes, endpoint=False)
        radii = np.sqrt(np.random.rand(nodes))
        vertices = np.c_[radii * np.cos(angles), radii * np.sin(angles)]
        triangles = Delaunay(vertices).simplices

    else:
        raise ValueError("Invalid mesh shape. Choose 'grid' or 'circle'.")

    if randomize_triangles:
        np.random.shuffle(triangles)
    if randomize_vertices:
        np.random.shuffle(vertices)

    return vertices, triangles


def plot_mesh_with_adjacency(vertices, triangles, title="Mesh"):
    """Plots the mesh, labels vertices and triangles, and displays the adjacency matrix."""
    
    adj_matrix = np.zeros((len(vertices), len(vertices)), dtype=int)
    for t in triangles:
        adj_matrix[t[:, None], t] = 1
    adj_matrix += adj_matrix.T

    fig, axes = plt.subplots(1, 2, figsize=(12, 6))

    # Plot mesh
    axes[0].triplot(vertices[:, 0], vertices[:, 1], triangles, 'go-', lw=1)
    axes[0].plot(vertices[:, 0], vertices[:, 1], 'ro')
    for i, v in enumerate(vertices):
        axes[0].text(*v, str(i + 1), fontsize=8)
    for i, t in enumerate(triangles):
        axes[0].text(np.mean(vertices[t, 0]), np.mean(vertices[t, 1]), str(i + 1), fontsize=12)
    axes[0].set_title(title)
    axes[0].set_aspect('equal')

    # Plot adjacency matrix
    im = axes[1].imshow(adj_matrix, cmap='gray_r', interpolation='none')
    axes[1].set_title("Adjacency Matrix")
    for i in range(len(vertices)):
        axes[1].text(i, i, str(i + 1), ha="center", va="center", color="w")
    fig.colorbar(im, ax=axes[1], label="0 = White, 1 = Black")

    plt.show()
    

# Example usage
plot_mesh_with_adjacency(*generate_mesh(5, shape="grid"), "Grid Mesh 5x5")
#plot_mesh_with_adjacency(*generate_mesh(10, shape="circle"), "Circle Mesh")