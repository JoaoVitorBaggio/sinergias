import time
import sys
from synergy_problem import read_instances, Synergy_Solution, represent_selected

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


def tabu_search(problem_instance,
                max_iter=1000, tabu_tenure=10):
    """
    Perform Tabu Search with:
      - on-the-fly neighbor generation (flip one bit)
      - incremental evaluation (flip_delta)
      - aspiration: allow tabu move if improves best
    """
    # unpack problem instance
    budget = problem_instance.budget
    n = problem_instance.n
    cost = problem_instance.cost_list
    power = problem_instance.power_list
    synergy = problem_instance.synergy_matrix

    # initial
    sol = initial_solution(n, cost, power, budget)
    best = sol[:]
    best_val = compute_value(sol, power, synergy)
    current_val = best_val
    tabu = {}  # map index -> remaining tenure

    start = time.time()
    for iteration in range(max_iter):
        candidate = None
        candidate_val = float('-inf')
        move_idx = None

        # explore neighborhood by flipping each bit
        for i in range(n):
            new_val = flip_delta(sol, i, power, cost, budget, synergy, current_val)
            if new_val is None:
                continue  # invalid by budget
            is_tabu = i in tabu and tabu[i] > 0
            # aspiration: if this move improves best, accept it
            if is_tabu and new_val <= best_val:
                continue
            # select best candidate
            if new_val > candidate_val:
                candidate = sol[:]
                candidate[i] = 1 - candidate[i]
                candidate_val = new_val
                move_idx = i

        if candidate is None:
            break

        # apply best move
        sol = candidate
        current_val = candidate_val

        # update tabu list: decrement and remove expired
        tabu = {k: v-1 for k, v in tabu.items() if v-1 > 0}
        # add this move to tabu
        tabu[move_idx] = tabu_tenure

        # update global best
        if current_val > best_val:
            best = sol[:]
            best_val = current_val
            solution_representation = represent_selected(sol) #type: ignore

            # print progress
            print(f"Iteration {iteration+1}: Best value = {solution_representation}, Time elapsed: {time.time() - start:.2f}s, Solution = {best}")

    elapsed = time.time() - start
    return Synergy_Solution(best, best_val, elapsed)


def main():
    filename = sys.argv[1]
    max_iter = int(sys.argv[2])
    tenure = int(sys.argv[3])

    problem_instance = read_instances(filename)
    solution = tabu_search(
        problem_instance,
        max_iter=max_iter, tabu_tenure=tenure
    )
    print(solution)


if __name__ == '__main__':
    main()
