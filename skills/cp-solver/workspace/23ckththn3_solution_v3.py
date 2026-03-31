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
    
    Uses digit-by-digit greedy construction.
    """
    total_len = k * N
    
    if total_len < len(L):
        return ""
    
    if total_len > len(L):
        # Any N-digit number works, return smallest
        return "1" + "0" * (N - 1)
    
    # total_len == len(L): Need repeat(B, k) > L
    # L = L[0:N] + L[N:2N] + ... + L[(k-1)N:kN]
    # repeat(B, k) = B + B + ... + B (k times)
    
    # Greedy: find first position where B differs from L's block
    # and makes repeat(B, k) > L
    
    # Extract blocks from L
    blocks = [L[i*N:(i+1)*N] for i in range(k)]
    
    # Try to find minimum B
    # Strategy: B should be >= some block and > some earlier block
    
    # Case 1: B > blocks[0] → repeat(B, k) > L (first block already larger)
    # Minimum such B = blocks[0] + 1 (as number)
    
    # Case 2: B == blocks[0], then need B > blocks[1] or (B == blocks[1] and ...)
    # This means B must be > min(blocks[1:]) for the first differing position
    
    # General: Find the minimum B such that for the first i where B != blocks[i],
    # we have B > blocks[i]
    
    # Approach: Try B = blocks[i] + 1 for each i, and check if it works
    # Also try B = max(blocks) + 1
    
    # More efficient: 
    # - If all blocks are the same, B = blocks[0] + 1
    # - Otherwise, find minimum B that works
    
    # Simple approach: B must be >= max(blocks[0..j]) for some j, and > blocks[j]
    # Minimum valid B = min over all j of (max(blocks[0..j]) + 1 if blocks[j] < max, else blocks[j] + 1)
    
    # Actually simpler: 
    # For repeat(B, k) > L, at the first position i where B != blocks[i], we need B > blocks[i]
    # So B must be > min{blocks[i] : i = 0..k-1} at the first differing position
    
    # Best strategy:
    # 1. Find minimum block: min_block = min(blocks)
    # 2. If B > min_block, then at the first occurrence of min_block, B > blocks[i]
    # 3. So minimum B = min_block + 1
    
    # But wait, we also need B to be valid for all earlier positions
    # If B = min_block + 1, and there's a block[j] > B for j < first_min, then B < blocks[j]
    # and repeat(B, k) < L at position j
    
    # Correct approach:
    # B must satisfy: for the first i where B != blocks[i], B > blocks[i]
    # This means: B >= blocks[0], and if B == blocks[0], then B >= blocks[1], etc.
    # Until at some point B > blocks[i]
    
    # So: B must be >= all blocks[0..i-1] and > blocks[i] for some i
    # Minimum B = min over i of (max(blocks[0..i]) + 1 if we can make B > blocks[i], 
    #                            but B >= all earlier)
    
    # Simplified: B = max(blocks[0..i]) + 1 for some i where blocks[i] < max(blocks[0..i])
    #             or B = blocks[i] + 1 if blocks[i] == max(blocks[0..i])
    
    # Even simpler: 
    # Let prefix_max[i] = max(blocks[0..i])
    # For each i, try B = prefix_max[i] + 1
    # Check if this B works (i.e., repeat(B, k) > L)
    # Return minimum valid B
    
    # Most efficient:
    # B must be at least max(blocks) to ensure B >= all blocks
    # If B = max(blocks), then repeat(B, k) >= L (might be equal)
    # If B = max(blocks) + 1, then repeat(B, k) > L (strictly greater)
    
    # So minimum B = max(blocks) + 1, unless max(blocks) = "999...9"
    
    max_block = max(blocks)
    
    # Try B = max_block + 1
    try:
        B_candidate = str(int(max_block) + 1).zfill(N)
        if len(B_candidate) > N:
            # Overflow, impossible with this length
            return ""
        
        # Verify: repeat(B_candidate, k) > L
        # Since B_candidate > max_block >= all blocks, repeat(B_candidate, k) > L
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
    
    # For repeat(B, k) < R, at first position where B != blocks[i], need B < blocks[i]
    # Maximum B = min(blocks) - 1 (if valid)
    
    min_block = min(blocks)
    
    try:
        B_candidate = str(int(min_block) - 1).zfill(N)
        if len(B_candidate) > N or (len(B_candidate) < N and B_candidate[0] != '0'):
            # Check if it's still N digits (might have leading zeros which is fine)
            pass
        
        # Ensure it's still N digits
        if int(B_candidate) < 10**(N-1):
            # Too small, not an N-digit number
            return ""
        
        return B_candidate
    except:
        return ""

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
