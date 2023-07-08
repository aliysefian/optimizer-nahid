import itertools
import numpy as np
from optimizer import ComputeTraffic


def minimize_TLj(A):
    # Generate all possible combinations of bj values
    combinations = list(itertools.product([0, 1], repeat=len(A)))
    print(combinations)
    min_TLj = float('inf')
    min_combination = None
    compute_traffic = ComputeTraffic(A)
    # Iterate through each combination
    for combination in combinations:
        TLj = 0

        # Calculate TLj for the current combination
        if sum(combination) != 1:
            continue
        for i, x in enumerate(A):
            bj = combination[i]
            ej = compute_traffic.calculate_ej(x, bj)
            # ej = fl(x) * l(x) * bj / cj(x)
            TLj += ej

        # Update minimum TLj if a smaller value is found
        if TLj < min_TLj:
            min_TLj = TLj
            min_combination = combination

    return min_TLj, min_combination


# Example usage
A = [1, 2, 3]  # List of values for x
# fl = lambda x: x** 2  # Example function for fl
# l = lambda x: x ** 3  # Example function for l
# cj = lambda x: x ** 2 + 1  # Example function for cj

min_TLj, min_combination = minimize_TLj(A)
print("Minimum TLj:", min_TLj)
print("Optimal combination of bj:", min_combination)
arg=np.argmin(min_combination)
print(f" minimu BS {A[arg-1]}")
#
# if __name__ == '__main__':
#     print_hi('PyCharm')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
