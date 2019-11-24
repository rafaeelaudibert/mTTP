import argparse

from neighbourhood import *

def read_instance(instance_file):
    distances_matrix = []
    f = open(instance_file, "r")
    for line in f:
        row = line.rstrip("\n\r")
        row_values = [int(s) for s in row.split() if s.isdigit()]
        distances_matrix.append(row_values)


    schedule_matrix = [row[:] for row in distances_matrix]

    teams = len(schedule_matrix)
    row_size = len(schedule_matrix)
    column_size = len(schedule_matrix) - 1

    for i in range(row_size):
        for j in range(column_size):
            schedule_matrix[i][j] = None


    return distances_matrix, schedule_matrix, teams

def main(distances_matrix, schedule_matrix_original, teams, neighbourhood_size, idle_iterations):

    games_location_matrix, schedule_matrix = calculate_initial_solution(schedule_matrix_original, teams)


    print('Distances matrix')
    for l in distances_matrix:
        print(l)

    print('\nMatchups')
    for l in schedule_matrix:
        print(l)

    print('\nLocations')
    for row in games_location_matrix:
        print(row)




#TODO: Transferir main() para tabu_search
def tabu_search(arg):
    # Step 0: create variables attached to tabu search logic implementation
    graph = [] # configuração do grafo de entrada *Na entrada que for definida/ED*
    iteration = best_iteration = 0
    best_solution = [] # irá guardar a melhor solução
    tabu_list = [] # lista tabu inicialmente vazia
    #capacidade_maxima = 23  Acredito que nao se aplica a nosso caso

    # TODO: criterio parada
    bt_max = 5 # quantidade máxima de iterações sem melhora no valor da melhor solução
    #TODO: maximo vizinhos (?)
        #max_vizinhos = 5 # quantidade máxima de vizinhos

    # Step 1: Generate a random initial solution
    initial_solution = calculate_initial_solution()
    best_solution = initial_solution

    objective_function_value = evaluate_instance_objective_function(graph, initial_solution)

    # Generate neighbours (neighbourhood)
    neighbours = generate_neighbours(best_solution, max_vizinhos, tabu_list)

    # Calculate neighbours avaliation
    neighbours_avaliation = evaluate_neighbours(neighbourhood, graph, max_vizinhos)

    # Obtain index of the best neighbour
    index_best_neighbour = get_index_best_neighbour(neighbours_avaliation, tabu_list, best_solution, neighbours)

    # Check if best neighbour has better avalation than the current best solution
    # TODO: decide how to define the "diff", which data structure
    if neighbours[index_best_neighbour] > best_solution:
        diff =  get_diff(best_solution, neighbours[index_best_neighbour])
        tabu_list.append(diff)
        best_solution = neighbours[index_best_neighbour][:] #copy best solution
        best_iteration +=1

    # Enf of Step1

    # Step2: iterate the generation of neighours until $(bt_max) consecutive iterations do not find a new best solution
    while iteration - best_iteration <= bt_max:
        # Generate neighbours (neighbourhood)
        neighbours = generate_neighbours(best_solution, max_vizinhos, tabu_list)

        # Calculate neighbours avaliation
        neighbours_avaliation = evaluate_neighbours(neighbourhood, graph, max_vizinhos)

        # Obtain index of the best neighbour
        index_best_neighbour = get_index_best_neighbour(neighbours_avaliation, tabu_list, best_solution, neighbours)

        # Check if best neighbour has better avalation than the current best solution
        # TODO: decide how to define the "diff", which data structure
        if neighbours[index_best_neighbour] > best_solution:
            diff =  get_diff(best_solution, neighbours[index_best_neighbour])
            tabu_list.append(diff)
            best_solution = neighbours[index_best_neighbour][:] #copy best solution
            best_iteration +=1

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Process path')
    parser.add_argument('-f', '--txt', required=True, type=str, help='Input instance txt path')
    parser.add_argument('-n', '--size', required=True, type=int, help='Input neighbourhood size')
    parser.add_argument('-i', '--iter', required=True, type=int, help='Input iterations')
    args = parser.parse_args()
    distances_matrix, schedule_matrix, teams = read_instance(args.txt)
    main(distances_matrix, schedule_matrix, teams, args.size, args.iter)
