# String Algorithms Patterns

## 1. String Matching

### Naive Pattern Matching (O(NM))

```cpp
vector<int> naive_match(const string& text, const string& pattern) {
    vector<int> positions;
    int n = text.size(), m = pattern.size();
    
    for (int i = 0; i <= n - m; i++) {
        bool match = true;
        for (int j = 0; j < m; j++) {
            if (text[i + j] != pattern[j]) {
                match = false;
                break;
            }
        }
        if (match) positions.push_back(i);
    }
    return positions;
}
```

### KMP Algorithm (O(N+M))

```cpp
vector<int> kmp_table(const string& pattern) {
    int m = pattern.size();
    vector<int> lps(m, 0);
    int len = 0, i = 1;
    
    while (i < m) {
        if (pattern[i] == pattern[len]) {
            len++;
            lps[i] = len;
            i++;
        } else {
            if (len != 0) {
                len = lps[len - 1];
            } else {
                lps[i] = 0;
                i++;
            }
        }
    }
    return lps;
}

vector<int> kmp_search(const string& text, const string& pattern) {
    vector<int> positions;
    int n = text.size(), m = pattern.size();
    vector<int> lps = kmp_table(pattern);
    
    int i = 0, j = 0;
    while (i < n) {
        if (pattern[j] == text[i]) {
            i++;
            j++;
        }
        if (j == m) {
            positions.push_back(i - j);
            j = lps[j - 1];
        } else if (i < n && pattern[j] != text[i]) {
            if (j != 0) j = lps[j - 1];
            else i++;
        }
    }
    return positions;
}
```

### Rabin-Karp (O(N+M) average)

```cpp
vector<int> rabin_karp(const string& text, const string& pattern, long long base = 31, long long mod = 1e9 + 7) {
    vector<int> positions;
    int n = text.size(), m = pattern.size();
    
    if (m > n) return positions;
    
    // Precompute base^m
    long long base_m = 1;
    for (int i = 0; i < m; i++)
        base_m = base_m * base % mod;
    
    // Hash of pattern
    long long pattern_hash = 0;
    for (int i = 0; i < m; i++)
        pattern_hash = (pattern_hash * base + pattern[i]) % mod;
    
    // Hash of first window
    long long text_hash = 0;
    for (int i = 0; i < m; i++)
        text_hash = (text_hash * base + text[i]) % mod;
    
    for (int i = 0; i <= n - m; i++) {
        if (text_hash == pattern_hash) {
            // Verify match
            bool match = true;
            for (int j = 0; j < m; j++) {
                if (text[i + j] != pattern[j]) {
                    match = false;
                    break;
                }
            }
            if (match) positions.push_back(i);
        }
        
        // Roll hash
        if (i < n - m) {
            text_hash = (text_hash - text[i] * base_m % mod + mod) % mod;
            text_hash = (text_hash * base + text[i + m]) % mod;
        }
    }
    return positions;
}
```

---

## 2. Z-Algorithm (O(N))

```cpp
vector<int> z_function(const string& s) {
    int n = s.size();
    vector<int> z(n, 0);
    int l = 0, r = 0;
    
    for (int i = 1; i < n; i++) {
        if (i < r) z[i] = min(r - i, z[i - l]);
        while (i + z[i] < n && s[z[i]] == s[i + z[i]]) z[i]++;
        if (i + z[i] > r) {
            l = i;
            r = i + z[i];
        }
    }
    return z;
}

// Pattern matching using Z-algorithm
vector<int> z_match(const string& text, const string& pattern) {
    string combined = pattern + "$" + text;
    vector<int> z = z_function(combined);
    vector<int> positions;
    
    int m = pattern.size();
    for (int i = m + 1; i < combined.size(); i++) {
        if (z[i] == m) positions.push_back(i - m - 1);
    }
    return positions;
}
```

---

## 3. Longest Common Substring

### DP Solution (O(N*M))

```cpp
string longest_common_substring(const string& s1, const string& s2) {
    int n = s1.size(), m = s2.size();
    vector<vector<int>> dp(n + 1, vector<int>(m + 1, 0));
    
    int max_len = 0, end_pos = 0;
    
    for (int i = 1; i <= n; i++) {
        for (int j = 1; j <= m; j++) {
            if (s1[i-1] == s2[j-1]) {
                dp[i][j] = dp[i-1][j-1] + 1;
                if (dp[i][j] > max_len) {
                    max_len = dp[i][j];
                    end_pos = i;
                }
            }
        }
    }
    
    return s1.substr(end_pos - max_len, max_len);
}
```

---

## 4. Longest Palindromic Substring

### Expand Around Center (O(N²))

```cpp
string longest_palindrome(const string& s) {
    int n = s.size();
    int start = 0, max_len = 1;
    
    auto expand = [&](int left, int right) {
        while (left >= 0 && right < n && s[left] == s[right]) {
            left--;
            right++;
        }
        return right - left - 1;
    };
    
    for (int i = 0; i < n; i++) {
        int len1 = expand(i, i);  // Odd length
        int len2 = expand(i, i + 1);  // Even length
        int len = max(len1, len2);
        
        if (len > max_len) {
            max_len = len;
            start = i - (len - 1) / 2;
        }
    }
    
    return s.substr(start, max_len);
}
```

### Manacher's Algorithm (O(N))

