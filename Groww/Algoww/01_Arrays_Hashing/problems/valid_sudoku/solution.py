# Valid Sudoku
# https://leetcode.com/problems/valid-sudoku/
#
# Determine if a 9x9 Sudoku board is valid. Only the filled cells
# need to be validated according to the following rules:
# 1. Each row must contain the digits 1-9 without repetition.
# 2. Each column must contain the digits 1-9 without repetition.
# 3. Each of the nine 3x3 sub-boxes must contain the digits 1-9
#    without repetition.
#
# Note: A partially filled board could be valid — it does NOT need
# to be solvable.
#
# Example 1:
# Input: board = [["5","3",".",".","7",".",".",".","."],
#                 ["6",".",".","1","9","5",".",".","."],
#                 [".","9","8",".",".",".",".","6","."],
#                 ["8",".",".",".","6",".",".",".","3"],
#                 ["4",".",".","8",".","3",".",".","1"],
#                 ["7",".",".",".","2",".",".",".","6"],
#                 [".","6",".",".",".",".","2","8","."],
#                 [".",".",".","4","1","9",".",".","5"],
#                 [".",".",".",".","8",".",".","7","9"]]
# Output: true
#
# Example 2: Same as above but board[0][0] = "8" → false
#   (Two 8s in the top-left 3x3 box)
#
# Constraints:
# - board.length == 9
# - board[i].length == 9
# - board[i][j] is a digit '1'-'9' or '.'
#
# Write your solution below:
from collections import defaultdict

def isValidSudoku(board: list[list[str]]) -> bool:
    row = defaultdict(set)
    col = defaultdict(set)
    box = defaultdict(set)

    for i in range(9):
        for j in range(9):
            curr = board[i][j]
            if curr == ".":
                continue

            if curr in row[i] or curr in col[j] or curr in box[(i//3, j//3)]:
                return False

            row[i].add(curr)
            col[j].add(curr)    
            box[(i//3, j//3)].add(curr) # // is for integer division!! remember

    return True


# ---- Test Cases ----
if __name__ == "__main__":
    # Test 1: Valid board
    valid_board = [
        ["5","3",".",".","7",".",".",".","."],
        ["6",".",".","1","9","5",".",".","."],
        [".","9","8",".",".",".",".","6","."],
        ["8",".",".",".","6",".",".",".","3"],
        ["4",".",".","8",".","3",".",".","1"],
        ["7",".",".",".","2",".",".",".","6"],
        [".","6",".",".",".",".","2","8","."],
        [".",".",".","4","1","9",".",".","5"],
        [".",".",".",".","8",".",".","7","9"]
    ]
    assert isValidSudoku(valid_board) == True, "Test 1 Failed: valid board"

    # Test 2: Invalid — duplicate in column
    invalid_board = [
        ["8","3",".",".","7",".",".",".","."],
        ["6",".",".","1","9","5",".",".","."],
        [".","9","8",".",".",".",".","6","."],
        ["8",".",".",".","6",".",".",".","3"],
        ["4",".",".","8",".","3",".",".","1"],
        ["7",".",".",".","2",".",".",".","6"],
        [".","6",".",".",".",".","2","8","."],
        [".",".",".","4","1","9",".",".","5"],
        [".",".",".",".","8",".",".","7","9"]
    ]
    assert isValidSudoku(invalid_board) == False, "Test 2 Failed: duplicate in column & box"

    # Test 3: Empty board (all dots) — valid
    empty_board = [["." for _ in range(9)] for _ in range(9)]
    assert isValidSudoku(empty_board) == True, "Test 3 Failed: empty board should be valid"

    # Test 4: Single element — valid
    single = [["." for _ in range(9)] for _ in range(9)]
    single[0][0] = "5"
    assert isValidSudoku(single) == True, "Test 4 Failed: single element"

    # Test 5: Duplicate in same row
    row_dup = [["." for _ in range(9)] for _ in range(9)]
    row_dup[0][0] = "1"
    row_dup[0][8] = "1"
    assert isValidSudoku(row_dup) == False, "Test 5 Failed: duplicate in row"

    # Test 6: Duplicate in same 3x3 box but different row/col
    box_dup = [["." for _ in range(9)] for _ in range(9)]
    box_dup[0][0] = "1"
    box_dup[2][2] = "1"
    assert isValidSudoku(box_dup) == False, "Test 6 Failed: duplicate in box"

    print("✅ All tests passed!")
