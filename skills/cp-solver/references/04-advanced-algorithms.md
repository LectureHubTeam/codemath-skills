# Advanced Algorithms — Thuật toán Nâng cao

> **Cách dùng file này:** Đọc phần "Khi nào dùng" và "Complexity" để chọn algorithm phù hợp.
> Sau đó dùng `view_file` để đọc implementation file tương ứng — KHÔNG cần đọc tất cả.

---

## Index — Chọn nhanh

| Algorithm | Khi nào dùng | Complexity | C++ | Python |
|-----------|-------------|------------|-----|--------|
| [Segment Tree](#1-segment-tree) | Range queries + point updates | O(log N) | [.cpp](implementations/segment-tree/segment_tree.cpp) | [.py](implementations/segment-tree/segment_tree.py) |
| [Segment Tree Lazy](#1b-segment-tree-lazy-propagation) | Range updates + range queries | O(log N) | [.cpp](implementations/segment-tree/segment_tree_lazy.cpp) | [.py](implementations/segment-tree/segment_tree_lazy.py) |
| [Fenwick Tree](#2-fenwick-tree-bit) | Point updates, prefix/range sum | O(log N) | [.cpp](implementations/fenwick-tree/fenwick_tree.cpp) | [.py](implementations/fenwick-tree/fenwick_tree.py) |
| [Mo's Algorithm](#3-mos-algorithm) | Offline range queries, no update | O(N√N) | [.cpp](implementations/mo-algorithm/mo_algorithm.cpp) | [.py](implementations/mo-algorithm/mo_algorithm.py) |
| [Digit DP](#4-digit-dp) | Đếm số thỏa điều kiện trên chữ số | O(log N × states) | [.cpp](implementations/digit-dp/digit_dp.cpp) | [.py](implementations/digit-dp/digit_dp.py) |
| [Matrix Exponentiation](#5-matrix-exponentiation) | Linear recurrence với N lớn ≤ 10^18 | O(K³ log N) | [.cpp](implementations/matrix-exp/matrix_exp.cpp) | [.py](implementations/matrix-exp/matrix_exp.py) |
| [HLD](#6-heavy-light-decomposition-hld) | Path queries trên cây với updates | O(log² N) | [.cpp](implementations/hld/hld.cpp) | [.py](implementations/hld/hld.py) |
| [Centroid Decomp](#7-centroid-decomposition) | Đếm paths thỏa điều kiện trên cây | O(N log N) | [.cpp](implementations/centroid-decomp/centroid.cpp) | — |
| [Suffix Array](#8-suffix-array--lcp) | String queries, LCS, pattern matching | O(N log N) build | [.cpp](implementations/suffix-array/suffix_array.cpp) | [.py](implementations/suffix-array/suffix_array.py) |

---

## 1. Segment Tree

### Khi nào dùng:
- **Range queries**: sum, min, max, GCD, XOR trên đoạn [l, r]
- **Point update**: cập nhật giá trị tại 1 vị trí
- N ≤ 10^5, Q ≤ 10^5

### Khi nào KHÔNG dùng:
- Không có update → dùng Prefix Sum hoặc Sparse Table (đơn giản hơn)
- Chỉ có prefix queries + point updates → dùng Fenwick Tree (ngắn gọn hơn)

### Complexity:
| Operation | Complexity |
|-----------|-----------|
| Build | O(N) |
| Point update | O(log N) |
| Range query | O(log N) |
| Memory | O(N) |

### Customize nhanh:
```
sum query:  op = +,   identity = 0
min query:  op = min, identity = +∞
max query:  op = max, identity = -∞
GCD query:  op = gcd, identity = 0
XOR query:  op = xor, identity = 0
```

### Implementation:
- **C++**: [implementations/segment-tree/segment_tree.cpp](implementations/segment-tree/segment_tree.cpp)
- **Python**: [implementations/segment-tree/segment_tree.py](implementations/segment-tree/segment_tree.py)

---

## 1b. Segment Tree — Lazy Propagation

### Khi nào dùng:
- **Range updates**: cập nhật toàn bộ đoạn [l, r] (add/set/multiply)
- **Range queries**: sau khi range update
- Khi Fenwick Tree không đủ (Fenwick chỉ có point update chuẩn)

### Complexity:
| Operation | Complexity |
|-----------|-----------|
| Range update | O(log N) |
| Range query | O(log N) |
| Memory | O(N) |

### Lưu ý:
Template hiện tại hỗ trợ **range add + range sum**.
Muốn range set hoặc multiply → cần thay `push()` và merge logic.

### Implementation:
- **C++**: [implementations/segment-tree/segment_tree_lazy.cpp](implementations/segment-tree/segment_tree_lazy.cpp)
- **Python**: [implementations/segment-tree/segment_tree_lazy.py](implementations/segment-tree/segment_tree_lazy.py)

---

## 2. Fenwick Tree (BIT)

### Khi nào dùng:
- **Point update** + **prefix sum** (hoặc range sum)
- Đơn giản hơn Segment Tree, constant factor nhỏ hơn
- Chỉ hỗ trợ phép toán có nghịch đảo: **sum, XOR** (không hỗ trợ min/max)

### So sánh với Segment Tree:
| | Fenwick | Segment Tree |
|--|---------|-------------|
| Code length | Ngắn (~15 lines) | Dài (~40 lines) |
| Constant factor | Nhỏ (~2x) | Lớn hơn |
| Range update | ❌ (cần trick) | ✅ (Lazy Prop) |
| Operations | sum, XOR | sum, min, max, GCD... |

### Complexity:
| Operation | Complexity |
|-----------|-----------|
| Update | O(log N) |
| Prefix query | O(log N) |
| Memory | O(N) |

### Bonus — Fenwick 2D:
File implementation có thêm **Fenwick 2D** cho bài toán trên ma trận.

### Implementation:
- **C++**: [implementations/fenwick-tree/fenwick_tree.cpp](implementations/fenwick-tree/fenwick_tree.cpp)
- **Python**: [implementations/fenwick-tree/fenwick_tree.py](implementations/fenwick-tree/fenwick_tree.py)

---

## 3. Mo's Algorithm

### Khi nào dùng:
- **Offline range queries** (biết trước tất cả queries)
- **Không có update** trong queries
- Điều kiện query phức tạp, khó dùng Segment Tree (vd: distinct count, mex, mode)
- N, Q ≤ 10^5

### Nguyên lý:
Sort queries theo block → pointer L, R di chuyển tổng O(N√N) thay vì O(N×Q).

### Complexity:
| | Complexity |
|--|-----------|
| Total | O((N+Q)√N) |
| Với N=Q=10^5 | ~3×10^7 operations |
| Optimal block size | √N |

### Customize:
Thay hàm `add(x)` và `remove(x)` trong file implementation:
- Distinct count: đếm khi cnt đổi 0↔1
- Sum: cộng/trừ giá trị
- Mode: dùng freq map

### Implementation:
- **C++**: [implementations/mo-algorithm/mo_algorithm.cpp](implementations/mo-algorithm/mo_algorithm.cpp)
- **Python**: [implementations/mo-algorithm/mo_algorithm.py](implementations/mo-algorithm/mo_algorithm.py)

---

## 4. Digit DP

### Khi nào dùng:
- Đếm số nguyên trong [1..N] thỏa điều kiện **trên chữ số**
- N cực lớn (10^18+), không thể duyệt trực tiếp
- Keywords: "đếm số có tổng chữ số = K", "không chứa chữ số X", "chia hết sau khi ghép digits"

### Cấu trúc DP:
```
dp(pos, state, tight, leading_zero)
  pos:          vị trí chữ số hiện tại (0 → len-1)
  state:        trạng thái tùy bài (sum mod K, last digit, bitmask...)
  tight:        đang bị ràng buộc bởi N không? (= digit ≤ N[pos])
  leading_zero: đang là số 0 đứng đầu? (để bỏ qua)
```

### Dấu hiệu nhận biết:
- "Tìm số trong đoạn [A, B] thỏa..." → f(B) - f(A-1)
- "Thỏa điều kiện trên chữ số" → Digit DP
- N có thể đến 10^18 → Digit DP (không thể duyệt)

### Implementation:
- **C++**: [implementations/digit-dp/digit_dp.cpp](implementations/digit-dp/digit_dp.cpp)
- **Python**: [implementations/digit-dp/digit_dp.py](implementations/digit-dp/digit_dp.py) — có `@lru_cache`, dễ customize hơn

---

## 5. Matrix Exponentiation

### Khi nào dùng:
- Tính **linear recurrence** với N cực lớn (N ≤ 10^18)
- Fibonacci, tribonacci, hay bất kỳ f(n) = c₁f(n-1) + c₂f(n-2) + ...
- Đếm đường đi độ dài K trên đồ thị
- DP transition có thể biểu diễn bằng matrix multiplication

### Nguyên lý:
```
[f(n)  ]   [1 1]^(n-1)   [f(1)]
[f(n-1)] = [1 0]       × [f(0)]
```

### Complexity:
| | Complexity |
|--|-----------|
| Matrix multiply (K×K) | O(K³) |
| Matrix power A^n | O(K³ log n) |
| Fibonacci (K=2) | O(8 log n) |

### Quy trình:
1. Xác định **state vector**: [f(n), f(n-1), ..., f(n-k+1)]
2. Xây **transition matrix** M sao cho state(n) = M × state(n-1)
3. Tính M^(n-k) × state(k)

### Implementation:
- **C++**: [implementations/matrix-exp/matrix_exp.cpp](implementations/matrix-exp/matrix_exp.cpp)
- **Python**: [implementations/matrix-exp/matrix_exp.py](implementations/matrix-exp/matrix_exp.py) — có helper `linear_recurrence()`

---

## 6. Heavy-Light Decomposition (HLD)

### Khi nào dùng:
- **Path queries** trên cây: sum/max/min trên toàn bộ path u→v
- **Path updates**: cập nhật giá trị trên path
- Kết hợp với Segment Tree để handle queries
- N ≤ 10^5

### Nguyên lý:
Phân rã cây thành các **heavy chains** → map về mảng 1D → Segment Tree.
Mỗi path u→v đi qua tối đa **O(log N)** chains.

### Complexity:
| | Complexity |
|--|-----------|
| Preprocessing | O(N log N) |
| Path query | O(log² N) |
| Path update | O(log² N) |

### Cần kết hợp với:
- Segment Tree (point update, range query) hoặc
- Segment Tree Lazy (range update, range query)

### Implementation:
- **C++**: [implementations/hld/hld.cpp](implementations/hld/hld.cpp)
- **Python**: [implementations/hld/hld.py](implementations/hld/hld.py) — iterative DFS, không stack overflow

---

## 7. Centroid Decomposition

### Khi nào dùng:
- **Đếm số paths** thỏa điều kiện trên cây (vd: path có tổng = K)
- Distance queries trên cây
- N ≤ 10^5

### Nguyên lý:
Tìm centroid (node mà khi xóa, subtree lớn nhất ≤ N/2) → Divide & Conquer trên cây.
Mỗi node chỉ là centroid tổ tiên của O(log N) nodes → tổng O(N log N).

### Complexity:
| | Complexity |
|--|-----------|
| Build centroid tree | O(N log N) |
| Queries (tùy loại) | O(N log N) hoặc O(N log² N) |

### Implementation:
- **C++**: [implementations/centroid-decomp/centroid.cpp](implementations/centroid-decomp/centroid.cpp)
- Python: Phức tạp với Python do recursion → khuyến nghị dùng C++ cho bài này

---

## 8. Suffix Array + LCP

### Khi nào dùng:
- **Pattern matching** với nhiều queries O(M log N) sau O(N log N) build
- **Longest Common Substring** của 2+ xâu
- **Số xâu con phân biệt**: N(N+1)/2 - sum(LCP)
- Bài toán xâu nâng cao với N ≤ 10^5

### Complexity:
| | Complexity |
|--|-----------|
| Build SA | O(N log² N) [prefix doubling] |
| Build LCP (Kasai) | O(N) |
| Pattern query | O(M log N) |

### So sánh với KMP:
| | KMP | Suffix Array |
|--|-----|-------------|
| Một pattern | O(N+M) | O(N log N + M log N) |
| Nhiều patterns | O(N × patterns) | O(N log N + Q × M log N) |
| Xâu con phân biệt | ❌ | ✅ |

### Implementation:
- **C++**: [implementations/suffix-array/suffix_array.cpp](implementations/suffix-array/suffix_array.cpp)
- **Python**: [implementations/suffix-array/suffix_array.py](implementations/suffix-array/suffix_array.py) — có `longest_common_substring()`

---

## Next Steps

Sau khi chọn algorithm:
1. `view_file` implementation C++ hoặc Python tương ứng
2. → Qua [03-optimization-patterns.md](03-optimization-patterns.md) nếu cần optimize thêm
3. → Qua [05-debugging-strategies.md](05-debugging-strategies.md) nếu gặp WA/TLE
