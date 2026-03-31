# Optimization Patterns - Pattern Tối ưu hóa

## Pattern 1: O(N²) → O(N log N)

### Khi nào dùng:
- N ≤ 10^5, hiện tại O(N²) bị TLE
- Có nested loops với N lớn

### Cách tiếp cận:

#### 1. Sort + Binary Search

```cpp
// ❌ SLOW: O(N²)
for (int i = 0; i < n; i++) {
    for (int j = i+1; j < n; j++) {
        if (a[j] > a[i]) count++;
    }
}

// ✅ FAST: O(N log N) - Sort + Binary Search
sort(a, a+n);
for (int i = 0; i < n; i++) {
    // Tìm số phần tử > a[i]
    auto it = upper_bound(a+i+1, a+n, a[i]);
    count += (a+n) - it;
}
```

#### 2. Two Pointers

```cpp
// ❌ SLOW: O(N²) - Tìm cặp có tổng = K
for (int i = 0; i < n; i++) {
    for (int j = i+1; j < n; j++) {
        if (a[i] + a[j] == K) return {i, j};
    }
}

// ✅ FAST: O(N) - Two Pointers (sau khi sort)
sort(a, a+n);
int l = 0, r = n-1;
while (l < r) {
    int sum = a[l] + a[r];
    if (sum == K) return {l, r};
    else if (sum < K) l++;
    else r--;
}
```

#### 3. Fenwick Tree / Segment Tree

```cpp
// ❌ SLOW: O(N²) - Đếm số cặp nghịch thế
for (int i = 0; i < n; i++)
    for (int j = i+1; j < n; j++)
        if (a[i] > a[j]) inversions++;

// ✅ FAST: O(N log N) - Fenwick Tree
FenwickTree ft(n);
for (int i = n-1; i >= 0; i--) {
    inversions += ft.query(a[i]-1);  // Số phần tử < a[i] đã xét
    ft.update(a[i], 1);
}
```

---

## Pattern 2: O(N³) → O(N²)

### Khi nào dùng:
- N ≤ 500-1000, O(N³) quá chậm
- Có 3 nested loops

### Cách tiếp cận:

#### 1. Precompute / Prefix Sum

```cpp
// ❌ SLOW: O(N³) - Tính sum của mọi subarray
for (int i = 0; i < n; i++)
    for (int j = i; j < n; j++) {
        int sum = 0;
        for (int k = i; k <= j; k++)
            sum += a[k];
    }

// ✅ FAST: O(N²) - Prefix Sum
vector<int> pref(n+1, 0);
for (int i = 0; i < n; i++)
    pref[i+1] = pref[i] + a[i];

for (int i = 0; i < n; i++)
    for (int j = i; j < n; j++)
        sum = pref[j+1] - pref[i];  // O(1)
```

#### 2. Fix one variable, optimize the rest

```cpp
// ❌ SLOW: O(N³) - Tìm tam giác có chu vi lớn nhất
for (int i = 0; i < n; i++)
    for (int j = i+1; j < n; j++)
        for (int k = j+1; k < n; k++)
            if (valid(a[i], a[j], a[k]))
                maxPerimeter = max(maxPerimeter, a[i]+a[j]+a[k]);

// ✅ FAST: O(N²) - Fix 2 cạnh, tìm cạnh thứ 3 bằng binary search
sort(a, a+n);
for (int i = 0; i < n; i++)
    for (int j = i+1; j < n; j++) {
        // Tìm k lớn nhất sao cho a[k] < a[i] + a[j]
        int target = a[i] + a[j];
        auto it = lower_bound(a+j+1, a+n, target);
        if (it != a+j+1) {
            k = it - a - 1;
            maxPerimeter = max(maxPerimeter, a[i]+a[j]+a[k]);
        }
    }
```

---

## Pattern 3: Brute Force → Dynamic Programming

### Khi nào dùng:
- Bài toán đếm số cách / tối ưu hóa
- Có overlapping subproblems
- Có optimal substructure

### Cách tiếp cận:

#### 1. Recursive → Memoization

```cpp
// ❌ SLOW: O(2^N) - Fibonacci
int fib(int n) {
    if (n <= 1) return n;
    return fib(n-1) + fib(n-2);
}

// ✅ FAST: O(N) - Memoization
int memo[100005];
int fib(int n) {
    if (n <= 1) return n;
    if (memo[n] != -1) return memo[n];
    return memo[n] = fib(n-1) + fib(n-2);
}
```

#### 2. Recursive → Iterative DP

