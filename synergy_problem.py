class Synergy_Problem_Data:
    def __init__(self, budget, n, cost_list, power_list, synergy_matrix):
        self.budget = budget
        self.n = n
        self.cost_list = cost_list
        self.power_list = power_list
        self.synergy_matrix = synergy_matrix

    def __repr__(self):
        return f"Instance(budget={self.budget}, n={self.n}, cost_list={self.cost_list}, power_list={self.power_list}, synergy_matrix={self.synergy_matrix})"

class Synergy_Solution:
    def __init__(self, selected, total_power, time_elapsed):
        self.selected = selected
        self.total_power = total_power
        self.time_elapsed = time_elapsed

    def __repr__(self):
        return f"Solution(selected={self.selected}, total_power={self.total_power}, time_elapsed={self.time_elapsed})"
    
    def __str__(self) -> str:
        selected_representation = represent_selected(self.selected)
        return f"total_power={self.total_power}, time_elapsed={self.time_elapsed:.2f},\n selected={selected_representation}"

def represent_selected(selected):
    """
    Convert a binary selection vector to a list of selected indices.
    :param selected: A list of binary values (0 or 1).
    :return: A list of indices where the value is 1.
    """
    return [i for i, val in enumerate(selected) if val > 0]

def read_instances(filename):
    """
    Read problem instance from file:
      - First line: <budget> <number_of_equipments>
      - Next lines: <cost> <power> for each equipment
      - Followed by synergy matrix: each row has number_of_equipments values
    Returns: budget, n, cost_list, power_list, synergy_matrix
    """
    with open(filename) as f:
        lines = f.readlines()

    # parse budget and number of equipments
    first = lines[0].split()
    budget = int(first[0])
    n = int(first[1])

    # parse cost and power
    cost = []
    power = []
    for i in range(1, n+1):
        c, p = map(int, lines[i].split())
        cost.append(c)
        power.append(p)

    # parse synergy matrix
    synergy = []
    start = n + 1
    for i in range(start, start + n):
        row = list(map(int, lines[i].split()))
        synergy.append(row)

    return Synergy_Problem_Data(budget, n, cost, power, synergy)

