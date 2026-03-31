// Fenwick Tree (Binary Indexed Tree) — Point Update, Prefix/Range Query
// Complexity: O(N) build, O(log N) update/query
// Chỉ hỗ trợ các phép toán có nghịch đảo: sum, XOR

#include <bits/stdc++.h>
using namespace std;

struct FenwickTree {
  int n;
  vector<long long> tree;

  FenwickTree(int n) : n(n), tree(n + 1, 0) {}

  // Build from array — O(N log N) simple, O(N) optimized below
  FenwickTree(int n, vector<int> &a) : n(n), tree(n + 1, 0) {
    for (int i = 0; i < n; i++)
      update(i, a[i]);
  }

  // Add delta to index i (0-indexed)
  void update(int i, long long delta) {
    for (++i; i <= n; i += i & (-i))
      tree[i] += delta;
  }

  // Prefix sum [0..i] (0-indexed)
  long long query(int i) {
    long long sum = 0;
    for (++i; i > 0; i -= i & (-i))
      sum += tree[i];
    return sum;
  }

  // Range sum [l..r] (0-indexed)
  long long query(int l, int r) {
    return query(r) - (l > 0 ? query(l - 1) : 0);
  }

  // Set a[i] = val (requires knowing old value)
  void set(int i, long long old_val, long long new_val) {
    update(i, new_val - old_val);
  }
};

// Fenwick 2D — for 2D range sum queries
struct Fenwick2D {
  int n, m;
  vector<vector<long long>> tree;

  Fenwick2D(int n, int m)
      : n(n), m(m), tree(n + 1, vector<long long>(m + 1, 0)) {}

  void update(int x, int y, long long delta) {
    for (int i = x + 1; i <= n; i += i & (-i))
      for (int j = y + 1; j <= m; j += j & (-j))
        tree[i][j] += delta;
  }

  long long query(int x, int y) {
    long long sum = 0;
    for (int i = x + 1; i > 0; i -= i & (-i))
      for (int j = y + 1; j > 0; j -= j & (-j))
        sum += tree[i][j];
    return sum;
  }

  // Range sum [x1..x2][y1..y2]
  long long query(int x1, int y1, int x2, int y2) {
    return query(x2, y2) - query(x1 - 1, y2) - query(x2, y1 - 1) +
           query(x1 - 1, y1 - 1);
  }
};

int main() {
  ios_base::sync_with_stdio(false);
  cin.tie(NULL);

  int n, q;
  cin >> n >> q;
  vector<int> a(n);
  for (auto &x : a)
    cin >> x;

  FenwickTree ft(n, a);

  while (q--) {
    int type;
    cin >> type;
    if (type == 1) {
      int i;
      long long val;
      cin >> i >> val;
      ft.update(i - 1, val); // 1-indexed
    } else {
      int l, r;
      cin >> l >> r;
      cout << ft.query(l - 1, r - 1) << "\n"; // 1-indexed
    }
  }
  return 0;
}
