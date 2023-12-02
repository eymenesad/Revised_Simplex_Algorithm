def read_matrix(filename):
    with open(filename, 'r') as file:
        m, n = map(int, file.readline().split())
        c = list(map(float, file.readline().split()))
        augmented_matrix = [list(map(float, line.split())) for line in file]

    return m, n, c, augmented_matrix

def print_matrix(matrix):
    for row in matrix:
        print(' '.join(map(str, row)))

def simplex_algorithm(m, n, c, augmented_matrix):
    # Phase 1: Convert the problem to standard form
    for i in range(m):
        if augmented_matrix[i][n] < 0:
            for j in range(n + 1):
                augmented_matrix[i][j] *= -1

    # Phase 2: Apply the simplex algorithm
    while any(x < 0 for x in augmented_matrix[m][:n]):
        pivot_column = augmented_matrix[m].index(min(augmented_matrix[m][:n]))

        ratios = [(augmented_matrix[i][n] / augmented_matrix[i][pivot_column], i) for i in range(m) if augmented_matrix[i][pivot_column] > 0]
        pivot_row = min(ratios)[1]

        pivot_element = augmented_matrix[pivot_row][pivot_column]

        # Update the tableau
        for j in range(n + 1):
            augmented_matrix[pivot_row][j] /= pivot_element

        for i in range(m + 1):
            if i != pivot_row:
                factor = augmented_matrix[i][pivot_column]
                for j in range(n + 1):
                    augmented_matrix[i][j] -= factor * augmented_matrix[pivot_row][j]

    # Output results
    optimal_variables = [augmented_matrix[i][n] for i in range(m)]
    optimal_result = sum(c[i] * optimal_variables[i] for i in range(n))

    print("Hence, optimal solution is arrived with value of variables as :")
    for i in range(n):
        print(f"x{i + 1} = {optimal_variables[i]:.2f}, ", end="")
    print()
    print(f"Max Z = {optimal_result:.2f}")

if __name__ == '__main__':
    for m in range(1, 4):
        print(f"Output for case {m}:")
        m, n, c, augmented_matrix = read_matrix(f"Assignment3_Data{m}.txt")
        simplex_algorithm(m, n, c, augmented_matrix)
        print("-" * 20)
