import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial import Delaunay
from scipy.sparse import lil_matrix
from scipy.sparse.linalg import spsolve

def generate_mesh(nodes, shape="grid", randomize_triangles=False, randomize_vertices=False):
    """Generates 2D meshes (grid or circular) with optional randomization."""
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

def assemble_global_matrix(vertices, triangles):
    """Assembles the global stiffness matrix and load vector."""
    num_vertices = len(vertices)
    A = lil_matrix((num_vertices, num_vertices))
    b = np.zeros(num_vertices)

    def element_matrix_area(coords):
        """Calculates the area of the triangle and its stiffness matrix."""
        x1, y1 = coords[0]
        x2, y2 = coords[1]
        x3, y3 = coords[2]
        area = 0.5 * np.abs(x1*(y2 - y3) + x2*(y3 - y1) + x3*(y1 - y2))
        B = np.array([
            [y2 - y3, y3 - y1, y1 - y2],
            [x3 - x2, x1 - x3, x2 - x1]
        ]) / (2 * area)
        return area, B.T @ B * area

    for t in triangles:
        coords = vertices[t]
        area, Ke = element_matrix_area(coords)
        for i in range(3):
            for j in range(3):
                A[t[i], t[j]] += Ke[i, j]
        b[t] += area / 3

    return A, b

def apply_boundary_conditions(A, b, vertices, boundary_value=0):
    """Applies Dirichlet boundary conditions to the system."""
    for i, (x, y) in enumerate(vertices):
        if x in [0, 1] or y in [0, 1]:
            A[i, :] = 0
            A[i, i] = 1
            b[i] = boundary_value

def solve_system(A, b):
    """Solves the linear system."""
    return spsolve(A.tocsc(), b)

def plot_solution(vertices, solution, title="Solution"):
    """Plots the solution over the mesh."""
    plt.figure(figsize=(8, 6))
    plt.tricontourf(vertices[:, 0], vertices[:, 1], solution, levels=14, cmap="viridis")
    plt.colorbar()
    plt.title(title)
    plt.show()

# Example usage
vertices, triangles = generate_mesh(5, shape="grid")
plot_mesh_with_adjacency(vertices, triangles, "Grid Mesh")
A, b = assemble_global_matrix(vertices, triangles)
apply_boundary_conditions(A, b, vertices)
solution = solve_system(A, b)
plot_solution(vertices, solution)
