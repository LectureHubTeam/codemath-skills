// Centroid Decomposition
// Complexity: O(N log N) build, O(N log N) or O(N log² N) queries
// Dùng cho: đếm paths thỏa điều kiện trên cây, distance queries

#include <bits/stdc++.h>
using namespace std;

const int MAXN = 100005;
vector<pair<int, int>> adj[MAXN]; // {neighbor, edge_weight}
bool removed[MAXN];
int subtree_size[MAXN];
int n;

// Tính subtree size (bỏ qua nodes đã removed)
void calc_size(int u, int p) {
  subtree_size[u] = 1;
  for (auto [v, w] : adj[u]) {
    if (v != p && !removed[v]) {
      calc_size(v, u);
      subtree_size[u] += subtree_size[v];
    }
  }
}

// Tìm centroid của subtree gốc u, tổng size = total
int find_centroid(int u, int p, int total) {
  for (auto [v, w] : adj[u]) {
    if (v != p && !removed[v]) {
      if (subtree_size[v] > total / 2)
        return find_centroid(v, u, total);
    }
  }
  return u;
}

// ===== Đếm số paths có length đúng bằng target =====
// Customize solve_centroid() cho từng bài

long long target;
long long answer = 0;

// Thu thập distances từ centroid đến tất cả nodes trong subtree
void collect(int u, int p, long long dist, vector<long long> &dists) {
  dists.push_back(dist);
  for (auto [v, w] : adj[u]) {
    if (v != p && !removed[v]) {
      collect(v, u, dist + w, dists);
    }
  }
}

// Đếm số paths qua centroid có length = target
void solve_centroid(int centroid) {
  vector<long long> all_dists = {0}; // Bao gồm bản thân centroid

  for (auto [v, w] : adj[centroid]) {
    if (!removed[v]) {
      vector<long long> sub_dists;
      collect(v, centroid, w, sub_dists);

      // Đếm pairs: dist_in_all + dist_in_sub = target
      // Dùng map hoặc sort + two pointers
      for (long long d : sub_dists) {
        long long need = target - d;
        // Count trong all_dists (có thể dùng sorted + binary search cho nhanh)
        answer += count(all_dists.begin(), all_dists.end(), need);
      }

      for (long long d : sub_dists)
        all_dists.push_back(d);
    }
  }
}

// Đệ quy phân rã centroid
void decompose(int u) {
  calc_size(u, -1);
  int centroid = find_centroid(u, -1, subtree_size[u]);

  solve_centroid(centroid);

  removed[centroid] = true;
  for (auto [v, w] : adj[centroid]) {
    if (!removed[v]) {
      decompose(v);
    }
  }
}

int main() {
  ios_base::sync_with_stdio(false);
  cin.tie(NULL);

  cin >> n >> target;
  for (int i = 0; i < n - 1; i++) {
    int u, v, w;
    cin >> u >> v >> w;
    adj[u].push_back({v, w});
    adj[v].push_back({u, w});
  }

  memset(removed, false, sizeof(removed));
  decompose(1); // root = 1

  cout << answer << "\n";
  return 0;
}
