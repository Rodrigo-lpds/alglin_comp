# 2D Mesh Generator and Visualizer

This Python script generates 2D meshes (grids or circles) and provides visualizations of the mesh structure along with their adjacency matrices.

## Features

- **Mesh Types:** Generate regular grid meshes or circular meshes with random radii.
- **Randomization:** Optionally randomize triangle order and vertex positions.
- **Visualization:** Plot the generated mesh with labeled vertices and triangles.
- **Adjacency Matrix:** Display the adjacency matrix of the mesh, showing connections between vertices.

## Dependencies

- NumPy
- Matplotlib
- SciPy (for Delaunay triangulation in circular meshes)

## Usage

1.  **Install Dependencies:**
    ```bash
    pip install numpy matplotlib scipy
    ```

2.  **Run the Script:**
    ```bash
    python mesh_generator.py
    ```

    This will generate two example plots:

    - A 5x5 grid mesh
    - A circular mesh with 10 points

3.  **Customization:**

    Modify the arguments to `generate_mesh` and `plot_mesh_with_adjacency` within the script to create meshes with different sizes, shapes, and randomization options.

## Function Descriptions

- `generate_mesh(nodes, shape="grid", randomize_triangles=False, randomize_vertices=False)`:
    - Generates the mesh vertices and triangles.
    - `nodes`: Number of nodes (grid side length or circular points).
    - `shape`: "grid" or "circle"
    - `randomize_triangles`: Shuffle triangle indices (True/False).
    - `randomize_vertices`: Shuffle vertex positions (True/False).

- `plot_mesh_with_adjacency(vertices, triangles, title="Mesh")`:
    - Plots the mesh and adjacency matrix.
    - `vertices`: Array of vertex coordinates.
    - `triangles`: Array of triangle indices.
    - `title`: Plot title.

## Example

```python
plot_mesh_with_adjacency(*generate_mesh(8, shape="grid", randomize_vertices=True), "Randomized Grid Mesh 8x8")
```

This will create and plot a randomized 8x8 grid mesh.

## Contributing

Feel free to fork this repository and submit pull requests with improvements or additional features.

## License

This project is licensed under the MIT License.
