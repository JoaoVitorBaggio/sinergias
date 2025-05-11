import time

def read_instances(filename):
    with open(filename) as f:
        lines = f.readlines()
    aux = lines[0].split()
    budget = int(aux[0])
    number_equipments = int(aux[1])

    equipment_cost_aux = []
    equipment_power_aux = []
    equipment_cost = []
    equipment_power = []

    for i in range(1, number_equipments):
        aux = lines[i].split()
        equipment_cost.append(int(aux[0]))
        equipment_power.append(int(aux[1]))
      
    sinergy = []
    aux_lst = []

    for i in range (number_equipments + 1, 2*number_equipments):
        aux = lines[i].split()
        aux_lst = list(map(int, aux))
        sinergy.append(aux_lst)

    return budget, number_equipments, equipment_cost, equipment_power, sinergy


def sort_power_equipments(equipment_power):
    sorted_candidates = sorted(range(len(equipment_power)), key=lambda i: equipment_power[i], reverse=True)
    return sorted_candidates




def calculate_objective_value(solution, equipment_power, sinergy,budget):
    value = 0
    total_cost = 0
    for i in range(len(solution)-1):
        if (total_cost + equipment_cost[i]) <= budget:
            value += solution[i] * equipment_power[i]
            total_cost += solution[i] * equipment_cost[i]

    
    for i in range(len(solution)-1):
        for j in range(len(solution)-1):
            if solution[i] == 1 and solution[j] == 1:
                value += sinergy[i][j]

    return value




def get_initial_solution(number_equipments, equipment_cost, budget, equipment_power):
    best_power_candidates = sort_power_equipments(equipment_power)
    solution = [0] * number_equipments
    total_cost = 0

    for i in best_power_candidates:
        if total_cost + equipment_cost[i] <= budget:
            solution[i] = 1
            total_cost += equipment_cost[i]


    return solution


def generate_neighborhood(solution, equipment_cost, budget):
    neighborhood = []
    for i in range(len(solution)-1):
        neighbor = solution[:]
        neighbor[i] = 1 - neighbor[i]  # Flip the bit
        if is_valid_solution(neighbor, equipment_cost, budget):
            neighborhood.append(neighbor)
    return neighborhood


def is_valid_solution(solution, equipment_cost, budget):
    total_cost = sum([solution[i] * equipment_cost[i] for i in range(len(solution)-1)])
    return total_cost <= budget


def tabu_search(initial_solution, equipment_cost, equipment_power, sinergy, budget, time_limit, tabu_tenure, output_file):
    current_solution = initial_solution[:]
    best_solution = initial_solution[:]
    best_objective_value = calculate_objective_value(best_solution, equipment_power, sinergy, budget)
    tabu_list = []
    start_time = time.time()  # Record the start time

    while time.time() - start_time < time_limit:  # Check if the elapsed time is within the limit
        neighborhood = generate_neighborhood(current_solution, equipment_cost, budget)
        best_neighbor = None
        best_neighbor_value = float('-inf')

        for neighbor in neighborhood:
            if neighbor not in tabu_list:
                neighbor_value = calculate_objective_value(neighbor, equipment_power, sinergy, budget)
                if neighbor_value > best_neighbor_value:
                    best_neighbor = neighbor
                    best_neighbor_value = neighbor_value

        if best_neighbor is None:
            break

        current_solution = best_neighbor
        if best_neighbor_value > best_objective_value:
            best_solution = best_neighbor
            best_objective_value = best_neighbor_value
            with open(output_file, 'a') as f:
                f.write(f"New best solution found: {best_solution}\n, Objective Value: {best_objective_value}  Time:{time.time() - start_time:.2f}s \n\n")

        

        tabu_list.append(current_solution)
        if len(tabu_list) > tabu_tenure:
            tabu_list.pop(0)

    #print("Best solution found:", best_solution)
    #print("Best objective value:", best_objective_value)
    return best_solution

