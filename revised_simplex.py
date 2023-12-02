def read_matrix(filename):
    with open(filename, 'r') as file:
        m, n = map(int, file.readline().split())
        c = list(map(float, file.readline().split()))
        augmented_matrix = [list(map(float, line.split())) for line in file]
    return m, n, c, augmented_matrix

def print_matrix(matrix):
    for row in matrix:
        print(' '.join(map(str, row)))

def add_slack_variables(c, augmented_matrix):
    slack_variables = [[0] * i + [1] + [0] * (len(augmented_matrix) - i - 1) for i in range(len(augmented_matrix))]
    c += [0] * len(slack_variables)
    augmented_matrix = [row + slack for row, slack in zip(augmented_matrix, slack_variables)]
    return c, augmented_matrix

def initialize_tableau(c, augmented_matrix):
    tableau = [row[:-1] for row in augmented_matrix]
    for i in range(len(tableau)):
        tableau[i].append(augmented_matrix[i][-1])
    tableau.insert(0, c + [0])
    return tableau

def find_entering_variable(tableau):
    pivot_column = min(tableau[0][:-1])
    if pivot_column >= 0:
        return None  # Optimal solution reached
    return tableau[0].index(pivot_column)

def find_leaving_variable(tableau, entering_variable):
    ratios = [(row[-1] / row[entering_variable], i) for i, row in enumerate(tableau[1:]) if row[entering_variable] > 0]
    if not ratios:
        return None  # Problem is unbounded
    min_ratio, leaving_variable_row = min(ratios, key=lambda x: x[0])
    return leaving_variable_row + 1

def update_tableau(tableau, entering_variable, leaving_variable):
    pivot_element = tableau[leaving_variable][entering_variable]
    pivot_row = [x / pivot_element for x in tableau[leaving_variable]]

    for i in range(len(tableau)):
        if i == leaving_variable:
            continue
        multiplier = tableau[i][entering_variable]
        for j in range(len(tableau[i])):
            tableau[i][j] -= multiplier * pivot_row[j]

def revised_simplex_algorithm(c, augmented_matrix):
    c, augmented_matrix = add_slack_variables(c, augmented_matrix)
    tableau = initialize_tableau(c, augmented_matrix)

    while True:
        entering_variable = find_entering_variable(tableau)
        if entering_variable is None:
            break  # Optimal solution reached
        leaving_variable = find_leaving_variable(tableau, entering_variable)
        if leaving_variable is None:
            print("Unbounded problem.")
            return
        update_tableau(tableau, entering_variable, leaving_variable)

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
        revised_simplex_algorithm(c, augmented_matrix)
        print("-" * 20)
