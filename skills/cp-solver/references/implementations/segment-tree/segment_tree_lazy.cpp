// Segment Tree với Lazy Propagation — Range Update, Range Query
// Supports: Range add + Range sum
// Complexity: O(N) build, O(log N) update/query
// Customize: Thay đổi apply_lazy() và combine_lazy() cho loại update khác

#include <bits/stdc++.h>
using namespace std;

struct SegmentTreeLazy {
  int n;
  vector<long long> tree, lazy;

  SegmentTreeLazy(int n, vector<int> &a) : n(n) {
    tree.assign(4 * n, 0);
    lazy.assign(4 * n, 0);
    build(1, 0, n - 1, a);
  }

  void build(int node, int l, int r, vector<int> &a) {
    if (l == r) {
      tree[node] = a[l];
      return;
    }
    int mid = (l + r) / 2;
    build(2 * node, l, mid, a);
    build(2 * node + 1, mid + 1, r, a);
    tree[node] = tree[2 * node] + tree[2 * node + 1];
  }

  // Push lazy xuống con
  void push(int node, int l, int r) {
    if (lazy[node] != 0) {
      int mid = (l + r) / 2;
      // Apply lazy to current node's sum
      tree[node] += (long long)(r - l + 1) * lazy[node];
      if (l != r) {
        lazy[2 * node] += lazy[node];
        lazy[2 * node + 1] += lazy[node];
      }
      lazy[node] = 0;
    }
  }

  // Range add: a[ql..qr] += val
  void update(int node, int l, int r, int ql, int qr, long long val) {
    if (qr < l || r < ql)
      return;
    if (ql <= l && r <= qr) {
      lazy[node] += val;
      push(node, l, r);
      return;
    }
    push(node, l, r);
    int mid = (l + r) / 2;
    update(2 * node, l, mid, ql, qr, val);
    update(2 * node + 1, mid + 1, r, ql, qr, val);
    // Recalculate after push (lazy already applied to children)
    tree[node] = tree[2 * node] + tree[2 * node + 1];
  }

  // Range sum query: sum(a[ql..qr])
  long long query(int node, int l, int r, int ql, int qr) {
    if (qr < l || r < ql)
      return 0;
    push(node, l, r);
    if (ql <= l && r <= qr)
      return tree[node];
    int mid = (l + r) / 2;
    return query(2 * node, l, mid, ql, qr) +
           query(2 * node + 1, mid + 1, r, ql, qr);
  }

  void update(int l, int r, long long val) { update(1, 0, n - 1, l, r, val); }
  long long query(int l, int r) { return query(1, 0, n - 1, l, r); }
};

int main() {
  ios_base::sync_with_stdio(false);
  cin.tie(NULL);

  int n, q;
  cin >> n >> q;
  vector<int> a(n);
  for (auto &x : a)
    cin >> x;

  SegmentTreeLazy st(n, a);

  while (q--) {
    int type;
    cin >> type;
    if (type == 1) {
      int l, r;
      long long val;
      cin >> l >> r >> val;
      st.update(l - 1, r - 1, val); // 1-indexed
    } else {
      int l, r;
      cin >> l >> r;
      cout << st.query(l - 1, r - 1) << "\n";
    }
  }
  return 0;
}
