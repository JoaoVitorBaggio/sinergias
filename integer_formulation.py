import pulp
import sys
from synergy_problem import read_instances, Synergy_Solution

"""
Como chamar esse script:
python integer_formulation.py <input_file> <max_time>
onde:
<input_file> é o caminho para o arquivo de instância
<max_time> é o tempo máximo em segundos para a execução do solver.
"""

"""
Instância Uma instância é composta por: um valor orçamentário O (um valor
inteiro e positivo); uma quantidade de equipamentos n (um valor inteiro
e positivo); cada equipamento i possui duas propriedades individuais,
um custo ci (um valor inteiro e positivo) e um nível de poder pi (um
valor inteiro); além disso, cada par (não-ordenado) de equipamentos i
e j possui uma sinergia sij (um valor inteiro).
Objetivo Selecionar um conjunto de equipamentos cuja soma dos custos 
individuais é menor ou igual ao valor orçamentário, e que maximiza a soma
dos níveis de poder individuais dos equipamentos selecionados e das
sinergias entre os equipamentos selecionados.
"""

def integer_formulation(problem_instance, max_time=None, seed=None):
    """
    Solve the equipment selection problem using integer programming.
    Args:
        problem_instance: An instance of Synergy_Problem_Data containing budget, n, cost_list, power_list, and synergy_matrix.
        max_time: Maximum time in seconds for the solver to run (optional).
    Returns:
        A tuple containing:
            - selected: List of indices of selected equipment.
            - total_power: Total power of the selected equipment.
            - time_elapsed: Time taken to solve the problem.
    """

    # Unpack the problem instance
    budget = problem_instance.budget
    n = problem_instance.n
    cost = problem_instance.cost_list
    power = problem_instance.power_list
    synergy = problem_instance.synergy_matrix

    # Create the problem
    prob = pulp.LpProblem("EquipmentSelection", pulp.LpMaximize)

    # Create binary variables for each equipment
    x = [pulp.LpVariable(f"x_{i}", cat='Binary') for i in range(n)]

    # Auxiliar decision variables for synergy
    y = {
        (i, j): pulp.LpVariable(f"y_{i}_{j}", cat='Binary')
        for i in range(n)
        for j in range(i)
    }

    # Objective function: maximize power and synergy
    prob += pulp.lpSum(power[i] * x[i] for i in range(n)) + \
            pulp.lpSum(synergy[i][j] * y[(i, j)] for i in range(n) for j in range(i))

    # Budget constraint
    prob += pulp.lpSum(cost[i] * x[i] for i in range(n)) <= budget

    # Synergy constraints: y_ij = 1 if both x_i and x_j are selected
    for i in range(n):
        for j in range(i):
            prob += y[(i, j)] <= x[i]
            prob += y[(i, j)] <= x[j]
            prob += y[(i, j)] >= x[i] + x[j] - 1  # y_ij = 1 if both are selected

    # Choose solver and set time limit and seed if provided
    solver = pulp.PULP_CBC_CMD()
    if max_time is not None:
        solver.timeLimit = max_time
    if seed is not None:
        solver.options.append(f'Seed={seed}')

    # Solve the problem
    prob.solve(solver)

    # Extract solution
    selected = [x[i].varValue for i in range(n)] #type: ignore
    total_power = pulp.value(prob.objective)
    time_elapsed = prob.solutionTime
    
    return Synergy_Solution(selected, total_power, time_elapsed)

def main():
    filename = sys.argv[1]
    max_time = int(sys.argv[2])
    seed = int(sys.argv[3]) 

    problem_instance = read_instances(filename)
    solution = integer_formulation(
        problem_instance,
        max_time=max_time,
        seed=seed
    )
    print(solution)


if __name__ == '__main__':
    main()
