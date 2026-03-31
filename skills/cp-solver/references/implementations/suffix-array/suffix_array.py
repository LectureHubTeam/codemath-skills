"""
Suffix Array + LCP Array
Complexity: O(N log N) build suffix array, O(N) build LCP
Dùng cho: string matching, longest common substring, pattern queries

sa[i]  = starting index của suffix thứ i theo thứ tự lexicographic
lcp[i] = LCP của sa[i] và sa[i-1]
"""
import sys
input = sys.stdin.readline


def build_suffix_array(s):
    """
    Build suffix array sử dụng prefix doubling — O(N log² N).
    Đủ nhanh cho N ≤ 10^5 trong Python.
    Trả về sa: list length N, sa[i] = starting index của suffix thứ i
    """
    n = len(s)
    sa = sorted(range(n), key=lambda i: s[i:])  # Initial sort O(N² log N) cho nhỏ

    # Prefix doubling O(N log² N)
    rank = [0] * n
    tmp  = [0] * n

    # Khởi tạo rank theo ký tự đầu
    rank = [ord(c) for c in s]

    k = 1
    while k < n:
        def key(i):
            return (rank[i], rank[i + k] if i + k < n else -1)

        sa = sorted(range(n), key=key)

        tmp[sa[0]] = 0
        for i in range(1, n):
            tmp[sa[i]] = tmp[sa[i-1]]
            if key(sa[i]) != key(sa[i-1]):
                tmp[sa[i]] += 1
        rank = tmp[:]

        if rank[sa[n-1]] == n - 1:
            break  # All ranks distinct, done
        k *= 2

    return sa


def build_lcp_array(s, sa):
    """
    Build LCP array sử dụng Kasai's algorithm — O(N).
    lcp[i] = LCP của suffix sa[i] và sa[i-1] (với lcp[0] = 0)
    """
    n = len(s)
    rank = [0] * n
    for i, idx in enumerate(sa):
        rank[idx] = i

    lcp = [0] * n
    h = 0
    for i in range(n):
        if rank[i] > 0:
            j = sa[rank[i] - 1]
            while i + h < n and j + h < n and s[i+h] == s[j+h]:
                h += 1
            lcp[rank[i]] = h
            if h > 0:
                h -= 1

    return lcp


def find_pattern(s, pattern, sa):
    """
    Tìm tất cả vị trí xuất hiện của pattern trong s — O(M log N).
    Trả về list các starting indices (sorted).
    """
    import bisect
    n, m = len(s), len(pattern)

    lo = bisect.bisect_left(sa, 0, key=lambda i: s[i:i+m] >= pattern)
    hi = bisect.bisect_right(sa, 0, key=lambda i: s[i:i+m] <= pattern)

    # Dùng binary search thủ công vì tinh tế hơn
    def lower():
        l, r = 0, n
        while l < r:
            mid = (l + r) // 2
            if s[sa[mid]:sa[mid]+m] < pattern:
                l = mid + 1
            else:
                r = mid
        return l

    def upper():
        l, r = 0, n
        while l < r:
            mid = (l + r) // 2
            if s[sa[mid]:sa[mid]+m] <= pattern:
                l = mid + 1
            else:
                r = mid
        return l

    lo, hi = lower(), upper()
    return sorted(sa[lo:hi])


def longest_common_substring(s, t):
    """Tìm LCS của 2 xâu s và t — O((N+M) log(N+M))."""
    combined = s + '#' + t   # '#' nhỏ hơn mọi ký tự thường
    n, m = len(s), len(t)
    N = len(combined)

    sa  = build_suffix_array(combined)
    lcp = build_lcp_array(combined, sa)

    best = 0
    for i in range(1, N):
        # LCP giữa sa[i] và sa[i-1]
        # Nếu hai suffix từ hai xâu khác nhau
        p = sa[i-1]
        q = sa[i]
        if (p < n) != (q < n):   # Một trong s, một trong t
            best = max(best, lcp[i])

    return best


# ===== USAGE EXAMPLE =====
def solve():
    s = input().strip()
    sa = build_suffix_array(s)
    lcp = build_lcp_array(s, sa)

    # In suffix array
    for i in sa:
        print(i, s[i:])

    # LCP
    print("LCP:", lcp)


if __name__ == '__main__':
    solve()
