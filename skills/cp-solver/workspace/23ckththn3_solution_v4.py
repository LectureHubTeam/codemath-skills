#!/usr/bin/env python3
"""
Problem 23ckththn3 - Số Tuần Hoàn (Cyclic Number)
FINAL OPTIMIZED solution - O(N*k) using digit-by-digit construction
"""

import sys

def construct_min_base(N: int, k: int, L: str) -> str:
    """
    Construct minimum N-digit base B such that repeat(B, k) > L.
    Returns empty string if impossible.
    """
    total_len = k * N
    
    if total_len < len(L):
        return ""
    
    if total_len > len(L):
        # Any N-digit number works, return smallest
        return "1" + "0" * (N - 1)
    
    # total_len == len(L): Need repeat(B, k) > L
    blocks = [L[i*N:(i+1)*N] for i in range(k)]
    
    # For repeat(B, k) > L:
    # At first position i where B != blocks[i], need B > blocks[i]
    # Strategy: B = max(blocks[0..i]) + 1 for some i, ensuring B > blocks[i]
    # and B >= all earlier blocks
    
    # Simple approach: B = max(all blocks) + 1
    # This ensures B > blocks[i] for all i, so repeat(B, k) > L
    
    max_block = max(blocks)
    
    try:
        B_val = int(max_block) + 1
        B_candidate = str(B_val)
        if len(B_candidate) > N:
            return ""  # Overflow
        # Pad with leading zeros if needed (but B should be N digits)
        B_candidate = B_candidate.zfill(N)
        return B_candidate
    except:
        return ""

def construct_max_base(N: int, k: int, R: str) -> str:
    """
    Construct maximum N-digit base B such that repeat(B, k) < R.
    Returns empty string if impossible.
    """
    total_len = k * N
    
    if total_len > len(R):
        return ""
    
    if total_len < len(R):
        # Any N-digit number works, return largest
        return "9" * N
    
    # total_len == len(R): Need repeat(B, k) < R
    blocks = [R[i*N:(i+1)*N] for i in range(k)]
    min_n_digit = 10**(N-1)  # Smallest N-digit number
    
    # For repeat(B, k) < R:
    # At first position i where B != blocks[i], need B < blocks[i]
    
    # Case 1: B < blocks[0] → works, max B = blocks[0] - 1
    # Case 2: B = blocks[0], then need B < blocks[1] (if exists)
    #         → works if blocks[0] < blocks[1], max B = blocks[0]
    # Case 3: B = blocks[0] = blocks[1], need B < blocks[2], etc.
    
    # General: Find first j where blocks[j] != blocks[0]
    # If blocks[j] > blocks[0]: B = blocks[0] works
    # If blocks[j] < blocks[0]: B must be < blocks[0], so B = blocks[0] - 1
    
    # If all blocks equal: B = blocks[0] - 1 (since B = blocks[0] gives equality)
    
    block0_val = int(blocks[0])
    
    # Check if all blocks are equal to blocks[0]
    all_equal = all(b == blocks[0] for b in blocks)
    
    if all_equal:
        # B = blocks[0] - 1
        B_val = block0_val - 1
        if B_val < min_n_digit:
            return ""  # Not an N-digit number
        return str(B_val).zfill(N)
    
    # Find first block that differs from blocks[0]
    first_diff_val = None
    for b in blocks:
        if b != blocks[0]:
            first_diff_val = int(b)
            break
    
    if first_diff_val > block0_val:
        # B = blocks[0] works (at first diff position, B < blocks[j])
        B_val = block0_val
        if B_val < min_n_digit:
            return ""
        return str(B_val).zfill(N)
    else:
        # first_diff_val < block0_val
        # B must be < blocks[0], so B = blocks[0] - 1
        B_val = block0_val - 1
        if B_val < min_n_digit:
            return ""
        return str(B_val).zfill(N)

def solve(N: int, L: str, R: str) -> str:
    """
    Main solution: Find cyclic number with period N in range (L, R).
    """
    len_L, len_R = len(L), len(R)
    
    k_min = max(1, (len_L + N - 1) // N)
    k_max = len_R // N
    
    for k in range(k_min, k_max + 1):
        total_len = k * N
        
        base_lo = 10**(N-1)
        base_hi = 10**N - 1
        
        # Find minimum base > L
        if total_len >= len(L):
            min_base_str = construct_min_base(N, k, L)
            if min_base_str:
                min_base = int(min_base_str)
                base_lo = max(base_lo, min_base)
            elif total_len == len(L):
                continue  # Impossible for this k
        
        # Find maximum base < R
        if total_len <= len(R):
            max_base_str = construct_max_base(N, k, R)
            if max_base_str:
                max_base = int(max_base_str)
                base_hi = min(base_hi, max_base)
            elif total_len == len(R):
                continue  # Impossible for this k
        
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
