// Heavy-Light Decomposition (HLD) + Segment Tree
// Complexity: O(N log N) preprocessing, O(log² N) per path query/update
// Dùng cho: path queries/updates trên cây

#include <bits/stdc++.h>
using namespace std;

const int MAXN = 100005;
const long long INF = 1e18;

// ===== Segment Tree (range sum, point update) =====
struct SegTree {
  int n;
  vector<long long> tree;
  SegTree(int n) : n(n), tree(4 * n, 0) {}

  void update(int node, int l, int r, int idx, long long val) {
    if (l == r) {
      tree[node] = val;
      return;
    }
    int mid = (l + r) / 2;
    if (idx <= mid)
      update(2 * node, l, mid, idx, val);
    else
      update(2 * node + 1, mid + 1, r, idx, val);
    tree[node] = tree[2 * node] + tree[2 * node + 1];
  }
  long long query(int node, int l, int r, int ql, int qr) {
    if (qr < l || r < ql)
      return 0;
    if (ql <= l && r <= qr)
      return tree[node];
    int mid = (l + r) / 2;
    return query(2 * node, l, mid, ql, qr) +
           query(2 * node + 1, mid + 1, r, ql, qr);
  }
  void update(int idx, long long val) { update(1, 0, n - 1, idx, val); }
  long long query(int l, int r) { return query(1, 0, n - 1, l, r); }
};

// ===== HLD =====
vector<int> adj[MAXN];
int parent[MAXN], depth[MAXN], heavy[MAXN];
int head[MAXN], pos[MAXN], subtree_size[MAXN];
int cur_pos;
int n;

int dfs_size(int u, int p, int d) {
  parent[u] = p;
  depth[u] = d;
  subtree_size[u] = 1;
  int max_sz = 0;
  heavy[u] = -1;
  for (int v : adj[u]) {
    if (v != p) {
      int sz = dfs_size(v, u, d + 1);
      subtree_size[u] += sz;
      if (sz > max_sz) {
        max_sz = sz;
        heavy[u] = v;
      }
    }
  }
  return subtree_size[u];
}

void dfs_hld(int u, int h) {
  head[u] = h;
  pos[u] = cur_pos++;
  if (heavy[u] != -1)
    dfs_hld(heavy[u], h); // Heavy child — cùng chain
  for (int v : adj[u])
    if (v != parent[u] && v != heavy[u])
      dfs_hld(v, v); // Light child — chain mới
}

void hld_build(int root) {
  cur_pos = 0;
  dfs_size(root, -1, 0);
  dfs_hld(root, root);
}

// Path query: sum của các node trên path u→v
long long path_query(int u, int v, SegTree &st) {
  long long result = 0;
  for (; head[u] != head[v]; v = parent[head[v]]) {
    if (depth[head[u]] > depth[head[v]])
      swap(u, v);
    result += st.query(pos[head[v]], pos[v]);
  }
  if (depth[u] > depth[v])
    swap(u, v);
  result += st.query(pos[u], pos[v]);
  return result;
}

// Path update: cập nhật 1 node trên path
void node_update(int u, long long val, SegTree &st) { st.update(pos[u], val); }

int main() {
  ios_base::sync_with_stdio(false);
  cin.tie(NULL);

  int q;
  cin >> n >> q;

  vector<long long> val(n + 1);
  for (int i = 1; i <= n; i++)
    cin >> val[i];

  for (int i = 0; i < n - 1; i++) {
    int u, v;
    cin >> u >> v;
    adj[u].push_back(v);
    adj[v].push_back(u);
  }

  hld_build(1); // 1-indexed, root = 1

  SegTree st(n);
  for (int i = 1; i <= n; i++)
    st.update(pos[i], val[i]);

  while (q--) {
    int type;
    cin >> type;
    if (type == 1) {
      int u;
      long long v;
      cin >> u >> v;
      node_update(u, v, st);
    } else {
      int u, v;
      cin >> u >> v;
      cout << path_query(u, v, st) << "\n";
    }
  }
  return 0;
}
