"""
Flood Fill (LC 733)
===================
Amazon OA Style:

Amazon's warehouse management system displays a top-down floor plan as an m x n
grid of colored zones. A maintenance team needs to repaint a section starting
from a specific zone. Starting from zone (sr, sc), repaint that zone AND all
connected zones of the SAME original color with a new color.

Two zones are connected if they are adjacent horizontally or vertically.

Given the grid `image`, starting row `sr`, starting column `sc`, and `color`,
return the modified image after the flood fill.

Example:
  Input:  image = [[1,1,1],[1,1,0],[1,0,1]], sr = 1, sc = 1, color = 2
  Output: [[2,2,2],[2,2,0],[2,0,1]]

  The 1s connected to (1,1) all become 2. The 1 at (2,2) is NOT connected
  (diagonal doesn't count, and (2,1) is 0 blocking it).

Constraints:
- m == image.length, n == image[i].length
- 1 <= m, n <= 50
- 0 <= image[i][j], color < 2^16
- 0 <= sr < m, 0 <= sc < n

Pattern: ___________
Time: O(___) Space: O(___)
"""
def flood_fill_connected(image, row, col, rows, cols, color, color_new):
    if row<0 or row>=rows or col<0 or col>=cols or image[row][col] != color or image[row][col] == color_new:
        # or image[row][col] == color_new -- important learning ... without this it goes into a infinite loop of coloring hte smae cell with same color again and again
        # this fives the case that if the cell is already colored wiht that color just skip it
        return 
    
    image[row][col] = color_new

    flood_fill_connected(image, row+1, col, rows, cols, color, color_new)
    flood_fill_connected(image, row-1, col, rows, cols, color, color_new)
    flood_fill_connected(image, row, col+1, rows, cols, color, color_new)
    flood_fill_connected(image, row, col-1, rows, cols, color, color_new)

    return


def flood_fill(image: list[list[int]], sr: int, sc: int, color: int) -> list[list[int]]:
    rows, cols = len(image), len(image[0])

    flood_fill_connected(image, sr, sc, rows, cols, image[sr][sc], color)

    return image


# ============================================
# TESTS — Do NOT modify
# ============================================
if __name__ == "__main__":
    # Test 1: basic
    img1 = [[1,1,1],[1,1,0],[1,0,1]]
    result1 = flood_fill(img1, 1, 1, 2)
    assert result1 == [[2,2,2],[2,2,0],[2,0,1]], f"Test 1 failed: {result1}"

    # Test 2: already the target color (edge case!)
    img2 = [[0,0,0],[0,0,0]]
    result2 = flood_fill(img2, 0, 0, 0)
    assert result2 == [[0,0,0],[0,0,0]], f"Test 2 failed: {result2}"

    # Test 3: single cell
    img3 = [[2]]
    result3 = flood_fill(img3, 0, 0, 5)
    assert result3 == [[5]], f"Test 3 failed: {result3}"

    # Test 4: only partial fill
    img4 = [[0,0,0],[0,1,1]]
    result4 = flood_fill(img4, 1, 1, 1)
    assert result4 == [[0,0,0],[0,1,1]], f"Test 4 failed: {result4}"

    # Test 5: L-shaped region
    img5 = [[1,1,0],[1,0,0],[1,1,1]]
    result5 = flood_fill(img5, 0, 0, 3)
    assert result5 == [[3,3,0],[3,0,0],[3,3,3]], f"Test 5 failed: {result5}"

    print("All tests passed!")
