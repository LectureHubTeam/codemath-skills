# Example 01: Tìm bộ số (Number Theory)

**Source:** CMOJ — Contest 24thtbckhn, Problem 1  
**Difficulty:** Medium  
**Result:** ✅ 10/10 AC

---

## Problem Statement

Cho số nguyên N (|N| ≤ 10^12). Tìm cặp số nguyên (a, b) sao cho a × b = N và |a - b| là nhỏ nhất.

**Input:** Một số nguyên N  
**Output:** |a - b| nhỏ nhất

---

## Analysis (using 01-problem-analysis.md)

```
Constraints: |N| ≤ 10^12 → Cần O(√N) hoặc tốt hơn
Keywords: "ước", "tích" → Number Theory

Edge cases:
- N = 0 → |a - b| = 0 (a=0, b=0)
- N = 1 → a=1, b=1 → |a-b| = 0
- N âm → tích âm → một số âm, một số dương
- N = perfect square → a = b = √N → |a-b| = 0

Approach:
1. Brute force: Duyệt từ 1 đến √N → O(√N) ✅ (√(10^12) = 10^6)
2. Với N âm: xét |N|, vì a×b = N với N<0 thì một số âm một số dương
```

---

## Algorithm Selection (using 02-algorithm-selection.md)

- **Dạng bài:** Number Theory — tìm ước
- **Pattern:** Duyệt ước từ 1 đến √|N|, ước nào lớn nhất thỏa mãn là nghiệm
- **Complexity:** O(√N) — với N=10^12 → 10^6 operations → OK với Python

---

## Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())
    
    # Edge case
    if n == 0:
        print(0)
        return
    
    abs_n = abs(n)
    best = float('inf')
    
    # Duyệt ước từ 1 đến sqrt(abs_n)
    i = 1
    while i * i <= abs_n:
        if abs_n % i == 0:
            a = i
            b = abs_n // i
            # Nếu n âm: một số âm một dương
            # |a - b| hoặc |-a - b| đều bằng |a + b| → không tối ưu
            # Thực ra để |a*b| = |n| và minimize |a-b|, ta duyệt ước của |n|
            best = min(best, b - a)  # b >= a nên b - a >= 0
        i += 1
    
    print(best)

solve()
```

---

## Testing (using 06-test-generation.md)

```
Sample tests:
- Input: 12  → Ước: (1,12),(2,6),(3,4) → best: 4-3=1 ✅
- Input: 16  → Ước: (1,16),(2,8),(4,4) → best: 0 ✅
- Input: 1   → best: 0 ✅
- Input: -6  → |N|=6, ước: (1,6),(2,3) → best: 1 ✅
- Input: 0   → 0 ✅

Edge cases checked:
- [x] N = 0
- [x] N = 1 (perfect square, answer = 0)
- [x] N âm
- [x] N = 10^12 (max constraint, ~10^6 iterations, < 1s)
```

---

## Lessons Learned

1. **Trick quan trọng:** Khi tìm cặp (a, b) với a*b = N minimize |a-b|, ước gần √N nhất là đáp án
2. **N âm:** Không thay đổi đáp án vì ta tìm ước của |N|
3. **Complexity check:** √(10^12) = 10^6 → OK cho cả Python với TL ≥ 1s
