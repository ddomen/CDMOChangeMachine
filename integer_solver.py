import numpy as np
from linear_solver import Simplex

# Check if number is Integer
def isInteger(num):
    return (isinstance(num, int) or isinstance(num, float)) and (num % 1.0 == 0)

# Vectorized function of isInteger
vecIsInteger = np.vectorize(isInteger)

# Check if a solution is Integer
# (all values excluding the objective are integers)
def isIntegerSolution(arr): 
    return np.all(vecIsInteger(arr[:-1]))

# Node structure to define Search Tree
class Node:
    def __init__(self, constraints, upper=np.inf):
        self.upper = upper
        self.constraints = [ c[:] for c in constraints ] 
        self.constNum = len(self.constraints[0])
        if isinstance(self.constraints[0][-1], str): self.constNum -= 1
    
    def copy(self):
        return Node(self.constraints, self.upper)

    def add(self, index, value, cst, cstType='<'):
        # Build up a new empty constraint row
        constraint = [ 0 ] * self.constNum
        # Fill the i-th variable and add the constraint
        constraint[index] = value
        constraint[-1] = cst
        constraint.append(cstType)
        self.constraints.append(constraint)
        return self

# Tree Search with Branch and Bound method
def BranchAndBound(variables, constraints):
    # Global variables of the search
    LOWER_BOUND = -np.inf
    # Best solution found
    BEST = None
    
    # Store root node in unexpanded list
    unexpanded = [ Node(constraints) ]

    while len(unexpanded) > 0:
        # Extract a node from the unexpanded node list
        node = unexpanded[0]
        del unexpanded[0]
        
        # Solve superproblem
        solution = Simplex(variables, node.constraints)

        # Check if solution is feasible (and positive as we don't need negative solutions)
        if solution is not None and solution[-1] >= 0:
            objective = solution[-1]
            
            # Check if the solution is Integer
            if isIntegerSolution(solution):
                
                # If the solution is better update global variables
                # else skip it
                if objective > LOWER_BOUND:
                    LOWER_BOUND = objective
                    BEST = solution
                    # Remove nodes with upper bound lower than the new lower bound
                    unexpanded = [ n for n in unexpanded if n.upper >= LOWER_BOUND ]
            
            # Check if the solution upper bound is greater than the current lower bound
            # else skip it
            elif objective > LOWER_BOUND:
                for i in range(len(solution) - 1):
                    xi = solution[i]

                    # For each variable non integer variable generate two children
                    # one with a constraint x[i] <= floor(value) and
                    # one with a constraint x[i] >= ceil(value)
                    # and set their upper limit to the current objective function value
                    if not isInteger(xi):
                        # Copy the current node constraints in a new one
                        newUpperNode = node.copy()
                        # Add a new constraint on the i-th variable of form
                        # 1 * x[i] <= floor(value)
                        newUpperNode.add(i, 1, np.floor(xi), '<')
                        newUpperNode.upper = objective
                        unexpanded.append(newUpperNode)

                        newLowerNode = node.copy()
                        newLowerNode.add(i, 1, np.ceil(xi), '>')
                        newLowerNode.upper = objective
                        unexpanded.append(newLowerNode)
        
    return BEST