def write_tabu_search_results(filename, initial_solution, equipment_cost, equipment_power, sinergy, budget, time_limit, tabu_tenure):
    
    final_solution = tabu_search(initial_solution, equipment_cost, equipment_power, sinergy, budget, time_limit, tabu_tenure, filename)
    final_objective_value = calculate_objective_value(final_solution, equipment_power, sinergy, budget)
    
    # Append results to the file
    with open(filename, 'a') as f:  # Open in append mode
        f.write("Tabu Search Results\n")
        f.write("===================\n")
        f.write(f"Final Solution: {final_solution}\n")
        f.write(f"Final Objective Value: {final_objective_value}\n")
        f.write(f"Time Limit: {time_limit} seconds\n")
        f.write(f"Tabu Tenure: {tabu_tenure}\n")
        f.write("-------------------\n")  
    
    print(f"Results appended to {filename}")




"""
budget, number_equipments, equipment_cost, equipment_power, sinergy = read_instances("./instances/01.txt")
initial




print(sinergy)
x = calculate_synergy_potential(sinergy)
print("Synergy potential:", x)

write_tabu_search_results(filename="tabu_search_results.txt",initial_solution=initial_solution,equipment_cost=equipment_cost,equipment_power=equipment_power,sinergy=sinergy,budget=budget,time_limit=5, tabu_tenure=10)


write_tabu_search_results(filename="tabu_search_results.txt",initial_solution=initial_solution,equipment_cost=equipment_cost,equipment_power=equipment_power,sinergy=sinergy,budget=budget,time_limit=300,tabu_tenure=10)


budget, number_equipments, equipment_cost, equipment_power, sinergy = read_instances("./instances/02.txt")
initial_solution = get_initial_solution(number_equipments, equipment_cost, budget, equipment_power)

write_tabu_search_results(filename="tabu_search_results.txt",initial_solution=initial_solution,equipment_cost=equipment_cost,equipment_power=equipment_power,sinergy=sinergy,budget=budget,time_limit=5, tabu_tenure=10)


write_tabu_search_results(filename="tabu_search_results.txt",initial_solution=initial_solution,equipment_cost=equipment_cost,equipment_power=equipment_power,sinergy=sinergy,budget=budget,time_limit=300,tabu_tenure=10)



budget, number_equipments, equipment_cost, equipment_power, sinergy = read_instances("./instances/03.txt")
initial_solution = get_initial_solution(number_equipments, equipment_cost, budget, equipment_power)

write_tabu_search_results(filename="tabu_search_results.txt",initial_solution=initial_solution,equipment_cost=equipment_cost,equipment_power=equipment_power,sinergy=sinergy,budget=budget,time_limit=5, tabu_tenure=25)

write_tabu_search_results(filename="tabu_search_results.txt",initial_solution=initial_solution,equipment_cost=equipment_cost,equipment_power=equipment_power,sinergy=sinergy,budget=budget,time_limit=300,tabu_tenure=25)

budget, number_equipments, equipment_cost, equipment_power, sinergy = read_instances("./instances/04.txt")
initial_solution = get_initial_solution(number_equipments, equipment_cost, budget, equipment_power)

write_tabu_search_results(filename="tabu_search_results.txt",initial_solution=initial_solution,equipment_cost=equipment_cost,equipment_power=equipment_power,sinergy=sinergy,budget=budget,time_limit=5, tabu_tenure=30)

write_tabu_search_results(filename="tabu_search_results.txt",initial_solution=initial_solution,equipment_cost=equipment_cost,equipment_power=equipment_power,sinergy=sinergy,budget=budget,time_limit=300,tabu_tenure=30)


budget, number_equipments, equipment_cost, equipment_power, sinergy = read_instances("./instances/05.txt")
initial_solution = get_initial_solution(number_equipments, equipment_cost, budget, equipment_power)

write_tabu_search_results(filename="tabu_search_results.txt",initial_solution=initial_solution,equipment_cost=equipment_cost,equipment_power=equipment_power,sinergy=sinergy,budget=budget,time_limit=5, tabu_tenure=150)

write_tabu_search_results(filename="tabu_search_results.txt",initial_solution=initial_solution,equipment_cost=equipment_cost,equipment_power=equipment_power,sinergy=sinergy,budget=budget,time_limit=300,tabu_tenure=150)


"""
budget, number_equipments, equipment_cost, equipment_power, sinergy = read_instances("./instances/06.txt")
initial_solution = get_initial_solution(number_equipments, equipment_cost, budget, equipment_power)

