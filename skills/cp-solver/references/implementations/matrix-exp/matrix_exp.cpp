// Matrix Exponentiation — Fast matrix power O(K³ log N)
// Dùng cho: linear recurrences với N lớn (10^18), DP transitions
// Template: Fibonacci, linear recurrence, graph powers

#include <bits/stdc++.h>
using namespace std;

const long long MOD = 1e9 + 7;
typedef vector<vector<long long>> Matrix;

Matrix multiply(const Matrix &A, const Matrix &B) {
  int n = A.size(), m = A[0].size(), p = B[0].size();
  Matrix C(n, vector<long long>(p, 0));
  for (int i = 0; i < n; i++)
    for (int k = 0; k < m; k++)
      if (A[i][k])
        for (int j = 0; j < p; j++)
          C[i][j] = (C[i][j] + A[i][k] * B[k][j]) % MOD;
  return C;
}

// Matrix power: A^n mod MOD in O(K³ log n)
Matrix power(Matrix A, long long n) {
  int sz = A.size();
  Matrix result(sz, vector<long long>(sz, 0));
  for (int i = 0; i < sz; i++)
    result[i][i] = 1; // identity

  while (n > 0) {
    if (n & 1)
      result = multiply(result, A);
    A = multiply(A, A);
    n >>= 1;
  }
  return result;
}

// ===== EXAMPLE: Fibonacci F(n) mod MOD =====
// F(n+1)   [1 1] [F(n)  ]
// F(n)   = [1 0] [F(n-1)]
long long fibonacci(long long n) {
  if (n <= 1)
    return n;
  Matrix M = {{1, 1}, {1, 0}};
  Matrix Mn = power(M, n - 1);
  return Mn[0][0]; // F(n) = M^(n-1)[0][0] * F(1) + M^(n-1)[0][1] * F(0)
}

// ===== EXAMPLE: Count paths of length K in graph =====
// adj_matrix^K[i][j] = số đường đi độ dài K từ i đến j
Matrix count_paths(Matrix adj, long long K) { return power(adj, K); }

int main() {
  ios_base::sync_with_stdio(false);
  cin.tie(NULL);

  long long n;
  cin >> n;
  cout << fibonacci(n) << "\n";

  return 0;
}
