// Suffix Array (O(N log² N) prefix doubling) + LCP Array (Kasai O(N))
// Dùng cho: pattern matching, longest common substring, distinct substrings

#include <bits/stdc++.h>
using namespace std;

// Build suffix array — O(N log² N)
vector<int> build_suffix_array(const string &s) {
  int n = s.size();
  vector<int> sa(n), rank_(n), tmp(n);

  iota(sa.begin(), sa.end(), 0);
  for (int i = 0; i < n; i++)
    rank_[i] = s[i];

  for (int k = 1; k < n; k <<= 1) {
    auto cmp = [&](int a, int b) {
      if (rank_[a] != rank_[b])
        return rank_[a] < rank_[b];
      int ra = (a + k < n) ? rank_[a + k] : -1;
      int rb = (b + k < n) ? rank_[b + k] : -1;
      return ra < rb;
    };
    sort(sa.begin(), sa.end(), cmp);

    tmp[sa[0]] = 0;
    for (int i = 1; i < n; i++)
      tmp[sa[i]] = tmp[sa[i - 1]] + (cmp(sa[i - 1], sa[i]) ? 1 : 0);
    rank_ = tmp;

    if (rank_[sa[n - 1]] == n - 1)
      break;
  }
  return sa;
}

// Build LCP array — Kasai O(N)
vector<int> build_lcp(const string &s, const vector<int> &sa) {
  int n = s.size();
  vector<int> rank_(n), lcp(n, 0);
  for (int i = 0; i < n; i++)
    rank_[sa[i]] = i;

  int h = 0;
  for (int i = 0; i < n; i++) {
    if (rank_[i] > 0) {
      int j = sa[rank_[i] - 1];
      while (i + h < n && j + h < n && s[i + h] == s[j + h])
        h++;
      lcp[rank_[i]] = h;
      if (h > 0)
        h--;
    }
  }
  return lcp;
}

// Pattern matching — tìm tất cả vị trí xuất hiện của pattern trong text — O(M
// log N)
pair<int, int> find_pattern(const string &s, const string &pattern,
                            const vector<int> &sa) {
  int n = sa.size(), m = pattern.size();

  int lo = 0, hi = n;
  // Lower bound: suffix >= pattern
  while (lo < hi) {
    int mid = (lo + hi) / 2;
    if (s.substr(sa[mid], m) < pattern)
      lo = mid + 1;
    else
      hi = mid;
  }
  int left = lo;

  lo = 0;
  hi = n;
  // Upper bound: suffix > pattern
  while (lo < hi) {
    int mid = (lo + hi) / 2;
    if (s.substr(sa[mid], m) <= pattern)
      lo = mid + 1;
    else
      hi = mid;
  }
  int right = lo;

  return {left, right}; // sa[left..right) chứa các occurrences
}

// Longest Common Substring của s và t — O((N+M) log(N+M))
string lcs(const string &s, const string &t) {
  string combined = s + "#" + t; // '#' < 'a'
  int n = s.size(), m = t.size(), N = combined.size();

  auto sa = build_suffix_array(combined);
  auto lcp = build_lcp(combined, sa);

  int best_len = 0, best_pos = -1;
  for (int i = 1; i < N; i++) {
    int p = sa[i - 1], q = sa[i];
    // Nếu hai suffix từ hai xâu khác nhau
    if ((p < n) != (q < n)) {
      if (lcp[i] > best_len) {
        best_len = lcp[i];
        best_pos = sa[i];
      }
    }
  }

  if (best_pos == -1)
    return "";
  if (best_pos < n)
    return s.substr(best_pos, best_len);
  return t.substr(best_pos - n - 1, best_len);
}

// Đếm số xâu con phân biệt — O(N log N)
long long count_distinct_substrings(const string &s) {
  int n = s.size();
  auto sa = build_suffix_array(s);
  auto lcp = build_lcp(s, sa);

  long long total = (long long)n * (n + 1) / 2; // Tổng tất cả xâu con
  for (int i = 1; i < n; i++)
    total -= lcp[i]; // Trừ trùng lặp
  return total;
}

int main() {
  ios_base::sync_with_stdio(false);
  cin.tie(NULL);

  string s;
  cin >> s;

  auto sa = build_suffix_array(s);
  auto lcp = build_lcp(s, sa);

  // In suffix array
  for (int i : sa)
    cout << i << " ";
  cout << "\n";

  // LCP
  for (int x : lcp)
    cout << x << " ";
  cout << "\n";

  // Distinct substrings
  cout << count_distinct_substrings(s) << "\n";

  return 0;
}