write_tabu_search_results(filename="tabu_search_results.txt",initial_solution=initial_solution,equipment_cost=equipment_cost,equipment_power=equipment_power,sinergy=sinergy,budget=budget,time_limit=5, tabu_tenure=75)

write_tabu_search_results(filename="tabu_search_results.txt",initial_solution=initial_solution,equipment_cost=equipment_cost,equipment_power=equipment_power,sinergy=sinergy,budget=budget,time_limit=300,tabu_tenure=75)

"""

budget, number_equipments, equipment_cost, equipment_power, sinergy = read_instances("./instances/07.txt")
initial_solution = get_initial_solution(number_equipments, equipment_cost, budget, equipment_power)

write_tabu_search_results(filename="tabu_search_results.txt",initial_solution=initial_solution,equipment_cost=equipment_cost,equipment_power=equipment_power,sinergy=sinergy,budget=budget,time_limit=5, tabu_tenure=300)

write_tabu_search_results(filename="tabu_search_results.txt",initial_solution=initial_solution,equipment_cost=equipment_cost,equipment_power=equipment_power,sinergy=sinergy,budget=budget,time_limit=300,tabu_tenure=300)


budget, number_equipments, equipment_cost, equipment_power, sinergy = read_instances("./instances/08.txt")
initial_solution = get_initial_solution(number_equipments, equipment_cost, budget, equipment_power)

write_tabu_search_results(filename="tabu_search_results.txt",initial_solution=initial_solution,equipment_cost=equipment_cost,equipment_power=equipment_power,sinergy=sinergy,budget=budget,time_limit=5, tabu_tenure=300)

write_tabu_search_results(filename="tabu_search_results.txt",initial_solution=initial_solution,equipment_cost=equipment_cost,equipment_power=equipment_power,sinergy=sinergy,budget=budget,time_limit=300,tabu_tenure=300)


budget, number_equipments, equipment_cost, equipment_power, sinergy = read_instances("./instances/09.txt")
initial_solution = get_initial_solution(number_equipments, equipment_cost, budget, equipment_power)

write_tabu_search_results(filename="tabu_search_results.txt",initial_solution=initial_solution,equipment_cost=equipment_cost,equipment_power=equipment_power,sinergy=sinergy,budget=budget,time_limit=5, tabu_tenure=450)

write_tabu_search_results(filename="tabu_search_results.txt",initial_solution=initial_solution,equipment_cost=equipment_cost,equipment_power=equipment_power,sinergy=sinergy,budget=budget,time_limit=300,tabu_tenure=450)


budget, number_equipments, equipment_cost, equipment_power, sinergy = read_instances("./instances/10.txt")
initial_solution = get_initial_solution(number_equipments, equipment_cost, budget, equipment_power)

write_tabu_search_results(filename="tabu_search_results.txt",initial_solution=initial_solution,equipment_cost=equipment_cost,equipment_power=equipment_power,sinergy=sinergy,budget=budget,time_limit=5, tabu_tenure=275)

write_tabu_search_results(filename="tabu_search_results.txt",initial_solution=initial_solution,equipment_cost=equipment_cost,equipment_power=equipment_power,sinergy=sinergy,budget=budget,time_limit=300,tabu_tenure=275)


#x = calculate_objective_value([0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], equipment_power, sinergy,budget)

#x = calculate_objective_value(initial_solution, equipment_power, sinergy,budget)
#print("Objective function value:", x)

"""







