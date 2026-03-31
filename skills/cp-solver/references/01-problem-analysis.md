# Problem Analysis - Phân tích Bài toán CP

## 5 Bước Phân tích Đề

### Bước 1: Đọc Constraints → Complexity cho phép

| Constraints | Max Complexity (C++) | Max Complexity (Python) | Thuật toán phù hợp |
|-------------|---------------------|------------------------|-------------------|
| N ≤ 10 | O(N!), O(2^N) | O(N!), O(2^N) | Brute force, Permutation, Recursion |
| N ≤ 20 | O(2^N) | O(2^N) | Bitmask, Recursion + Memo |
| N ≤ 100 | O(N³) | O(N³) | Floyd-Warshall, O(N³) DP |
| N ≤ 500 | O(N³) | O(N²) ✅ O(N³) ⚠️ | DP, Matrix exponentiation |
| N ≤ 1000 | O(N²) | O(N²) ✅ | DP, BFS/DFS, Nested loops |
| N ≤ 3000 | O(N²) dễ dàng | O(N²) ⚠️ (~9s, cần fast) | DP O(N²), chú ý constant factor |
| N ≤ 10^4 | O(N√N), O(N log²N) | O(N log N) ✅ O(N√N) ⚠️ | Mo's algorithm, Square root decomp |
| N ≤ 10^5 | O(N log N), O(N) | O(N log N) ✅ (cần fast I/O) | Sort + Binary search, Segment Tree, Linear scan |
| N ≤ 10^6 | O(N), O(log N) | O(N) ⚠️ (cần sys.stdin) | Two pointers, Prefix sums, Binary search |
| N ≤ 10^9 | O(√N), O(log N) | O(√N), O(log N) | Math formula, Binary search |
| N ≤ 10^18 | O(log N) | O(log N) | Matrix exponentiation, Binary exponentiation |
| N ≤ 10^100 (string) | O(len) | O(len) | Digit processing, Big integer |

**⚠️ Lưu ý về Time Limit:**
- C++: Time limit 1s → ~10^8 operations
- C++: Time limit 2s → ~2×10^8 operations
- **Python chậm hơn C++ khoảng 10–50x** (KHÔNG phải 3-5x):
  - Python thực tế: ~10^6–10^7 operations/giây
  - Python với TL=1s: chịu được N ≤ ~3×10^3 với O(N²), N ≤ ~10^5 với O(N log N)
  - Python với TL=3s (CMOJ thường generous hơn): N ≤ ~3×10^5 với O(N)
  - **Luôn kiểm tra time limit của từng OJ với Python trước khi chọn complexity**

---

### Bước 2: Identify Keywords → Dạng bài

#### Signal Keywords Table

| Keywords | Dạng bài | Hướng tiếp cận |
|----------|----------|----------------|
| "nguyên tố", "ước", "bội", "GCD", "LCM", "chia hết", "modular" | **Number Theory** | Sieve, GCD, Modular arithmetic |
| "chữ số", "tổng chữ số", "số đặc biệt", N là số lớn | **Digit Processing** | Extract digits, Digit DP |
| "dãy con", "tối ưu", "lớn nhất/nhỏ nhất", "đếm số cách" | **Dynamic Programming** | State definition, Recurrence |
| "đường đi", "ngắn nhất", "đỉnh", "cạnh", "kết nối", "cây" | **Graph/Tree** | BFS, DFS, Dijkstra, MST, LCA |
| "xâu", "chuỗi", "palindrome", "substring", "pattern" | **String** | KMP, Suffix array, String DP |
| "sắp xếp", "thứ tự", "tìm kiếm", "nhỏ nhất thứ k" | **Sorting/Searching** | Sort, Binary search, Two pointers |
| "khoảng", "đoạn", "range", "query", "update" | **Data Structures** | Segment Tree, Fenwick Tree |
| "tam giác", "tọa độ", "vectơ", "diện tích", "góc" | **Geometry** | Coordinate geometry, Convex hull |
| "tổ hợp", "chỉnh hợp", "xác suất" | **Combinatorics** | nCr, nPr, Probability |
| "ma trận", "lũy thừa" | **Matrix** | Matrix multiplication, Exponentiation |

---

### Bước 3: Phân tích Input/Output

#### Check I/O Format

```python
# Standard I/O (stdin/stdout)
import sys
input = sys.stdin.readline

n = int(input())
a = list(map(int, input().split()))
print(answer)
```

```cpp
// Fast I/O
#include <bits/stdc++.h>
using namespace std;

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(NULL);
    
    int n;
    cin >> n;
    // solve
    cout << answer << "\n";
    return 0;
}
```

```python
# File I/O (khi đề yêu cầu)
import sys
sys.stdin = open('INPUT.INP', 'r')
sys.stdout = open('OUTPUT.OUT', 'w')
```

#### Multiple Test Cases?

```python
# Pattern: T test cases
t = int(input())
for _ in range(t):
    n = int(input())
    solve(n)
```

```cpp
// Pattern: T test cases
int t;
cin >> t;
while (t--) {
    int n;
    cin >> n;
    solve(n);
}
```

---

### Bước 4: Edge Cases Checklist

#### Common Edge Cases

- [ ] **N = 0**: Empty input?
- [ ] **N = 1**: Single element?
- [ ] **N = max**: Boundary value?
- [ ] **All same**: Tất cả phần tử giống nhau?
- [ ] **Sorted**: Đã sắp xếp (increasing/decreasing)?
- [ ] **Negative values**: Số âm?
- [ ] **Zero values**: Số 0?
- [ ] **Large values**: Overflow potential?
- [ ] **Prime/Special numbers**: Số nguyên tố, perfect square?

