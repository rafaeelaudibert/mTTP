/* 
 * mTTP problem MathProg Modeling
 *
 */

# Parameter which indicates the number of teams
param T_size integer;

# Teams set.
set T := 1..T_size;

# Distance between each team pair
param dist{T, T} integer default 0 >= 0;

# Maximum games that can be played in a sequence of "home" or "away" games
param U default 3 >= 1;

# Round sets
set S := 0..((2 * (T_size - 1)) + 1)

# Variáveis de decisão.
# Modela se iremos, para o time t, sair da casa do time i para a do time j no tempo s
var used_edge{t in T, i in T, j in T, s in S} binary;

# Objective function
# Minimize the cost for traveling in the mTTP
minimize distance: sum {t in T, i in T, j in T, s in S} dist[i, j] * used_edge[t, i, j, s];

# Each team t must play once at every opponent's venue
s.t. playAwayOnce {t in T, i in T diff {t}}: sum {s in 1..(2 * (T_size - 1)), j in T} used_edge[t, i, j, s] == 1

# Restrição de capacidade das arestas
# s.t. limCapacidade {v1 in V, v2 in V}: edge_flow[v1, v2] <= E_capacidade[v1, v2];

# Restrição de obediencia a quantidade de valores em cada nodo
# s.t. restrDemanda {v in V}; 


# Restrições do número máximo de bilhetes que podem ser reservados.
# s.t. limReservas {(c1,c2) in V, t in T}: x[c1,c2,t] <= maxBilhetes[c1,c2,t];


# Restrições de capacidade da aeronave.
# s.t. capacidadeAero {e in E}:
#   sum {(i,j) in TR[e], t in T} x[i,j,t] <= 30;

# Fim do bloco de modelo.
end; 

