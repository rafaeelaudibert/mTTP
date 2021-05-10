from random import randint, choice
import copy

MAX_GAMES = 3
HOME, AWAY = 1, -1
SCHEDULE, LOCATION, CHANGE = 0, 1, 2


def fill_teams_and_its_opponents(teams):
    teams_and_its_opponents = []

    # Will be generated n lists
    for i in range(teams):
        # Creates indexes from 0..n
        # Only if the actual index != actual team i.e. Team 1 doesn't face team 1
        teams_and_its_opponents.append(
            [num for num in range(teams) if num != i])

    return teams_and_its_opponents


def isValidOpponent(chosen_opponent, i, j, schedule_matrix):
    return schedule_matrix[i][j] == None and schedule_matrix[chosen_opponent][j] == None


def select_opponent(i, j, teams_and_its_opponents, schedule_matrix):
    # Pega os oponentes que o time atual ainda tem que enfrentar
    # E cria uma copia da lista dos oponentes que o time tem que enfrentar
    remaining_opponents_list = teams_and_its_opponents[i].copy()
    remaining_opponents_size = len(remaining_opponents_list)
    processing = True

    # Enquanto não achar um oponente válido no confronto atual
    while processing:
        rand_index = randint(0, remaining_opponents_size - 1)
        chosen_opponent = remaining_opponents_list[rand_index]

        if isValidOpponent(chosen_opponent, i, j, schedule_matrix):
            teams_and_its_opponents[i].remove(chosen_opponent)
            teams_and_its_opponents[chosen_opponent].remove(i)
            processing = False
        else:
            # Caso o oponente selecionado não possa jogar nessa rodada (mesmo tendo que jogar contra esse oponente, ele ta busy essa rodada já)
            # Se remove ele da copia da lista de oponentes que o time atual ainda tem que enfrentar (para nao perder a original)
            remaining_opponents_list.remove(chosen_opponent)
            remaining_opponents_size -= 1

    return chosen_opponent


# Extende as colunas da matrix para 2n colunas copiando as n colunas originais
def mirror_schedule(schedule_matrix):
    return [row + row for row in schedule_matrix]


def compute_obj_function(distance_matrix, schedule_matrix,
                         location_matrix, teams, rounds):
    # Cummulator variable
    distance = 0

    # Compute for each team
    for team in range(teams):
        last_played = HOME  # Remembering that it starts at home

        # For each round
        for round in range(rounds):
            # If play away on this round
            if location_matrix[team][round] == AWAY:
                # Use ternary operator to know if account distance from home or from other team field last match
                distance += distance_matrix[team if last_played == HOME else schedule_matrix[team][round - 1]
                                            ][schedule_matrix[team][round]]
                last_played = AWAY
            else:  # Play home this round
                if last_played == AWAY:
                    distance += distance_matrix[schedule_matrix[team]
                                                [round - 1]][team]
                last_played = HOME
        distance += distance_matrix[schedule_matrix[team][rounds - 1]][team]

    return distance


# TODO: Not generate tabu neighbours
def generate_neighbours(schedule_solution, location_solution, max_neighbours, tabu_list):
    # Return variables
    neighbours_schedule = []
    neighbours_location = []
    neighbours_changes = []

    # Helper variables
    teams = len(schedule_solution)
    rounds = len(schedule_solution[0])
    rounds_per_turn = rounds // 2

    # Generate one new neighbour for each max_vizinhos
    HAS, RS, TS = range(3)
    neighbours = 0
    iterations = 0
    while neighbours < max_neighbours:
        iterations += 1
        schedule = copy.deepcopy(schedule_solution)
        location = copy.deepcopy(location_solution)
        chosen = choice([HAS, RS, TS])
        if chosen == HAS:
            team_i = choice(range(teams))
            team_j = choice(list(set(range(teams)) - set([team_i])))
            round_match = schedule[team_i].index(team_j)
            tabu_tuple = (HAS, team_i, team_j)

            location[team_i][round_match] *= -1
            location[team_j][round_match] *= -1
            location[team_i][round_match + rounds_per_turn] *= -1
            location[team_j][round_match + rounds_per_turn] *= -1

            # As this can change model feasibility with MAX_GAMES restriction
            # Check if there is any row with more than MAX_GAMES added unintentionally
            should_not_add = False
            for row in location:
                for i in range(rounds + 1):
                    seq = row[max(0, i - (MAX_GAMES + 1)):i]
                    if sum(seq) == AWAY * (MAX_GAMES + 1) or sum(seq) == HOME * (MAX_GAMES + 1):
                        should_not_add = True
            if tabu_tuple in tabu_list or should_not_add:
                continue

            neighbours_changes.append(tabu_tuple)

        elif chosen == RS:
            round_i = choice(range(rounds_per_turn))
            round_j = choice(
                list(set(range(rounds_per_turn)) - set([round_i])))
            tabu_tuple = (RS, round_i, round_j)

            for team in range(teams):
                schedule[team][round_i], schedule[team][round_j] = schedule[team][round_j], schedule[team][round_i]
                location[team][round_i], location[team][round_j] = location[team][round_j], location[team][round_i]
                schedule[team][round_i + rounds_per_turn], schedule[team][round_j +
                                                                          rounds_per_turn] = schedule[team][round_j + rounds_per_turn], schedule[team][round_i + rounds_per_turn]
                location[team][round_i + rounds_per_turn], location[team][round_j +
                                                                          rounds_per_turn] = location[team][round_j + rounds_per_turn], location[team][round_i + rounds_per_turn]

            # As this can change model feasibility with MAX_GAMES restriction
            # Check if there is any row with more than MAX_GAMES added unintentionally
            should_not_add = False
            for row in location:
                for i in range(rounds + 1):
                    seq = row[max(0, i - (MAX_GAMES + 1)):i]
                    if sum(seq) == AWAY * (MAX_GAMES + 1) or sum(seq) == HOME * (MAX_GAMES + 1):
                        should_not_add = True
            if tabu_tuple in tabu_list or should_not_add:
                continue

            neighbours_changes.append(tabu_tuple)
        elif chosen == TS:
            team_i = choice(range(teams))
            team_j = choice(list(set(range(teams)) - set([team_i])))
            round_match = schedule[team_i].index(team_j)
            tabu_tuple = (TS, team_i, team_j)

            for round in range(rounds):
                if round != round_match and round != round_match + rounds_per_turn:  # If not one against each other
                    # Store variables
                    against_i, location_against_i = schedule[team_i][round], location[team_i][round]
                    against_j, location_against_j = schedule[team_j][round], location[team_j][round]

                    # Play against the one other was playing
                    schedule[team_i][round] = against_j
                    # Other play against the current team
                    schedule[against_j][round] = team_i
                    # Change location where current team is playing
                    location[team_i][round] = location_against_j

                    # Play against the one current team was playing
                    schedule[team_j][round] = against_i
                    # The one current team was play against plays the other team
                    schedule[against_i][round] = team_j
                    # Change location where other team is playing
                    location[team_j][round] = location_against_i

            # As this can change model feasibility with MAX_GAMES restriction
            # Check if there is any row with more than MAX_GAMES added unintentionally
            should_not_add = False
            for row in location:
                for i in range(rounds + 1):
                    seq = row[max(0, i - (MAX_GAMES + 1)):i]
                    if sum(seq) == AWAY * (MAX_GAMES + 1) or sum(seq) == HOME * (MAX_GAMES + 1):
                        should_not_add = True
            if tabu_tuple in tabu_list or should_not_add:
                continue

            neighbours_changes.append(tabu_tuple)

        neighbours_schedule.append(schedule)
        neighbours_location.append(location)
        neighbours += 1

    print(f"Generated {neighbours} neighbours in {iterations} iterations")
    return neighbours_schedule, neighbours_location, neighbours_changes