#### Example Analysis

```
Đề: Tìm số lớn nhất chưa xuất hiện trong dãy N số

Edge cases:
- N = 0: Output = 1
- Dãy = [1, 2, 3]: Output = 4 (max + 1)
- Dãy = [5, 10, 15]: Output = 14 (gap lớn nhất)
- Dãy toàn số âm: Xử lý riêng
```

---

### Bước 5: Think Through Examples

#### Tự test với sample nhỏ

```python
# Sample 1: N = 3, a = [1, 2, 3]
# Expected: 4
# Run: solve([1, 2, 3]) → 4 ✅

# Sample 2: N = 5, a = [5, 3, 1, 4, 2]
# Expected: 6
# Run: solve([5, 3, 1, 4, 2]) → 6 ✅

# Sample 3: N = 3, a = [10, 20, 30]
# Expected: 29 (gap giữa 20 và 30)
# Run: solve([10, 20, 30]) → 29 ✅
```

---

## Problem Analysis Template

```markdown
## Problem: [Tên bài]

### Constraints
- N ≤ ...
- Time limit: ...s
- Memory limit: ...MB

### Input/Output
- Input: ...
- Output: ...

### Keywords identified
- "..." → Dạng bài: ...

### Complexity required
- N = ... → Cần O(...) hoặc tốt hơn

### Edge cases to check
1. ...
2. ...
3. ...

### Sample walkthrough
- Sample 1: ...
- Sample 2: ...

### Potential approaches
1. Brute force: O(...) - để verify
2. Optimized: O(...) - để submit

### Algorithm selected
[Algorithm name]

### Why?
- ...
```

---

## Red Flags - Dấu hiệu cần lưu ý

### 🚩 TLE Risk
- Nested loops với N > 1000
- Recursion không memo với N > 20
- String concatenation trong loop
- I/O không optimization

### 🚩 WA Risk
- Floating point comparison
- Integer overflow (N > 2×10^9)
- Off-by-one errors (1-indexed vs 0-indexed)
- Not handling empty input

### 🚩 RE Risk
- Array out of bounds
- Division by zero
- Recursion depth > 10000
- Null pointer dereference

---

## Quick Reference: Problem Types

| Type | Common Patterns | Time Complexity |
|------|----------------|-----------------|
| **Array** | Prefix sum, Two pointers, Sliding window | O(N) |
| **String** | KMP, Suffix array, Hashing | O(N) or O(N log N) |
| **Number Theory** | Sieve, GCD, Modular arithmetic | O(√N) or O(log N) |
| **DP** | LIS, Knapsack, Digit DP | O(N²) or O(N) |
| **Graph** | BFS, DFS, Dijkstra, MST | O(V+E) or O(E log V) |
| **Tree** | DFS, LCA, Heavy-Light | O(N log N) |
| **Geometry** | Convex hull, Line sweep | O(N log N) |
| **Data Structures** | Segment Tree, Fenwick Tree | O(N log N) |

---

## Examples

### Example 1: Basic Analysis

**Problem**: Cho dãy N số, tìm số lớn nhất chưa xuất hiện.

**Analysis**:
```
Constraints: N ≤ 10^6 → Cần O(N) hoặc O(N log N)
Keywords: "lớn nhất", "chưa xuất hiện" → Set/Hashing
Input: N, sau đó N số
Output: 1 số nguyên

Edge cases:
- N = 0 → Output = 1
- Dãy đầy đủ 1→N → Output = N+1
- Dãy có gap → Output = số lớn nhất trong gap

Approach:
1. Brute force: Check 1, 2, 3, ... → O(N²) ❌
2. Optimized: Dùng set + scan → O(N) ✅
```

### Example 2: Advanced Analysis

**Problem**: Cho N queries, mỗi query cho (l, r, x). Đếm số phần tử chia hết cho x trong a[l..r].

**Analysis**:
```
Constraints: N, Q ≤ 10^5 → Cần O(N log N) hoặc O(N√N)
Keywords: "query", "khoảng", "đếm" → Range query
Input: N, Q, dãy a, sau đó Q dòng (l, r, x)
Output: Q dòng kết quả

Edge cases:
- l = r (single element)
- x = 1 (tất cả chia hết)
- x > max(a) (không có nào chia hết)

Approach:
1. Brute force: O(N*Q) ❌ TLE
2. Mo's algorithm: O(N√N) ✅
3. Offline + Fenwick: O(N log N + Q log N) ✅
```

---

## Practice Problems

| Problem | Difficulty | Focus |
|---------|------------|-------|
| Two Sum | Easy | Hashing, Two pointers |
| Maximum Subarray | Easy | Kadane's algorithm |
| Longest Increasing Subsequence | Medium | DP, Binary search |
| Merge Intervals | Medium | Sorting, Greedy |
| Number of Islands | Medium | BFS/DFS |
| Segment Tree Range Sum | Hard | Data structures |

---

## Next Steps

Sau khi phân tích xong:
1. → Qua [02-algorithm-selection.md](02-algorithm-selection.md) để chọn thuật toán
2. → Qua [03-optimization-patterns.md](03-optimization-patterns.md) để optimize
3. → Qua [05-debugging-strategies.md](05-debugging-strategies.md) nếu gặp lỗi
