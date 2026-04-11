"""
DFS on a Grid — Template + Traced Example
==========================================
Pattern: Visit a cell → mark it → recurse to all valid neighbors

Use when: "count islands", "flood fill", "find connected regions"
"""

# ============================================
# TEMPLATE — Copy this for any grid DFS problem
# ============================================
def dfs(grid, r, c, rows, cols):
    # Step 1: GUARD — stop if out of bounds or invalid
    if r < 0 or r >= rows or c < 0 or c >= cols:
        return
    if grid[r][c] != 1:  # adjust condition per problem
        return

    # Step 2: MARK — so we don't revisit
    grid[r][c] = -1  # or use a visited set

    # Step 3: RECURSE — visit all 4 neighbors
    dfs(grid, r + 1, c, rows, cols)  # down
    dfs(grid, r - 1, c, rows, cols)  # up
    dfs(grid, r, c + 1, rows, cols)  # right
    dfs(grid, r, c - 1, rows, cols)  # left


# ============================================
# EXAMPLE — Count number of islands
# ============================================
# Grid:
#   1 1 0
#   0 1 0
#   0 0 1
#
# Expected: 2 islands
#   Island 1: (0,0), (0,1), (1,1) — connected
#   Island 2: (2,2) — alone

def count_islands(grid):
    rows = len(grid)
    cols = len(grid[0])
    count = 0

    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == 1:       # found unvisited land
                count += 1            # new island!
                dfs(grid, r, c, rows, cols)  # sink the whole island

    return count


# ============================================
# TRACE — What happens step by step
# ============================================
# Grid at start:
#   1 1 0
#   0 1 0
#   0 0 1
#
# Scan (0,0): it's 1! → count = 1, start DFS
#   dfs(0,0): mark (0,0) = -1, recurse 4 dirs
#     dfs(1,0): grid[1][0] = 0 → GUARD stops
#     dfs(-1,0): out of bounds → GUARD stops
#     dfs(0,1): it's 1! mark (0,1) = -1, recurse
#       dfs(1,1): it's 1! mark (1,1) = -1, recurse
#         dfs(2,1): grid[2][1] = 0 → GUARD stops
#         dfs(0,1): grid[0][1] = -1 (visited) → GUARD stops
#         dfs(1,2): grid[1][2] = 0 → GUARD stops
#         dfs(1,0): grid[1][0] = 0 → GUARD stops
#       dfs(-1,1): out of bounds → GUARD stops
#       dfs(0,2): grid[0][2] = 0 → GUARD stops
#       dfs(0,0): grid[0][0] = -1 (visited) → GUARD stops
#     dfs(0,-1): out of bounds → GUARD stops
#
# Grid after island 1:
#   -1 -1  0
#    0 -1  0
#    0  0  1
#
# Scan continues... (0,1)=-1 skip, (0,2)=0 skip, (1,0)=0 skip...
# Scan (2,2): it's 1! → count = 2, start DFS
#   dfs(2,2): mark (2,2) = -1, recurse → all neighbors are 0 or OOB
#
# Final: count = 2 ✓


# ============================================
# RUN IT
# ============================================
if __name__ == "__main__":
    grid = [
        [1, 1, 0],
        [0, 1, 0],
        [0, 0, 1]
    ]
    result = count_islands(grid)
    print(f"Grid: {[[1,1,0],[0,1,0],[0,0,1]]}")
    print(f"Islands found: {result}")
    assert result == 2, f"Expected 2, got {result}"

    # Test 2: all connected = 1 island
    grid2 = [
        [1, 1, 1],
        [1, 1, 1],
    ]
    assert count_islands(grid2) == 1

    # Test 3: no land = 0 islands
    grid3 = [
        [0, 0],
        [0, 0],
    ]
    assert count_islands(grid3) == 0

    # Test 4: all separate = 4 islands
    grid4 = [
        [1, 0],
        [0, 1],
    ]
    assert count_islands(grid4) == 2

    print("All tests passed!")
