# Number Theory Patterns

## 1. Prime Testing & Sieve

### Primality Test (O(√N))

```cpp
bool isPrime(long long n) {
    if (n < 2) return false;
    if (n == 2 || n == 3) return true;
    if (n % 2 == 0 || n % 3 == 0) return false;
    for (long long i = 5; i * i <= n; i += 6)
        if (n % i == 0 || n % (i + 2) == 0) return false;
    return true;
}
```

### Sieve of Eratosthenes (O(N log log N))

```cpp
const int MAXN = 1e6 + 5;
vector<bool> is_prime(MAXN, true);
vector<int> primes;

void sieve() {
    is_prime[0] = is_prime[1] = false;
    for (int i = 2; i * i < MAXN; i++) {
        if (is_prime[i]) {
            for (int j = i * i; j < MAXN; j += i)
                is_prime[j] = false;
        }
    }
    for (int i = 2; i < MAXN; i++)
        if (is_prime[i]) primes.push_back(i);
}
```

### Miller-Rabin (for large N > 10^12)

```cpp
long long power(long long base, long long exp, long long mod) {
    long long result = 1;
    base %= mod;
    while (exp > 0) {
        if (exp & 1) result = (__int128)result * base % mod;
        base = (__int128)base * base % mod;
        exp >>= 1;
    }
    return result;
}

bool miller_rabin(long long n, int k = 5) {
    if (n < 2) return false;
    if (n == 2 || n == 3) return true;
    if (n % 2 == 0) return false;
    
    long long d = n - 1, r = 0;
    while (d % 2 == 0) d /= 2, r++;
    
    static const vector<long long> witnesses = {2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37};
    for (long long a : witnesses) {
        if (n <= a) break;
        long long x = power(a, d, n);
        if (x == 1 || x == n - 1) continue;
        bool composite = true;
        for (int i = 0; i < r - 1; i++) {
            x = (__int128)x * x % n;
            if (x == n - 1) {
                composite = false;
                break;
            }
        }
        if (composite) return false;
    }
    return true;
}
```

---

## 2. GCD & LCM

### Euclidean Algorithm

```cpp
long long gcd(long long a, long long b) {
    return b == 0 ? a : gcd(b, a % b);
}

long long lcm(long long a, long long b) {
    return a / gcd(a, b) * b;  // Avoid overflow
}
```

### Extended Euclidean

```cpp
// Returns (g, x, y) such that a*x + b*y = g = gcd(a, b)
tuple<long long, long long, long long> extended_gcd(long long a, long long b) {
    if (b == 0) return {a, 1, 0};
    auto [g, x1, y1] = extended_gcd(b, a % b);
    return {g, y1, x1 - (a / b) * y1};
}
```

---

## 3. Modular Arithmetic

### Modular Exponentiation

```cpp
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
```

### Modular Inverse

```cpp
// Using Fermat's Little Theorem (mod must be prime)
long long mod_inverse(long long a, long long mod) {
    return power(a, mod - 2, mod);
}

// Using Extended Euclidean (mod doesn't need to be prime)
long long mod_inverse_extended(long long a, long long mod) {
    auto [g, x, y] = extended_gcd(a, mod);
    if (g != 1) return -1;  // No inverse
    return (x % mod + mod) % mod;
}
```

---

## 4. Combinatorics

### nCr Precomputation

```cpp
const int MAXN = 1e6 + 5;
const long long MOD = 1e9 + 7;
long long fact[MAXN], inv_fact[MAXN];

long long power(long long base, long long exp, long long mod);

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
```

### Lucas Theorem (for large n, small mod)

```cpp
long long lucas(long long n, long long r, long long mod) {
    if (r == 0) return 1;
    return lucas(n / mod, r / mod, mod) * 
           nCr(n % mod, r % mod) % mod;
}
```

---

## 5. Divisor Functions

### Find All Divisors (O(√N))

```cpp
vector<long long> get_divisors(long long n) {
    vector<long long> divisors;
    for (long long i = 1; i * i <= n; i++) {
        if (n % i == 0) {
            divisors.push_back(i);
            if (i != n / i) divisors.push_back(n / i);
        }
    }
    sort(divisors.begin(), divisors.end());
    return divisors;
}
```

### Count Divisors from Prime Factorization

