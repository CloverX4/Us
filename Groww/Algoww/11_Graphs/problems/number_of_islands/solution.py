"""
Number of Islands (LC 200)
==========================
Amazon OA Style:

Amazon Logistics is mapping out warehouse zones in a new fulfillment region.
The region is represented as an m x n grid where:
- '1' represents a warehouse zone
- '0' represents empty land

Two warehouse zones are considered part of the SAME cluster if they are
adjacent horizontally or vertically (not diagonally).

Given the grid, return the total number of warehouse clusters.

Constraints:
- m == grid.length
- n == grid[i].length
- 1 <= m, n <= 300
- grid[i][j] is '0' or '1'

Pattern: ____GRID DFS_______
Time: O(m * n) Space: O(m * n) - 
"""

def dfs_connected_components(grid, row, col, rows, cols):
    if row < 0 or row >=rows or col < 0 or col >= cols or grid[row][col] == '0':
        return 0
    
    grid[row][col] = '0'

    dfs_connected_components(grid, row+1, col, rows, cols)
    dfs_connected_components(grid, row-1, col, rows, cols)
    dfs_connected_components(grid, row, col+1, rows, cols)
    dfs_connected_components(grid, row, col-1, rows, cols)

    return 1


def num_islands(grid: list[list[str]]) -> int:
    if not grid:
        return 0
    
    rows, cols = len(grid), len(grid[0])
    count = 0

    for row in range(rows):
        for col in range(cols):
            if grid[row][col] == '1':
                count += dfs_connected_components(grid, row, col, rows, cols)


    return count


# ============================================
# TESTS — Do NOT modify
# ============================================
if __name__ == "__main__":
    # Test 1: basic
    grid1 = [
        ["1","1","1","1","0"],
        ["1","1","0","1","0"],
        ["1","1","0","0","0"],
        ["0","0","0","0","0"]
    ]
    assert num_islands(grid1) == 1, f"Test 1 failed: {num_islands(grid1)}"

    # Test 2: multiple islands
    grid2 = [
        ["1","1","0","0","0"],
        ["1","1","0","0","0"],
        ["0","0","1","0","0"],
        ["0","0","0","1","1"]
    ]
    assert num_islands(grid2) == 3, f"Test 2 failed: {num_islands(grid2)}"

    # Test 3: all water
    grid3 = [
        ["0","0","0"],
        ["0","0","0"]
    ]
    assert num_islands(grid3) == 0

    # Test 4: all land
    grid4 = [
        ["1","1"],
        ["1","1"]
    ]
    assert num_islands(grid4) == 1

    # Test 5: diagonal doesn't count
    grid5 = [
        ["1","0"],
        ["0","1"]
    ]
    assert num_islands(grid5) == 2

    # Test 6: single cell
    grid6 = [["1"]]
    assert num_islands(grid6) == 1

    print("All tests passed!")
