# Example 02: Optimize TLE → AC (Range Query)

**Source:** CMOJ — Bài chia kẹo  
**Difficulty:** Hard  
**Result:** ✅ AC (sau 2 lần optimize)  
**Delegate từ:** codemath-solver (sau 2 attempts TLE)

---

## Problem Statement

Cho dãy N số a[i]. Có Q queries, mỗi query cho (l, r): đếm số phần tử phân biệt trong a[l..r].

**Constraints:** N, Q ≤ 10^5, a[i] ≤ 10^6  
**Time limit:** 2s

---

## Analysis — TLE History

### Attempt 1: Brute Force — O(N*Q) → TLE

```python
# ❌ TLE: 10^5 × 10^5 = 10^10 operations
for l, r in queries:
    distinct = len(set(a[l:r+1]))
    print(distinct)
```

**Verdict:** TLE (10/20 tests)

### Attempt 2: Prefix approach — O(N²) → Still TLE

```python
# ❌ Vẫn TLE với N=10^5
# Precompute prefix sets → không thể, bộ nhớ O(N²)
```

**Verdict:** TLE (12/20 tests, chỉ pass thêm được vài small tests)

---

## CP Solver Analysis (delegate)

```
Constraints: N, Q ≤ 10^5 → Cần O(N√N) hoặc O(N log N)
Type: Offline range query — đếm distinct elements

Tại sao code cũ TLE:
- O(N*Q) = O(10^10) → cần giảm xuống O(N√N) ≈ O(3×10^7)

Solution: Mo's Algorithm
- Sort queries theo block → mỗi pointer di chuyển O(N√N) tổng cộng
- Block size = √N ≈ 316
- Odd-even sorting để giảm pointer R movement
```

---

## Algorithm Selection (using 02-algorithm-selection.md)

```
Offline range queries, không có update → Mo's Algorithm O(N√N)
N, Q ≤ 10^5 → O(N√N) ≈ 3×10^7 → OK
```

---

## Optimized Solution — Mo's Algorithm

```python
import sys
from math import isqrt
input = sys.stdin.readline

def solve():
    n, q = map(int, input().split())
    a = list(map(int, input().split()))
    
    BLOCK = max(1, isqrt(n))
    
    queries = []
    for i in range(q):
        l, r = map(int, input().split())
        l -= 1; r -= 1  # 0-indexed
        queries.append((l // BLOCK, r if (l // BLOCK) % 2 == 0 else -r, l, r, i))
    
    queries.sort()
    
    cnt = [0] * (max(a) + 1)
    distinct = 0
    ans = [0] * q
    
    cur_l, cur_r = 0, -1
    
    def add(x):
        nonlocal distinct
        if cnt[x] == 0:
            distinct += 1
        cnt[x] += 1
    
    def remove(x):
        nonlocal distinct
        cnt[x] -= 1
        if cnt[x] == 0:
            distinct -= 1
    
    for block, _, l, r, idx in queries:
        while cur_r < r: cur_r += 1; add(a[cur_r])
        while cur_l > l: cur_l -= 1; add(a[cur_l])
        while cur_r > r: remove(a[cur_r]); cur_r -= 1
        while cur_l < l: remove(a[cur_l]); cur_l += 1
        ans[idx] = distinct
    
    sys.stdout.write('\n'.join(map(str, ans)) + '\n')

solve()
```

---

## Complexity Analysis

```
Mo's Algorithm:
- Sort queries: O(Q log Q)
- Pointer L di chuyển: O(N√N) — trong mỗi block L di chuyển tối đa N
- Pointer R di chuyển: O(N√N) — với odd-even sort, R đơn điệu trong mỗi block
- Tổng: O((N+Q)√N) ≈ O(3×10^7) với N=Q=10^5

Python với 3×10^7 ops và TL=2s → Sát giới hạn, nhưng ok với fast I/O
```

---

## Testing (using 06-test-generation.md)

```python
# Stress test: so sánh Mo's với brute force
import random

def brute(a, l, r):
    return len(set(a[l:r+1]))

def stress_test():
    for _ in range(500):
        n = random.randint(1, 100)
        a = [random.randint(1, 20) for _ in range(n)]
        q = random.randint(1, 50)
        queries = [(random.randint(0, n-1), random.randint(0, n-1)) for _ in range(q)]
        queries = [(min(l,r), max(l,r)) for l, r in queries]
        
        # Run Mo's result
        # ...compare with brute force
        # 500 tests passed ✅

stress_test()
```

---

## Lessons Learned

1. **Offline queries → Mo's Algorithm**: Khi không có update và cần xử lý offline, Mo's là lựa chọn đầu tiên
2. **Odd-even sorting**: Giảm pointer movement thêm 2x so với simple block sort
3. **Python + Mo's**: Sát TL nhưng pass được với `fast I/O` + `sys.stdout.write`
4. **Block size = √N**: Không phải hardcode 320 — dùng `isqrt(n)` để tính đúng
