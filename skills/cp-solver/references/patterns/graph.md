# Graph Algorithms Patterns

## 1. Graph Representation

### Adjacency List

```cpp
vector<int> adj[MAXN];  // Unweighted
vector<pair<int,int>> adj[MAXN];  // Weighted: {neighbor, weight}

// Add edge
void add_edge(int u, int v) {
    adj[u].push_back(v);
    adj[v].push_back(u);  // For undirected
}

void add_edge(int u, int v, int w) {
    adj[u].push_back({v, w});
    adj[v].push_back({u, w});  // For undirected
}
```

---

## 2. BFS - Breadth First Search

### Shortest Path (Unweighted)

```cpp
vector<int> bfs(int start, vector<vector<int>>& adj, int n) {
    vector<int> dist(n + 1, -1);
    queue<int> q;
    
    dist[start] = 0;
    q.push(start);
    
    while (!q.empty()) {
        int u = q.front(); q.pop();
        for (int v : adj[u]) {
            if (dist[v] == -1) {
                dist[v] = dist[u] + 1;
                q.push(v);
            }
        }
    }
    return dist;
}

// Usage
vector<int> dist = bfs(1, adj, n);
cout << "Distance to node " << k << ": " << dist[k] << endl;
```

### BFS with Path Reconstruction

```cpp
vector<int> bfs_path(int start, int end, vector<vector<int>>& adj, int n) {
    vector<int> dist(n + 1, -1), parent(n + 1, -1);
    queue<int> q;
    
    dist[start] = 0;
    q.push(start);
    
    while (!q.empty()) {
        int u = q.front(); q.pop();
        if (u == end) break;
        
        for (int v : adj[u]) {
            if (dist[v] == -1) {
                dist[v] = dist[u] + 1;
                parent[v] = u;
                q.push(v);
            }
        }
    }
    
    // Reconstruct path
    if (dist[end] == -1) return {};  // No path
    
    vector<int> path;
    for (int v = end; v != -1; v = parent[v])
        path.push_back(v);
    reverse(path.begin(), path.end());
    return path;
}
```

---

## 3. DFS - Depth First Search

### Basic DFS

```cpp
vector<int> adj[MAXN];
bool visited[MAXN];

void dfs(int u) {
    visited[u] = true;
    for (int v : adj[u]) {
        if (!visited[v]) {
            dfs(v);
        }
    }
}

// Count connected components
int count_components(int n) {
    int count = 0;
    memset(visited, false, sizeof(visited));
    for (int i = 1; i <= n; i++) {
        if (!visited[i]) {
            count++;
            dfs(i);
        }
    }
    return count;
}
```

### DFS with Discovery/Finish Times

```cpp
int timer;
int tin[MAXN], tout[MAXN];

void dfs(int u, int p = -1) {
    tin[u] = ++timer;
    for (int v : adj[u]) {
        if (v != p) {
            dfs(v, u);
        }
    }
    tout[u] = ++timer;
}

// Check if u is ancestor of v
bool is_ancestor(int u, int v) {
    return tin[u] <= tin[v] && tout[u] >= tout[v];
}
```

---

## 4. Dijkstra - Shortest Path (Weighted)

### Basic Dijkstra (O(E log V))

```cpp
vector<pair<int,int>> adj[MAXN];  // {neighbor, weight}

vector<long long> dijkstra(int start, int n) {
    vector<long long> dist(n + 1, LLONG_MAX);
    priority_queue<pair<long long,int>, vector<pair<long long,int>>, greater<>> pq;
    
    dist[start] = 0;
    pq.push({0, start});
    
    while (!pq.empty()) {
        auto [d, u] = pq.top(); pq.pop();
        if (d > dist[u]) continue;
        
        for (auto [v, w] : adj[u]) {
            if (dist[u] + w < dist[v]) {
                dist[v] = dist[u] + w;
                pq.push({dist[v], v});
            }
        }
    }
    return dist;
}
```

### Dijkstra with Path Reconstruction

