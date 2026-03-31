# Problem 23ckththn3 - Số Tuần Hoàn (Cyclic Number)

## Problem Analysis

**Definition:** A cyclic number with period N is formed by repeating a base B (exactly N digits) multiple times.

**Task:** Find any cyclic number with period N in range (L, R).

**Constraints:**
- N ≤ 10^5
- L, R ≤ 10^(10^5) (very large - need string handling!)

## Key Observations

1. **Length must be multiple of N:** A cyclic number with period N has length k*N for some k ≥ 1.

2. **Base B has exactly N digits:** B ∈ [10^(N-1), 10^N - 1]

3. **Cyclic number construction:** repeat(B, k) = B concatenated k times

4. **Range check:** We need L < repeat(B, k) < R

## Algorithm Design

### Approach: Iterate over possible lengths, binary search on base

For each possible length = k*N (k = 1, 2, 3, ...):
1. Find minimum base B_min such that repeat(B_min, k) > L
2. Find maximum base B_max such that repeat(B_max, k) < R
3. If B_min ≤ B_max and both are valid N-digit numbers, return repeat(B_min, k)

### Binary Search Strategy

For a fixed k:
- **Lower bound:** Binary search for smallest B where repeat(B, k) > L
- **Upper bound:** Binary search for largest B where repeat(B, k) < R

**Comparison:** Compare repeat(B, k) with L/R lexicographically (as strings)

### Optimization Insights

1. **Early termination:** If length of L < k*N < length of R, any valid N-digit base works
2. **Length bounds:** Only check k where k*N is between len(L) and len(R)
3. **Direct computation:** When k*N > len(L) and k*N < len(R), use smallest valid base (10^(N-1))

## Edge Cases (WA on test #6)

1. **L and R have same length:** Need careful binary search
2. **No valid k exists:** Return -1
3. **N is large:** Only k=1 might be possible
4. **R - L is small:** May not contain any cyclic number
5. **Boundary conditions:** L < T < R (strict inequality!)

## TLE Issues (test #16)

1. **String operations:** Avoid creating full repeated strings for comparison
2. **Binary search optimization:** Use string comparison without full construction
3. **Early exit:** Stop when length exceeds len(R)

## Optimized Algorithm

```python
def solve(N, L, R):
    len_L, len_R = len(L), len(R)
    
    # Try each possible length = k * N
    for k in range(1, (len_R // N) + 2):
        total_len = k * N
        
        # Skip if too short
        if total_len < len_L:
            continue
        
        # Stop if too long
        if total_len > len_R:
            break
        
        # Find valid base range
        B_min = 10**(N-1)  # Smallest N-digit number
        B_max = 10**N - 1  # Largest N-digit number
        
        # Binary search for lower bound
        if total_len == len_L:
            B_min = find_lower_bound(N, k, L, B_min, B_max)
        
        # Binary search for upper bound
        if total_len == len_R:
            B_max = find_upper_bound(N, k, R, B_min, B_max)
        
        # Check if valid range exists
        if B_min <= B_max:
            return str(B_min) * k
    
    return "-1"
```

## Complexity

- **Time:** O(k_max * N * log(10^N)) where k_max = len(R)/N
- **Space:** O(N) for string operations

## Test Cases to Verify

1. Sample 1: N=2, L=1234, R=9876 → 2222 (or any valid)
2. Sample 2: N=2, L=1234, R=2000 → 1515
3. Sample 3: N=2, L=1234, R=1300 → -1
4. Edge: N=1, L=5, R=10 → 6,7,8,9 (any single digit)
5. Edge: Large N, small range
