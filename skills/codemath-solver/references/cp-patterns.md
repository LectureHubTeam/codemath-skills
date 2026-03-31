# Competitive Programming Patterns Reference

Tham khảo nhanh các pattern thuật toán thường gặp trên CMOJ, giúp agent chọn đúng thuật toán dựa trên constraints.

## Chọn thuật toán theo Constraints

| N range | Target Complexity | Thuật toán phổ biến |
|---------|-------------------|---------------------|
| N ≤ 10 | O(N!) hoặc O(2^N) | Brute force, Permutation |
| N ≤ 20 | O(2^N) | Bitmask DP, Backtracking |
| N ≤ 100 | O(N^3) | Floyd-Warshall, Matrix exponentiation |
| N ≤ 1,000 | O(N^2) | DP, BFS/DFS, Simple nested loops |
| N ≤ 10,000 | O(N√N) | Mo's algorithm, Square root decomposition |
| N ≤ 100,000 | O(N log N) | Sorting + Binary search, Merge sort, Segment tree |
| N ≤ 1,000,000 | O(N) | Prefix sums, Two pointers, Sliding window, Linear DP |
| N ≤ 10^9 | O(√N) hoặc O(log N) | Math, Binary search, Matrix exponentiation |
| N ≤ 10^18 | O(log N) | Binary exponentiation, Math formulas |
| N ≤ 10^100+ | O(len) | Big number (string operations), Digit-level processing |

## Common Problem Types & Templates

### 1. Number Theory (Số học)
**Indicators**: "nguyên tố", "ước", "bội", "GCD", "LCM", "modular"

```cpp
// Kiểm tra số nguyên tố
bool isPrime(long long n) {
    if (n < 2) return false;
    if (n < 4) return true;
    if (n % 2 == 0 || n % 3 == 0) return false;
    for (long long i = 5; i * i <= n; i += 6)
        if (n % i == 0 || n % (i + 2) == 0) return false;
    return true;
}

// Sàng Eratosthenes
vector<bool> sieve(int n) {
    vector<bool> is_prime(n + 1, true);
    is_prime[0] = is_prime[1] = false;
    for (int i = 2; i * i <= n; i++)
        if (is_prime[i])
            for (int j = i * i; j <= n; j += i)
                is_prime[j] = false;
    return is_prime;
}

// GCD
long long gcd(long long a, long long b) {
    return b == 0 ? a : gcd(b, a % b);
}
```

### 2. Digit Processing (Xử lý chữ số)
**Indicators**: "chữ số", "tổng các chữ số", "số đặc biệt", N lớn (> 10^18)

```cpp
// Khi N rất lớn (>10^18), đọc dưới dạng string
string s;
cin >> s;
int digitSum = 0;
for (char c : s) digitSum += c - '0';
// Tổng chữ số tối đa: 9 * 255 = 2295 (nếu N ≤ 10^255)
```

### 3. Dynamic Programming (Quy hoạch động)
**Indicators**: "dãy con", "đếm số cách", "tối ưu", "lớn nhất/nhỏ nhất"

```cpp
// LIS (Longest Increasing Subsequence) - O(N log N)
int lis(vector<int>& a) {
    vector<int> dp;
    for (int x : a) {
        auto it = lower_bound(dp.begin(), dp.end(), x);
        if (it == dp.end()) dp.push_back(x);
        else *it = x;
    }
    return dp.size();
}

// Knapsack 0/1
int knapsack(int W, vector<int>& wt, vector<int>& val, int n) {
    vector<int> dp(W + 1, 0);
    for (int i = 0; i < n; i++)
        for (int w = W; w >= wt[i]; w--)
            dp[w] = max(dp[w], dp[w - wt[i]] + val[i]);
    return dp[W];
}
```

### 4. Graph (Đồ thị)
**Indicators**: "đỉnh", "cạnh", "đường đi", "kết nối", "shortest path"

