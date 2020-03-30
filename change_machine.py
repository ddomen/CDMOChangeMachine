from integer_solver import BranchAndBound

# CONSTANTS:
#   V = size of the coin
#   Q = quantity of coins available
#   R = change
#
# OBJECTIVE FUNCTION (MAXIMIZE):
#   V1*x1 + V2*x2 + ... + Vn*xn             (1.0)
#
# CONSTRAINTS:
#   V1*x1 + V2*x2 + ... + Vn*xn <= R        (2.0)
#   V1*x1 <= Q1                             (2.1)
#   V2*x2 <= Q2                             (2.2)
#   ...
#   Vn*nx <= Qn                             (2.n)

# Given a storage (dictionary of available coins) and the
# change request (int) return the given change (dictionary)
def ChangeMachine(storage, change):
    # Storage informations
    sizes = tuple(storage.keys())
    numSizes = len(sizes)
    coins = tuple(storage.values())

    # Building up Change Problem
    variables = list(sizes) # (1.0)
    constraints = [ list(sizes) + [ change, '=' ] ] # (2.0)
    for i in range(numSizes): # (2.1 - 2.n)
        # Building up empty constraint
        cst = [ 0 ] * numSizes
        # Setting i-th variable forming constraint x[i] <= Qi
        cst[i] = 1
        cst.append(storage[sizes[i]])
        cst.append('<')
        constraints.append(cst)

    # Retrive result of the integer problem with B&B Three Search
    result = BranchAndBound(variables, constraints)

    # Building up the change dictionary (if change solution is feasible)
    if result is None:
        return None
    else:
        return { sizes[i]: result[i] for i in range(numSizes) if result[i] > 0 }