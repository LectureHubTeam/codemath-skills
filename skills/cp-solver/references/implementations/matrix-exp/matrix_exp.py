"""
Matrix Exponentiation — Fast matrix power O(K³ log N)
Dùng cho: linear recurrences với N lớn (10^18), DP transitions

Usage:
    mat = Matrix([[1,1],[1,0]])
    result = mat ** n       # A^n mod MOD
    val = result[0][0]
"""
import sys
input = sys.stdin.readline

MOD = 10**9 + 7


class Matrix:
    def __init__(self, data):
        self.data = data
        self.n = len(data)
        self.m = len(data[0])

    def __mul__(self, other):
        n, m, p = self.n, self.m, other.m
        result = [[0] * p for _ in range(n)]
        for i in range(n):
            for k in range(m):
                if self.data[i][k] == 0: continue
                for j in range(p):
                    result[i][j] = (result[i][j] + self.data[i][k] * other.data[k][j]) % MOD
        return Matrix(result)

    def __pow__(self, n):
        """A^n mod MOD — O(K³ log n)"""
        sz = self.n
        # Identity matrix
        result = Matrix([[1 if i == j else 0 for j in range(sz)] for i in range(sz)])
        A = Matrix([row[:] for row in self.data])
        while n > 0:
            if n & 1:
                result = result * A
            A = A * A
            n >>= 1
        return result

    def __getitem__(self, idx):
        return self.data[idx]

    def __repr__(self):
        return '\n'.join(str(row) for row in self.data)


def fibonacci(n):
    """F(n) mod MOD sử dụng matrix exponentiation — O(log n)"""
    if n <= 1: return n
    M = Matrix([[1, 1], [1, 0]])
    Mn = M ** (n - 1)
    return Mn[0][0]


def linear_recurrence(coeffs, initial, n):
    """
    Tính f(n) với recurrence: f(i) = sum(coeffs[j] * f(i-1-j))
    coeffs: list length K
    initial: f(0), f(1), ..., f(K-1)
    n: giá trị cần tính

    Ví dụ Fibonacci: coeffs=[1,1], initial=[0,1], n=10 → f(10)=55
    """
    k = len(coeffs)
    if n < k: return initial[n]

    # Companion matrix
    M = [[0] * k for _ in range(k)]
    for j in range(k):
        M[0][j] = coeffs[j]
    for i in range(1, k):
        M[i][i-1] = 1

    # State vector [f(k-1), f(k-2), ..., f(0)]
    Mn = Matrix(M) ** (n - k + 1)

    result = 0
    for j in range(k):
        result = (result + Mn[0][j] * initial[k-1-j]) % MOD
    return result


# ===== USAGE EXAMPLE =====
def solve():
    n = int(input())
    print(fibonacci(n))


if __name__ == '__main__':
    solve()