```cpp
vector<long long> dijkstra_path(int start, int end, int n, vector<int>& path) {
    vector<long long> dist(n + 1, LLONG_MAX);
    vector<int> parent(n + 1, -1);
    priority_queue<pair<long long,int>, vector<pair<long long,int>>, greater<>> pq;
    
    dist[start] = 0;
    pq.push({0, start});
    
    while (!pq.empty()) {
        auto [d, u] = pq.top(); pq.pop();
        if (u == end) break;
        if (d > dist[u]) continue;
        
        for (auto [v, w] : adj[u]) {
            if (dist[u] + w < dist[v]) {
                dist[v] = dist[u] + w;
                parent[v] = u;
                pq.push({dist[v], v});
            }
        }
    }
    
    // Reconstruct path
    if (dist[end] == LLONG_MAX) return {};
    
    for (int v = end; v != -1; v = parent[v])
        path.push_back(v);
    reverse(path.begin(), path.end());
    
    return dist;
}
```

---

## 5. Bellman-Ford (Handles Negative Edges)

```cpp
struct Edge {
    int u, v, w;
};

vector<long long> bellman_ford(int start, int n, vector<Edge>& edges) {
    vector<long long> dist(n + 1, LLONG_MAX);
    dist[start] = 0;
    
    // Relax edges n-1 times
    for (int i = 0; i < n - 1; i++) {
        for (auto& e : edges) {
            if (dist[e.u] != LLONG_MAX && dist[e.u] + e.w < dist[e.v]) {
                dist[e.v] = dist[e.u] + e.w;
            }
        }
    }
    
    // Check for negative cycles
    for (auto& e : edges) {
        if (dist[e.u] != LLONG_MAX && dist[e.u] + e.w < dist[e.v]) {
            // Negative cycle detected
            return {};
        }
    }
    
    return dist;
}
```

---

## 6. Floyd-Warshall (All Pairs Shortest Path)

```cpp
const long long INF = 1e18;

vector<vector<long long>> floyd_warshall(int n, vector<vector<int>>& adj) {
    vector<vector<long long>> dist(n + 1, vector<long long>(n + 1, INF));
    
    // Initialize
    for (int i = 1; i <= n; i++) {
        dist[i][i] = 0;
        for (auto [v, w] : adj[i])
            dist[i][v] = w;
    }
    
    // Floyd-Warshall
    for (int k = 1; k <= n; k++)
        for (int i = 1; i <= n; i++)
            for (int j = 1; j <= n; j++)
                if (dist[i][k] != INF && dist[k][j] != INF)
                    dist[i][j] = min(dist[i][j], dist[i][k] + dist[k][j]);
    
    return dist;
}
```

---

## 7. Minimum Spanning Tree

### Kruskal's Algorithm (O(E log E))

```cpp
struct Edge {
    int u, v, w;
    bool operator<(const Edge& other) const {
        return w < other.w;
    }
};

struct DSU {
    vector<int> parent, rank;
    DSU(int n) {
        parent.resize(n + 1);
        iota(parent.begin(), parent.end(), 0);
        rank.assign(n + 1, 0);
    }
    int find(int x) {
        if (parent[x] != x) parent[x] = find(parent[x]);
        return parent[x];
    }
    bool unite(int x, int y) {
        x = find(x), y = find(y);
        if (x == y) return false;
        if (rank[x] < rank[y]) swap(x, y);
        parent[y] = x;
        if (rank[x] == rank[y]) rank[x]++;
        return true;
    }
};

long long kruskal(int n, vector<Edge>& edges) {
    sort(edges.begin(), edges.end());
    DSU dsu(n);
    long long mst_weight = 0;
    int edges_count = 0;
    
    for (auto& e : edges) {
        if (dsu.unite(e.u, e.v)) {
            mst_weight += e.w;
            edges_count++;
            if (edges_count == n - 1) break;
        }
    }
    
    return mst_weight;
}
```

### Prim's Algorithm (O(E log V))