def calculate_games_location(mirrored_schedule_matrix, teams, rounds):
    games_location_matrix = [
        [None] * rounds for row in mirrored_schedule_matrix]

    try:
        local_or_visitant = choice([-1, 1])
        for row in range(teams):
            place_sequence = randint(0, MAX_GAMES)
            # Itera so metade das colunas, outra metade preenche pelo complemento
            for column in range(int(rounds/2)):
                # Se a posicao atual já ta preenchida
                if games_location_matrix[row][column] != None:
                    # Caso seja o inicio de uma nova sequencia ajusta isso (I.E seta que agora proximos jogos vao ser away ou home e inicia contador em 0)
                    if games_location_matrix[row][column] != local_or_visitant:
                        local_or_visitant = games_location_matrix[row][column]
                        place_sequence = 1
                        if place_sequence == MAX_GAMES:
                            place_sequence = 0
                            local_or_visitant *= -1
                        continue
                    # Se seguir no mesmo sentido so aumenta contador da sequencia (I.E. continua sendo away ou continua sendo local)
                    else:
                        place_sequence += 1

                # Se nao tava preenchido entao continua a sequencia atual e só aumenta contador
                else:
                    opponent = mirrored_schedule_matrix[row][column]
                    # Seta o confronto para ambos os times
                    games_location_matrix[row][column] = local_or_visitant
                    games_location_matrix[opponent][column] = - \
                        local_or_visitant

                    # Seta o complemento na 2a rodada
                    games_location_matrix[row][column +
                                               int(rounds/2)] = -local_or_visitant
                    games_location_matrix[opponent][column +
                                                    int(rounds/2)] = local_or_visitant

                # SE chegou no maximo de sequencia de jogos local/visitante, muda para a proxima iteracao e zera contador
                place_sequence += 1
                if place_sequence == MAX_GAMES:
                    place_sequence = 0
                    local_or_visitant *= -1

    except Exception as e:
        print(e)

    # Check if there is any row with more than MAX_GAMES added unintentionally
    for row in games_location_matrix:
        for i in range(rounds + 1):
            seq = row[max(0, i - (MAX_GAMES + 1)):i]
            if sum(seq) == AWAY * (MAX_GAMES + 1) or sum(seq) == HOME * (MAX_GAMES + 1):
                raise Exception('MAX_GAMES exceeded')

    return games_location_matrix


def get_initial_solution(model_schedule_matrix, teams):
    i = 0
    rounds = teams - 1
    mirrored_schedule_matrix = []
    cant_found = True

    while cant_found:
        i += 1
        schedule_matrix = [row[0:-1] for row in model_schedule_matrix]

        try:
            teams_and_its_opponents = fill_teams_and_its_opponents(teams)

            # Para cada linha e cada coluna
            # Se a posicao do confronto ainda nao foi preenchida
            # Seleciona um oponente e marca o confronto pra ambos
            for j in range(teams-1):
                for i in range(teams):
                    if schedule_matrix[i][j] is None:
                        opponent = select_opponent(
                            i, j, teams_and_its_opponents, schedule_matrix)
                        schedule_matrix[i][j] = opponent
                        schedule_matrix[opponent][j] = i

            # Havia sido calculado para apenas 1 turno, pro 2o turno se espelham todos os confrontos
            mirrored_schedule_matrix = mirror_schedule(schedule_matrix)

            # Para a localizacao dos jogos, se avaliam todos os jogos programados da schedule
            games_location_matrix = calculate_games_location(
                mirrored_schedule_matrix, teams, rounds*2)

            cant_found = False
        except Exception as e:
            pass

    return mirrored_schedule_matrix, games_location_matrix
