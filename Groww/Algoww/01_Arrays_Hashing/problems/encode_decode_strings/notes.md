# Encode and Decode Strings — Notes

## Pattern: Length-Prefixed Encoding (Delimiter Design)

## Approach: `length#string` Format
- **Encode**: For each string, prepend `len(str)#` → `"5#hello5#world"`
- **Decode**: Read digits until `#`, parse length, slice exactly that many chars, advance pointer

## Key Insight
Simple delimiters (`,`, `#`, `|`) fail because the string itself can contain any character. The solution: **don't search for delimiters in the content**. Instead, tell the decoder the exact length, so it reads by counting — never by searching.

Same principle as HTTP's `Content-Length` header — server says "next N bytes are the body", client reads exactly N bytes regardless of content.

## Why `length#string` Works for ANY Input
- The `#` only appears between the length digits and the string start
- Decoder reads digits → hits `#` → knows length → reads exactly that many chars
- Even if string contains `#` or digits, decoder skips over them by count, not by search

## Two Pythonic Tips
1. **f-strings for encode**: `res += f"{len(st)}#{st}"` — clean one-liner
2. **`str.find('#', i)` for decode**: Replaces manual character-by-character inner loop. Returns index of first `#` starting from position `i`.

## Complexity
- **Time**: O(n) — n = total characters across all strings. Single pass each for encode and decode.
- **Space**: O(1) extra — just pointer variable `i` (output doesn't count)

## Bugs I Hit
1. **Used `.append()` on a string** — strings don't have append. Then tried `.join()` which also wasn't right. Fix: `res += ...` (string concatenation). Root cause: confusing list methods with string operations.
2. **Forgot to initialize `i = 0`** in decode — used `i` without declaring it.

## Key Takeaways
- **Strings are immutable in Python** — every method returns a new string, never modifies in place. Build strings with `+=` or `"".join(list)`.
- **`str.join()` is a string method called ON the separator**: `",".join(["a","b"])` → `"a,b"`. It takes a list, not a single string.
- **Length-prefix is a universal encoding pattern** — HTTP, TCP, Protocol Buffers, and many serialization formats use it.

## Growth Observations
- Decode logic was clean on first attempt — the two-pointer/while-loop structure was solid
- Bugs were all in encode (Python string method confusion) — shows gap is in Python fluency, not algorithm thinking
- Connected the pattern to real-world systems (HTTP Content-Length) unprompted — systems thinking developing
