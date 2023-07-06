
import itertools

def minimize_TLj(A, fl, l, cj):
    # Generate all possible combinations of bj values
    combinations = list(itertools.product([0, 1], repeat=len(A)))
    print(combinations)
    min_TLj = float('inf')
    min_combination = None
    
    # Iterate through each combination
    for combination in combinations:
        TLj = 0
        
        # Calculate TLj for the current combination
        if sum(combination) != 1:
            continue
        for i, x in enumerate(A):
            bj = combination[i]
            ej = fl(x) * l(x) * bj / cj(x)
            TLj += ej
        
        # Update minimum TLj if a smaller value is found
        if TLj < min_TLj:
            min_TLj = TLj
            min_combination = combination
    
    return min_TLj, min_combination

# Example usage
A = [1, 2, 3]  # List of values for x
fl = lambda x: x**2  # Example function for fl
l = lambda x: x**3  # Example function for l
cj = lambda x: x**2 + 1  # Example function for cj

min_TLj, min_combination = minimize_TLj(A, fl, l, cj)
print("Minimum TLj:", min_TLj)
print("Optimal combination of bj:", min_combination)
