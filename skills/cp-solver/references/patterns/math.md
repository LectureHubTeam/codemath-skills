# Math & Combinatorics Patterns

## 1. Basic Combinatorics

### nCr, nPr

```cpp
const int MAXN = 1e6 + 5;
const long long MOD = 1e9 + 7;
long long fact[MAXN], inv_fact[MAXN];

long long power(long long base, long long exp, long long mod) {
    long long result = 1;
    base %= mod;
    while (exp > 0) {
        if (exp & 1) result = result * base % mod;
        base = base * base % mod;
        exp >>= 1;
    }
    return result;
}

void precompute() {
    fact[0] = 1;
    for (int i = 1; i < MAXN; i++)
        fact[i] = fact[i-1] * i % MOD;
    inv_fact[MAXN-1] = power(fact[MAXN-1], MOD - 2, MOD);
    for (int i = MAXN - 2; i >= 0; i--)
        inv_fact[i] = inv_fact[i+1] * (i+1) % MOD;
}

long long nCr(int n, int r) {
    if (r < 0 || r > n) return 0;
    return fact[n] * inv_fact[r] % MOD * inv_fact[n-r] % MOD;
}

long long nPr(int n, int r) {
    if (r < 0 || r > n) return 0;
    return fact[n] * inv_fact[n-r] % MOD;
}
```

---

## 2. Inclusion-Exclusion Principle

```cpp
// Count elements in union of sets
// |A ∪ B ∪ C| = |A| + |B| + |C| - |A ∩ B| - |A ∩ C| - |B ∩ C| + |A ∩ B ∩ C|

// Example: Count numbers from 1 to N divisible by at least one of {a, b, c}
long long count_divisible(long long N, vector<long long>& divisors) {
    int k = divisors.size();
    long long result = 0;
    
    for (int mask = 1; mask < (1 << k); mask++) {
        long long lcm_val = 1;
        int cnt = 0;
        
        for (int i = 0; i < k; i++) {
            if (mask & (1 << i)) {
                lcm_val = lcm(lcm_val, divisors[i]);
                cnt++;
            }
        }
        
        if (cnt & 1) result += N / lcm_val;
        else result -= N / lcm_val;
    }
    return result;
}
```

---

## 3. Catalan Numbers

```cpp
// C_n = (2n)! / ((n+1)! * n!) = C(2n, n) / (n+1)
// Applications: Valid parentheses, BST count, triangulation

long long catalan(int n) {
    return nCr(2*n, n) * power(n + 1, MOD - 2, MOD) % MOD;
}

// First few: 1, 1, 2, 5, 14, 42, 132, 429, ...
```

---

## 4. Stars and Bars

```cpp
// Number of ways to distribute n identical items into k distinct bins
// = C(n + k - 1, k - 1)

long long stars_and_bars(int n, int k) {
    return nCr(n + k - 1, k - 1);
}

// With minimum constraint (each bin ≥ 1)
// = C(n - 1, k - 1)
long long stars_and_bars_min1(int n, int k) {
    if (n < k) return 0;
    return nCr(n - 1, k - 1);
}
```

---

## 5. Derangements

```cpp
// !n = number of permutations with no fixed points
// !n = (n-1) * (!(n-1) + !(n-2))
// !n = n! * sum((-1)^i / i!) for i = 0 to n

long long derangement(int n) {
    if (n == 0) return 1;
    if (n == 1) return 0;
    
    vector<long long> d(n + 1);
    d[0] = 1;
    d[1] = 0;
    
    for (int i = 2; i <= n; i++)
        d[i] = (i - 1) * (d[i-1] + d[i-2]) % MOD;
    
    return d[n];
}
```

---

## 6. Burnside's Lemma

```cpp
// Count distinct objects under symmetry
// |X/G| = (1/|G|) * sum(|X^g|) for all g in G

// Example: Count distinct colorings of n-bead necklace with k colors
// under rotation

long long gcd(long long a, long long b) {
    return b == 0 ? a : gcd(b, a % b);
}

long long necklace_count(int n, int k) {
    long long result = 0;
    for (int i = 0; i < n; i++) {
        int cycles = gcd(n, i);
        result += power(k, cycles, MOD);
    }
    return result * power(n, MOD - 2, MOD) % MOD;
}
```

---

## 7. Game Theory

### Nim Game

