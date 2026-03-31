"""
Segment Tree — Generic (Point Update, Range Query)
Supports: sum, min, max, GCD, XOR — any associative operation
Complexity: O(N) build, O(log N) update/query

Usage:
    st = SegmentTree(n)                           # range sum
    st = SegmentTree(n, min, float('inf'))        # range min
    st = SegmentTree(n, max, float('-inf'))       # range max
    st.build(a)         # build from list (0-indexed)
    st.update(i, val)   # set a[i] = val
    st.query(l, r)      # query [l, r] (0-indexed, inclusive)
"""
import sys
input = sys.stdin.readline


class SegmentTree:
    def __init__(self, n, op=lambda a, b: a + b, identity=0):
        self.n = n
        self.op = op
        self.identity = identity
        self.tree = [identity] * (4 * n)

    def build(self, a, node=1, l=0, r=None):
        if r is None: r = self.n - 1
        if l == r:
            self.tree[node] = a[l]
            return
        mid = (l + r) // 2
        self.build(a, 2*node, l, mid)
        self.build(a, 2*node+1, mid+1, r)
        self.tree[node] = self.op(self.tree[2*node], self.tree[2*node+1])

    def update(self, idx, val, node=1, l=0, r=None):
        if r is None: r = self.n - 1
        if l == r:
            self.tree[node] = val
            return
        mid = (l + r) // 2
        if idx <= mid:
            self.update(idx, val, 2*node, l, mid)
        else:
            self.update(idx, val, 2*node+1, mid+1, r)
        self.tree[node] = self.op(self.tree[2*node], self.tree[2*node+1])

    def query(self, ql, qr, node=1, l=0, r=None):
        if r is None: r = self.n - 1
        if qr < l or r < ql:
            return self.identity
        if ql <= l and r <= qr:
            return self.tree[node]
        mid = (l + r) // 2
        return self.op(
            self.query(ql, qr, 2*node, l, mid),
            self.query(ql, qr, 2*node+1, mid+1, r)
        )


# ===== USAGE EXAMPLE =====
def solve():
    import sys
    sys.setrecursionlimit(400000)
    input = sys.stdin.readline

    n, q = map(int, input().split())
    a = list(map(int, input().split()))

    st = SegmentTree(n)          # default: range sum
    st.build(a)

    out = []
    for _ in range(q):
        t, l, r = map(int, input().split())
        if t == 1:
            st.update(l - 1, r)   # 1-indexed → 0-indexed
        else:
            out.append(st.query(l - 1, r - 1))

    sys.stdout.write('\n'.join(map(str, out)) + '\n')


if __name__ == '__main__':
    solve()
