/*
 * Problem: 23ckththn4 - Dãy số đối xứng (Symmetric Sequence)
 * 
 * Problem: Find the longest palindromic subsequence with length <= K
 * 
 * Approach:
 * - For small N (<= 5000): Use O(N^2) DP for exact LPS
 * - For large N: Use center expansion with binary search, O(N * K * log(N))
 * 
 * Key insight: Since K <= 100 is small, we can limit the expansion to K/2 pairs
 * 
 * Time Complexity: O(N^2) for N <= 5000, O(N * K * log(N)) for N > 5000
 * Space Complexity: O(N^2) for N <= 5000, O(N) for N > 5000
 */

#include <iostream>
#include <vector>
#include <map>
#include <algorithm>
using namespace std;

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(nullptr);
    
    int N, K;
    cin >> N >> K;
    
    vector<int> A(N);
    for (int i = 0; i < N; i++) {
        cin >> A[i];
    }
    
    // Edge cases
    if (N == 0) {
        cout << 0 << "\n";
        return 0;
    }
    
    if (K == 1) {
        cout << 1 << "\n";
        return 0;
    }
    
    // For small N, use O(N^2) DP for exact LPS
    if (N <= 5000) {
        vector<vector<int>> dp(N, vector<int>(N, 1));
        
        for (int len = 2; len <= N; len++) {
            for (int i = 0; i <= N - len; i++) {
                int j = i + len - 1;
                if (A[i] == A[j]) {
                    dp[i][j] = (len == 2 ? 2 : 2 + dp[i+1][j-1]);
                } else {
                    dp[i][j] = max(dp[i+1][j], dp[i][j-1]);
                }
            }
        }
        
        cout << min(dp[0][N-1], K) << "\n";
        return 0;
    }
    
    // For large N, use center expansion with binary search
    // Precompute position lists for each value
    map<int, vector<int>> positions;
    for (int i = 0; i < N; i++) {
        positions[A[i]].push_back(i);
    }
    
    int maxLen = 1;
    
    // Odd-length palindromes (center at element)
    for (int center = 0; center < N; center++) {
        int len = 1;
        int l = center - 1, r = center + 1;
        
        while (l >= 0 && r < N && len + 2 <= K) {
            int targetVal = A[l];
            auto& pos = positions[targetVal];
            auto it = lower_bound(pos.begin(), pos.end(), r);
            
            if (it != pos.end()) {
                l--;
                r = *it + 1;
                len += 2;
            } else {
                l--;
            }
        }
        
        maxLen = max(maxLen, len);
        if (maxLen == K) {
            cout << K << "\n";
            return 0;
        }
    }
    
    // Even-length palindromes (center between elements)
    for (int center = 0; center < N - 1; center++) {
        int len = 0;
        int l = center, r = center + 1;
        
        while (l >= 0 && r < N && len + 2 <= K) {
            int targetVal = A[l];
            auto& pos = positions[targetVal];
            auto it = lower_bound(pos.begin(), pos.end(), r);
            
            if (it != pos.end()) {
                l--;
                r = *it + 1;
                len += 2;
            } else {
                l--;
            }
        }
        
        maxLen = max(maxLen, len);
        if (maxLen == K) {
            cout << K << "\n";
            return 0;
        }
    }
    
    cout << maxLen << "\n";
    
    return 0;
}
