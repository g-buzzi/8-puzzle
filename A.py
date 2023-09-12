from evaluator import Evaluator
from frontier import Frontier
from node import Node
from time import time

def A_star(puzzle, algorithm):
    evaluator = Evaluator()
    match algorithm:
        case 0:
            heuristic = evaluator.h_a_simple
        case 1:
            heuristic = evaluator.h_a6
        case _:
            heuristic = lambda x:0
    frontier = Frontier()
    visited = dict()

    t0 = time()
    frontier.insert(Node(puzzle, 0, heuristic(puzzle), ''))
    while(True):
        node = frontier.pop()
        visited[node.puzzle] = True
        if(node.puzzle == "123456780"):
            break
        derivations = node.derive(heuristic)
        for derivation in derivations:
            if(derivation.puzzle not in visited):
                frontier.insert(derivation)
    t1 = time()
    
    print("Resultado: " + node.puzzle)
    print("Passos: " + node.steps)
    print("Número de passos: " + str(len(node.steps)))
    print("Tamanho da fronteira: " + str(frontier.size))
    print("Número de visitados: " + str(len(visited)))
    print("Tempo total:", round(t1 - t0, 4))
            