import numpy as np
from standard_form import StandardForm

# Remove printed warings from 0, inf and NaN divisions
np.seterr(divide = 'ignore', invalid = 'ignore')

# BIG M method - Simplex
def Simplex(variables, constraints, maxIterations = 300):
    # usefull variables describing the prolem
    nVar = len(variables)
    nConst = len(constraints)

    rows = nConst + 1
    cols = nVar + nConst + 2

    # building tableau in standard form
    tableau, artificials = StandardForm(variables, constraints)

    # array to keep track of basic changes (basic/non-basic variables)
    # needed to map rows in the solution columns with non-basic variables
    varIndexes = [ -1 ] * nVar
    # same for artificial variables to check feasibility
    artificialIndexes = [ -1 ] * len(artificials)

    #pivoting
    iterations = 0
    while np.sometrue(tableau[-1, :-1] < 0):
        # Check last row for gradient minimization
        # and retrieve the column index of minimum direction
        pivotColumnIndex = np.argmin(tableau[-1,:-1])
        pivotColumn = tableau[:-1, pivotColumnIndex]

        # Bland's rule preventing cycling for alternating solutions
        divisor = tableau[:-1, -1]
        divPivotColumn = divisor / pivotColumn

        # negative and meaningless elements elimination
        divPivotColumn[divPivotColumn < 0] = np.inf
        divPivotColumn[np.isnan(divPivotColumn)] = np.inf

        # Check pivot column for gradient minimization
        # and retrive the row index
        pivotRowIndex = np.argmin(divPivotColumn)
        pivotRow = tableau[pivotRowIndex]

        # Pivot element
        pivot = tableau[pivotRowIndex, pivotColumnIndex]

        # Attach variable name to a basis row
        if pivotColumnIndex < nVar and pivotRowIndex < nConst:
            # Check presence of row in the basis
            if pivotRowIndex in varIndexes:
                # if present remove it from the basis
                rIndex = varIndexes.index(pivotRowIndex)
                varIndexes[rIndex] = -1
            # Attach variable name to row
            varIndexes[pivotColumnIndex] = pivotRowIndex
        # Attach artificial variable name to a basis row
        elif pivotColumnIndex in artificials:
            rIndex = artificials.index(pivotColumnIndex)
            artificialIndexes[rIndex] = pivotRowIndex
        
        # Matrix substitution to perform pivot operation
        for i in range(rows):
            if i == pivotRowIndex: continue
            pivotFactor = -tableau[i, pivotColumnIndex] / pivot
            if pivotFactor == 0: continue
            tableau[i] += pivotRow * pivotFactor
        
        # Cleaning pivot
        tableau[pivotRowIndex] /= pivot

        # Current solution found in tableau (Partial optimal)
        partial = tableau[:, -1]
        
        # Check iterations over the max number to prevent
        # degeneration of the solution
        if iterations > maxIterations: return None
        iterations += 1

    # Solution column extraction
    solutionColumn = tableau[:, -1]

    # Artificial variables must be absent or negative in the solution
    # for the solution to be feasible
    for a in artificialIndexes:
        # variable absent
        if a < 0: continue
        # positive solution -> unfeasible
        elif solutionColumn[a] > 0: return None
        
    # Initial problem variable mapping
    result = [ 0 ] * nVar
    
    for i in range(nVar):
        # index of the variable in the solution column
        index = varIndexes[i]
        # variable absent -> variable is 0
        if index < 0: result[i] = 0
        # take present variable from correspondent row
        else: result[i] = solutionColumn[index]

    # Adding objective function value in the found solution (z)
    result.append(solutionColumn[-1])

    return np.array(result)