```cpp
long long prim(int start, int n, vector<vector<pair<int,int>>>& adj) {
    vector<bool> visited(n + 1, false);
    priority_queue<pair<int,int>, vector<pair<int,int>>, greater<>> pq;
    long long mst_weight = 0;
    
    pq.push({0, start});
    
    while (!pq.empty() && mst_weight < LLONG_MAX) {
        auto [w, u] = pq.top(); pq.pop();
        if (visited[u]) continue;
        
        visited[u] = true;
        mst_weight += w;
        
        for (auto [v, weight] : adj[u]) {
            if (!visited[v]) {
                pq.push({weight, v});
            }
        }
    }
    
    return mst_weight;
}
```

---

## 8. Topological Sort

### Kahn's Algorithm (BFS-based)

```cpp
vector<int> topological_sort(int n, vector<vector<int>>& adj) {
    vector<int> indegree(n + 1, 0);
    for (int u = 1; u <= n; u++)
        for (int v : adj[u])
            indegree[v]++;
    
    queue<int> q;
    for (int i = 1; i <= n; i++)
        if (indegree[i] == 0) q.push(i);
    
    vector<int> result;
    while (!q.empty()) {
        int u = q.front(); q.pop();
        result.push_back(u);
        
        for (int v : adj[u]) {
            indegree[v]--;
            if (indegree[v] == 0) q.push(v);
        }
    }
    
    if (result.size() != n) return {};  // Cycle detected
    return result;
}
```

### DFS-based

```cpp
vector<int> topological_sort_dfs(int n, vector<vector<int>>& adj) {
    vector<int> result;
    vector<bool> visited(n + 1, false), rec_stack(n + 1, false);
    
    function<bool(int)> dfs = [&](int u) -> bool {
        visited[u] = true;
        rec_stack[u] = true;
        
        for (int v : adj[u]) {
            if (rec_stack[v]) return true;  // Cycle
            if (!visited[v] && dfs(v)) return true;
        }
        
        rec_stack[u] = false;
        result.push_back(u);
        return false;
    };
    
    for (int i = 1; i <= n; i++) {
        if (!visited[i] && dfs(i)) return {};  // Cycle
    }
    
    reverse(result.begin(), result.end());
    return result;
}
```

---

## 9. LCA - Lowest Common Ancestor

### Binary Lifting (O(N log N) preprocessing, O(log N) query)

```cpp
const int LOG = 20;
vector<int> adj[MAXN];
int up[MAXN][LOG], depth[MAXN];

void dfs(int u, int p, int d) {
    depth[u] = d;
    up[u][0] = p;
    for (int i = 1; i < LOG; i++)
        up[u][i] = up[up[u][i-1]][i-1];
    
    for (int v : adj[u]) {
        if (v != p) dfs(v, u, d + 1);
    }
}

void preprocess(int root, int n) {
    dfs(root, root, 0);
}

int lca(int u, int v) {
    if (depth[u] < depth[v]) swap(u, v);
    
    // Bring u to same depth as v
    for (int i = LOG - 1; i >= 0; i--)
        if (depth[u] - (1 << i) >= depth[v])
            u = up[u][i];
    
    if (u == v) return u;
    
    // Binary lift until just below LCA
    for (int i = LOG - 1; i >= 0; i--)
        if (up[u][i] != up[v][i]) {
            u = up[u][i];
            v = up[v][i];
        }
    
    return up[u][0];
}

int distance(int u, int v) {
    return depth[u] + depth[v] - 2 * depth[lca(u, v)];
}
```

---

## Common Graph Problems

| Problem | Algorithm | Complexity |
|---------|-----------|------------|
| Shortest path (unweighted) | BFS | O(V+E) |
| Shortest path (weighted, non-negative) | Dijkstra | O(E log V) |
| Shortest path (with negative edges) | Bellman-Ford | O(VE) |
| All pairs shortest path | Floyd-Warshall | O(V³) |
| Minimum Spanning Tree | Kruskal/Prim | O(E log E) |
| Topological sort | Kahn/DFS | O(V+E) |
| LCA queries | Binary Lifting | O(log N) per query |
| Connected components | DFS/BFS/DSU | O(V+E) |

---

## Next Steps

- → Practice graph problems on CMOJ
- → Learn [04-advanced-algorithms.md](04-advanced-algorithms.md) for HLD, Centroid Decomposition
- → Combine with [patterns/dp.md](dp.md) for Tree DP
