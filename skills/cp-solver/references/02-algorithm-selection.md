## Decision Tree Tổng quát

**Bước 1: Xác định loại bài toán**

```
(A) Tìm kiếm / đếm trong mảng/range?
    ├─ Có queries?
    │   ├─ Có update? → Segment Tree / Fenwick Tree
    │   └─ Không update?
    │       ├─ Mảng đã sort → Binary Search O(log N)
    │       ├─ Range sum/min/max → Prefix Sum / Sparse Table
    │       └─ Điều kiện phức tạp → Mo's Algorithm O(N√N)
    └─ Không có queries → Two Pointers / Sliding Window O(N)

(B) Tối ưu hóa (min/max/count)?
    ├─ Có cấu trúc con lằp nhau (overlapping subproblems)?
    │   └─ YES → Dynamic Programming
    ├─ Lựa chọn tham làm (greedy choice)?
    │   └─ YES → Greedy Algorithm
    └─ Hàm kiểm tra monotonic?
        └─ YES → Binary Search on Answer

(C) Bài toán trên đồ thị?
    ├─ Đường đi ngắn nhất → BFS / Dijkstra / Bellman-Ford
    ├─ Cây khung nhỏ nhất → Kruskal / Prim
    ├─ Liên thông, SCC → DFS / Tarjan / Kosaraju
    └─ Bài toán trên cây → DFS + DP / LCA / HLD

(D) Bài toán xâu/chuỗi?
    └─ → KMP / Suffix Array / Z-algorithm / Aho-Corasick

(E) Bài toán số học?
    └─ → Sieve / GCD / Modular / Miller-Rabin
```

**Bước 2:** Xác định cụ thể theo các section dưới đây.

---

## Decision Tree Chi tiết theo Dạng

### 1. Array/Sequence Problems

```
Bài toán trên dãy/mảng?
│
├─ Tìm phần tử thỏa mãn điều kiện?
│  ├─ Dãy đã sort → Binary Search O(log N)
│  └─ Dãy chưa sort → Sort + Binary Search O(N log N)
│
├─ Đếm số phần tử thỏa mãn?
│  ├─ Điều kiện đơn giản → Linear scan O(N)
│  ├─ Có nhiều queries → Prefix sum / Fenwick Tree
│  └─ Điều kiện phức tạp → Mo's Algorithm O(N√N)
│
├─ Tìm dãy con (subarray/subsequence)?
│  ├─ Dãy con liên tiếp → Sliding Window / Two Pointers
│  ├─ Dãy con không liên tiếp → DP
│  └─ Dãy con có tính chất đặc biệt → Binary Search on Answer
│
├─ Tối ưu (min/max/sum) trên khoảng?
│  ├─ Không có update → Segment Tree / Sparse Table
│  ├─ Có update → Segment Tree / Fenwick Tree
│  └─ Update range → Segment Tree với Lazy Propagation
│
└─ Sắp xếp lại / hoán vị?
   ├─ N nhỏ (≤ 10) → Brute force permutations O(N!)
   ├─ Tìm hoán vị thứ k → Next permutation / Factorial number system
   └─ Đếm số hoán vị → Combinatorics
```

### 2. Number Theory Problems

```
Bài toán số học?
│
├─ Liên quan số nguyên tố?
│  ├─ Kiểm tra 1 số → Trial division O(√N)
│  ├─ Kiểm tra nhiều số → Sieve of Eratosthenes O(N log log N)
│  └─ Số nguyên tố lớn (10^12+) → Miller-Rabin test
│
├─ Liên quan ước/bội?
│  ├─ Tìm GCD/LCM → Euclidean algorithm O(log N)
│  ├─ Đếm số ước → Prime factorization O(√N)
│  └─ Tìm ước chung → GCD + Divisor enumeration
│
├─ Tính toán modular?
│  ├─ Lũy thừa modular → Binary exponentiation O(log N)
│  ├─ Nghịch đảo modular → Extended Euclidean / Fermat's little theorem
│  └─ Tổ hợp modular → Lucas theorem / Precompute factorials
│
└─ Phương trình Diophantine?
   ├─ ax + by = c → Extended Euclidean
   ├─ ax ≡ b (mod n) → Modular inverse
   └─ Hệ phương trình → Chinese Remainder Theorem
```

