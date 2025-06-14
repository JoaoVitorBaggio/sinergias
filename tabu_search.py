import time
import sys
from synergy_problem import read_instances, Synergy_Solution, Synergy_Problem_Data

"""
Como chamar esse script:
python tabu_search.py <input_file> <max_iterations> <tabu_tenure>
Onde:
<input_file> é o caminho para o arquivo de instância
<max_iterations> é o número máximo de iterações do algoritmo Tabu Search,
<tabu_tenure> é o tempo de tabu (número de iterações que uma solução fica tabu).
"""

def sort_by_power(power, cost):
    """
    Return equipment indices sorted by descending power-to-cost ratio
    """
    ratios = [p / c if c > 0 else 0 for p, c in zip(power, cost)]
    return sorted(range(len(power)), key=lambda i: ratios[i], reverse=True)


def initial_solution(n, cost, power, budget):
    """
    Greedy initial solution by selecting highest power-to-cost until budget exhausted
    """
    sol = [0] * n
    total = 0
    for i in sort_by_power(power, cost):
        if total + cost[i] <= budget:
            sol[i] = 1
            total += cost[i]
    return sol


def compute_value(sol, power, synergy):
    """
    Compute objective: sum of selected power plus pairwise synergy
    """
    val = sum(p for p, s in zip(power, sol) if s)
    # add pairwise synergy only once (i < j)
    for i in range(len(sol)):
        if sol[i]:
            for j in range(i+1, len(sol)):
                if sol[j]:
                    val += synergy[i][j]
    return val


def flip_delta(sol, i, power, cost, budget, synergy, current_val):
    """
    Compute incremental change if flipping bit i (0->1 or 1->0)
    without full recompute: use current_val and local contributions.
    Returns new_val or None if invalid (budget exceed).
    """
    delta = 0
    n = len(sol)
    # cost delta
    if sol[i] == 0:
        # adding equipment
        if sum(sol[k]*cost[k] for k in range(n)) + cost[i] > budget:
            return None
        delta += power[i]  # add power
        # add synergy with existing selected
        for j in range(i):
            if sol[j]: delta += synergy[i][j]
    else:
        # removing equipment
        delta -= power[i]
        for j in range(i):
            if sol[j] and j != i:
                delta -= synergy[i][j]
    return current_val + delta

def calculate_power(solution, problem: Synergy_Problem_Data):
    total = 0
    for i in range(problem.n):
        if solution[i] == 1:
            total += problem.power_list[i]
    for i in range(problem.n):
        for j in range(i + 1, problem.n):
            if solution[i] == 1 and solution[j] == 1:
                total += problem.synergy_matrix[i][j] + problem.synergy_matrix[j][i]
    return total

def calculate_cost(solution, problem: Synergy_Problem_Data):
    return sum(c for c, sel in zip(problem.cost_list, solution) if sel == 1)

def generate_initial_greedy_solution(problem: Synergy_Problem_Data):
    solution = [0] * problem.n
    items = list(range(problem.n))
    efficiency = [(i, problem.power_list[i] / problem.cost_list[i] if problem.cost_list[i] > 0 else 0) for i in items]
    efficiency.sort(key=lambda x: x[1], reverse=True)
    total_cost = 0
    for i, _ in efficiency:
        if total_cost + problem.cost_list[i] <= problem.budget:
            solution[i] = 1
            total_cost += problem.cost_list[i]
    print(f"Solução inicial gulosa: {solution}, Custo: {total_cost}, Poder: {calculate_power(solution, problem)}")
    return solution

def generate_neighbors(solution, problem: Synergy_Problem_Data):
    neighbors = []
    for i in range(problem.n):
        new_solution = solution.copy()
        new_solution[i] = 1 - new_solution[i]
        neighbors.append((new_solution, i))
    return neighbors

def tabu_search(problem: Synergy_Problem_Data, max_iter=1000, tabu_size=10, time_limit=300):
    current_solution = generate_initial_greedy_solution(problem)
    best_solution = current_solution
    best_value = calculate_power(best_solution, problem)
    tabu_list = []
    start_time = time.time()

    for iteration in range(max_iter):
        elapsed_time = time.time() - start_time
        if elapsed_time >= time_limit:
            print(f"\nTempo limite de {time_limit} segundos atingido. Encerrando busca.")
            break

        neighbors = generate_neighbors(current_solution, problem)
        candidates = []
        for neighbor, move in neighbors:
            cost = calculate_cost(neighbor, problem)
            if cost <= problem.budget and (move not in tabu_list):
                candidates.append((neighbor, move))

        if not candidates:
            candidates = [(neighbor, move) for neighbor, move in neighbors if calculate_cost(neighbor, problem) <= problem.budget]
            if not candidates:
                print("Sem vizinhos válidos, parando busca.")
                break

        selected_neighbor, selected_move = max(candidates, key=lambda x: calculate_power(x[0], problem))
        neighbor_value = calculate_power(selected_neighbor, problem)

        if neighbor_value > best_value:
            best_value = neighbor_value
            best_solution = selected_neighbor
            time_to_best = time.time() - start_time
            print(f"\n>>> Nova melhor solução! Valor = {best_value}, Tempo decorrido: {time_to_best:.2f} segundos <<<")

        print(f"\nIteração {iteration + 1}:")
        print(f"Movimento tabu adicionado: flip no equipamento índice {selected_move}")
        tabu_list.append(selected_move)
        if len(tabu_list) > tabu_size:
            removed = tabu_list.pop(0)
            print(f"Removendo movimento mais antigo da lista tabu: índice {removed}")

        print(f"Lista Tabu atual: {tabu_list}")
        print(f"Poder da solução atual: {neighbor_value}, Custo: {calculate_cost(selected_neighbor, problem)}")

        current_solution = selected_neighbor

    total_time = time.time() - start_time
    print(f"\nBusca finalizada. Tempo total: {total_time:.2f} segundos.")

    return Synergy_Solution(best_solution, best_value, total_time)


def main():
    filename = sys.argv[1]
    max_iter = int(sys.argv[2])
    tenure = int(sys.argv[3])

    problem_instance = read_instances(filename)
    solution = tabu_search(
        problem_instance,
        max_iter=max_iter, tabu_size=tenure
    )
    print(solution)


if __name__ == '__main__':
    main()
