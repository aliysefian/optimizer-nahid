import itertools
import numpy as np
from optimizer import ComputeTraffic, ComputeLoad
import queue

pq = queue.PriorityQueue()



def minimize_TLj(A, l, cj):
    # Generate all possible combinations of bj values
    combinations = list(itertools.product([0, 1], repeat=len(A)))
    cost=[]
    print(combinations)
    min_TLj = float('inf')
    min_combination = None
    compute_traffic = ComputeTraffic(A)
    min_CLj = float('inf')
    compute_load = ComputeLoad(A)
    test = []

    # Iterate through each combination
    for combination in combinations:
        TLj = 0
        CLj = 0
        # Calculate TLj for the current combination
        if sum(combination) != 1:
            continue
        for i, x in enumerate(A):
            bj = combination[i]
            ej = compute_traffic.calculate_ej(x, bj)

            # 

            e_hat_j = compute_load.calculate_ej(l[i], bj, cj[i])
            # ej = fl(x) * l(x) * bj / cj(x)
            CLj += e_hat_j

            # 
            # ej = fl(x) * l(x) * bj / cj(x)
            TLj += ej
            Lm=float(TLj/(1-TLj))
            # TLj = float(TLj / 1 - TLj)
            Lp = float(CLj / (1 - CLj))
            result = Lm + Lp
            test.append(result)

        # Update minimum TLj if a smaller value is found
        cost.append(min_TLj)
        if result < min_TLj:
            min_TLj = result
            min_combination = combination

    return min_TLj, min_combination,cost


def minimize_CLj(A, l, cj):
    # Generate all possible combinations of bj values
    combinations = list(itertools.product([0, 1], repeat=len(A)))
    print(combinations)
    min_CLj = float('inf')
    min_combination = None
    compute_traffic = ComputeLoad(A)
    # Iterate through each combination
    for combination in combinations:
        CLj = 0

        # Calculate TLj for the current combination
        if sum(combination) != 1:
            continue
        for i, x in enumerate(A):
            bj = combination[i]

            ej = compute_traffic.calculate_ej(l[i], bj, cj[i])
            # ej = fl(x) * l(x) * bj / cj(x)
            CLj += ej

        # Update minimum TLj if a smaller value is found
        if CLj < min_CLj:
            min_CLj = CLj
            min_combination = combination

    return min_CLj, min_combination


# Example usage
A = [2000, 100, 1500]  # List of values for x
load_of_each_server = [10, 15, 20]
capacity_of_each_server = [10, 15, 40]
# min_Lj, min_combination_lj =minimize_CLj(A, load_of_each_server, capacity_of_each_server)

# fl = lambda x: x** 2  # Example function for fl
# l = lambda x: x ** 3  # Example function for l
# cj = lambda x: x ** 2 + 1  # Example function for cj

# min_TLj, min_combination ,cost= minimize_TLj(A, load_of_each_server, capacity_of_each_server)
# print("Minimum TLj:", min_TLj)
# print("Optimal combination of bj:", min_combination)
# arg = np.argmin(min_combination)
# print(f" minimu BS {A[arg - 1]}")
# print(f" minimu LM {min_Lj}")
#
# if __name__ == '__main__':
#     print_hi('PyCharm')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