```cpp
// If n = p1^a1 * p2^a2 * ... * pk^ak
// Number of divisors = (a1+1) * (a2+1) * ... * (ak+1)

int count_divisors(int n) {
    int count = 1;
    for (int i = 2; i * i <= n; i++) {
        if (n % i == 0) {
            int exponent = 0;
            while (n % i == 0) {
                n /= i;
                exponent++;
            }
            count *= (exponent + 1);
        }
    }
    if (n > 1) count *= 2;  // Prime factor left
    return count;
}
```

---

## 6. Prime Factorization

### Trial Division (O(√N))

```cpp
map<int, int> prime_factorize(int n) {
    map<int, int> factors;
    for (int i = 2; i * i <= n; i++) {
        while (n % i == 0) {
            factors[i]++;
            n /= i;
        }
    }
    if (n > 1) factors[n]++;
    return factors;
}
```

### Sieve for Smallest Prime Factor (SPF)

```cpp
const int MAXN = 1e6 + 5;
int spf[MAXN];

void build_spf() {
    iota(spf, spf + MAXN, 0);
    for (int i = 2; i * i < MAXN; i++) {
        if (spf[i] == i) {
            for (int j = i * i; j < MAXN; j += i)
                if (spf[j] == j) spf[j] = i;
        }
    }
}

vector<int> factorize(int n) {
    vector<int> factors;
    while (n > 1) {
        factors.push_back(spf[n]);
        n /= spf[n];
    }
    return factors;
}
```

---

## 7. Euler's Totient Function

### Single Value (O(√N))

```cpp
int phi(int n) {
    int result = n;
    for (int i = 2; i * i <= n; i++) {
        if (n % i == 0) {
            while (n % i == 0) n /= i;
            result -= result / i;
        }
    }
    if (n > 1) result -= result / n;
    return result;
}
```

### Sieve for All Values up to N

```cpp
const int MAXN = 1e6 + 5;
int phi[MAXN];

void build_phi() {
    iota(phi, phi + MAXN, 0);
    for (int i = 2; i < MAXN; i++) {
        if (phi[i] == i) {  // i is prime
            for (int j = i; j < MAXN; j += i)
                phi[j] -= phi[j] / i;
        }
    }
}
```

---

## 8. Chinese Remainder Theorem

```cpp
// Solve: x ≡ a[i] (mod m[i]) for all i
// Returns x mod (product of all m[i])

long long crt(const vector<long long>& a, const vector<long long>& m) {
    long long M = 1;
    for (long long mi : m) M *= mi;
    
    long long result = 0;
    for (int i = 0; i < a.size(); i++) {
        long long Mi = M / m[i];
        long long yi = mod_inverse_extended(Mi, m[i]);
        result = (result + a[i] * Mi % M * yi % M) % M;
    }
    return result;
}
```

---

## 9. Common Patterns

### Pattern: Count Numbers Divisible by K in Range [L, R]

```cpp
// Count = floor(R/K) - floor((L-1)/K)
long long count_divisible(long long L, long long R, long long K) {
    return R / K - (L - 1) / K;
}
```

### Pattern: Sum of GCDs

```cpp
// Sum of gcd(i, n) for i = 1 to n
long long sum_gcd(int n) {
    long long sum = 0;
    for (int i = 1; i * i <= n; i++) {
        if (n % i == 0) {
            sum += i * phi(n / i);
            if (i != n / i) sum += (n / i) * phi(i);
        }
    }
    return sum;
}
```

### Pattern: Count Coprime Pairs

```cpp
// Count pairs (i, j) with 1 ≤ i < j ≤ N and gcd(i, j) = 1
long long count_coprime_pairs(int N) {
    long long count = 0;
    for (int i = 1; i <= N; i++)
        count += phi(i);
    return count;
}
```

---

## Problems to Practice

| Problem | Difficulty | Topic |
|---------|------------|-------|
| Prime Testing | Easy | Primality |
| Sieve | Easy | Prime generation |
| GCD/LCM | Easy | Number theory |
| nCr modulo P | Medium | Combinatorics |
| Divisors | Medium | Factorization |
| CRT | Hard | Modular arithmetic |

---

## Next Steps

- → Practice problems on CMOJ with tag "number-theory"
- → Combine with [03-optimization-patterns.md](03-optimization-patterns.md) for efficiency
- → Check [05-debugging-strategies.md](05-debugging-strategies.md) if stuck
