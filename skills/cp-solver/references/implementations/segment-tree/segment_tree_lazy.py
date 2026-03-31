"""
Segment Tree với Lazy Propagation — Range Add, Range Sum
Complexity: O(N) build, O(log N) update/query

Usage:
    st = SegmentTreeLazy(n, a)  # build from list a (0-indexed)
    st.update(l, r, val)        # a[l..r] += val (0-indexed, inclusive)
    st.query(l, r)              # sum(a[l..r]) (0-indexed, inclusive)
"""
import sys
input = sys.stdin.readline


class SegmentTreeLazy:
    def __init__(self, n, a=None):
        self.n = n
        self.tree = [0] * (4 * n)
        self.lazy = [0] * (4 * n)
        if a:
            self._build(a, 1, 0, n - 1)

    def _build(self, a, node, l, r):
        if l == r:
            self.tree[node] = a[l]
            return
        mid = (l + r) // 2
        self._build(a, 2*node, l, mid)
        self._build(a, 2*node+1, mid+1, r)
        self.tree[node] = self.tree[2*node] + self.tree[2*node+1]

    def _push(self, node, l, r):
        if self.lazy[node]:
            mid = (l + r) // 2
            val = self.lazy[node]
            # Apply to children
            self.lazy[2*node]   += val
            self.lazy[2*node+1] += val
            self.tree[2*node]   += val * (mid - l + 1)
            self.tree[2*node+1] += val * (r - mid)
            self.lazy[node] = 0

    def _update(self, node, l, r, ql, qr, val):
        if qr < l or r < ql:
            return
        if ql <= l and r <= qr:
            self.lazy[node] += val
            self.tree[node] += val * (r - l + 1)
            return
        self._push(node, l, r)
        mid = (l + r) // 2
        self._update(2*node, l, mid, ql, qr, val)
        self._update(2*node+1, mid+1, r, ql, qr, val)
        self.tree[node] = self.tree[2*node] + self.tree[2*node+1]

    def _query(self, node, l, r, ql, qr):
        if qr < l or r < ql:
            return 0
        if ql <= l and r <= qr:
            return self.tree[node]
        self._push(node, l, r)
        mid = (l + r) // 2
        return (self._query(2*node, l, mid, ql, qr) +
                self._query(2*node+1, mid+1, r, ql, qr))

    def update(self, l, r, val):    # 0-indexed, inclusive
        self._update(1, 0, self.n-1, l, r, val)

    def query(self, l, r):          # 0-indexed, inclusive
        return self._query(1, 0, self.n-1, l, r)


# ===== USAGE EXAMPLE =====
def solve():
    import sys
    sys.setrecursionlimit(400000)
    input = sys.stdin.readline

    n, q = map(int, input().split())
    a = list(map(int, input().split()))
    st = SegmentTreeLazy(n, a)

    out = []
    for _ in range(q):
        line = list(map(int, input().split()))
        if line[0] == 1:
            _, l, r, val = line
            st.update(l-1, r-1, val)   # 1-indexed
        else:
            _, l, r = line
            out.append(st.query(l-1, r-1))

    sys.stdout.write('\n'.join(map(str, out)) + '\n')


if __name__ == '__main__':
    solve()
