# Data Structures Patterns

## 1. Segment Tree

### Range Sum Query

```cpp
template<typename T>
struct SegmentTree {
    int n;
    vector<T> tree;
    T identity;
    T (*op)(T, T);
    
    SegmentTree(int n, T (*op)(T,T), T identity) 
        : n(n), op(op), identity(identity) {
        tree.assign(4*n, identity);
    }
    
    void update(int node, int l, int r, int idx, T val) {
        if (l == r) {
            tree[node] = val;
            return;
        }
        int mid = (l + r) / 2;
        if (idx <= mid) update(2*node, l, mid, idx, val);
        else update(2*node+1, mid+1, r, idx, val);
        tree[node] = op(tree[2*node], tree[2*node+1]);
    }
    
    T query(int node, int l, int r, int ql, int qr) {
        if (qr < l || r < ql) return identity;
        if (ql <= l && r <= qr) return tree[node];
        int mid = (l + r) / 2;
        return op(query(2*node, l, mid, ql, qr),
                  query(2*node+1, mid+1, r, ql, qr));
    }
    
    void update(int idx, T val) { update(1, 0, n-1, idx, val); }
    T query(int l, int r) { return query(1, 0, n-1, l, r); }
};

// Usage
long long add(long long a, long long b) { return a + b; }
SegmentTree<long long> st(n, add, 0LL);
st.update(i, val);
long long sum = st.query(l, r);
```

### Range Minimum Query

```cpp
long long min_op(long long a, long long b) { return min(a, b); }
SegmentTree<long long> rmq(n, min_op, LLONG_MAX);

rmq.update(i, val);
long long mn = rmq.query(l, r);
```

---

## 2. Fenwick Tree (Binary Indexed Tree)

### Point Update, Range Query

```cpp
struct FenwickTree {
    int n;
    vector<long long> tree;
    
    FenwickTree(int n) : n(n) {
        tree.assign(n + 1, 0);
    }
    
    void update(int i, int delta) {
        for (++i; i <= n; i += i & (-i))
            tree[i] += delta;
    }
    
    long long query(int i) {
        long long sum = 0;
        for (++i; i > 0; i -= i & (-i))
            sum += tree[i];
        return sum;
    }
    
    long long query(int l, int r) {
        return query(r) - query(l - 1);
    }
};

// Usage
FenwickTree ft(n);
ft.update(i, val);
long long sum = ft.query(l, r);
```

### Range Update, Point Query

```cpp
struct FenwickTreeRange {
    int n;
    vector<long long> tree;
    
    FenwickTreeRange(int n) : n(n) {
        tree.assign(n + 1, 0);
    }
    
    void update(int l, int r, int delta) {
        update_point(l, delta);
        update_point(r + 1, -delta);
    }
    
    void update_point(int i, int delta) {
        for (++i; i <= n; i += i & (-i))
            tree[i] += delta;
    }
    
    long long query(int i) {
        long long sum = 0;
        for (++i; i > 0; i -= i & (-i))
            sum += tree[i];
        return sum;
    }
};
```

---

## 3. Disjoint Set Union (DSU)

### Basic DSU

```cpp
struct DSU {
    vector<int> parent, rank;
    
    DSU(int n) {
        parent.resize(n + 1);
        iota(parent.begin(), parent.end(), 0);
        rank.assign(n + 1, 0);
    }
    
    int find(int x) {
        if (parent[x] != x)
            parent[x] = find(parent[x]);  // Path compression
        return parent[x];
    }
    
    bool unite(int x, int y) {
        x = find(x), y = find(y);
        if (x == y) return false;
        
        // Union by rank
        if (rank[x] < rank[y]) swap(x, y);
        parent[y] = x;
        if (rank[x] == rank[y]) rank[x]++;
        return true;
    }
    
    bool same(int x, int y) {
        return find(x) == find(y);
    }
};

// Usage
DSU dsu(n);
dsu.unite(u, v);
bool connected = dsu.same(u, v);
```

### DSU with Size

```cpp
struct DSUSize {
    vector<int> parent, size;
    
    DSUSize(int n) {
        parent.resize(n + 1);
        iota(parent.begin(), parent.end(), 0);
        size.assign(n + 1, 1);
    }
    
    int find(int x) {
        if (parent[x] != x)
            parent[x] = find(parent[x]);
        return parent[x];
    }
    
    void unite(int x, int y) {
        x = find(x), y = find(y);
        if (x == y) return;
        
        if (size[x] < size[y]) swap(x, y);
        parent[y] = x;
        size[x] += size[y];
    }
    
    int get_size(int x) {
        return size[find(x)];
    }
};
```

---

## 4. Sparse Table (RMQ Static)

```cpp
struct SparseTable {
    int n, LOG;
    vector<vector<long long>> st;
    vector<int> log;
    
    SparseTable(vector<long long>& a) {
        n = a.size();
        LOG = __builtin_clz(1) - __builtin_clz(n);
        st.assign(n, vector<long long>(LOG + 1));
        log.resize(n + 1);
        
        log[1] = 0;
        for (int i = 2; i <= n; i++)
            log[i] = log[i/2] + 1;
        
        for (int i = 0; i < n; i++)
            st[i][0] = a[i];
        
        for (int j = 1; j <= LOG; j++)
            for (int i = 0; i + (1 << j) <= n; i++)
                st[i][j] = min(st[i][j-1], st[i + (1 << (j-1))][j-1]);
    }
    
    long long query(int l, int r) {
        int j = log[r - l + 1];
        return min(st[l][j], st[r - (1 << j) + 1][j]);
    }
};

// Usage: O(1) query, O(N log N) build
SparseTable st(a);
long long mn = st.query(l, r);
```

