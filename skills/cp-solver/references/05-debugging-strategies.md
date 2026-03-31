# Debugging Strategies - Chiến lược Debug

## ⚠️ Python-Specific Issues (Đọc trước nếu dùng Python)

### 1. RecursionError — Default limit chỉ 1000

```python
# ❌ Lỗi phổ biến: RecursionError với cây/đồ thị sâu
def dfs(u, parent):
    for v in adj[u]:
        if v != parent:
            dfs(v, u)  # Crash nếu cây sâu hơn 1000 tầng

# ✅ Fix 1: Tăng limit — đặt ở đầu mỗi file CP
import sys
sys.setrecursionlimit(300000)  # Đủ cho cây N=10^5

# ✅ Fix 2 (An toàn hơn): Iterative DFS
def dfs_iterative(root, n):
    visited = [False] * n
    stack = [(root, -1)]
    while stack:
        u, parent = stack.pop()
        if visited[u]: continue
        visited[u] = True
        for v in adj[u]:
            if v != parent and not visited[v]:
                stack.append((v, u))
```

### 2. I/O chậm — input()/print() mặc định

```python
# ❌ SLOW: input() quá chậm với N ≥ 10^4
n = int(input())
a = list(map(int, input().split()))

# ✅ FAST: sys.stdin.readline — LUÔN dùng khi N ≥ 10^4
import sys
input = sys.stdin.readline

n = int(input())
a = list(map(int, input().split()))

# ✅ FASTEST: Đọc toàn bộ stdin 1 lần (cho bài nhiều query)
import sys
data = sys.stdin.buffer.read().split()
idx = 0
n = int(data[idx]); idx += 1
a = [int(data[idx+i]) for i in range(n)]; idx += n

# ✅ Output nhanh:
sys.stdout.write('\n'.join(map(str, answers)) + '\n')
# Hoặc:
print('\n'.join(map(str, answers)))
```

### 3. Global state không reset giữa các test cases

```python
# ❌ Lỗi: biến global không reset → WA từ test case 2 trở đi
visited = [False] * MAX_N  # Khai báo ngoài hàm
# ... giải test case 1 → visited bị thay đổi
# ... giải test case 2 → visited vẫn còn giá trị cũ!

# ✅ Fix: Reset trong mỗi test case
t = int(input())
for _ in range(t):
    n = int(input())
    visited = [False] * (n + 1)  # Reset mỗi lần
    solve(n)
```

### 4. Python trên CMOJ vs PyPy

```
- CMOJ thường chỉ có Python 3 (không có PyPy)
- Python: ~10^6–10^7 ops/giây → O(N²) với N=10^4 là giới hạn an toàn
- Nếu TLE với Python mà đã fast I/O và thuật toán đúng → Chuyển C++
- Python hợp với: Math, Binary search, String manipulation, DP đơn giản
- Python KHÔNG hợp với: Heavy Segment Tree queries, intensive loops với N=10^5
```

### 5. Negative modulo trong Python

```python
# Python xử lý modulo khác C++:
# Python: -7 % 3 = 2  (luôn non-negative)
# C++:    -7 % 3 = -1 (theo dấu của dividend)

# ✅ Python thường an toàn hơn, nhưng nếu cần đảm bảo:
result = ((a % MOD) + MOD) % MOD  # Chắc chắn non-negative
```

---

## Debug WA (Wrong Answer)

### Checklist khi bị WA

- [ ] **Edge cases**: N=0, N=1, max values
- [ ] **Overflow**: Dùng `long long` chưa? (N > 2×10^9)
- [ ] **Off-by-one**: 1-indexed vs 0-indexed?
- [ ] **Output format**: Có trailing newline không?
- [ ] **Multiple test cases**: Đã reset variables chưa?
- [ ] **Integer division**: Có bị truncation không?
- [ ] **Negative modulo**: `(a % n + n) % n`?
- [ ] **Floating point**: So sánh với epsilon?

### Strategy Debug WA

#### Bước 1: Test với sample nhỏ nhất

```python
# Sample từ đề
input_data = "3\n1 2 3"
expected = "4"
actual = run_solution(input_data)
assert actual == expected, f"Sample failed: {actual} != {expected}"
```

#### Bước 2: Tự tạo test cases

```python
# Edge cases
test_cases = [
    ("0\n", "1"),  # N = 0
    ("1\n5", "6"),  # N = 1
    ("3\n1 2 3", "4"),  # Full sequence
    ("3\n5 10 15", "14"),  # With gaps
]

for input_data, expected in test_cases:
    actual = run_solution(input_data)
    if actual != expected:
        print(f"WA: Input={input_data}, Expected={expected}, Got={actual}")
```

