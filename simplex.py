def determinant(matrix):
    size = len(matrix)
    if size == 1:
        return matrix[0][0]
    elif size == 2:
        return matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]
    else:
        det = 0
        for i in range(size):
            cofactor = matrix[0][i] * determinant([row[:i] + row[i+1:] for row in matrix[1:]])
            det += ((-1) ** i) * cofactor
        return det
# Inverse of B matrix
def modify_B(augmented_matrix):
    det = determinant(augmented_matrix)
    if det == 0:
        print("Unbounded solution")
        return 0
    augmented_matrix = [row+[0] for row in augmented_matrix]
    n = len(augmented_matrix)
    
    inverted_matrix = [[0 for x in range(n)] for y in range(n)]
    for w in range(n):
        inverted_matrix[w][w] = 1
    
    for i in range(n):
        pivot = augmented_matrix[i][i]
        if pivot == 0:
            if i == n - 1:
                if augmented_matrix[i][-1] != 0:
                    print("Unbounded solution")

                    #No solution
                    return 0
                
                else:
                    #Infinite solution
                    print("Infinite solution")
                    return 2
            
            else:

                for m in range(i + 1, n):
                    if augmented_matrix[m][i] != 0:
                        augmented_matrix[i], augmented_matrix[m] = augmented_matrix[m], augmented_matrix[i]
                        inverted_matrix[i], inverted_matrix[m] = inverted_matrix[m], inverted_matrix[i]
                        break
                pivot = augmented_matrix[i][i] # pivot is now non-zero
        
        if pivot == 0:
            continue
            #return 2       


        for j in range(0, n + 1):
            augmented_matrix[i][j] /= pivot
            if abs(augmented_matrix[i][j]) < pow(10, -10):
                    augmented_matrix[i][j] = 0
            if j != n:
                inverted_matrix[i][j] /= pivot
                if abs(inverted_matrix[i][j]) < pow(10, -10):
                        inverted_matrix[i][j] = 0

        for k in range(n):
            if k == i:
                continue

            factor = augmented_matrix[k][i]
            for j in range(0, n + 1):
                augmented_matrix[k][j] -= factor * augmented_matrix[i][j] #- augmented_matrix[k][j]
                if abs(augmented_matrix[k][j]) < pow(10, -10):
                    augmented_matrix[k][j] = 0
                if j != n:
                    inverted_matrix[k][j] -= factor * inverted_matrix[i][j]
                    if abs(inverted_matrix[k][j]) < pow(10, -10):
                        inverted_matrix[k][j] = 0

    return inverted_matrix

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
            ans[i] += c_B[j] * inverse_B[i][j]
    return ans

def find_entering_variable():
    new_c = dict()
    inverse_B = modify_B(B_matrix)
    if inverse_B == 0 or inverse_B == 2:
        return -1

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
    if inverse_B == 0 or inverse_B == 2:
        return None

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
    while True:

        
        entering_variable = find_entering_variable()
        if entering_variable is None:
            break  # Optimal solution reached
        if entering_variable == -1:
            print("Unbounded problem.")
            return
        leaving_variable = find_leaving_variable(entering_variable)
        if leaving_variable is None:
            print("Unbounded problem.")
            return
        update_tableau(entering_variable, leaving_variable)
       



    print("Optimal solution is arrived with value of variables as :")
    
    
    inverse_B = modify_B(B_matrix)
    if inverse_B == 0 or inverse_B == 2:
        print("Unbounded solution")
        return None
    b_star_optimum = [0 for i in range(m)]
    for h in range(m):
        for l in range(m):
            b_star_optimum[h] += b[l] * inverse_B[l][h]

    
    for y in range(m):
        element = basic_set[y]
        if element >= n:
            continue
        print(f"x{element+1} = {round(b_star_optimum[y],6)}")

if __name__ == '__main__':
    for m in range(1, 4):
        
        
        print(f"Output for case {m}:")
        #if m == 2:
        #    print("Unbounded problem.") #Todo, infinite loop, we could not understand
        #    continue
        m, n, c, augmented_matrix = read_matrix(f"Assignment3_Data{m}.txt")
        mn = m+n
        b = [row[-1] for row in augmented_matrix]
        c = [-x for x in c]
        c = c + [0]*m
        normal_matrix = [row[:-1] for row in augmented_matrix]
        


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
        