```cpp
// BFS shortest path
vector<int> bfs(int start, vector<vector<int>>& adj, int n) {
    vector<int> dist(n + 1, -1);
    queue<int> q;
    dist[start] = 0;
    q.push(start);
    while (!q.empty()) {
        int u = q.front(); q.pop();
        for (int v : adj[u]) {
            if (dist[v] == -1) {
                dist[v] = dist[u] + 1;
                q.push(v);
            }
        }
    }
    return dist;
}

// Dijkstra
vector<long long> dijkstra(int start, vector<vector<pair<int,long long>>>& adj, int n) {
    vector<long long> dist(n + 1, LLONG_MAX);
    priority_queue<pair<long long,int>, vector<pair<long long,int>>, greater<>> pq;
    dist[start] = 0;
    pq.push({0, start});
    while (!pq.empty()) {
        auto [d, u] = pq.top(); pq.pop();
        if (d > dist[u]) continue;
        for (auto [v, w] : adj[u]) {
            if (dist[u] + w < dist[v]) {
                dist[v] = dist[u] + w;
                pq.push({dist[v], v});
            }
        }
    }
    return dist;
}
```

### 5. String (Xâu/Chuỗi)
**Indicators**: "xâu", "chuỗi", "palindrome", "substring", "pattern matching"

```cpp
// KMP
vector<int> kmpTable(string& p) {
    int m = p.size();
    vector<int> lps(m, 0);
    for (int i = 1, len = 0; i < m;) {
        if (p[i] == p[len]) { lps[i++] = ++len; }
        else if (len) { len = lps[len - 1]; }
        else { lps[i++] = 0; }
    }
    return lps;
}
```

### 6. Sorting & Searching
**Indicators**: "sắp xếp", "tìm kiếm", "thứ tự", "nhỏ nhất thứ k"

```cpp
// Binary search template
int binarySearch(vector<int>& a, int target) {
    int lo = 0, hi = a.size() - 1;
    while (lo <= hi) {
        int mid = lo + (hi - lo) / 2;
        if (a[mid] == target) return mid;
        else if (a[mid] < target) lo = mid + 1;
        else hi = mid - 1;
    }
    return -1;
}

// Binary search on answer
long long bsAnswer(long long lo, long long hi) {
    while (lo < hi) {
        long long mid = lo + (hi - lo) / 2;
        if (check(mid)) hi = mid;
        else lo = mid + 1;
    }
    return lo;
}
```

## I/O Templates

### C++17 Standard I/O
```cpp
#include <bits/stdc++.h>
using namespace std;

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(NULL);
    
    // Read & solve
    
    return 0;
}
```

### C++17 File I/O (khi đề yêu cầu)
```cpp
#include <bits/stdc++.h>
using namespace std;

int main() {
    freopen("INPUT.INP", "r", stdin);
    freopen("OUTPUT.OUT", "w", stdout);
    
    // Read & solve
    
    return 0;
}
```

### Python 3 Standard I/O
```python
import sys
input = sys.stdin.readline

def solve():
    # Read & solve
    pass

solve()
```

### Python 3 File I/O
```python
import sys
sys.stdin = open('INPUT.INP', 'r')
sys.stdout = open('OUTPUT.OUT', 'w')

def solve():
    # Read & solve
    pass

solve()
```

## Common Gotchas trên CMOJ

1. **Overflow**: Dùng `long long` cho C++ khi N > 2×10^9
2. **Trailing newline**: Một số OJ yêu cầu newline cuối cùng
3. **Multiple test cases**: Đọc kỹ xem có nhiều test case trong 1 input không (T test cases)
4. **1-indexed vs 0-indexed**: CMOJ thường dùng 1-indexed
5. **File I/O**: Một số bài yêu cầu đọc/ghi file, không dùng stdin/stdout
6. **Big numbers**: N > 10^18 → phải dùng string/big integer
7. **Time limit**: Thường 1-2 giây. Python thường cho thêm thời gian (×3-5)
