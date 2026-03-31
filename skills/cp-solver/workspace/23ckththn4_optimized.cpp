#include <iostream>
#include <vector>
#include <algorithm>
using namespace std;

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(nullptr);
    
    int N, K;
    cin >> N >> K;
    
    vector<int> A(N + 1);
    vector<int> values;
    for (int i = 1; i <= N; i++) {
        cin >> A[i];
        values.push_back(A[i]);
    }
    
    // Coordinate compression
    sort(values.begin(), values.end());
    values.erase(unique(values.begin(), values.end()), values.end());
    
    auto get_id = [&](int v) {
        return lower_bound(values.begin(), values.end(), v) - values.begin();
    };
    
    int M = values.size();
    
    // positions[v] = list of positions where value v appears
    vector<vector<int>> positions(M);
    for (int i = 1; i <= N; i++) {
        positions[get_id(A[i])].push_back(i);
    }
    
    int max_pairs = K / 2;
    const int INF = 1e9;
    
    // dp[i] = minimum ending position for current number of pairs starting from i
    vector<int> dp(N + 2);
    for (int i = 1; i <= N + 1; i++) dp[i] = i - 1;
    
    int ans = (K >= 1 && N > 0) ? 1 : 0;
    
    for (int p = 1; p <= max_pairs; p++) {
        vector<int> new_dp(N + 2, INF);
        for (int i = N; i >= 1; i--) {
            // Option 1: skip position i
            new_dp[i] = new_dp[i + 1];
            
            // Option 2: use A[i] as left of outermost pair
            int prev_end = dp[i + 1];
            if (prev_end <= N) {
                int v = get_id(A[i]);
                const vector<int>& posList = positions[v];
                // Binary search for first position > prev_end
                auto idx = upper_bound(posList.begin(), posList.end(), prev_end);
                if (idx != posList.end() && *idx <= N) {
                    new_dp[i] = min(new_dp[i], *idx);
                }
            }
        }
        dp = new_dp;
        
        if (dp[1] <= N) {
            if (2 * p <= K) ans = max(ans, 2 * p);
            if (2 * p + 1 <= K && N > 2 * p) ans = max(ans, 2 * p + 1);
        }
    }
    
    cout << ans << endl;
    return 0;
}
