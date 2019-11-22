

def main():

    # Step 0: create variables attached to tabu search logic implementation
    graph = [] # configuração do grafo de entrada *Na entrada que for definida/ED*
    iteration = best_iteration = 0
    best_solution = [] # irá guardar a melhor solução
    tabu_list = [] # lista tabu inicialmente vazia
    #capacidade_maxima = 23  Acredito que nao se aplica a nosso caso

    # TODO: criterio parada
        #bt_max = 1 # quantidade máxima de iterações sem melhora no valor da melhor solução
    #TODO: maximo vizinhos (?)
        #max_vizinhos = 5 # quantidade máxima de vizinhos

    # Step 1: Generate a random initial solution
    initial_solution = calculate_initial_solution()
    best_solution = initial_solution

    objective_function_value = evaluate_instance_objective_function(graph, initial_solution)

    # Generate neighbours (neighbourhood)
    neighbours = generate_neighbours(best_solution, max_vizinhos)

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

if __name__ == '__main__':
    main()
