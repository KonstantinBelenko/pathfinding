from main import bfs, mark_path, print_grid, bfs_shortest_path, solve_tsp_dynamic, mark_path_on_grid
from collections import defaultdict

def calculate_distances(grid, points_of_interest, N):
    distances = defaultdict(dict)
    for i, point in enumerate(points_of_interest):
        distances[point] = bfs_shortest_path(grid, point, N)
    return distances

def handle_gem_inclusion(grid, start, target, N):
    points_of_interest = [start, target]
    points_of_interest += [(r, c) for r in range(N) for c in range(N) if grid[r][c] == 'G']
    distances = calculate_distances(grid, points_of_interest, N)
    path_order = solve_tsp_dynamic(points_of_interest, distances)
    return path_order

def process_grid(grid_dict):
    N = len(grid_dict["data"])
    grid = [list(row) for row in grid_dict["data"]]
    start, target = grid_dict["start"], grid_dict["target"]

    if any('G' in row for row in grid_dict["data"]):
        path_order = handle_gem_inclusion(grid, start, target, N)
        if path_order:
            for i in range(1, len(path_order)):
                mark_path_on_grid(grid, path_order[i - 1], path_order[i])
        else:
            print("No path found")
    else:
        path = bfs(grid, start, target, N)
        if path:
            mark_path(grid, path, start, target)
        else:
            print("No path found")
    print_grid(grid)

example_grids = [
    {"start": (0, 0), "target": (4, 4), "data": ["S....", ".#...", ".#...", ".#...", "....T"]},
    {"start": (0, 0), "target": (5, 6), "data": ["S.....", "######", "#....#", "#.##.#", "#....#", "#####T"]},
    {"start": (0, 0), "target": (6, 6), "data": ["S......", "###.###", "..#.#..", ".##.##.", ".#...#.", ".#####.", "......T"]},
    {"start": (0, 0), "target": (7, 7), "data": ["S.......", ".#######", "..#.....", ".##.###.", ".#...#.#", ".####.#.", ".#.....#", ".######T"]},
    {"start": (0, 0), "target": (8, 8), "data": ["S........", ".########", "..#......", ".##.#####", ".#...#...", ".####.#.#", ".#.....#.", ".######.#", ".......#T"]},
    {"start": (0, 0), "target": (8, 8), "data": ["S........", ".######.#", "..#......", "###.#####", ".#..#....", ".##.#.#.#", ".#....#..", ".######.#", "........T"]},
    {"start": (0, 0), "target": (8, 0), "data": ["S........", ".........", ".....G...", ".........", ".........", ".........", ".........", ".........", "T........"]}
]

# Test each example grid
for i, grid in enumerate(example_grids):
    print(f"Example Grid {i + 1}")
    process_grid(grid)
    print()