#### Bước 3: Print intermediate values

```cpp
// Thêm debug output
cerr << "i=" << i << ", a[i]=" << a[i] << ", sum=" << sum << endl;
cerr << "dp[" << i << "]=" << dp[i] << endl;
```

#### Bước 4: So sánh với Brute Force

```python
def brute_force(n, a):
    # O(N²) - correct but slow
    pass

def optimized(n, a):
    # O(N) - fast but might be wrong
    pass

# Compare
for n in range(1, 100):
    a = [random.randint(1, 100) for _ in range(n)]
    bf = brute_force(n, a.copy())
    opt = optimized(n, a.copy())
    if bf != opt:
        print(f"WA at n={n}, a={a}")
        print(f"BF={bf}, Opt={opt}")
        break
```

---

## Debug TLE (Time Limit Exceeded)

### Checklist khi bị TLE

- [ ] **Complexity đúng?** Check với constraints
- [ ] **Infinite loop?** Check loop conditions
- [ ] **Fast I/O?** (C++: `ios_base::sync_with_stdio(false);`)
- [ ] **Constant factor lớn?** Nested loops, string concatenation
- [ ] **Recursion depth?** Stack overflow risk
- [ ] **Unnecessary operations?** Redundant calculations

### Strategy Debug TLE

#### Bước 1: Profile - Test case nào chậm nhất?

```python
import time

start = time.time()
# Run solution
end = time.time()
print(f"Time: {end-start:.3f}s")
```

#### Bước 2: Count Operations

```
Max operations = Time limit (s) × 10^8

Example:
- 1s time limit → ~10^8 operations
- N = 10^5, O(N²) = 10^10 → TLE ❌
- N = 10^5, O(N log N) = 1.7×10^6 → AC ✅
```

#### Bước 3: Find Bottleneck

```cpp
// Thêm timing
auto start = chrono::high_resolution_clock::now();

// Code section 1
auto end1 = chrono::high_resolution_clock::now();
cerr << "Section 1: " << chrono::duration_cast<chrono::milliseconds>(end1-start).count() << "ms" << endl;

// Code section 2
auto end2 = chrono::high_resolution_clock::now();
cerr << "Section 2: " << chrono::duration_cast<chrono::milliseconds>(end2-end1).count() << "ms" << endl;
```

#### Bước 4: Optimize Hot Loops

```cpp
// ❌ SLOW: String concatenation trong loop
string result = "";
for (int i = 0; i < n; i++) {
    result += to_string(a[i]) + " ";  // O(N²)
}

// ✅ FAST: Dùng ostringstream
ostringstream oss;
for (int i = 0; i < n; i++) {
    oss << a[i] << " ";  // O(N)
}
string result = oss.str();
```

---

## Debug RE (Runtime Error)

### Common Causes

| Error | Nguyên nhân | Fix |
|-------|-------------|-----|
| **Segmentation Fault** | Array out of bounds | Check indices, array size |
| **Division by Zero** | `x % 0` hoặc `x / 0` | Check divisor before divide |
| **Stack Overflow** | Recursion depth > 10000 | Convert to iterative + stack |
| **Null Pointer** | Dereference null/invalid pointer | Check pointer before use |

### Strategy Debug RE

#### Bước 1: Check Array Bounds

```cpp
// Check trước khi access
if (i >= 0 && i < n && j >= 0 && j < m) {
    value = a[i][j];
} else {
    cerr << "Out of bounds: i=" << i << ", j=" << j << endl;
}
```

#### Bước 2: Check Division

```cpp
// Check divisor
if (divisor != 0) {
    result = dividend / divisor;
} else {
    cerr << "Division by zero!" << endl;
}
```

#### Bước 3: Check Recursion Depth

```cpp
// Thêm depth counter
int max_depth = 0;
void dfs(int u, int depth) {
    max_depth = max(max_depth, depth);
    if (depth > 10000) {
        cerr << "Deep recursion: depth=" << depth << endl;
        return;
    }
    // ...
}
```

---

## Debug CE (Compilation Error)

### Common Causes

| Error | Nguyên nhân | Fix |
|-------|-------------|-----|
| **Syntax Error** | Missing `;`, `)`, `}` | Check syntax carefully |
| **Type Mismatch** | Assign wrong type | Check variable types |
| **Undefined Variable** | Typo, scope issue | Check variable declaration |
| **Missing Header** | Forgot `#include` | Add required headers |

---

## Debug MLE (Memory Limit Exceeded)

### Checklist

