# Dynamic Programming Patterns

## 1. LIS - Longest Increasing Subsequence

### O(N²) DP

```cpp
int lis_n2(vector<int>& a) {
    int n = a.size();
    vector<int> dp(n, 1);
    for (int i = 0; i < n; i++)
        for (int j = 0; j < i; j++)
            if (a[j] < a[i])
                dp[i] = max(dp[i], dp[j] + 1);
    return *max_element(dp.begin(), dp.end());
}
```

### O(N log N) with Binary Search

```cpp
int lis_nlogn(vector<int>& a) {
    vector<int> dp;
    for (int x : a) {
        auto it = lower_bound(dp.begin(), dp.end(), x);
        if (it == dp.end()) dp.push_back(x);
        else *it = x;
    }
    return dp.size();
}

// To reconstruct the LIS
vector<int> lis_with_path(vector<int>& a) {
    int n = a.size();
    vector<int> dp(n, 1), parent(n, -1);
    vector<int> tail_idx;
    
    for (int i = 0; i < n; i++) {
        auto it = lower_bound(tail_idx.begin(), tail_idx.end(), i,
            [&](int idx1, int idx2) { return a[idx1] < a[idx2]; });
        int pos = it - tail_idx.begin();
        
        if (pos > 0) parent[i] = tail_idx[pos - 1];
        if (pos == tail_idx.size()) tail_idx.push_back(i);
        else *it = i;
        
        dp[i] = pos + 1;
    }
    
    // Reconstruct
    int len = tail_idx.size();
    vector<int> lis(len);
    int idx = tail_idx.back();
    for (int i = len - 1; i >= 0; i--) {
        lis[i] = a[idx];
        idx = parent[idx];
    }
    return lis;
}
```

---

## 2. Knapsack Problems

### 0/1 Knapsack

```cpp
// N items, weight W
// Item i: weight wt[i], value val[i]
// Maximize total value with weight ≤ W

int knapsack_01(int N, int W, vector<int>& wt, vector<int>& val) {
    vector<int> dp(W + 1, 0);
    for (int i = 0; i < N; i++)
        for (int w = W; w >= wt[i]; w--)
            dp[w] = max(dp[w], dp[w - wt[i]] + val[i]);
    return dp[W];
}
```

### Unbounded Knapsack

```cpp
// Each item can be used multiple times

int knapsack_unbounded(int N, int W, vector<int>& wt, vector<int>& val) {
    vector<int> dp(W + 1, 0);
    for (int i = 0; i < N; i++)
        for (int w = wt[i]; w <= W; w++)
            dp[w] = max(dp[w], dp[w - wt[i]] + val[i]);
    return dp[W];
}
```

### Bounded Knapsack (K copies)

```cpp
// Each item has at most K copies

int knapsack_bounded(int N, int W, vector<int>& wt, vector<int>& val, vector<int>& K) {
    vector<int> dp(W + 1, 0);
    for (int i = 0; i < N; i++) {
        int k = K[i];
        // Binary decomposition: 1, 2, 4, ..., 2^p, remainder
        for (int mult = 1; k > 0; mult *= 2) {
            int take = min(mult, k);
            int weight = take * wt[i];
            int value = take * val[i];
            for (int w = W; w >= weight; w--)
                dp[w] = max(dp[w], dp[w - weight] + value);
            k -= take;
        }
    }
    return dp[W];
}
```

---

## 3. Range DP

### Matrix Chain Multiplication

```cpp
// Minimum cost to multiply matrices A1, A2, ..., An
// Matrix Ai has dimensions p[i-1] x p[i]

int matrix_chain(vector<int>& p) {
    int n = p.size() - 1;
    vector<vector<int>> dp(n, vector<int>(n, 0));
    
    for (int len = 2; len <= n; len++) {
        for (int i = 0; i <= n - len; i++) {
            int j = i + len - 1;
            dp[i][j] = INT_MAX;
            for (int k = i; k < j; k++)
                dp[i][j] = min(dp[i][j], 
                    dp[i][k] + dp[k+1][j] + p[i] * p[k+1] * p[j+1]);
        }
    }
    return dp[0][n-1];
}
```

