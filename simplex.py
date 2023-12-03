import numpy as np


#inverse of B matrix
def modify_B(input_matrix):
    return np.linalg.inv(input_matrix)


def read_matrix(filename):
    with open(filename, 'r') as file:
        m, n = map(int, file.readline().split())
        c = list(map(float, file.readline().split()))
        augmented_matrix = [list(map(float, line.split())) for line in file]
    return m, n, c, augmented_matrix

def print_matrix(matrix):
    for row in matrix:
        print(' '.join(map(str, row)))

def initialize_tableau(c, normal_matrix):
    tableau = [row for row in normal_matrix]
    for i in range(m):
        tableau[i].extend([0] * i)
        tableau[i].extend([1.0])
        tableau[i].extend([0] * (m - i - 1))
        
    negative_c = [-x for x in c]
    tableau.insert(0, negative_c + [0]*m)
    return tableau
def c_B_multiply_Bmatrix(c_B, inverse_B):
    ans = [0 for t in range(m)]
    for i in range(m):
        for j in range(m):
            ans[i] += c_B[j] * inverse_B[j][i]
    return ans

def find_entering_variable():
    new_c = [0 for ii in range(n)]
    inverse_B = modify_B(B_matrix)

    c_B_inverseB = c_B_multiply_Bmatrix(c_B, inverse_B)

    for i in range(n):
        if i in basic_set:
            continue
        c_B_A_i = 0
        for j in range(m):
            c_B_A_i += c_B_inverseB[j] * tableau[i][j]
        new_c[i] = c[i] - c_B_A_i
    pivot_column = min(new_c)
    if pivot_column >= 0:
        return None  # Optimal solution reached
    return new_c.index(pivot_column), new_c

def find_leaving_variable(entering_variable):
    ratios = []
    for r in range(m):
        if tableau[r][entering_variable] > 0:
            ratios.append((b[r] / tableau[r][entering_variable], r))

    if not ratios:
        return None  # Problem is unbounded
    min_ratio, leaving_variable_row = min(ratios, key=lambda x: x[0])
    return leaving_variable_row

def update_tableau(entering_variable, leaving_variable):


    basic_set.append(entering_variable)
    basic_set.remove(leaving_variable)

    B_matrix = []
    for i in range(m):
        arr=[]
        for basic in basic_set:
            arr.append(tableau[i][basic])
        B_matrix.append(arr)

    c_B = []
    for basic in basic_set:
        c_B.append(c[basic])

    # tableu = inverse_of_B * tableau
    inverse_B = modify_B(B_matrix)
    for i in range(m):
        for j in range(n):
            tableau[i][j] = 0
            for k in range(m):
                tableau[i][j] += inverse_B[i][k] * B_matrix[k][j]



def revised_simplex_algorithm():
    while True:
        
        entering_variable, c = find_entering_variable()
        if entering_variable is None:
            break  # Optimal solution reached
        leaving_variable = find_leaving_variable(tableau, entering_variable)
        if leaving_variable is None:
            print("Unbounded problem.")
            return
        update_tableau(entering_variable, leaving_variable)

    optimal_solution = [0] * (len(tableau[0]) - 1)
    for i in range(len(optimal_solution)):
        column = [row[i] for row in tableau[1:]]
        if column.count(0) == len(column) - 1 and column[-1] == 1:
            pivot_row = column.index(1)
            optimal_solution[i] = tableau[pivot_row + 1][-1]

    optimal_result = sum(x * y for x, y in zip(c, optimal_solution))

    print("Hence, optimal solution is arrived with value of variables as :")
    for i, value in enumerate(optimal_solution):
        print(f"x{i + 1} = {value}", end=", ")

    print(f"\nMax Z = {optimal_result}")


if __name__ == '__main__':
    for m in range(1, 4):
        print(f"Output for case {m}:")
        m, n, c, augmented_matrix = read_matrix(f"Assignment3_Data{m}.txt")
        b = [row[-1] for row in augmented_matrix]
        normal_matrix = [row[:-1] for row in augmented_matrix]
        n = n+m


        tableau = initialize_tableau(c, normal_matrix)
  
        basic_set = [f for f in range(n, n+m)]
        B_matrix = []
        for i in range(m):
            arr=[]
            for basic in basic_set:
                arr.append(tableau[i][basic])
            B_matrix.append(arr)

        c_B = []
        for basic in basic_set:
            c_B.append(c[basic])
        revised_simplex_algorithm()
        print("-" * 20)
        break