### 3. Dynamic Programming Problems

```
Bài toán DP?
│
├─ Dạng dãy con?
│  ├─ Dãy con tăng dần → LIS O(N log N)
│  ├─ Dãy con có tổng lớn nhất → Kadane's / Prefix max
│  └─ Dãy con thỏa điều kiện → DP với state phù hợp
│
├─ Dạng đếm số cách?
│  ├─ Không giới hạn → DP đếm O(N²)
│  ├─ Giới hạn phần tử → DP với bitmask
│  └─ Giới hạn tổng → Knapsack-style DP
│
├─ Dạng tối ưu hóa?
│  ├─ Chia nhỏ bài toán → DP với recurrence
│  ├─ Có nhiều trạng thái → DP với memoization
│  └─ State quá lớn → DP optimization (Convex hull, CHT, etc.)
│
├─ Dạng trên cây?
│  ├─ DP trên cây → DFS + DP state
│  ├─ Đường đi dài nhất → Tree DP với 2 DFS
│  └─ Đếm số cách → Tree DP với combinatorics
│
└─ Dạng với chữ số?
   ├─ Đếm số thỏa điều kiện → Digit DP
   ├─ Tìm số thứ k → Digit DP với binary search
   └─ Tổng các chữ số → Digit DP với state sum
```

### 4. Graph Problems

```
Bài toán đồ thị?
│
├─ Đường đi ngắn nhất?
│  ├─ Unweighted graph → BFS O(V+E)
│  ├─ Weighted, non-negative → Dijkstra O(E log V)
│  ├─ Weighted, có âm → Bellman-Ford O(VE)
│  └─ All pairs → Floyd-Warshall O(V³) hoặc N lần Dijkstra
│
├─ Cây khung nhỏ nhất (MST)?
│  ├─ Dense graph → Prim O(E + V log V)
│  └─ Sparse graph → Kruskal O(E log E) với DSU
│
├─ Liên thông thành phần?
│  ├─ Undirected → DFS/BFS + count components
│  ├─ Directed → Kosaraju / Tarjan cho SCC
│  └─ Dynamic connectivity → DSU
│
├─ Luồng cực đại?
│  ├─ Nhỏ → Ford-Fulkerson O(V E²)
│  ├─ Vừa → Edmonds-Karp O(V E²)
│  └─ Lớn → Dinic O(V² E)
│
└─ Bài toán trên cây?
   ├─ Tìm LCA → Binary lifting O(N log N) preprocessing
   ├─ Đường đi dài nhất → 2 DFS hoặc Tree DP
   └─ Subtree queries → DFS order + Segment Tree
```

### 5. String Problems

```
Bài toán xâu/chuỗi?
│
├─ Tìm pattern trong text?
│  ├─ Pattern ngắn → Naive O(NM)
│  ├─ Pattern dài → KMP O(N+M)
│  └─ Nhiều patterns → Aho-Corasick
│
├─ Xâu con chung dài nhất?
│  ├─ 2 xâu → LCS DP O(N²)
│  ├─ Nhiều xâu → Suffix Automaton
│  └─ Xâu con chung của tất cả → Binary search + Hash/Rabin-Karp
│
├─ Palindrome?
│  ├─ Tìm palindrome dài nhất → Manacher O(N)
│  ├─ Đếm palindrome → DP hoặc Manacher
│  └─ Palindrome queries → Hash hoặc Palindrome Tree
│
├─ So sánh xâu / suffix?
│  ├─ Sort suffixes → Suffix Array O(N log²N)
│  ├─ LCP queries → Suffix Array + LCP array
│  └─ Pattern matching → Suffix Array + Binary search
│
└─ Xâu với operations?
   ├─ Edit distance → DP O(N²)
   ├─ String transformations → BFS trên state space
   └─ String construction → Greedy hoặc DP
```