```cpp
// ❌ SLOW: O(2^N) - Knapsack recursive
int knapsack(int i, int w) {
    if (i == n) return 0;
    if (wt[i] > w) return knapsack(i+1, w);
    return max(knapsack(i+1, w), 
               val[i] + knapsack(i+1, w - wt[i]));
}

// ✅ FAST: O(N*W) - Iterative DP
int dp[N+1][W+1];
for (int i = 0; i <= n; i++)
    for (int w = 0; w <= W; w++) {
        if (i == 0 || w == 0) dp[i][w] = 0;
        else if (wt[i-1] <= w)
            dp[i][w] = max(val[i-1] + dp[i-1][w-wt[i-1]], dp[i-1][w]);
        else dp[i][w] = dp[i-1][w];
    }
```

---

## Pattern 4: Recursion → Iterative + Stack

### Khi nào dùng:
- Recursion depth quá lớn (> 10000)
- Stack overflow risk

### Cách tiếp cận:

```cpp
// ❌ RISK: Stack overflow với N lớn
void dfs(int u, int p) {
    for (int v : adj[u]) {
        if (v != p) dfs(v, u);
    }
}

// ✅ SAFE: Iterative DFS với stack
stack<pair<int,int>> st;
st.push({root, -1});
while (!st.empty()) {
    auto [u, p] = st.top();
    st.pop();
    for (int v : adj[u]) {
        if (v != p) st.push({v, u});
    }
}
```

---

## Pattern 5: Naive → Data Structure

### Khi nào dùng:
- Range queries với updates
- Cần O(log N) per query

### Cách tiếp cận:

#### 1. Range Sum → Fenwick Tree

```cpp
// ❌ SLOW: O(N) per query
int query(int l, int r) {
    int sum = 0;
    for (int i = l; i <= r; i++) sum += a[i];
    return sum;
}

void update(int i, int val) {
    a[i] = val;  // O(1)
}

// ✅ FAST: O(log N) per query
FenwickTree ft(n);

int query(int l, int r) {
    return ft.query(r) - ft.query(l-1);  // O(log N)
}

void update(int i, int delta) {
    ft.update(i, delta);  // O(log N)
}
```

#### 2. Range Min/Max → Segment Tree

```cpp
// ❌ SLOW: O(N) per query
int queryMin(int l, int r) {
    int mn = INF;
    for (int i = l; i <= r; i++) mn = min(mn, a[i]);
    return mn;
}

// ✅ FAST: O(log N) per query
SegmentTree st(n, [](int a, int b) { return min(a, b); }, INF);

int queryMin(int l, int r) {
    return st.query(l, r);  // O(log N)
}
```

---

## Pattern 6: Binary Search on Answer

### Khi nào dùng:
- Tìm giá trị X thỏa mãn điều kiện
- Hàm f(X) monotonic (tăng/giảm)
- Có thể check nhanh điều kiện

### Template:

```cpp
// Pattern: Tìm min X sao cho check(X) = true
bool check(long long x) {
    // Check if x satisfies condition
    // Return true/false
}

long long binarySearch(long long lo, long long hi) {
    while (lo < hi) {
        long long mid = lo + (hi - lo) / 2;
        if (check(mid)) hi = mid;
        else lo = mid + 1;
    }
    return lo;
}

// Usage:
long long answer = binarySearch(1, 1e18);
```

### Example: Tìm thời gian nhỏ nhất

```cpp
// Problem: N workers, mỗi worker làm 1 sản phẩm mất t_i giây.
// Tìm thời gian nhỏ nhất để làm được K sản phẩm.

bool check(long long time, vector<int>& t, int K) {
    long long products = 0;
    for (int ti : t) {
        products += time / ti;  // Số sản phẩm worker i làm được
    }
    return products >= K;
}

long long minTime(vector<int>& t, int K) {
    long long lo = 1, hi = 1e18;
    while (lo < hi) {
        long long mid = lo + (hi - lo) / 2;
        if (check(mid, t, K)) hi = mid;
        else lo = mid + 1;
    }
    return lo;
}
```

---

## Pattern 7: Square Root Decomposition

### Khi nào dùng:
- N, Q ≤ 10^5
- Range queries, khó dùng Segment Tree
- Offline processing được

### Template (Mo's Algorithm):

