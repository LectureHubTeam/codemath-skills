// Digit DP — Đếm số thỏa điều kiện trong [1..N]
// Template chuẩn với tight constraint và leading_zero flag
// Customize: STATE, transition, is_valid()

#include <bits/stdc++.h>
using namespace std;

string s;
int n;
int memo[20][200][2][2]; // [pos][state][tight][leading_zero]
int TARGET_SUM;

// Đếm số trong [1..N] có tổng chữ số = TARGET_SUM
int dp(int pos, int sum, bool tight, bool leading_zero) {
  if (sum > TARGET_SUM)
    return 0;
  if (pos == n) {
    return (!leading_zero && sum == TARGET_SUM) ? 1 : 0;
  }

  int &ref = memo[pos][sum][tight][leading_zero];
  if (ref != -1)
    return ref;

  int limit = tight ? (s[pos] - '0') : 9;
  int result = 0;

  for (int digit = 0; digit <= limit; digit++) {
    bool new_leading = leading_zero && (digit == 0);
    int new_sum = new_leading ? 0 : sum + digit;
    bool new_tight = tight && (digit == limit);
    result += dp(pos + 1, new_sum, new_tight, new_leading);
  }

  return ref = result;
}

// ===== GENERAL TEMPLATE =====
// Customize STATE và transition cho từng bài:
//
// int STATE;  // ví dụ: last digit, sum mod K, bitmask
//
// int transition(int state, int digit) {
//     return (state + digit) % K;  // ví dụ sum mod K
// }
//
// bool is_valid(int state) {
//     return state == TARGET;
// }
//
// int dp_general(int pos, int state, bool tight, bool leading_zero) {
//     if (pos == n) return is_valid(state) && !leading_zero;
//     auto& ref = memo[pos][state][tight][leading_zero];
//     if (ref != -1) return ref;
//     int limit = tight ? (s[pos] - '0') : 9;
//     int result = 0;
//     for (int d = 0; d <= limit; d++) {
//         bool nl = leading_zero && d == 0;
//         int ns = nl ? INITIAL_STATE : transition(state, d);
//         result += dp_general(pos+1, ns, tight && (d==limit), nl);
//     }
//     return ref = result;
// }

int main() {
  ios_base::sync_with_stdio(false);
  cin.tie(NULL);

  long long N;
  cin >> N >> TARGET_SUM;

  s = to_string(N);
  n = s.size();
  memset(memo, -1, sizeof(memo));

  cout << dp(0, 0, true, true) << "\n";
  return 0;
}