### Optimal Binary Search Tree

```cpp
// Given frequencies of keys, find optimal BST

int optimal_bst(vector<int>& freq) {
    int n = freq.size();
    vector<vector<int>> dp(n, vector<int>(n, 0));
    vector<vector<int>> sum(n, vector<int>(n, 0));
    
    for (int i = 0; i < n; i++) {
        dp[i][i] = freq[i];
        sum[i][i] = freq[i];
    }
    
    for (int len = 2; len <= n; len++) {
        for (int i = 0; i <= n - len; i++) {
            int j = i + len - 1;
            sum[i][j] = sum[i][j-1] + freq[j];
            dp[i][j] = INT_MAX;
            for (int r = i; r <= j; r++) {
                int left = (r > i) ? dp[i][r-1] : 0;
                int right = (r < j) ? dp[r+1][j] : 0;
                dp[i][j] = min(dp[i][j], left + right + sum[i][j]);
            }
        }
    }
    return dp[0][n-1];
}
```

---

## 4. Digit DP

### Count Numbers with Property

```cpp
// Count numbers from 0 to N with digit sum = K

string s;
int K;
int memo[20][200][2];

int dp(int pos, int sum, bool tight) {
    if (sum > K) return 0;
    if (pos == s.size()) return sum == K;
    if (memo[pos][sum][tight] != -1) return memo[pos][sum][tight];
    
    int limit = tight ? (s[pos] - '0') : 9;
    int result = 0;
    
    for (int d = 0; d <= limit; d++) {
        bool new_tight = tight && (d == limit);
        result += dp(pos + 1, sum + d, new_tight);
    }
    
    return memo[pos][sum][tight] = result;
}

int count_numbers(int N, int K) {
    s = to_string(N);
    memset(memo, -1, sizeof(memo));
    return dp(0, 0, true);
}
```

### Count Numbers without Consecutive 1s

```cpp
// Count numbers from 0 to N without consecutive 1s in binary

string s;
int memo[65][2][2];  // [pos][last_digit][tight]

int dp(int pos, int last, bool tight) {
    if (pos == s.size()) return 1;
    if (memo[pos][last][tight] != -1) return memo[pos][last][tight];
    
    int limit = tight ? (s[pos] - '0') : 1;
    int result = 0;
    
    for (int d = 0; d <= limit; d++) {
        if (last == 1 && d == 1) continue;  // No consecutive 1s
        bool new_tight = tight && (d == limit);
        result += dp(pos + 1, d, new_tight);
    }
    
    return memo[pos][last][tight] = result;
}
```

---

## 5. Tree DP

### Maximum Independent Set on Tree

```cpp
vector<int> adj[MAXN];
int dp[MAXN][2];  // dp[u][0] = u not taken, dp[u][1] = u taken

void dfs(int u, int p) {
    dp[u][0] = 0;
    dp[u][1] = 1;  // Weight of u
    
    for (int v : adj[u]) {
        if (v == p) continue;
        dfs(v, u);
        dp[u][0] += max(dp[v][0], dp[v][1]);  // u not taken, v can be either
        dp[u][1] += dp[v][0];  // u taken, v must not be taken
    }
}

int max_independent_set(int root) {
    dfs(root, -1);
    return max(dp[root][0], dp[root][1]);
}
```

### Tree Diameter

```cpp
vector<int> adj[MAXN];
int max_dist[MAXN];
int diameter = 0;

void dfs(int u, int p) {
    max_dist[u] = 0;
    int max1 = 0, max2 = 0;  // Two longest paths from u
    
    for (int v : adj[u]) {
        if (v == p) continue;
        dfs(v, u);
        max_dist[u] = max(max_dist[u], max_dist[v] + 1);
        
        // Update two longest paths
        if (max_dist[v] + 1 > max1) {
            max2 = max1;
            max1 = max_dist[v] + 1;
        } else if (max_dist[v] + 1 > max2) {
            max2 = max_dist[v] + 1;
        }
    }
    
    diameter = max(diameter, max1 + max2);
}
```

---

## 6. DP with Bitmask

