"""
BFS on a Grid — Template + Traced Example
==========================================
Pattern: Start from cell → add to queue → process level by level

Use when: "shortest path", "minimum steps", "rotting oranges", "nearest exit"
Key difference from DFS: BFS gives you LEVELS (= distance/time)
"""

from collections import deque


# ============================================
# TEMPLATE — Copy this for any grid BFS problem
# ============================================
def bfs(grid, start_r, start_c, rows, cols):
    queue = deque()
    queue.append((start_r, start_c))
    grid[start_r][start_c] = -1  # mark visited BEFORE entering queue

    while queue:
        r, c = queue.popleft()

        # Process current cell here (depends on problem)

        # Check all 4 neighbors
        for dr, dc in [(1,0), (-1,0), (0,1), (0,-1)]:
            nr, nc = r + dr, c + dc

            # GUARD — skip if out of bounds or invalid
            if nr < 0 or nr >= rows or nc < 0 or nc >= cols:
                continue
            if grid[nr][nc] != 1:  # adjust per problem
                continue

            # MARK + ENQUEUE
            grid[nr][nc] = -1
            queue.append((nr, nc))


# ============================================
# EXAMPLE — Rotting Oranges (LC 994)
# ============================================
# Grid values: 0 = empty, 1 = fresh orange, 2 = rotten orange
# Each minute, rotten oranges rot their 4 neighbors
# Return: minutes until all oranges are rotten, or -1 if impossible
#
# Grid:
#   2 1 1
#   1 1 0
#   0 1 1
#
# Expected: 4 minutes

def rotting_oranges(grid):
    rows = len(grid)
    cols = len(grid[0])
    queue = deque()
    fresh = 0

    # Step 1: SEED the queue with ALL rotten oranges + count fresh
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == 2:
                queue.append((r, c))
            elif grid[r][c] == 1:
                fresh += 1

    if fresh == 0:
        return 0  # nothing to rot

    minutes = 0

    # Step 2: BFS level by level (each level = 1 minute)
    while queue:
        # Process ALL cells at current time step
        for _ in range(len(queue)):  # <-- THIS is the "level" trick
            r, c = queue.popleft()

            for dr, dc in [(1,0), (-1,0), (0,1), (0,-1)]:
                nr, nc = r + dr, c + dc

                if nr < 0 or nr >= rows or nc < 0 or nc >= cols:
                    continue
                if grid[nr][nc] != 1:  # skip if not fresh
                    continue

                grid[nr][nc] = 2  # rot it
                fresh -= 1
                queue.append((nr, nc))

        minutes += 1

    # We counted 1 extra minute (the last level had no new rotting)
    # Actually: we increment after every level including the last one
    # where nothing new was added. So subtract 1.
    return minutes - 1 if fresh == 0 else -1


# ============================================
# TRACE — What happens step by step
# ============================================
# Grid at start:
#   2 1 1       Rotten: (0,0)
#   1 1 0       Fresh: 5
#   0 1 1
#
# Queue seeded: [(0,0)]
#
# --- Minute 0 processing ---
# Pop (0,0): check neighbors
#   (1,0) = 1 fresh → rot it, fresh=4, enqueue
#   (0,1) = 1 fresh → rot it, fresh=3, enqueue
# minutes = 1
# Grid:     Queue: [(1,0), (0,1)]
#   2 2 1
#   2 1 0
#   0 1 1
#
# --- Minute 1 processing ---
# Pop (1,0): check neighbors
#   (2,0) = 0 → skip
#   (0,0) = 2 → skip (already rotten)
#   (1,1) = 1 fresh → rot it, fresh=2, enqueue
#   (1,-1) OOB → skip
# Pop (0,1): check neighbors
#   (1,1) = 2 → skip (just rotted!)
#   (0,2) = 1 fresh → rot it, fresh=1, enqueue
#   (0,0) = 2 → skip
# minutes = 2
# Grid:     Queue: [(1,1), (0,2)]
#   2 2 2
#   2 2 0
#   0 1 1
#
# --- Minute 2 processing ---
# Pop (1,1): check neighbors
#   (2,1) = 1 fresh → rot it, fresh=0, enqueue
#   (1,2) = 0 → skip
# Pop (0,2): no fresh neighbors
# minutes = 3
# Grid:     Queue: [(2,1)]
#   2 2 2
#   2 2 0
#   0 2 1
#
# --- Minute 3 processing ---
# Pop (2,1): check neighbors
#   (2,2) = 1 fresh → rot it, fresh=-1... wait
#   Actually fresh was 0, now fresh = -1? No!
#   Let me recount: we had fresh=1 after minute 2
#   (2,1) rotted → fresh=0? No, fresh was already 0.
#   Actually: after minute 2, fresh=0? Let me recount...
#
# RECOUNT carefully:
#   Start: fresh = 5
#   Min 0: rot (1,0) and (0,1) → fresh = 3
#   Min 1: rot (1,1) and (0,2) → fresh = 1
#   Min 2: rot (2,1)           → fresh = 0 ← but (2,2) is still fresh!
#   Wait: (2,2) = 1, it IS fresh. Let me recount original fresh.
#
#   Original grid fresh cells: (0,1), (0,2), (1,0), (1,1), (2,1), (2,2) = 6!
#   Start: fresh = 6 (not 5, I miscounted)
#   Min 0: rot (1,0), (0,1) → fresh = 4
#   Min 1: rot (1,1), (0,2) → fresh = 2
#   Min 2: rot (2,1)        → fresh = 1
#   Min 3: rot (2,2)        → fresh = 0
#   Queue empty, fresh = 0
#   minutes = 4, return 4 - 1... wait that gives 3.
#
# Hmm, let me re-examine the loop:
#   After minute 3 processing, minutes becomes 4
#   Queue is now empty → while loop ends
#   return 4 - 1 = 3? But expected answer is 4!
#
# The issue: we process minute 3 (pop (2,1), enqueue (2,2))
#   minutes = 4
# Then: minute 4 processing — pop (2,2), no fresh neighbors
#   minutes = 5
# Queue empty → return 5 - 1 = 4 ✓
#
# The "-1" accounts for the final empty pass!


# ============================================
# RUN IT
# ============================================
if __name__ == "__main__":
    # Test 1: standard case
    grid1 = [
        [2, 1, 1],
        [1, 1, 0],
        [0, 1, 1]
    ]
    result1 = rotting_oranges(grid1)
    print(f"Test 1: {result1} minutes")
    assert result1 == 4, f"Expected 4, got {result1}"

    # Test 2: impossible — isolated fresh orange
    grid2 = [
        [2, 1, 1],
        [0, 1, 1],
        [1, 0, 1]
    ]
    result2 = rotting_oranges(grid2)
    print(f"Test 2: {result2} (should be -1, impossible)")
    assert result2 == -1, f"Expected -1, got {result2}"

    # Test 3: already all rotten
    grid3 = [[2, 2]]
    result3 = rotting_oranges(grid3)
    print(f"Test 3: {result3} minutes")
    assert result3 == 0

    # Test 4: single fresh next to rotten
    grid4 = [[2, 1]]
    result4 = rotting_oranges(grid4)
    print(f"Test 4: {result4} minutes")
    assert result4 == 1

    print("All tests passed!")
