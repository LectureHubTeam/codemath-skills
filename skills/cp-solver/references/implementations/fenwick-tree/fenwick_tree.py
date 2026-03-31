"""
Fenwick Tree (Binary Indexed Tree) — Point Update, Prefix/Range Query
Complexity: O(N) build, O(log N) update/query
Chỉ hỗ trợ phép toán có nghịch đảo: sum, XOR

Usage:
    ft = FenwickTree(n)          # zero-initialized
    ft = FenwickTree(n, a)       # build from list a (0-indexed)
    ft.update(i, delta)          # a[i] += delta (0-indexed)
    ft.query(i)                  # prefix sum [0..i]
    ft.range_query(l, r)         # range sum [l..r] (0-indexed, inclusive)
"""
import sys
input = sys.stdin.readline


class FenwickTree:
    def __init__(self, n, a=None):
        self.n = n
        self.tree = [0] * (n + 1)
        if a:
            for i, v in enumerate(a):
                self.update(i, v)

    def update(self, i, delta):     # 0-indexed
        i += 1
        while i <= self.n:
            self.tree[i] += delta
            i += i & (-i)

    def query(self, i):             # prefix sum [0..i], 0-indexed
        i += 1
        s = 0
        while i > 0:
            s += self.tree[i]
            i -= i & (-i)
        return s

    def range_query(self, l, r):    # [l..r], 0-indexed, inclusive
        if l == 0:
            return self.query(r)
        return self.query(r) - self.query(l - 1)


class FenwickTree2D:
    """Fenwick Tree 2D — Point update, prefix/range sum queries on matrix."""
    def __init__(self, n, m):
        self.n = n
        self.m = m
        self.tree = [[0] * (m + 1) for _ in range(n + 1)]

    def update(self, x, y, delta):   # 0-indexed
        x += 1
        while x <= self.n:
            y1 = y + 1
            while y1 <= self.m:
                self.tree[x][y1] += delta
                y1 += y1 & (-y1)
            x += x & (-x)

    def query(self, x, y):           # prefix sum [0..x][0..y]
        x += 1
        s = 0
        while x > 0:
            y1 = y + 1
            while y1 > 0:
                s += self.tree[x][y1]
                y1 -= y1 & (-y1)
            x -= x & (-x)
        return s

    def range_query(self, x1, y1, x2, y2):  # [x1..x2][y1..y2], 0-indexed
        ans = self.query(x2, y2)
        if x1 > 0: ans -= self.query(x1-1, y2)
        if y1 > 0: ans -= self.query(x2, y1-1)
        if x1 > 0 and y1 > 0: ans += self.query(x1-1, y1-1)
        return ans


# ===== USAGE EXAMPLE =====
def solve():
    n, q = map(int, input().split())
    a = list(map(int, input().split()))
    ft = FenwickTree(n, a)

    out = []
    for _ in range(q):
        t, *args = map(int, input().split())
        if t == 1:
            i, val = args
            ft.update(i-1, val)           # 1-indexed
        else:
            l, r = args
            out.append(ft.range_query(l-1, r-1))  # 1-indexed

    sys.stdout.write('\n'.join(map(str, out)) + '\n')


if __name__ == '__main__':
    import sys
    input = sys.stdin.readline
    solve()