```cpp
// Nim: Multiple piles, each turn remove any number from one pile
// Winning condition: XOR of all pile sizes != 0

bool nim_win(vector<int>& piles) {
    int xor_sum = 0;
    for (int p : piles) xor_sum ^= p;
    return xor_sum != 0;  // First player wins if XOR != 0
}

// Sprague-Grundy Theorem
// Every impartial game is equivalent to a Nim pile of size g
// g(Game) = mex{g(Game') for all reachable Game'}
```

### Grundy Numbers

```cpp
int mex(set<int>& s) {
    int m = 0;
    while (s.count(m)) m++;
    return m;
}

// Example: Game where you can remove 1, 2, or 3 stones
int grundy(int n, vector<int>& memo) {
    if (n == 0) return 0;
    if (memo[n] != -1) return memo[n];
    
    set<int> reachable;
    for (int take : {1, 2, 3}) {
        if (n >= take)
            reachable.insert(grundy(n - take, memo));
    }
    
    return memo[n] = mex(reachable);
}
```

---

## 8. Probability

### Expected Value

```cpp
// E[X] = sum(x * P(X=x)) for all x

// Linearity of expectation: E[X + Y] = E[X] + E[Y]

// Example: Expected number of heads in n coin flips
double expected_heads(int n, double p) {
    return n * p;  // Linearity of expectation
}
```

### Birthday Paradox

```cpp
// Probability that at least 2 people share birthday in n people
// P = 1 - (365/365) * (364/365) * ... * ((365-n+1)/365)

double birthday_paradox(int n, int days = 365) {
    if (n > days) return 1.0;
    double p = 1.0;
    for (int i = 0; i < n; i++)
        p *= (double)(days - i) / days;
    return 1.0 - p;
}
```

---

## 9. Number Theory Math

### Sum of Divisors

```cpp
// If n = p1^a1 * p2^a2 * ... * pk^ak
// Sum of divisors = (p1^(a1+1) - 1)/(p1 - 1) * ... * (pk^(ak+1) - 1)/(pk - 1)

long long sum_of_divisors(long long n) {
    long long sum = 1;
    for (long long i = 2; i * i <= n; i++) {
        if (n % i == 0) {
            long long term = 1, power_of_i = 1;
            while (n % i == 0) {
                n /= i;
                power_of_i *= i;
                term += power_of_i;
            }
            sum *= term;
        }
    }
    if (n > 1) sum *= (n + 1);
    return sum;
}
```

### Euler's Totient Sum

```cpp
// Sum of phi(i) for i = 1 to n
// Can be computed in O(n^(2/3)) using Dirichlet convolution

long long phi_sum(int n) {
    vector<long long> phi(n + 1);
    iota(phi.begin(), phi.end(), 0);
    
    for (int i = 2; i <= n; i++) {
        if (phi[i] == i) {  // i is prime
            for (int j = i; j <= n; j += i)
                phi[j] -= phi[j] / i;
        }
    }
    
    long long sum = 0;
    for (int i = 1; i <= n; i++)
        sum += phi[i];
    return sum;
}
```

---

## 10. Pick's Theorem

```cpp
// For a polygon with integer coordinates:
// Area = I + B/2 - 1
// where I = interior lattice points, B = boundary lattice points

// Boundary points on segment from (x1,y1) to (x2,y2):
// gcd(|x2-x1|, |y2-y1|) + 1

long long boundary_points(pair<int,int> p1, pair<int,int> p2) {
    return gcd(abs(p1.first - p2.first), abs(p1.second - p2.second)) + 1;
}

// For a polygon, sum all edges and subtract vertices (counted twice)
```

---

## Common Math Problems

| Problem Type | Formula/Algorithm |
|-------------|-------------------|
| nCr modulo P | Precompute factorials |
| Inclusion-Exclusion | Iterate all subsets |
| Catalan numbers | C(2n,n)/(n+1) |
| Stars and Bars | C(n+k-1, k-1) |
| Derangements | !(n) = (n-1)(!(n-1) + !(n-2)) |
| Nim game | XOR of pile sizes |
| Expected value | Linearity of expectation |

---

## Next Steps

- → Practice combinatorics problems on CMOJ
- → Combine with [patterns/number-theory.md](number-theory.md) for number theory
- → Use [06-test-generation.md](06-test-generation.md) to verify formulas
