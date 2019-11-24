#!/usr/bin/env glpsol

# Define o número de equipes.
param numTeams;

# Define o conjunto das equipes.
set T := 1..numTeams;

# Define a distância entre as cidades das equipes.
param dist {T,T};

# Define o nro de slots por turno do campeonato.
param Nbar := numTeams - 1;

# Quantidade máxima de partidas em sequência away e home.
param U := 3;

# Define o conjunto dos slots do campeonato completo.
set S := 1..2*Nbar;

# Define o conjunto de arcos do grafo de cada equipe.
# As triplas são (i, j, s), e indicam a equipe se deslocando de 
# i, no slot s, para jogar contra j no slot s+1.
set A {t in T} :=
   setof {j in T} (t, j, 0) union       # Arcos saintes do SOURCE
   setof {i in T} (i, t, 2*Nbar) union  # Arcos entrantes no SINK
   setof {i in T, j in T, s in S: i != j and s != 2*Nbar} (i, j, s) union # Arcos entre nós de cidades não t
   setof {s in S: s != 2*Nbar} (t, t, s) # Arco entre nós da cidade de t
;

# Define as variáveis de decisão do problema.
var x {t in T, (i, j, s) in A[t]} binary;

# Define a função objetivo que minimiza a distância percorrida.
minimize totalTravelDist: sum {t in T} sum {(i, j, s) in A[t]} dist[i, j] * x[t, i, j, s];

# Restrição de fluxo para cada grafo de cada equipe.
s.t. flowConservation {t in T, j in T, s in S}:
   sum {(i, j, s-1) in A[t]} x[t, i, j, s-1] - sum {(j, i, s) in A[t]} x[t, j, i, s] == 0;

# Restrição que força uma equipe a confrontar todas os seus adversários, 
# em algum dos turnos do campeonato.
s.t. confrontAllOpponents {t in T, i in T: i != t}:
   sum {s in S} sum {(i, j, s) in A[t]} x[t, i, j, s] == 1;

# Restrições de ligação entre os grafos das equipes.
s.t. linkFlows {t in T, s in S}:
   sum {i in T: i != t} sum {(i, j, s) in A[t]} x[t, i, j, s] +
   sum {tp in T: tp != t} sum {(t, j, s) in A[tp]} x[tp, t, j, s] == 1;

# Limita a quantidade de disputas "away".
s.t. boundAwayMatches {t in T, s in S: s <= 2*Nbar - U}:
   sum {u in 0..U-1} sum {(i, j, s+u) in A[t]: i != t and j != t} x[t, i, j, s+u] <= U-1;

# Limita a quantidade de disputas "home".
s.t. boundHomeMatches {t in T, s in S: s <= 2*Nbar - U}:
   sum {u in 0..U-1} sum {(i, j, s+u) in A[t]: i == t and j == t} x[t, i, j, s+u] <= U-1;

# Restrição referente ao turno e contra-turno espelhado
s.t. mirroredGames {t in T, tbar in T, s in 0..(Nbar - 1): t != tbar}:
  sum {(j, tbar, s) in A[t]: tbar != j} x[t, j, tbar, s] - sum {(j, t, s + Nbar) in A[t]: t != j} x[tbar, j, t, s + Nbar] == 0;

end;

