% Hechos
es_animal(perro).
es_animal(gato).

tiene_patas(perro, 4).
tiene_patas(gato, 4).
tiene_patas(ave, 2).

% Regla
es_mamifero(X) :- es_animal(X), tiene_patas(X, 4).