- [ ] **Array size quá lớn?** Giảm kích thước
- [ ] **Vector/Map không clear?** Clear sau khi dùng
- [ ] **Recursion depth lớn?** Convert to iterative
- [ ] **Unnecessary data structures?** Optimize memory

### Strategy

```cpp
// ❌ SLOW: Allocate quá nhiều
vector<vector<vector<long long>>> dp(n, vector<vector<long long>>(n, vector<long long>(n)));

// ✅ FAST: Optimize memory
vector<vector<long long>> dp(n, vector<long long>(n));
// Hoặc dùng 1D array với indexing
vector<long long> dp(n*n*n);
auto get = [&](int i, int j, int k) { return dp[i*n*n + j*n + k]; };
```

---

## Debug Tools

### 1. Stress Testing Framework

```python
import random
import subprocess

def generate_test(n_max, val_max):
    n = random.randint(1, n_max)
    a = [random.randint(1, val_max) for _ in range(n)]
    return f"{n}\n" + " ".join(map(str, a))

def run_solution(input_data, solution_file):
    result = subprocess.run(
        ['python3', solution_file],
        input=input_data,
        capture_output=True,
        text=True
    )
    return result.stdout.strip()

# Stress test
for i in range(1000):
    test_input = generate_test(100, 100)
    bf = run_solution(test_input, 'brute_force.py')
    opt = run_solution(test_input, 'optimized.py')
    if bf != opt:
        print(f"Test {i}: WA!")
        print(f"Input: {test_input}")
        print(f"BF: {bf}, Opt: {opt}")
        with open('failed_test.txt', 'w') as f:
            f.write(test_input)
        break
else:
    print("All tests passed!")
```

### 2. Local Test with File I/O

```cpp
// test.cpp
#include <bits/stdc++.h>
using namespace std;

int main() {
    freopen("test.inp", "r", stdin);
    freopen("test.out", "w", stdout);
    
    // Run solution
    
    return 0;
}
```

### 3. Valgrind (cho C++)

```bash
# Check memory leaks
valgrind --leak-check=full ./solution < input.txt

# Check invalid memory access
valgrind --tool=memcheck ./solution < input.txt
```

---

## Debug Checklist Template

```markdown
## Debug Checklist

### WA
- [ ] Test với sample từ đề
- [ ] Test edge cases (N=0, N=1, max values)
- [ ] Check overflow (dùng long long?)
- [ ] Check off-by-one (1-indexed vs 0-indexed)
- [ ] Check output format (newline, spaces)
- [ ] Compare với brute force

### TLE
- [ ] Complexity đúng với constraints?
- [ ] Fast I/O?
- [ ] Infinite loop?
- [ ] Constant factor lớn?
- [ ] Profile: section nào chậm nhất?

### RE
- [ ] Array out of bounds?
- [ ] Division by zero?
- [ ] Stack overflow (recursion depth)?
- [ ] Null pointer?

### MLE
- [ ] Array size quá lớn?
- [ ] Vector/Map không clear?
- [ ] Unnecessary data structures?
```

---

## Examples

### Example 1: Debug WA

**Problem**: Tìm số lớn nhất chưa xuất hiện.

**Bug**: Không handle case N=0.

**Fix**:
```cpp
// ❌ BUG
int solve() {
    int max_val = *max_element(a.begin(), a.end());
    // ...
}

// ✅ FIX
int solve() {
    if (n == 0) return 1;  // Handle edge case
    int max_val = *max_element(a.begin(), a.end());
    // ...
}
```

### Example 2: Debug TLE

**Problem**: Đếm số cặp (i,j) với i<j và a[i]>a[j].

**Bug**: O(N²) với N=10^5.

**Fix**:
```cpp
// ❌ SLOW: O(N²)
for (int i = 0; i < n; i++)
    for (int j = i+1; j < n; j++)
        if (a[i] > a[j]) count++;

// ✅ FAST: O(N log N) - Fenwick Tree
FenwickTree ft(n);
for (int i = n-1; i >= 0; i--) {
    count += ft.query(a[i]-1);
    ft.update(a[i], 1);
}
```

---

## Next Steps

Sau khi debug xong:
1. → Re-submit và check verdict
2. → Nếu vẫn fail → Repeat debugging process
3. → Nếu AC → Qua bài tiếp theo hoặc contest

---

## Resources

- [Codeforces Debugging Tips](https://codeforces.com/blog/entry/97391)
- [C++ Debugging with GDB](https://www.gnu.org/software/gdb/)
- [Python Debugging with pdb](https://docs.python.org/3/library/pdb.html)
