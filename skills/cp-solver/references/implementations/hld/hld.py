"""
Heavy-Light Decomposition (HLD) — Path queries trên cây
Complexity: O(N log N) preprocessing, O(log² N) per query
Dùng khi: path queries với updates, N ≤ 10^5

Đây là skeleton — kết hợp với Segment Tree để query path sum/max/min.
"""
import sys
from collections import defaultdict
sys.setrecursionlimit(300000)
input = sys.stdin.readline


class HLD:
    def __init__(self, n, root=0):
        self.n = n
        self.root = root
        self.adj = defaultdict(list)

        # HLD arrays
        self.parent   = [-1] * n
        self.depth    = [0]  * n
        self.subtree  = [1]  * n
        self.heavy    = [-1] * n   # heavy child của mỗi node
        self.head     = [0]  * n   # đầu của chain chứa node này
        self.pos      = [0]  * n   # vị trí trong segment tree
        self.pos_node = [0]  * n   # node tại vị trí pos (inverse)
        self._cur_pos = 0

    def add_edge(self, u, v):
        self.adj[u].append(v)
        self.adj[v].append(u)

    def build(self):
        self._dfs_size(self.root, -1)
        self._dfs_hld(self.root, self.root)

    def _dfs_size(self, u, p):
        """Tính subtree size + tìm heavy child — iterative để tránh RecursionError."""
        stack = [(u, p, False)]
        order = []
        while stack:
            node, par, done = stack.pop()
            if done:
                for v in self.adj[node]:
                    if v != self.parent[node]:
                        self.subtree[node] += self.subtree[v]
                        if self.heavy[node] == -1 or self.subtree[v] > self.subtree[self.heavy[node]]:
                            self.heavy[node] = v
            else:
                self.parent[node] = par
                stack.append((node, par, True))
                for v in self.adj[node]:
                    if v != par:
                        self.depth[v] = self.depth[node] + 1
                        stack.append((v, node, False))

    def _dfs_hld(self, u, h):
        """Phân rã thành heavy chains — iterative."""
        stack = [(u, h)]
        while stack:
            node, head = stack.pop()
            self.head[node] = head
            self.pos[node] = self._cur_pos
            self.pos_node[self._cur_pos] = node
            self._cur_pos += 1

            # Xử lý light children trước (đẩy vào stack trước)
            for v in self.adj[node]:
                if v != self.parent[node] and v != self.heavy[node]:
                    stack.append((v, v))  # Light child → chain mới

            # Heavy child cuối (LIFO → xử lý tiếp theo)
            if self.heavy[node] != -1:
                stack.append((self.heavy[node], head))

    def lca(self, u, v):
        """LCA sử dụng HLD — O(log N)."""
        while self.head[u] != self.head[v]:
            if self.depth[self.head[u]] < self.depth[self.head[v]]:
                u, v = v, u
            u = self.parent[self.head[u]]
        return u if self.depth[u] < self.depth[v] else v

    def path_query(self, u, v, seg_query):
        """
        Query trên path u→v bằng seg_query(l, r).
        seg_query: function(pos_l, pos_r) → result
        Cần merge result phù hợp với loại query (sum, max, min...).
        """
        result = 0  # Thay identity phù hợp
        while self.head[u] != self.head[v]:
            if self.depth[self.head[u]] < self.depth[self.head[v]]:
                u, v = v, u
            result += seg_query(self.pos[self.head[u]], self.pos[u])   # merge
            u = self.parent[self.head[u]]
        if self.depth[u] > self.depth[v]:
            u, v = v, u
        result += seg_query(self.pos[u], self.pos[v])  # merge
        return result


# ===== USAGE EXAMPLE =====
def solve():
    n, q = map(int, input().split())
    values = list(map(int, input().split()))

    hld = HLD(n, root=0)
    for _ in range(n - 1):
        u, v = map(int, input().split())
        hld.add_edge(u-1, v-1)   # 1-indexed

    hld.build()

    # Tạo Segment Tree theo pos (DFS order của HLD)
    # Đây là nơi plug in SegmentTree từ segment_tree.py
    # from segment_tree import SegmentTree
    # reordered = [values[hld.pos_node[i]] for i in range(n)]
    # st = SegmentTree(n)
    # st.build(reordered)

    # Query
    # for _ in range(q):
    #     u, v = map(int, input().split())
    #     print(hld.path_query(u-1, v-1, st.query))


if __name__ == '__main__':
    solve()
