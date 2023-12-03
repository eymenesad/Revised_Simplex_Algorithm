import numpy as np
# Inverse of B matrix
def modify_B(input_matrix):
    return np.linalg.inv(input_matrix)

# Vector multiplication: c_B * inverse_B
def c_B_multiply_Bmatrix(c_B, inverse_B):
    result = [0] * len(c_B)
    for i in range(len(c_B)):
        result[i] = sum(c_B[j] * inverse_B[j][i] for j in range(len(c_B)))
    return result

# Read matrix from file
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
  
    return tableau
def c_B_multiply_Bmatrix(c_B, inverse_B):
    ans = [0 for t in range(m)]
    for i in range(m):
        for j in range(m):
            ans[i] += c_B[j] * inverse_B[j][i]
    return ans

def find_entering_variable():
    new_c = dict()
    inverse_B = modify_B(B_matrix)


    c_B_inverseB = c_B_multiply_Bmatrix(c_B, inverse_B)

    for i in range(mn):
        if i in basic_set:
            continue
        c_B_A_i = 0
        for j in range(m):
            c_B_A_i += c_B_inverseB[j] * tableau[j][i]
            
        new_c[i] = c[i] - c_B_A_i
    
    flag = 0
    for element in new_c:

        print(element, "new_c[element]: ", new_c[element])
        if new_c[element] < 0:
            flag = 1
            break
    if flag == 0:
        return None  # Optimal solution reached

    min_val = 100000000
    for element in new_c:
        if new_c[element] < min_val:
            min_val = new_c[element]
            min_index = element


    return min_index
        

def find_leaving_variable(entering_variable):

    inverse_B = modify_B(B_matrix)

    column_star = [0 for i in range(m)]
    for h in range(m):
        for l in range(m):
            column_star[h] += tableau[l][entering_variable] * inverse_B[h][l]

    b_star = [0 for i in range(m)]
    for h in range(m):
        for l in range(m):
            b_star[h] += b[l] * inverse_B[h][l]

    ratios = []
    for r in range(m):
        if column_star[r] == 0:
            ratios.append(10000000)
            continue
        val = b_star[r] / column_star[r]
        if val>0:
            ratios.append(val)
        else:
            ratios.append(10000000)

    if not ratios:
        return None  # Problem is unbounded     

    min_ratio = min(ratios)
    return ratios.index(min_ratio)

def update_tableau(entering_variable, leaving_variable):


    basic_set[leaving_variable] = entering_variable
    #basic_set.remove(basic_set[leaving_variable])

    
    
    B_matrix.clear()
    for basic in basic_set:
        arr=[]
        for i in range(m):
            arr.append(tableau[i][basic])
        B_matrix.append(arr)


    c_B.clear()
    for basic in basic_set:
        c_B.append(c[basic])





def revised_simplex_algorithm():
    sas = 0
    while True:

        print("basic_set: ", basic_set)
        
        entering_variable = find_entering_variable()
        if entering_variable is None:
            break  # Optimal solution reached
        leaving_variable = find_leaving_variable(entering_variable)
        if leaving_variable is None:
            print("Unbounded problem.")
            return
        update_tableau(entering_variable, leaving_variable)
        sas += 1
        if sas == 100:
            return


    print("Hence, optimal solution is arrived with value of variables as :")
    
    print("b:", b)
    print("B_matrix:", B_matrix)

    inverse_B = modify_B(B_matrix)
    b_star_optimum = [0 for i in range(m)]
    for h in range(m):
        for l in range(m):
            b_star_optimum[h] += b[l] * inverse_B[l][h]

    print("b_star_optimum:", b_star_optimum)
    
    for y in range(m):
        element = basic_set[y]
        if element >= n:
            continue
        print(f"x{element+1} = {b_star_optimum[y]}")





if __name__ == '__main__':
    for m in range(1, 4):
        if m != 3:
            continue
        print(f"Output for case {m}:")
        m, n, c, augmented_matrix = read_matrix(f"Assignment3_Data{m}.txt")
        mn = m+n
        b = [row[-1] for row in augmented_matrix]
        c = [-x for x in c]
        c = c + [0]*m
        normal_matrix = [row[:-1] for row in augmented_matrix]
        #print(f"normal matrix {normal_matrix}")
        #n = n+m


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
        