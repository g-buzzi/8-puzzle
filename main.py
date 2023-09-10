from A import A_star

puzzle = input("Digite o puzzle: ")

while(len(puzzle) != 9):
    puzzle = input("Puzzle deve possuir nove caracteres, digite novamente: ")

algorithm = int(input("Escolha o algoritmo:\n0 - A* com heurística simples\n1 - A* com heurística precisa\n2 - Custo uniforme\n\n"))
A_star(puzzle, algorithm)

