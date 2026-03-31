// Segment Tree — Generic (Point Update, Range Query)
// Supports: sum, min, max, GCD, XOR — any associative operation
// Complexity: O(N) build, O(log N) update/query
// Usage: Thay op và identity tương ứng với bài toán

#include <bits/stdc++.h>
using namespace std;

template<typename T>
struct SegmentTree {
    int n;
    vector<T> tree;
    T identity;
    function<T(T,T)> op;

    SegmentTree(int n, function<T(T,T)> op, T identity)
        : n(n), op(op), identity(identity) {
        tree.assign(4 * n, identity);
    }

    // Build from array — O(N)
    void build(int node, int l, int r, vector<T>& a) {
        if (l == r) { tree[node] = a[l]; return; }
        int mid = (l + r) / 2;
        build(2*node, l, mid, a);
        build(2*node+1, mid+1, r, a);
        tree[node] = op(tree[2*node], tree[2*node+1]);
    }

    void _update(int node, int l, int r, int idx, T val) {
        if (l == r) { tree[node] = val; return; }
        int mid = (l + r) / 2;
        if (idx <= mid) _update(2*node, l, mid, idx, val);
        else            _update(2*node+1, mid+1, r, idx, val);
        tree[node] = op(tree[2*node], tree[2*node+1]);
    }

    T _query(int node, int l, int r, int ql, int qr) {
        if (qr < l || r < ql) return identity;
        if (ql <= l && r <= qr) return tree[node];
        int mid = (l + r) / 2;
        return op(_query(2*node, l, mid, ql, qr),
                  _query(2*node+1, mid+1, r, ql, qr));
    }

    void build(vector<T>& a)    { build(1, 0, n-1, a); }
    void update(int idx, T val) { _update(1, 0, n-1, idx, val); }
    T    query(int l, int r)    { return _query(1, 0, n-1, l, r); }
};

// ===== USAGE EXAMPLES =====

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(NULL);

    int n, q;
    cin >> n >> q;
    vector<long long> a(n);
    for (auto& x : a) cin >> x;

    // Range Sum
    SegmentTree<long long> st_sum(n, [](long long a, long long b){ return a+b; }, 0LL);

    // Range Min
    SegmentTree<long long> st_min(n, [](long long a, long long b){ return min(a,b); }, LLONG_MAX);

    // Range Max
    SegmentTree<long long> st_max(n, [](long long a, long long b){ return max(a,b); }, LLONG_MIN);

    st_sum.build(a);
    st_min.build(a);
    st_max.build(a);

    while (q--) {
        int type, l, r;
        cin >> type >> l >> r;
        if (type == 1) {
            // Point update: a[l] = r
            st_sum.update(l, r);
        } else {
            // Range query [l, r]
            cout << st_sum.query(l, r) << "\n";
        }
    }
    return 0;
}
