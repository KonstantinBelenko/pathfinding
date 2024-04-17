from collections import deque, defaultdict
import sys

DIRECTIONS = [(-1, 0), (1, 0), (0, -1), (0, 1)]
SYMBOLS = {
    ".": "🌊", "#": "🧱", "S": "🦈", "T": "🎯", "o": "🔷", "G": "💎"
}

def read_input():
    N = int(input().strip())
    grid = [list(input().strip()) for _ in range(N)]
    return N, grid

def mark_path(grid, path, start, target):
    for i in range(1, len(path)):
        grid[path[i][0]][path[i][1]] = 'o'
    grid[target[0]][target[1]] = 'T'

def mark_grid_from_path_order(grid, path_order):
    for i in range(1, len(path_order)):
        mark_path_on_grid(grid, path_order[i - 1], path_order[i])

def mark_path_on_grid(grid, start, end):
    queue = deque([start])
    visited = set([start])
    parents = {start: None}
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    
    while queue:
        current = queue.popleft()
        if current == end:
            break
        for dx, dy in directions:
            nx, ny = current[0] + dx, current[1] + dy
            if 0 <= nx < len(grid) and 0 <= ny < len(grid[0]) and (nx, ny) not in visited and grid[nx][ny] != '#':
                visited.add((nx, ny))
                queue.append((nx, ny))
                parents[(nx, ny)] = current
    
    step = end
    while parents[step] is not None:
        grid[step[0]][step[1]] = 'o'
        step = parents[step]
    grid[start[0]][start[1]] = 'S'
    grid[end[0]][end[1]] = 'T'

def print_grid(grid):
    translation_map = str.maketrans(SYMBOLS)
    for row in grid:
        print("".join(row).translate(translation_map))

def bfs(grid, start, target, N):
    queue = deque([start])
    visited = set([start])
    path = {}
    
    while queue:
        current = queue.popleft()
        if current == target:
            return reconstruct_path(path, start, target)
        
        for dr, dc in DIRECTIONS:
            nr, nc = current[0] + dr, current[1] + dc
            if 0 <= nr < N and 0 <= nc < N and grid[nr][nc] != '#' and (nr, nc) not in visited:
                visited.add((nr, nc))
                queue.append((nr, nc))
                path[(nr, nc)] = current

def reconstruct_path(path, start, target):
    current = target
    reconstructed_path = [current]
    while current != start:
        current = path[current]
        reconstructed_path.append(current)
    reconstructed_path.reverse()
    return reconstructed_path

def bfs_shortest_path(grid, start, N):
    queue = deque([start])
    visited = set([start])
    distance = {start: 0}
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    
    while queue:
        current = queue.popleft()
        for dr, dc in directions:
            nr, nc = current[0] + dr, current[1] + dc
            if 0 <= nr < N and 0 <= nc < N and grid[nr][nc] != '#' and (nr, nc) not in visited:
                visited.add((nr, nc))
                queue.append((nr, nc))
                distance[(nr, nc)] = distance[current] + 1
    
    return distance

def solve_tsp_dynamic(points, distances):
    n = len(points)
    if n == 2:
        return points
    dp = [[sys.maxsize] * n for _ in range(1 << n)]
    backtrack = [[-1] * n for _ in range(1 << n)]
    dp[1][0] = 0

    for mask in range(1 << n):
        for i in range(n):
            if mask & (1 << i):
                for j in range(n):
                    if not mask & (1 << j):
                        next_mask = mask | (1 << j)
                        new_dist = dp[mask][i] + distances[points[i]][points[j]]
                        if new_dist < dp[next_mask][j]:
                            dp[next_mask][j] = new_dist
                            backtrack[next_mask][j] = i

    min_cost = sys.maxsize
    last_point = -1
    for i in range(1, n):
        cost = dp[(1 << n) - 1][i]
        if cost < min_cost:
            min_cost = cost
            last_point = i

    if last_point == -1:
        return None

    order = []
    mask = (1 << n) - 1
    while last_point != -1:
        order.append(points[last_point])
        next_point = backtrack[mask][last_point]
        mask ^= (1 << last_point)
        last_point = next_point

    order.reverse()
    return order

def main():
    N, grid = read_input()
    points_of_interest = []
    distances = defaultdict(dict)

    for r in range(N):
        for c in range(N):
            if grid[r][c] in 'SGT' or grid[r][c] == 'G':
                points_of_interest.append((r, c))

    for i, point in enumerate(points_of_interest):
        dist = bfs_shortest_path(grid, point, N)
        for j, other in enumerate(points_of_interest):
            distances[point][other] = dist.get(other, sys.maxsize)

    order = solve_tsp_dynamic(points_of_interest, distances)
    if order:
        print("Path order:", order)
    else:
        print("No path found from start to target through all gems.")

if __name__ == "__main__":
    main()