---

## 5. Treap (Cartesian Tree)

```cpp
struct Treap {
    struct Node {
        int key, priority;
        Node *left = nullptr, *right = nullptr;
        Node(int k, int p) : key(k), priority(p) {}
    };
    
    Node* root = nullptr;
    mt19937 rng;
    
    Treap() : rng(chrono::steady_clock::now().time_since_epoch().count()) {}
    
    pair<Node*, Node*> split(Node* t, int key) {
        if (!t) return {nullptr, nullptr};
        if (t->key < key) {
            auto [l, r] = split(t->right, key);
            t->right = l;
            return {t, r};
        } else {
            auto [l, r] = split(t->left, key);
            t->left = r;
            return {l, t};
        }
    }
    
    Node* merge(Node* l, Node* r) {
        if (!l || !r) return l ? l : r;
        if (l->priority > r->priority) {
            l->right = merge(l->right, r);
            return l;
        } else {
            r->left = merge(l, r->left);
            return r;
        }
    }
    
    void insert(int key) {
        auto [l, r] = split(root, key);
        root = merge(merge(l, new Node(key, rng())), r);
    }
    
    bool find(int key) {
        Node* t = root;
        while (t) {
            if (t->key == key) return true;
            t = t->key < key ? t->right : t->left;
        }
        return false;
    }
};
```

---

## 6. Square Root Decomposition

```cpp
struct SqrtDecomp {
    int n, block_size;
    vector<int> a, block_sum;
    
    SqrtDecomp(vector<int>& arr) {
        n = arr.size();
        block_size = sqrt(n);
        a = arr;
        block_sum.assign((n + block_size - 1) / block_size, 0);
        
        for (int i = 0; i < n; i++)
            block_sum[i / block_size] += a[i];
    }
    
    void update(int i, int val) {
        block_sum[i / block_size] -= a[i];
        a[i] = val;
        block_sum[i / block_size] += a[i];
    }
    
    int query(int l, int r) {
        int sum = 0;
        
        // Left partial block
        while (l <= r && l % block_size != 0) {
            sum += a[l];
            l++;
        }
        
        // Full blocks
        while (l + block_size - 1 <= r) {
            sum += block_sum[l / block_size];
            l += block_size;
        }
        
        // Right partial block
        while (l <= r) {
            sum += a[l];
            l++;
        }
        
        return sum;
    }
};
```

---

## 7. Order Statistic Tree (Policy Based DS)

```cpp
#include <ext/pb_ds/assoc_container.hpp>
#include <ext/pb_ds/tree_policy.hpp>
using namespace __gnu_pbds;

template<typename T>
using ordered_set = tree<T, null_type, less<T>, rb_tree_tag, tree_order_statistics_node_update>;

// Usage
ordered_set<int> ost;
ost.insert(5);
ost.insert(3);
ost.insert(7);

int rank = ost.order_of_key(5);  // Number of elements < 5
int kth = *ost.find_by_order(1);  // 0-indexed k-th element
```

---

## 8. Monotonic Stack/Queue

### Monotonic Stack (Next Greater Element)

```cpp
vector<int> next_greater(vector<int>& a) {
    int n = a.size();
    vector<int> result(n, -1);
    stack<int> st;
    
    for (int i = 0; i < n; i++) {
        while (!st.empty() && a[st.top()] < a[i]) {
            result[st.top()] = a[i];
            st.pop();
        }
        st.push(i);
    }
    return result;
}
```

### Monotonic Queue (Sliding Window Maximum)

```cpp
vector<int> sliding_window_max(vector<int>& a, int k) {
    deque<int> dq;
    vector<int> result;
    
    for (int i = 0; i < a.size(); i++) {
        // Remove elements outside window
        while (!dq.empty() && dq.front() <= i - k)
            dq.pop_front();
        
        // Maintain decreasing order
        while (!dq.empty() && a[dq.back()] < a[i])
            dq.pop_back();
        
        dq.push_back(i);
        
        if (i >= k - 1)
            result.push_back(a[dq.front()]);
    }
    return result;
}
```

---

## Common Data Structure Problems

| Problem | Data Structure | Complexity |
|---------|---------------|------------|
| Range sum | Fenwick / Segment Tree | O(log N) |
| Range min/max | Segment Tree / Sparse Table | O(log N) / O(1) |
| Connected components | DSU | O(α(N)) |
| K-th element | Order Statistic Tree | O(log N) |
| Sliding window max | Monotonic Queue | O(N) |
| Offline range queries | Mo's Algorithm | O(N√N) |

---

## Next Steps

- → Practice problems using these data structures
- → Learn [04-advanced-algorithms.md](04-advanced-algorithms.md) for Segment Tree with Lazy
- → Combine with [patterns/graph.md](graph.md) for graph algorithms