### 6. Data Structure Problems

```
Bài toán cấu trúc dữ liệu?
│
├─ Range queries (sum/min/max)?
│  ├─ Static (không update) → Sparse Table O(1) query
│  ├─ Dynamic (có update) → Segment Tree O(log N)
│  └─ Point update only → Fenwick Tree O(log N)
│
├─ Range updates?
│  ├─ Set/Add trên khoảng → Segment Tree với Lazy Prop
│  └─ Complex updates → Segment Tree Beats
│
├─ Order statistics (k-th element)?
│  ├─ Static → Sort + Binary search
│  ├─ Dynamic → Order Statistic Tree / Segment Tree
│  └─ Range k-th → Merge Sort Tree / Persistent Segment Tree
│
├─ Queries trên cây?
│  ├─ Subtree queries → DFS order + Segment Tree
│  ├─ Path queries → Heavy-Light Decomposition
│  └─ LCA queries → Binary lifting
│
└─ Offline queries?
   ├─ Có thể sort queries → Mo's Algorithm O(N√N)
   ├─ Scan line → Sweep line algorithm
   └─ Process in specific order → Offline processing
```

---

### 7. Greedy Problems

```
Bài toán tham lam (Greedy)?
│
├─ Dấu hiệu nhận biết Greedy:
│  ├─ Tìm min/max bằng cách chọn lần lượt phần tử tối ưu
│  ├─ Không cần "hoàn tác" quyết định
│  └─ Có thể chứng minh lựa chọn cục bộ → tối ưu toàn cục
│
├─ Dạng Interval / Scheduling?
│  ├─ Chọn nhiều interval không chồng → Sort theo end time O(N log N)
│  ├─ Phủ khoảng bằng ít điểm nhất → Interval covering
│  └─ Merge intervals → Sort + scan O(N log N)
│
├─ Dạng Exchange Argument?
│  ├─ Sắp xếp lại để minimize/maximize → Custom sort comparator
│  └─ Chèm 2 phần tử kề nhau → Chứng minh thứ tự tối ưu
│
├─ Dạng Priority Queue / Huffman?
│  └─ Luôn chọn phần tử nhỏ/lớn nhất → Min-heap / Max-heap O(N log N)
│
└─ Dạng Fractional Knapsack / Ratio?
   └─ Sort theo giá trị/trọng lượng giảm dần → O(N log N)

⚠️ Lưu ý quan trọng: Greedy cần CHỨNG MINH tính đúng đắn.
Nếu không chứng minh được → cân nhắc dùng DP thay thế.
```

---

## Pattern Matching Table

### Khi gặp các tình huống sau:

| Tình huống | Pattern | Complexity |
|------------|---------|------------|
| "Tìm x thỏa mãn f(x) = k" | Binary Search | O(log N) |
| "Tìm min/max sao cho thỏa điều kiện" | Binary Search on Answer | O(log N * cost_of_check) |
| "Đếm số cặp (i,j) thỏa..." | Two Pointers / Fenwick Tree | O(N log N) |
| "Tìm dãy con dài nhất/ngắn nhất" | DP / Greedy | O(N²) or O(N log N) |
| "Có Q queries, mỗi query trên khoảng [l,r]" | Segment Tree / Mo's | O(Q log N) or O(N√N) |
| "Tìm đường đi ngắn nhất trên đồ thị" | BFS / Dijkstra | O(V+E) or O(E log V) |
| "Đếm số cách thực hiện X" | DP / Combinatorics | O(N²) or O(N) |
| "Xử lý trên cây, subtree, path" | DFS + Data Structure | O(N log N) |
| "Số lớn (> 10^18), xử lý chữ số" | Digit DP | O(log N * states) |
| "Tổ hợp chập k của n" | nCr với modular | O(N) preprocessing |

---

## Trade-off Analysis

### Khi có nhiều lựa chọn:

