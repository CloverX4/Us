# 14 — Intervals

## 🧠 Core Intuition
Interval problems follow a consistent approach: **Sort, then scan with overlap detection.**

The key question at each step: "Does this interval overlap with the previous one?"
- **Overlap**: `a.start < b.end AND b.start < a.end`
- **No overlap**: One ends before the other starts

## 🔑 Key Patterns

### 1. Merge Overlapping
- **When**: "Merge all overlapping intervals"
- **How**: Sort by start, merge with running end
```python
intervals.sort()
merged = [intervals[0]]
for start, end in intervals[1:]:
    if start <= merged[-1][1]:  # overlap
        merged[-1][1] = max(merged[-1][1], end)
    else:
        merged.append([start, end])
```

### 2. Insert Interval
- **When**: Add a new interval and merge if needed
- **How**: Find position, merge with overlapping, keep rest

### 3. Sweep Line / Event-Based
- **When**: "Maximum overlapping at any point" (Meeting Rooms II)
- **How**: Create events (start = +1, end = -1), sort, sweep
```python
events = []
for start, end in intervals:
    events.append((start, 1))   # meeting starts
    events.append((end, -1))    # meeting ends
events.sort()
active = max_active = 0
for time, delta in events:
    active += delta
    max_active = max(max_active, active)
```

## 🎯 Problems in This Section

| # | Problem | Difficulty | Status | Key Pattern |
|---|---------|-----------|--------|-------------|
| 1 | Meeting Rooms | Easy | ⬜ | Sort + overlap check |
| 2 | Merge Intervals | Medium | ⬜ | Sort + merge |
| 3 | Insert Interval | Medium | ⬜ | Binary search / linear scan |
| 4 | Non-Overlapping Intervals | Medium | ⬜ | Greedy (remove minimum) |
| 5 | Meeting Rooms II | Medium | ⬜ | Sweep line or heap |
| 6 | Minimum Interval to Include Each Query | Hard | ⬜ | Sort + heap |

## 💡 Interview Tips
- **Always sort first** — by start time (or end time for non-overlapping selection)
- Draw intervals on a number line — visualization is key
- Overlap condition: memorize it and verify with examples

## 🔗 Connections to Other Patterns
- Non-overlapping intervals → **Greedy** (sort by end time)
- Meeting Rooms II → **Heap** for tracking active meetings
- Sweep line → foundation for computational geometry
