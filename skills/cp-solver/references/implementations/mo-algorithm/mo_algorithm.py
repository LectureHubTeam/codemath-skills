"""
Mo's Algorithm — Offline Range Queries
Complexity: O((N+Q)√N)
Dùng khi: offline queries (không có update), N,Q ≤ 10^5

Template: đếm distinct elements trong [l, r]
Customize: thay add() và remove() cho bài khác

Usage:
    mo = MoSolver(n, a)
    mo.add_query(l, r)      # 0-indexed, inclusive
    results = mo.solve()    # trả về list kết quả theo thứ tự queries
"""
import sys
from math import isqrt
input = sys.stdin.readline


class MoSolver:
    def __init__(self, n, a):
        self.n = n
        self.a = a
        self.queries = []
        self.block = max(1, isqrt(n))

        # State — customize cho bài cụ thể
        max_val = max(a) + 1 if a else 1
        self.cnt = [0] * max_val
        self.cur_answer = 0   # = số distinct elements hiện tại

    def add_query(self, l, r, idx=None):
        """Add query (l, r) — 0-indexed, inclusive."""
        if idx is None:
            idx = len(self.queries)
        self.queries.append((l, r, idx))

    def _add(self, x):
        """Thêm phần tử x vào window — customize ở đây."""
        if self.cnt[x] == 0:
            self.cur_answer += 1
        self.cnt[x] += 1

    def _remove(self, x):
        """Bỏ phần tử x khỏi window — customize ở đây."""
        self.cnt[x] -= 1
        if self.cnt[x] == 0:
            self.cur_answer -= 1

    def solve(self):
        """Trả về list kết quả, đúng thứ tự query ban đầu."""
        block = self.block
        a = self.a

        # Odd-even sort
        def sort_key(q):
            l, r, idx = q
            bl = l // block
            return (bl, r if bl % 2 == 0 else -r)

        sorted_queries = sorted(self.queries, key=sort_key)
        answers = [0] * len(self.queries)

        L, R = 0, -1
        for ql, qr, orig_idx in sorted_queries:
            while R < qr: R += 1; self._add(a[R])
            while L > ql: L -= 1; self._add(a[L])
            while R > qr: self._remove(a[R]); R -= 1
            while L < ql: self._remove(a[L]); L += 1
            answers[orig_idx] = self.cur_answer

        return answers


# ===== USAGE EXAMPLE =====
def solve():
    n, q = map(int, input().split())
    a = list(map(int, input().split()))

    mo = MoSolver(n, a)
    for i in range(q):
        l, r = map(int, input().split())
        mo.add_query(l-1, r-1, i)   # 1-indexed → 0-indexed

    results = mo.solve()
    sys.stdout.write('\n'.join(map(str, results)) + '\n')


if __name__ == '__main__':
    import sys
    input = sys.stdin.readline
    solve()
