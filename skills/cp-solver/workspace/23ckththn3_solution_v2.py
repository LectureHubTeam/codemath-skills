#!/usr/bin/env python3
"""
Problem 23ckththn3 - Số Tuần Hoàn (Cyclic Number)
OPTIMIZED solution - avoids full string construction for comparison
"""

import sys

def compare_cyclic_with_string(base_str: str, k: int, target: str) -> int:
    """
    Compare repeat(base_str, k) with target without full construction.
    Returns: -1 if < target, 0 if == target, 1 if > target
    
    Key optimization: Only compare character by character, no full string build.
    """
    N = len(base_str)
    total_len = N * k
    target_len = len(target)
    
    # Length comparison first
    if total_len < target_len:
        return -1
    if total_len > target_len:
        return 1
    
    # Same length - compare character by character
    # repeat(base_str, k)[i] = base_str[i % N]
    for i in range(total_len):
        c_cyclic = base_str[i % N]
        c_target = target[i]
        if c_cyclic < c_target:
            return -1
        if c_cyclic > c_target:
            return 1
    
    return 0

def find_min_base_greater(N: int, k: int, L: str) -> int:
    """
    Find minimum N-digit base B such that repeat(B, k) > L.
    Returns -1 if no such base exists.
    """
    total_len = k * N
    
    if total_len < len(L):
        return -1
    
    lo = 10**(N-1)
    hi = 10**N - 1
    result = -1
    
    while lo <= hi:
        mid = (lo + hi) // 2
        mid_str = str(mid)
        
        cmp = compare_cyclic_with_string(mid_str, k, L)
        if cmp > 0:  # mid works (repeat(mid, k) > L)
            result = mid
            hi = mid - 1
        else:
            lo = mid + 1
    
    return result

def find_max_base_less(N: int, k: int, R: str) -> int:
    """
    Find maximum N-digit base B such that repeat(B, k) < R.
    Returns -1 if no such base exists.
    """
    total_len = k * N
    
    if total_len > len(R):
        return -1
    
    lo = 10**(N-1)
    hi = 10**N - 1
    result = -1
    
    while lo <= hi:
        mid = (lo + hi) // 2
        mid_str = str(mid)
        
        cmp = compare_cyclic_with_string(mid_str, k, R)
        if cmp < 0:  # mid works (repeat(mid, k) < R)
            result = mid
            lo = mid + 1
        else:
            hi = mid - 1
    
    return result

def solve(N: int, L: str, R: str) -> str:
    """
    Main solution: Find cyclic number with period N in range (L, R).
    """
    len_L, len_R = len(L), len(R)
    
    # k * N must be in [len_L, len_R]
    k_min = max(1, (len_L + N - 1) // N)
    k_max = len_R // N
    
    for k in range(k_min, k_max + 1):
        total_len = k * N
        
        # Base bounds (N-digit numbers)
        base_lo = 10**(N-1)
        base_hi = 10**N - 1
        
        # Adjust lower bound based on L
        if total_len == len_L:
            min_base = find_min_base_greater(N, k, L)
            if min_base == -1:
                continue
            base_lo = max(base_lo, min_base)
        # If total_len > len_L, any N-digit base gives number > L
        
        # Adjust upper bound based on R
        if total_len == len_R:
            max_base = find_max_base_less(N, k, R)
            if max_base == -1:
                continue
            base_hi = min(base_hi, max_base)
        # If total_len < len_R, any N-digit base gives number < R
        
        # Check if valid range exists
        if base_lo <= base_hi:
            base_str = str(base_lo)
            return base_str * k
    
    return "-1"

def main():
    input_line = sys.stdin.readline().strip()
    parts = input_line.split()
    N = int(parts[0])
    L = parts[1]
    R = parts[2]
    
    result = solve(N, L, R)
    print(result)

if __name__ == "__main__":
    main()