```cpp
vector<int> manacher(const string& s) {
    string t = "#";
    for (char c : s) {
        t += c;
        t += "#";
    }
    
    int n = t.size();
    vector<int> p(n, 0);
    int l = 0, r = -1;
    
    for (int i = 0; i < n; i++) {
        int k = (i > r) ? 1 : min(p[l + r - i], r - i + 1);
        while (i - k >= 0 && i + k < n && t[i - k] == t[i + k]) k++;
        p[i] = --k;
        if (i + k > r) {
            l = i - k;
            r = i + k;
        }
    }
    
    return p;
}

string longest_palindrome_manacher(const string& s) {
    vector<int> p = manacher(s);
    int max_len = 0, center = 0;
    for (int i = 0; i < p.size(); i++) {
        if (p[i] > max_len) {
            max_len = p[i];
            center = i;
        }
    }
    int start = (center - max_len) / 2;
    return s.substr(start, max_len);
}
```

---

## 5. String Hashing

### Rolling Hash

```cpp
struct RollingHash {
    vector<long long> hash, power;
    long long base, mod;
    
    RollingHash(const string& s, long long base = 31, long long mod = 1e9 + 7) 
        : base(base), mod(mod) {
        int n = s.size();
        hash.resize(n + 1, 0);
        power.resize(n + 1, 1);
        
        for (int i = 0; i < n; i++) {
            hash[i + 1] = (hash[i] * base + s[i]) % mod;
            power[i + 1] = (power[i] * base) % mod;
        }
    }
    
    long long get_hash(int l, int r) {  // 0-indexed, inclusive
        long long h = (hash[r + 1] - hash[l] * power[r - l + 1]) % mod;
        return (h + mod) % mod;
    }
};

// Usage
RollingHash rh(s);
long long h1 = rh.get_hash(0, 4);  // Hash of s[0..4]
```

---

## 6. Suffix Array (O(N log²N))

```cpp
vector<int> suffix_array(string s) {
    s += "$";
    int n = s.size();
    vector<int> p(n), c(n);
    vector<int> cnt(max(n, 256), 0);
    
    // Sort by first character
    for (char ch : s) cnt[ch]++;
    for (int i = 1; i < 256; i++) cnt[i] += cnt[i-1];
    for (int i = 0; i < n; i++) p[--cnt[s[i]]] = i;
    
    c[p[0]] = 0;
    int classes = 1;
    for (int i = 1; i < n; i++) {
        if (s[p[i]] != s[p[i-1]]) classes++;
        c[p[i]] = classes - 1;
    }
    
    vector<int> pn(n), cn(n);
    for (int h = 0; (1 << h) < n; h++) {
        for (int i = 0; i < n; i++) {
            pn[i] = p[i] - (1 << h);
            if (pn[i] < 0) pn[i] += n;
        }
        
        fill(cnt.begin(), cnt.begin() + classes, 0);
        for (int i = 0; i < n; i++) cnt[c[pn[i]]]++;
        for (int i = 1; i < classes; i++) cnt[i] += cnt[i-1];
        for (int i = n-1; i >= 0; i--) p[--cnt[c[pn[i]]]] = pn[i];
        
        cn[p[0]] = 0;
        classes = 1;
        for (int i = 1; i < n; i++) {
            pair<int, int> cur = {c[p[i]], c[(p[i] + (1 << h)) % n]};
            pair<int, int> prev = {c[p[i-1]], c[(p[i-1] + (1 << h)) % n]};
            if (cur != prev) ++classes;
            cn[p[i]] = classes - 1;
        }
        c.swap(cn);
    }
    
    p.erase(p.begin());  // Remove $ position
    return p;
}
```

---

## 7. Aho-Corasick (Multiple Pattern Matching)

```cpp
struct AhoCorasick {
    vector<map<char, int>> trie;
    vector<int> fail;
    vector<vector<int>> output;
    int nodes;
    
    AhoCorasick() {
        trie.push_back(map<char, int>());
        fail.push_back(0);
        output.push_back(vector<int>());
        nodes = 1;
    }
    
    void insert(const string& pattern, int id) {
        int node = 0;
        for (char c : pattern) {
            if (!trie[node].count(c)) {
                trie.push_back(map<char, int>());
                fail.push_back(0);
                output.push_back(vector<int>());
                trie[node][c] = nodes++;
            }
            node = trie[node][c];
        }
        output[node].push_back(id);
    }
    
    void build() {
        queue<int> q;
        for (auto& [c, node] : trie[0]) {
            q.push(node);
        }
        
        while (!q.empty()) {
            int u = q.front(); q.pop();
            for (auto& [c, v] : trie[u]) {
                int f = fail[u];
                while (f && !trie[f].count(c)) f = fail[f];
                fail[v] = trie[f].count(c) && trie[f][c] != v ? trie[f][c] : 0;
                output[v].insert(output[v].end(), output[fail[v]].begin(), output[fail[v]].end());
                q.push(v);
            }
        }
    }
    
    vector<int> search(const string& text) {
        vector<int> matches;
        int node = 0;
        for (char c : text) {
            while (node && !trie[node].count(c)) node = fail[node];
            if (trie[node].count(c)) node = trie[node][c];
            for (int id : output[node]) matches.push_back(id);
        }
        return matches;
    }
};
```

---

## Common String Problems

| Problem | Algorithm | Complexity |
|---------|-----------|------------|
| Pattern matching | KMP / Z-algo | O(N+M) |
| Multiple pattern matching | Aho-Corasick | O(N + M + Z) |
| Longest common substring | DP / Suffix Array | O(N*M) / O(N log N) |
| Longest palindrome | Manacher | O(N) |
| Count distinct substrings | Suffix Array | O(N log²N) |
| String hashing | Rolling Hash | O(1) per query |

---

## Next Steps

- → Practice string problems on CMOJ
- → Learn [04-advanced-algorithms.md](04-advanced-algorithms.md) for Suffix Automaton
- → Use [06-test-generation.md](06-test-generation.md) to test string solutions
