from bisect import bisect_right
import sys

def solve():
    input = sys.stdin.readline
    
    N, K = map(int, input().split())
    A = [0] + list(map(int, input().split()))  # 1-indexed
    
    # Precompute positions for each value
    positions = {}
    for i in range(1, N + 1):
        if A[i] not in positions:
            positions[A[i]] = []
        positions[A[i]].append(i)
    
    def next_occurrence(pos, v):
        """Smallest index k > pos such that A[k] = v, or None if no such k."""
        if v not in positions:
            return None
        idx = bisect_right(positions[v], pos)
        if idx < len(positions[v]):
            return positions[v][idx]
        return None
    
    INF = N + 1
    
    # dp[i] = minimum ending position j such that current number of pairs can be formed starting from i
    # Size: N + 2 to handle indices 1 to N+1
    dp = list(range(N + 2))  # Base case: 0 pairs, dp[i] = i - 1, but we'll adjust
    for i in range(N + 2):
        dp[i] = i - 1
    
    # Track the maximum length found so far
    ans = 0
    
    # Check L = 1 (odd, p = 0) - single element is always a palindrome
    if K >= 1 and N > 0:
        ans = 1
    
    max_pairs = K // 2
    
    for p in range(1, max_pairs + 1):
        new_dp = [INF] * (N + 2)
        for i in range(N, 0, -1):
            # Option 1: skip position i
            new_dp[i] = new_dp[i + 1]
            
            # Option 2: use A[i] as left of outermost pair
            # Find matching element after the inner p-1 pairs end
            prev_end = dp[i + 1]
            if prev_end <= N:
                k = next_occurrence(prev_end, A[i])
                if k is not None and k <= N:
                    new_dp[i] = min(new_dp[i], k)
        dp = new_dp
        
        # Check if p pairs can be formed
        if dp[1] <= N:
            # Even length: 2 * p
            if 2 * p <= K:
                ans = max(ans, 2 * p)
            # Odd length: 2 * p + 1 (need one more element for middle)
            if 2 * p + 1 <= K and N > 2 * p:
                ans = max(ans, 2 * p + 1)
    
    print(ans)

if __name__ == "__main__":
    solve()
