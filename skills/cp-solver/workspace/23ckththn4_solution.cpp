#include <iostream>
#include <vector>
#include <map>
#include <algorithm>
using namespace std;

const int INF = 1e9;

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(nullptr);
    
    int N, K;
    cin >> N >> K;
    
    vector<int> A(N + 1);
    for (int i = 1; i <= N; i++) {
        cin >> A[i];
    }
    
    // Precompute positions for each value
    map<int, vector<int>> positions;
    for (int i = 1; i <= N; i++) {
        positions[A[i]].push_back(i);
    }
    
    // Function to find next occurrence
    auto next_occurrence = [&](int pos, int v) -> int {
        auto it = positions.find(v);
        if (it == positions.end()) return -1;
        const vector<int>& posList = it->second;
        auto idx = upper_bound(posList.begin(), posList.end(), pos);
        if (idx == posList.end()) return -1;
        return *idx;
    };
    
    int max_pairs = K / 2;
    
    // dp[i] = minimum ending position for current number of pairs starting from i
    vector<int> dp(N + 2);
    for (int i = 1; i <= N + 1; i++) {
        dp[i] = i - 1;
    }
    
    int ans = 0;
    if (K >= 1 && N > 0) {
        ans = 1;
    }
    
    for (int p = 1; p <= max_pairs; p++) {
        vector<int> new_dp(N + 2, INF);
        for (int i = N; i >= 1; i--) {
            // Option 1: skip position i
            new_dp[i] = new_dp[i + 1];
            
            // Option 2: use A[i] as left of outermost pair
            int prev_end = dp[i + 1];
            if (prev_end <= N) {
                int k = next_occurrence(prev_end, A[i]);
                if (k != -1 && k <= N) {
                    new_dp[i] = min(new_dp[i], k);
                }
            }
        }
        dp = new_dp;
        
        // Check if p pairs can be formed
        if (dp[1] <= N) {
            // Even length: 2 * p
            if (2 * p <= K) {
                ans = max(ans, 2 * p);
            }
            // Odd length: 2 * p + 1
            if (2 * p + 1 <= K && N > 2 * p) {
                ans = max(ans, 2 * p + 1);
            }
        }
    }
    
    cout << ans << endl;
    
    return 0;
}
