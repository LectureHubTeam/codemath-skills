"""
Digit DP — Đếm số thỏa điều kiện trong [1..N]
Template chuẩn: có 'tight' constraint và 'leading_zero' flag
Complexity: O(log N × states)

Modify:
- Thay STATE và transition() cho từng bài
- Thay is_valid() nếu cần check ở leaf
"""
import sys
from functools import lru_cache
input = sys.stdin.readline


def count_with_digit_sum(N, target_sum):
    """
    Đếm số trong [1..N] có tổng chữ số = target_sum
    """
    s = str(N)
    n = len(s)

    @lru_cache(maxsize=None)
    def dp(pos, current_sum, tight, leading_zero):
        # Base case: đã xét hết tất cả digits
        if pos == n:
            return 1 if (current_sum == target_sum and not leading_zero) else 0

        result = 0
        limit = int(s[pos]) if tight else 9

        for digit in range(0, limit + 1):
            new_leading = leading_zero and (digit == 0)
            new_sum = current_sum if new_leading else current_sum + digit

            # Prune: nếu sum đã vượt target
            if new_sum > target_sum:
                break

            new_tight = tight and (digit == limit)
            result += dp(pos + 1, new_sum, new_tight, new_leading)

        return result

    return dp(0, 0, True, True)


def count_without_digit(N, forbidden_digit):
    """
    Đếm số trong [1..N] không chứa chữ số 'forbidden_digit'
    """
    s = str(N)
    n = len(s)

    @lru_cache(maxsize=None)
    def dp(pos, tight, leading_zero):
        if pos == n:
            return 0 if leading_zero else 1

        result = 0
        limit = int(s[pos]) if tight else 9

        for digit in range(0, limit + 1):
            if digit == forbidden_digit and not (leading_zero and digit == 0):
                continue  # Skip forbidden digit (allow leading zero = 0)
            new_tight = tight and (digit == limit)
            new_leading = leading_zero and (digit == 0)
            result += dp(pos + 1, new_tight, new_leading)

        return result

    return dp(0, True, True)


# ===== GENERAL TEMPLATE =====
def digit_dp_template(N):
    """
    Template tổng quát — customize cho từng bài:
    1. Định nghĩa STATE (ví dụ: sum mod K, last digit, parity)
    2. Thay transition(state, digit) → new_state
    3. Thay is_valid(state) tại leaf
    """
    s = str(N)
    n = len(s)
    INITIAL_STATE = 0  # Customize

    def transition(state, digit):
        return state  # Customize: ví dụ (state + digit) % K

    def is_valid(state):
        return True  # Customize: ví dụ state == target

    @lru_cache(maxsize=None)
    def dp(pos, state, tight, leading_zero):
        if pos == n:
            return 1 if (is_valid(state) and not leading_zero) else 0

        result = 0
        limit = int(s[pos]) if tight else 9

        for digit in range(0, limit + 1):
            new_leading = leading_zero and (digit == 0)
            new_state = INITIAL_STATE if new_leading else transition(state, digit)
            new_tight = tight and (digit == limit)
            result += dp(pos + 1, new_state, new_tight, new_leading)

        return result

    return dp(0, INITIAL_STATE, True, True)


# ===== USAGE EXAMPLE =====
def solve():
    N, K = map(int, input().split())
    # Đếm số trong [1..N] có tổng chữ số = K
    print(count_with_digit_sum(N, K))


if __name__ == '__main__':
    solve()
