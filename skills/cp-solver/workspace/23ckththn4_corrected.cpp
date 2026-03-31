/*
 * Problem: 23ckththn4 - Dãy số đối xứng (Symmetric Sequence)
 * 
 * Find the longest palindromic subsequence with length <= K
 * 
 * CORRECTED SOLUTION: O(N * K * D * log N) where D = number of distinct values
 * 
 * Algorithm:
 * - For each center position c, expand outward greedily
 * - At each step, find the innermost matching pair (l, r) where:
 *   - l < current_left_boundary, r > current_right_boundary
 *   - A[l] = A[r]
 *   - l is maximized (closest to current boundary) to leave room for more pairs
 * - This greedy approach works because choosing innermost pair leaves maximum room
 * 
 * Time Complexity: O(N * K * D * log N)
 * Space Complexity: O(N)
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
    if (!(cin >> N >> K)) {
        cout << 0 << "\n";
        return 0;
    }

    vector<int> A(N);
    for (int i = 0; i < N; i++) {
        cin >> A[i];
    }

    // Edge cases
    if (N == 0 || K == 0) {
        cout << 0 << "\n";
        return 0;
    }

    // Precompute position lists for each value
    map<int, vector<int>> pos;
    for (int i = 0; i < N; i++) {
        pos[A[i]].push_back(i);
    }

    int maxLen = 0;

    // Helper: find largest position < bound with value v
    auto findRightmostBefore = [&](int v, int bound) -> int {
        auto it = pos.find(v);
        if (it == pos.end()) return -1;
        const vector<int>& p = it->second;
        auto iter = lower_bound(p.begin(), p.end(), bound);
        if (iter == p.begin()) return -1;
        return *(--iter);
    };

    // Helper: find smallest position > bound with value v
    auto findLeftmostAfter = [&](int v, int bound) -> int {
        auto it = pos.find(v);
        if (it == pos.end()) return -1;
        const vector<int>& p = it->second;
        auto iter = upper_bound(p.begin(), p.end(), bound);
        if (iter == p.end()) return -1;
        return *iter;
    };

    // For each center position
    for (int c = 0; c < N; c++) {
        // Odd-length palindrome with center c
        int len = 1;
        int innerL = c, innerR = c;
        
        while (len < K) {
            // Find the innermost pair (l, r) with l < innerL, r > innerR, A[l] = A[r]
            // We want to maximize l (closest to innerL) to leave room for more pairs
            int bestL = -1, bestR = -1;
            
            for (const auto& [v, positions] : pos) {
                int l = findRightmostBefore(v, innerL);
                if (l == -1) continue;
                
                int r = findLeftmostAfter(v, innerR);
                if (r == -1) continue;
                
                // Choose the pair with largest l (innermost on left)
                if (bestL == -1 || l > bestL) {
                    bestL = l;
                    bestR = r;
                }
            }
            
            if (bestL == -1) break;  // No more pairs available
            
            innerL = bestL;
            innerR = bestR;
            len += 2;
        }
        
        maxLen = max(maxLen, len);
        
        // Early termination if we found K
        if (maxLen == K) {
            cout << K << "\n";
            return 0;
        }
    }

    // Even-length palindromes (center between c and c+1)
    for (int c = 0; c < N - 1; c++) {
        int len = 0;
        int innerL = c, innerR = c + 1;
        
        while (len < K) {
            int bestL = -1, bestR = -1;
            
            for (const auto& [v, positions] : pos) {
                int l = findRightmostBefore(v, innerL + 1);  // l <= innerL
                if (l == -1) continue;
                
                int r = findLeftmostAfter(v, innerR - 1);  // r >= innerR
                if (r == -1) continue;
                
                if (bestL == -1 || l > bestL) {
                    bestL = l;
                    bestR = r;
                }
            }
            
            if (bestL == -1) break;
            
            innerL = bestL;
            innerR = bestR;
            len += 2;
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
