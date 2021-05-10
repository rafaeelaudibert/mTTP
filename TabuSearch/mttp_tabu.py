from neighbourhood import *

import argparse
import copy
from random import seed


def read_instance(instance_file):
    distance_matrix = []
    with open(instance_file, "r") as f:
        for line in f:
            distance_matrix.append([int(s) for s in line.rstrip(
                "\n\r").split() if s.isdigit()])

    schedule_matrix = [row[:] for row in distance_matrix]

    teams = len(schedule_matrix)
    row_size = len(schedule_matrix)
    column_size = len(schedule_matrix) - 1

    for i in range(row_size):
        for j in range(column_size):
            schedule_matrix[i][j] = None

    return distance_matrix, schedule_matrix, teams


def tabu_search(distance_matrix, model_schedule_matrix, teams, neighbourhood_size, max_iterations=15):
    # Step 0: create variables attached to tabu search logic implementation
    rounds = (teams - 1) * 2
    iteration = best_iteration = 0
    best_solution_schedule, best_solution_location = [], []  # will store best solution
    best_solution = 0
    tabu_list = []  # initially empty tabu list

    # Step 1: Generate a random initial solution
    schedule_matrix, location_matrix = get_initial_solution(
        model_schedule_matrix, teams)
    best_solution_schedule, best_solution_location = schedule_matrix, location_matrix

    best_solution = compute_obj_function(
        distance_matrix, schedule_matrix, location_matrix, teams, rounds)
    print(f"Initial solution is {best_solution}")

    # Enf of Step1

    # Step2: iterate the generation of neighours until $(max_iterations) consecutive iterations do not find a new best solution
    while iteration - best_iteration <= max_iterations:
        iteration += 1
        print(f"Started iteration {iteration}")

        # Generate neighbours (neighbourhood)
        neighbours = generate_neighbours(
            best_solution_schedule, best_solution_location, neighbourhood_size, tabu_list)

        # Calculate neighbours avaliation
        neighbours_avaliation = [compute_obj_function(
            distance_matrix, n_schedule, n_location, teams, rounds) for n_schedule, n_location, _n_change in zip(*neighbours)]

        # Obtain index of the best neighbour
        best_neighbour_idx = neighbours_avaliation.index(
            min(neighbours_avaliation))

        # Check if best neighbour has better avalation than the current best solution
        if min(neighbours_avaliation) < best_solution:
            diff = neighbours[CHANGE][best_neighbour_idx]
            tabu_list.append(diff)

            # copy best solution
            best_solution_schedule = copy.deepcopy(
                neighbours[SCHEDULE][best_neighbour_idx])
            best_solution_location = copy.deepcopy(
                neighbours[LOCATION][best_neighbour_idx])
            best_solution = min(neighbours_avaliation)
            best_iteration = iteration
            print(f"Improved on iteration {best_iteration} to {best_solution}")

    print(f"Final solution is {best_solution}")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Process path')
    parser.add_argument('-f', '--txt', required=True,
                        type=str, help='Input instance txt path')
    parser.add_argument('-n', '--neighbourhood-size', required=True,
                        type=int, help='Input neighbourhood size')
    parser.add_argument('-i', '--iter', required=True,
                        type=int, help='Input iterations')
    parser.add_argument('-s', '--seed', default=1,
                        type=int, help='Random seed number')
    args = parser.parse_args()

    seed(args.seed)
    distance_matrix, model_schedule_matrix, teams = read_instance(args.txt)
    tabu_search(distance_matrix, model_schedule_matrix, teams,
                args.neighbourhood_size, args.iter)
