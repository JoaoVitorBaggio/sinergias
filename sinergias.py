import math
import random


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
    best_power_candidates = find_best_power_candidates(equipment_power)
    solution = [0] * number_equipments
    total_cost = 0
    for i in range(len(best_power_candidates) - 1):
        if total_cost + equipment_cost[i] <= budget:
            solution[best_power_candidates[i]] = 1
            total_cost += equipment_cost[i]

    print("Initial solution:", solution)
    return solution


def find_best_power_candidates(equipament_power):
    best_power_candidates = []
    for i in range(len(equipament_power)-1):
        if equipament_power[i] > 0:
            best_power_candidates.append(i)

    print("Best power candidates:", best_power_candidates)
    return best_power_candidates



budget, number_equipments, equipment_cost, equipment_power, sinergy = read_instances("./instances/10.txt")





find_best_power_candidates(equipment_power)

initial_solution = get_initial_solution(number_equipments, equipment_cost, budget, equipment_power)



#x = calculate_objective_value([0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], equipment_power, sinergy,budget)

x = calculate_objective_value(initial_solution, equipment_power, sinergy,budget)


print("Objective function value:", x)

#calculate_objective_value(solution, equipment_power, sinergy,budget)