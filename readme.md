# **DANIELE DOMENICHELLI - UNIBO** ![UNIBO](unibo_res.png)
## **Combinatorial Decision Making and Optimization - PROJECT:**
## ***Change Machine:** Branch and Bound - Big M solution*

This program calculate the coin change starting from an available quantity of coins and sizes.

The problem was chosen because it is linear, integer and because it is intrinsically combinatorial, requiring a deeper knowledge on the use of LPI.

The solution is reached by applying 3 different steps:
1. Standardization (Standard Form - LP)
2. Big M method (Simplex - LP)
3. Breanch and Bound (Search Tree - LPI)

## 1. Standardization
In order to solve any problem with the Simplex method, it is necessary to describe it in the standard form. The standard form is represented by a matrix with this form:

```
[ NBV | BV | OS | RHS ]
[ ------------------- ]
[        -OBJF        ]

with:

NBV = Non-Basic Variables
BV = Basic Variables
OS = Objective Solution
RHS = Right Hand Side (positive form)
OBJG = OBJective Function
```

The program takes a convetional matrix that simply describe wanted variables and problem constraints, and transforms it in a standard form matrix.

## 2. Big M Method (Simplex)
The Big M method is an extension of the Simplex method for linear problem solution. In the Simplex method is not allowed to use inverted sign constraints (>= for maximization, <= for minimization), so a big variety of problems are not solvable through it, expecially those of combinatorial and integer nature.

The inverted sign constraints usually bring to a negative solution for relative slack variables and an unfeasible solution. This is not a problem if the slack variable does not appear on the solution base, but in almost any general problem at least one of them appears. The underlying effect is an unwanted reduction of the feasible solution space given by the bad formulation of the problem, and not instric in the problem. In practice we are adding constraints that are not present in the original problem.

The Big M method introduce artificial variables in the tableau. An artificial variable have an initial huge negative solution that obscures the negativity of the relative slack variable leading the inverted sign constraint to be achievable. Even the artifical variables are subject to region of feasibility: all of those that appear on the solution base must be non negative. A positive one will mean that the solution is unfeasible. In this way we better describe the problem.

The final matrix in standard form will be:

```
[  NBV | BV | AV | OS | RHS  ]
[  ------------------------  ]
[  -OBJF(0) | -M |  -OBJF(1) ]

with:

AV = Artificial Variables (just inserted in the matrix)
```

## 3. Branch And Bound
The Branc and Bound is an exact linear integer programming method. It generates and explores a tree of solutions, where each node have narrower constraints on the variables. At each step this method calculate the linear solution with the Big M method. If it have at least one non integer variable, two new nodes are added to the tree: one will have a constraint forcing the variable to be equal or lesser than the closest integer value, the other will have the same constraint but with equal or greater sybmol.

In order optimize the search, it is possible to cut unfeasible solutions and those which have an upper bound (maximum value granted) lesser than the best ever found. Once the tree search expires, the best integer solution found (if any) will be the optimal integer solution.

## Program
At the end, the program will just build up the problem given a certain target change (request) and the available quantity and size of the coins.