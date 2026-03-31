// Mo's Algorithm — Offline Range Queries
// Complexity: O((N+Q)√N)
// Dùng khi: offline queries (không có update), N,Q ≤ 10^5
// Template: đếm distinct elements — customize add()/remove() cho bài khác

#include <bits/stdc++.h>
using namespace std;

const int MAXVAL = 1000001;
int cnt[MAXVAL];
int cur_distinct = 0;

void add(int x) {
  if (cnt[x] == 0)
    cur_distinct++;
  cnt[x]++;
}

void rem(int x) {
  cnt[x]--;
  if (cnt[x] == 0)
    cur_distinct--;
}

int main() {
  ios_base::sync_with_stdio(false);
  cin.tie(NULL);

  int n, q;
  cin >> n >> q;

  vector<int> a(n);
  for (auto &x : a)
    cin >> x;

  int BLOCK = max(1, (int)sqrt(n));

  struct Query {
    int l, r, id;
    bool operator<(const Query &o) const {
      int bl = l / BLOCK, bo = o.l / BLOCK;
      if (bl != bo)
        return bl < bo;
      // Odd-even sort: giảm pointer movement
      return (bl & 1) ? (r > o.r) : (r < o.r);
    }
  };

  vector<Query> queries(q);
  for (int i = 0; i < q; i++) {
    cin >> queries[i].l >> queries[i].r;
    queries[i].l--;
    queries[i].r--; // 0-indexed
    queries[i].id = i;
  }

  sort(queries.begin(), queries.end());

  vector<int> ans(q);
  int L = 0, R = -1;

  for (auto &query : queries) {
    while (R < query.r)
      add(a[++R]);
    while (L > query.l)
      add(a[--L]);
    while (R > query.r)
      rem(a[R--]);
    while (L < query.l)
      rem(a[L++]);
    ans[query.id] = cur_distinct;
  }

  for (int x : ans)
    cout << x << "\n";
  return 0;
}
