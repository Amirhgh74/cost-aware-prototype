import csv
import random

input_file = 'new_result.txt'
input_csv = 'function_data_redis.csv'

def knapsack_genetic(values, weights, max_weight, population_size, num_generations, mutation_rate):
    n = len(values)
    
    # Generate initial population
    population = []
    for _ in range(population_size):
        individual = [random.choice([0, 1]) for _ in range(n)]
        population.append(individual)

    # Evolution process
    for _ in range(num_generations):
        # Calculate fitness scores for each individual
        fitness_scores = []
        for individual in population:
            total_weight = sum([weights[i] for i in range(n) if individual[i] == 1])
            if total_weight <= max_weight:
                fitness_scores.append(sum([values[i] for i in range(n) if individual[i] == 1]))
            else:
                fitness_scores.append(0)
        
        # Selection
        selected_population = []
        for _ in range(population_size):
            parent1 = random.choices(population, weights=fitness_scores)[0]
            parent2 = random.choices(population, weights=fitness_scores)[0]
            child = crossover(parent1, parent2)
            selected_population.append(child)
        
        # Mutation
        for individual in selected_population:
            for i in range(n):
                if random.random() < mutation_rate:
                    individual[i] = 1 - individual[i]
        
        population = selected_population

    # Find the best solution
    best_fitness = 0
    best_solution = []
    for individual in population:
        total_weight = sum([weights[i] for i in range(n) if individual[i] == 1])
        if total_weight <= max_weight:
            total_value = sum([values[i] for i in range(n) if individual[i] == 1])
            if total_value > best_fitness:
                best_fitness = total_value
                best_solution = individual

    return best_fitness, best_solution

def crossover(parent1, parent2):
    # Perform one-point crossover
    crossover_point = random.randint(1, len(parent1) - 1)
    child = parent1[:crossover_point] + parent2[crossover_point:]
    return child

def knapsack_01(weights, values, capacity):
    n = len(weights)
    dp = [[0] * (capacity + 1) for _ in range(n + 1)]

    for i in range(1, n + 1):
        for w in range(1, capacity + 1):
            if weights[i - 1] <= w:
                dp[i][w] = max(values[i - 1] + dp[i - 1][w - weights[i - 1]], dp[i - 1][w])
            else:
                dp[i][w] = dp[i - 1][w]

    # Backtracking to find the chosen items
    chosen_items = []
    i, w = n, capacity
    while i > 0 and w > 0:
        if dp[i][w] != dp[i - 1][w]:
            chosen_items.append(i - 1)
            w -= weights[i - 1]
        i -= 1

    chosen_items.reverse()
    return dp[n][capacity], chosen_items


# Open the input file for reading
with open(input_file, 'r') as file:
    lines = file.readlines()
    

# Process the lines and extract function names and call counts
data = {} # key : function name  * values = [calls, cpu , io, network, input, output]


skip_header = True
for line in lines:
    line = line.strip()
    if skip_header:
        skip_header = False
        continue
    if line and not line.startswith("="):
        parts = line.split()
        function = parts[-1]
        calls = parts[-2]
        data[function] = [int(calls)]




# Read the CSV file
with open(input_csv, 'r') as file:
    reader = csv.reader(file)
    header = next(reader)  # Skip the header row

    # Iterate over the rows and update the dictionary values
    for row in reader:
        function = row[0]
        if function in data:
            values = [float(value) for value in row[1:]]
            data[function].extend(values)

print (data)

names = []
values = []
costs = []

budget = 12000000000

for key in data.keys():
    if len(data[key]) > 1:
        names.append(key)
        values.append(round(data[key][3], 3))
        freq = int (data[key][0])
        in_size = float (data[key][-2])
        delay = 1 

        if in_size <= 4:
            delay = 0.15
        elif in_size <= 16:
            delay = 0.22
        elif in_size <= 64:
            delay = 0.35
        
        cost = int (delay * freq * 2 *1000)
        costs.append(cost)


population_size = 100
num_generations = 150
mutation_rate = 0.2

print (names)
print(values)

best_fitness, best_solution = knapsack_genetic(values, costs, budget, population_size, num_generations, mutation_rate)
selected_items = [names[i] for i in range(len(best_solution)) if best_solution[i] == 1]

print("Best fitness:", best_fitness)
print("Selected items:", best_solution)
print ("functions selected: " , selected_items)
print ("number of selected functions : ", len(selected_items))