**Example 1: Range Sum Queries**
```
Options:
1. Prefix Sum:      O(1) query, O(N) build, NO updates
2. Fenwick Tree:    O(log N) query, O(N) build, YES updates
3. Segment Tree:    O(log N) query, O(N) build, YES updates + more features

Decision:
- Không có update → Prefix Sum (đơn giản nhất)
- Có update → Fenwick (ngắn gọn) hoặc Segment Tree (nhiều tính năng)
```

**Example 2: Shortest Path**
```
Options:
1. BFS:      O(V+E), unweighted only
2. Dijkstra: O(E log V), weighted non-negative
3. Bellman-Ford: O(VE), handles negative edges

Decision:
- Unweighted → BFS (nhanh nhất)
- Weighted, non-negative → Dijkstra
- Có edge âm → Bellman-Ford
```

**Example 3: String Matching**
```
Options:
1. Naive:     O(NM), simple to implement
2. KMP:       O(N+M), optimal for single pattern
3. Rabin-Karp: O(N+M) average, good for multiple patterns
4. Suffix Array: O(N log²N) build, O(M log N) query

Decision:
- Single pattern, N,M nhỏ → Naive (đơn giản)
- Single pattern, N,M lớn → KMP
- Multiple patterns → Aho-Corasick hoặc Rabin-Karp
- Nhiều queries → Suffix Array
```

---

## Algorithm Complexity Cheat Sheet

| Algorithm | Time | Space | When to use |
|-----------|------|-------|-------------|
| **Binary Search** | O(log N) | O(1) | Sorted array, monotonic function |
| **Two Pointers** | O(N) | O(1) | Sorted array, pair finding |
| **Sliding Window** | O(N) | O(1) | Subarray with property |
| **Prefix Sum** | O(1) query | O(N) | Range sum queries (static) |
| **Segment Tree** | O(log N) | O(N) | Range queries + updates |
| **Fenwick Tree** | O(log N) | O(N) | Point update, prefix queries |
| **Mo's Algorithm** | O(N√N) | O(N) | Offline range queries |
| **Dijkstra** | O(E log V) | O(V) | Shortest path, non-negative |
| **BFS** | O(V+E) | O(V) | Shortest path, unweighted |
| **DFS** | O(V+E) | O(V) | Traversal, connectivity |
| **KMP** | O(N+M) | O(M) | String matching |
| **LIS** | O(N log N) | O(N) | Longest increasing subsequence |
| **LCS** | O(N²) | O(N) | Longest common subsequence |
| **Sieve** | O(N log log N) | O(N) | Prime generation |
| **GCD** | O(log N) | O(1) | Greatest common divisor |

---

## Examples

### Example 1: Basic Selection

**Problem**: Cho dãy N số, Q queries dạng (l, r, k): tìm số nhỏ thứ k trong a[l..r].

**Analysis**:
```
Constraints: N, Q ≤ 10^5
Type: Range query + Order statistics

Options:
1. Sort mỗi query → O(Q * N log N) ❌ TLE
2. Merge Sort Tree → O(Q * log³N) ⚠️ Có thể TLE
3. Persistent Segment Tree → O((N+Q) log N) ✅

Decision: Persistent Segment Tree
```

### Example 2: Advanced Selection

**Problem**: Cho đồ thị N đỉnh, M cạnh. Tìm số thành phần liên thông sau mỗi lần thêm cạnh.

**Analysis**:
```
Constraints: N, M ≤ 10^5
Type: Dynamic connectivity

Options:
1. BFS/DFS sau mỗi query → O(M * (V+E)) ❌ TLE
2. DSU (Disjoint Set Union) → O(M * α(N)) ✅

Decision: DSU với path compression + union by rank
```

---

## Next Steps

Sau khi chọn thuật toán:
1. → Qua [03-optimization-patterns.md](03-optimization-patterns.md) để optimize
2. → Qua [04-advanced-algorithms.md](04-advanced-algorithms.md) nếu cần advanced technique
3. → Qua [05-debugging-strategies.md](05-debugging-strategies.md) nếu gặp lỗi
