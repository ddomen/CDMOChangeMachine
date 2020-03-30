import numpy as np

# big M variable
M = 1000000

# Big M method - Standard Form
def StandardForm(variables, constraints):
    # number of initial variables
    nVars = len(variables)
    # vector of the objective function coefficients (non basic variables)
    objective = [ x for x in variables ]
    # vector of basic variables
    basics = [ ]
    # vector of artificial variables
    artificials = []
    # array of artificial variables indexes
    artificialIndexes = []
    # vector of right-hand-side coefficients
    rhs = []
    # keep trace of M on artificial variables columns
    dirtyColumns = []

    # number of artificial variables
    nArt = 0
    # current row and column
    row = 0
    col = 0

    # building table row by row
    for c in constraints:
        art = [ 0 ] * nArt
        obj = 0
        # Equality Constraint
        # Add -M to correspective column in the objective function
        if c[-1] == '=':
            obj = -M
            dirtyColumns.append(row)
        # Greather Then Constraint
        # Add a new artificial variable
        # and -M to correspective column in the objective function
        elif c[-1] == '>':
            nArt += 1
            art.append(-1)
            objective.append(0)
            col += 1
            artificialIndexes.append(col + nVars)
            obj = -M
            dirtyColumns.append(row)

        objective.append(obj)

        # Any Constraint
        # Add a new slack variable
        art.append(1)
        nArt += 1
        artificials.append(art)

        base = list(c)
        if isinstance(base[-1], str):
            base = base[:-1]
        rhs.append(base[-1])
        base = base[:-1]
        basics.append(base)
        row += 1
        col += 1

    # Initialize objective function value to 0    
    rhs.append(0)
    # Expanding artificial table in order to have same dimension in each row
    artificials = [ a + [0] * (nArt - len(a)) for a in artificials ]

    # Building up the tableau
    # Constraint table [ B | Av ]
    csts = np.hstack([ basics, artificials ])
    # Problem table [  CST  ]
    #               [ ---- ]
    #               [ -OBJ ]
    problem = np.vstack([ csts, -np.array(objective) ])

    # Building solution variable vector
    P = [0] * problem.shape[0]
    P[-1] = 1

    # Dirty Tableau [ PROB | P | RHS ]
    tableau = np.hstack([problem, np.array([P, rhs]).T ])
    tableau = tableau.astype(float)

    # Clean up tableu for Big M (remove M from artificial variables)
    for dirty in dirtyColumns:
        tableau[-1] += (-M) * tableau[dirty]

    return tableau, artificialIndexes