### Traveling Salesman Problem

```cpp
// TSP: Find minimum cost to visit all cities starting from 0

int n;
int cost[MAXN][MAXN];
int memo[MAXN][1 << MAXN];

int dp(int mask, int u) {
    if (mask == (1 << n) - 1) return cost[u][0];  // Return to start
    if (memo[u][mask] != -1) return memo[u][mask];
    
    int result = INT_MAX;
    for (int v = 0; v < n; v++) {
        if (!(mask & (1 << v))) {  // v not visited
            result = min(result, dp(mask | (1 << v), u) + cost[u][v]);
        }
    }
    return memo[u][mask] = result;
}

int tsp() {
    memset(memo, -1, sizeof(memo));
    return dp(1, 0);  // Start from city 0, mask = 1 (city 0 visited)
}
```

### Count Valid Arrangements

```cpp
// Count ways to arrange N items with constraints

int n;
int memo[1 << MAXN];

int dp(int mask) {
    if (mask == (1 << n) - 1) return 1;
    if (memo[mask] != -1) return memo[mask];
    
    int pos = __builtin_popcount(mask);  // Next position to fill
    int result = 0;
    
    for (int i = 0; i < n; i++) {
        if (!(mask & (1 << i))) {  // Item i not used
            if (can_place(i, pos)) {  // Check constraint
                result += dp(mask | (1 << i));
            }
        }
    }
    return memo[mask] = result;
}
```

---

## 7. DP Optimization

### Prefix Sum Optimization

```cpp
// When dp[i] = sum(dp[j]) for j in some range

vector<long long> dp(n + 1, 0);
vector<long long> pref(n + 2, 0);

dp[0] = 1;
pref[1] = 1;

for (int i = 1; i <= n; i++) {
    // dp[i] = sum(dp[j]) for j in [L, R]
    int L = /* ... */, R = /* ... */;
    dp[i] = (pref[R + 1] - pref[L] + MOD) % MOD;
    pref[i + 1] = (pref[i] + dp[i]) % MOD;
}
```

### Convex Hull Trick (for specific recurrences)

```cpp
// When dp[i] = min/max(a[j] * x[i] + b[j]) + c[i]

struct Line {
    long long m, b;
    long long eval(long long x) { return m * x + b; }
};

vector<Line> hull;

void add_line(long long m, long long b) {
    // Add line y = mx + b to hull
    // Remove lines that are never optimal
    while (hull.size() >= 2) {
        Line& l1 = hull[hull.size() - 2];
        Line& l2 = hull[hull.size() - 1];
        Line l3 = {m, b};
        // Check if l2 is redundant
        if ((l3.b - l1.b) * (l1.m - l2.m) <= (l2.b - l1.b) * (l1.m - l3.m))
            hull.pop_back();
        else break;
    }
    hull.push_back({m, b});
}

long long query(long long x) {
    // Binary search for optimal line
    int lo = 0, hi = hull.size() - 1;
    while (lo < hi) {
        int mid = (lo + hi) / 2;
        if (hull[mid].eval(x) > hull[mid + 1].eval(x))
            lo = mid + 1;
        else hi = mid;
    }
    return hull[lo].eval(x);
}
```

---

## Common DP States

| Problem Type | State | Transition |
|-------------|-------|------------|
| LIS | dp[i] = length ending at i | dp[i] = max(dp[j] + 1) for j < i |
| Knapsack | dp[w] = max value with weight w | dp[w] = max(dp[w], dp[w-wt] + val) |
| Range | dp[l][r] = optimal for range [l,r] | dp[l][r] = min/max over split points |
| Tree | dp[u][state] = optimal for subtree | dp[u] = combine dp[children] |
| Bitmask | dp[mask] = optimal for subset | dp[mask] = min/max over next element |
| Digit | dp[pos][state][tight] | dp[pos] = sum over digits |

---

## Next Steps

- → Practice DP problems on CMOJ
- → Learn [04-advanced-algorithms.md](04-advanced-algorithms.md) for advanced techniques
- → Use [06-test-generation.md](06-test-generation.md) to verify DP solutions