```cpp
// Pattern: Đếm số phần tử distinct trong range [l, r]

const int BLOCK_SIZE = sqrt(N);

struct Query {
    int l, r, id;
    bool operator<(const Query& other) const {
        int block_a = l / BLOCK_SIZE, block_b = other.l / BLOCK_SIZE;
        if (block_a != block_b) return block_a < block_b;
        return (block_a & 1) ? (r < other.r) : (r > other.r);
    }
};

int cnt[MAX_VAL];
int distinct_count = 0;

void add(int x) {
    if (cnt[x] == 0) distinct_count++;
    cnt[x]++;
}

void remove(int x) {
    cnt[x]--;
    if (cnt[x] == 0) distinct_count--;
}

vector<int> mo(vector<Query>& queries, vector<int>& a) {
    sort(queries.begin(), queries.end());
    vector<int> answers(queries.size());
    
    int L = 0, R = -1;
    for (auto& q : queries) {
        while (L > q.l) add(a[--L]);
        while (R < q.r) add(a[++R]);
        while (L < q.l) remove(a[L++]);
        while (R > q.r) remove(a[R--]);
        answers[q.id] = distinct_count;
    }
    return answers;
}
```

---

## Pattern 8: Coordinate Compression

### Khi nào dùng:
- Giá trị lớn (10^9+) nhưng số lượng giá trị khác nhau nhỏ
- Cần dùng giá trị làm index trong array/tree

### Template:

```cpp
// Pattern: Nén tọa độ từ 10^9 xuống O(N)

vector<int> compress(vector<int>& values) {
    vector<int> sorted = values;
    sort(sorted.begin(), sorted.end());
    sorted.erase(unique(sorted.begin(), sorted.end()), sorted.end());
    
    vector<int> compressed;
    for (int v : values) {
        int idx = lower_bound(sorted.begin(), sorted.end(), v) - sorted.begin();
        compressed.push_back(idx);
    }
    return compressed;
}

// Usage:
vector<int> a = {1000000000, 500000000, 1000000000, 1};
vector<int> compressed = compress(a);
// Result: {2, 1, 2, 0}
```

---

## Pattern 9: Lazy Propagation

### Khi nào dùng:
- Range updates (set/add/multiply)
- Range queries
- Segment Tree với updates

### Template:

```cpp
// Segment Tree với Lazy Propagation cho range add

struct SegmentTree {
    int n;
    vector<long long> tree, lazy;
    
    SegmentTree(int n, vector<int>& a) : n(n) {
        tree.assign(4*n, 0);
        lazy.assign(4*n, 0);
        build(1, 0, n-1, a);
    }
    
    void build(int node, int l, int r, vector<int>& a) {
        if (l == r) {
            tree[node] = a[l];
            return;
        }
        int mid = (l+r)/2;
        build(2*node, l, mid, a);
        build(2*node+1, mid+1, r, a);
        tree[node] = tree[2*node] + tree[2*node+1];
    }
    
    void push(int node, int l, int r) {
        if (lazy[node] != 0) {
            tree[node] += (r-l+1) * lazy[node];
            if (l != r) {
                lazy[2*node] += lazy[node];
                lazy[2*node+1] += lazy[node];
            }
            lazy[node] = 0;
        }
    }
    
    void update(int node, int l, int r, int ql, int qr, int val) {
        push(node, l, r);
        if (qr < l || r < ql) return;
        if (ql <= l && r <= qr) {
            lazy[node] += val;
            push(node, l, r);
            return;
        }
        int mid = (l+r)/2;
        update(2*node, l, mid, ql, qr, val);
        update(2*node+1, mid+1, r, ql, qr, val);
        tree[node] = tree[2*node] + tree[2*node+1];
    }
    
    long long query(int node, int l, int r, int ql, int qr) {
        push(node, l, r);
        if (qr < l || r < ql) return 0;
        if (ql <= l && r <= qr) return tree[node];
        int mid = (l+r)/2;
        return query(2*node, l, mid, ql, qr) + 
               query(2*node+1, mid+1, r, ql, qr);
    }
};
```

---

## Optimization Checklist

Trước khi submit, check:

- [ ] **Complexity đúng với constraints?**
- [ ] **Fast I/O?** (C++: `ios_base::sync_with_stdio(false); cin.tie(NULL);`)
- [ ] **Dùng `long long` cho giá trị lớn?**
- [ ] **Constant factor nhỏ?** (tránh unnecessary operations)
- [ ] **Memory usage OK?** (không allocate quá nhiều)
- [ ] **Edge cases handled?**

---

## Next Steps

Sau khi optimize:
1. → Test với sample và edge cases
2. → Stress test với brute force (xem [06-test-generation.md](06-test-generation.md))
3. → Nếu vẫn TLE/WA → Qua [05-debugging-strategies.md](05-debugging-strategies.md)
