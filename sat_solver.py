from itertools import product
import pycosat
import time

def varnum(i, j, k):
    """Returns a unique variable number for the SAT solver given cell (i, j) and digit k."""
    return i * 81 + j * 9 + k + 1

def encode_sudoku_to_dimacs(grid):
    """Encodes a Sudoku grid into DIMACS format."""
    clauses = []

    #each cell contains exactly one number (1-9)
    for i, j in product(range(9), repeat=2):
        clauses.append([varnum(i, j, k) for k in range(9)])
        for k in range(9):
            for l in range(k + 1, 9):
                clauses.append([-varnum(i, j, k), -varnum(i, j, l)])

    # each number appears exactly once in each row
    for k in range(9):
        for i in range(9):
            clauses.extend([[varnum(i, j, k) for j in range(9)]])
            for j in range(9):
                for l in range(j + 1, 9):
                    clauses.append([-varnum(i, j, k), -varnum(i, l, k)])

    # each number appears exactly once in each column   
    for k in range(9):
        for j in range(9):
            clauses.extend([[varnum(i, j, k) for i in range(9)]])
            for i in range(9):
                for l in range(i + 1, 9):
                    clauses.append([-varnum(i, j, k), -varnum(l, j, k)])

    #each number appears exactly once in each 3x3 sub-grid
    for k in range(9):
        for a, b in product(range(3), repeat=2):
            subgrid = [varnum(a * 3 + di, b * 3 + dj, k) for di, dj in product(range(3), repeat=2)]
            clauses.append(subgrid)
            for m in range(9):
                for n in range(m + 1, 9):
                    clauses.append([-subgrid[m], -subgrid[n]])

    # add the initial clues to the clauses 
    for i in range(9):
        for j in range(9):
            if grid[i][j] != 0:
                k = grid[i][j] - 1
                clauses.append([varnum(i, j, k)])

    return clauses

def solve_sudoku(grid):
    """Solves a Sudoku grid."""
    clauses = encode_sudoku_to_dimacs(grid)
    start_time = time.time()
    solution = pycosat.solve(clauses)
    end_time = time.time()
    solve_time = end_time - start_time
    if solution == "UNSAT":
        print("No solution exists.")
        return None, solve_time
    else:
        solution_grid = [[0] * 9 for _ in range(9)]
        for literal in solution:
            if literal > 0:
                i, j, k = (literal - 1) // 81, ((literal - 1) % 81) // 9, ((literal - 1) % 81) % 9
                solution_grid[i][j] = k + 1
        return solution_grid, solve_time

# Sudoku puzzle (0 represents empty cells)
puzzle = [
    [0, 0, 0, 0, 0, 0, 0, 0, 9],
    [3, 0, 5, 6, 9, 0, 0, 7, 1],
    [0, 9, 4, 0, 0, 3, 6, 0, 0],
    [2, 7, 8, 0, 4, 6, 9, 0, 0],
    [0, 4, 0, 7, 8, 1, 0, 6, 2],
    [5, 1, 6, 0, 2, 0, 0, 0, 8],
    [0, 5, 7, 0, 0, 0, 0, 9, 0],
    [0, 3, 9, 0, 6, 0, 2, 8, 0],
    [0, 8, 0, 9, 0, 7, 3, 0, 0]
]   

solution, solve_time = solve_sudoku(puzzle)
if solution:
    print("Solution:")
    for row in solution:
        print(row)
    print("Solving time:", solve_time, "seconds")
