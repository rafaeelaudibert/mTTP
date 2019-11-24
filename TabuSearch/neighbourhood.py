from random import randint
from random import seed
seed(1)

MAX_GAMES = 3

def fill_teams_and_its_opponents(teams):
    teams_and_its_opponents = []
    #Will be generated n lists
    for i in range(teams):
        line = []
        #Creates indexes from 0..n
        for num in range(teams):
            #Append the index only if the actual index != actual team i.e. Team 1 doesn't face team 1
            if num != i:
                line.append(num)
        teams_and_its_opponents.append(line)

    return teams_and_its_opponents


def isValidOpponent(chosen_opponent,i,j,schedule_matrix):
    return schedule_matrix[i][j] == None and schedule_matrix[chosen_opponent][j] == None

def select_opponent(i, j, teams_and_its_opponents, schedule_matrix):
    #Pega os oponentes que o time atual ainda tem que enfrentar
    #E cria uma copia da lista dos oponentes que o time tem que enfrentar
    remaining_opponents_lst = teams_and_its_opponents[i].copy()
    remaining_opponents_size = len(remaining_opponents_lst)
    processing = True

    #Enquanto não achar um oponente válido no confronto atual
    while processing:
        rand_index = randint(0, remaining_opponents_size - 1)
        chosen_opponent = remaining_opponents_lst[rand_index]

        if isValidOpponent(chosen_opponent,i,j,schedule_matrix):
            teams_and_its_opponents[i].remove(chosen_opponent)
            teams_and_its_opponents[chosen_opponent].remove(i)
            processing = False
        else:
            #Caso o oponente selecionado não possa jogar nessa rodada (mesmo tendo que jogar contra esse oponente, ele ta busy essa rodada já)
            #Se remove ele da copia da lista de oponentes que o time atual ainda tem que enfrentar (para nao perder a original)
            remaining_opponents_lst.remove(chosen_opponent)
            remaining_opponents_size -= 1

    return chosen_opponent

def mirror_schedule(schedule_matrix):
    #Extende as colunas da matrix para 2n colunas copiando as n colunas originais
    mirrored_schedule_matrix = []
    for row in schedule_matrix:
        new_line = row + row
        mirrored_schedule_matrix.append(new_line)
    return mirrored_schedule_matrix

def calculate_games_location(mirrored_schedule_matrix, teams, rodadas):
    games_location_matrix = []
    for row in mirrored_schedule_matrix:
        new_line = [None] * rodadas
        games_location_matrix.append(new_line)

    try:
        local_or_visitant = 1
        for row in range(teams):
            place_sequence = 0
            #Itera so metade das colunas, outra metade preenche pelo complemento
            for column in range(int(rodadas/2)):
                #Se a posicao atual já ta preenchida
                if games_location_matrix[row][column] != None:
                    #Caso seja o inicio de uma nova sequencia ajusta isso (I.E seta que agora proximos jogos vao ser away ou home e inicia contador em 0)
                    if games_location_matrix[row][column] != local_or_visitant:
                        local_or_visitant = games_location_matrix[row][column]
                        place_sequence = 1
                        if place_sequence == MAX_GAMES:
                            place_sequence = 0
                            local_or_visitant *= -1
                        continue
                    #Se seguir no mesmo sentido so aumenta contador da sequencia (I.E. continua sendo away ou continua sendo local)
                    else:
                        place_sequence += 1

                #Se nao tava preenchido entao continua a sequencia atual e só aumenta contador
                else:
                    opponent = mirrored_schedule_matrix[row][column]
                    #Seta o confronto para ambos os times
                    games_location_matrix[row][column] = local_or_visitant
                    games_location_matrix[opponent][column] =  -local_or_visitant

                    #Seta o complemento na 2a rodada
                    games_location_matrix[row][column + int(rodadas/2)] = -local_or_visitant
                    games_location_matrix[opponent][column + int(rodadas/2)] =  local_or_visitant


                #SE chegou no maximo de sequencia de jogos local/visitante, muda para a proxima iteracao e zera contador
                place_sequence +=1
                if place_sequence == MAX_GAMES:
                    place_sequence = 0
                    local_or_visitant *= -1

    except Exception as e:
        print(e)


    return games_location_matrix

def calculate_initial_solution(schedule_matrix_original, teams):
    i = 0
    rodadas = teams - 1
    mirrored_schedule_matrix = []
    vamo = True
    while vamo:
        i+=1
        schedule_matrix = [row[0:-1] for row in schedule_matrix_original]
        try:
            teams_and_its_opponents = fill_teams_and_its_opponents(teams)

            #Para cada linha e cada coluna
            for j in range(teams-1):
                for i in range(teams):
                    #Se a posicao do confronto ainda nao foi preenchida
                    if schedule_matrix[i][j] == None:
                        #Seleciona um oponente e marca o confronto pra ambos
                        opponent =  select_opponent(i,j, teams_and_its_opponents, schedule_matrix)
                        schedule_matrix[i][j] = opponent
                        schedule_matrix[opponent][j] = i


            #Havia sido calculado para apenas 1 turno, pro 2o turno se espelham todos os confrontos
            mirrored_schedule_matrix = mirror_schedule(schedule_matrix)

            #Para a localizacao dos jogos, se avaliam todos os jogos programados da schedule
            games_location_matrix = calculate_games_location(mirrored_schedule_matrix, teams, rodadas*2)

            vamo = False
        except Exception as e:
            # print(e)
            pass



    return games_location_matrix, mirrored_schedule_matrix

        # print('opponent = ', opponent)
