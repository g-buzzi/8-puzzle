import math

class Evaluator:
    def __init__(self):
        self.__size = [3, 3]

    def distancia(self, posicao_1, posicao_2):
        return abs((posicao_1 % self.__size[0]) - (posicao_2 % self.__size[0])) + abs((posicao_1 // self.__size[1]) - (posicao_2 // self.__size[1]))
    
    def conflito_linear(self, puzzle):
        conflicts = 0 
        for i in range(3):
            for j in range(3):
                if(int(puzzle[i * 3 + j]) != 0 and (int(puzzle[i * 3 + j]) - 1)//3 == i):
                    k = j + 1
                    while k < 3:
                        if(int(puzzle[i * 3 + k]) != 0 and (int(puzzle[i * 3 + k]) - 1)//3 == i and int(puzzle[i * 3 + j]) > int(puzzle[i * 3 + k])):
                            puzzle = self._reverte_conflito_linear(puzzle, i*3 + j, i*3 + k)
                            conflicts += 1
                        else:
                            k += 1
        return conflicts
    
    def _reverte_conflito_linear(self, puzzle, left_pos, right_pos):
        return puzzle[0:left_pos] + puzzle[right_pos] + puzzle[left_pos] + puzzle[left_pos + 1 : right_pos] + puzzle[right_pos + 1:]
    
    def conflito_colunar(self, puzzle):
        conflicts = 0 
        for j in range(3):
            for i in range(3):
                if(int(puzzle[i * 3 + j]) != 0 and (int(puzzle[i * 3 + j]) - 1)%3 == j):
                    k = i + 1
                    while k < 3:
                        if(int(puzzle[k * 3 + j]) != 0 and (int(puzzle[k * 3 + j]) - 1)%3 == j and int(puzzle[i * 3 + j]) > int(puzzle[k * 3 + j])):
                            conflicts += 1
                            puzzle = self._reverte_conflito_colunar(puzzle, i * 3 + j, k * 3 + j)
                        else:
                            k += 1
        return conflicts
    
    def _reverte_conflito_colunar(self, puzzle, up_pos, down_pos):
        distance = down_pos - up_pos
        if (distance == 3):
            return puzzle[0:up_pos] + puzzle[down_pos] + puzzle[up_pos + 1: down_pos] + puzzle[up_pos] + puzzle[down_pos + 1: ]
        elif(distance == 6):
            return puzzle[0:up_pos] + puzzle[down_pos] + puzzle[up_pos + 1: up_pos + 3] + puzzle[up_pos] + puzzle[up_pos + 4: down_pos] + puzzle[up_pos + 3] + puzzle[down_pos + 1 :]
    
    def min_dist_error(self, empty_pos: int, incorrect_positions: list):
        if(len(incorrect_positions) == 0):
            return 0
        min_dist = math.inf
        for pos in incorrect_positions:
            min_dist = min(self.distancia(pos, empty_pos), min_dist)
        return min_dist

    def max_dist_error(self, empty_pos: int, incorrect_positions: list): # Inválido conforme 023156478 quando combinado com a distância.
        max_dist = 0
        for pos in incorrect_positions:
            max_dist = max(self.distancia(pos, empty_pos), max_dist)
        return max_dist
    
    # Blocos na posição correta
    def h_a_dumb(self, puzzle):
        cost = 0
        for i in range(3):
            for j in range(3):
                number = int(puzzle[i * 3 + j])
                if number == 0:
                    continue
                if number - 1 != i*3 + j:
                    cost += 1
        return cost

    # Distância dos blocos de sua linha e coluna correta
    def h_a_simple(self, puzzle):
        cost = 0
        for i in range(3):
            for j in range(3):
                number = int(puzzle[i * 3 + j])
                if number == 0:
                    continue
                cost += self.distancia(i*3 + j, number - 1)
        return cost
    
    # Distância dos blocos de sua linha e coluna correta + 2 . (número de conflitos lineares)
    def h_a1(self, puzzle):
        cost = 0
        for i in range(3):
            for j in range(3):
                number = int(puzzle[i * 3 + j])
                if number == 0:
                    continue
                cost += self.distancia(i*3 + j, number - 1)
        cost += self.conflito_linear(puzzle) * 2
        return cost
    
    # Distância dos blocos de sua linha e coluna correta + 2 . (número de conflitos lineares) + 2.(distância do vazio até o bloco em posição incorreta mais próximo - 1)
    def h_a2(self, puzzle):
        cost = 0
        incorrect = []
        empty_pos = 0
        for i in range(3):
            for j in range(3):
                pos = i * 3 + j
                number = int(puzzle[pos])
                if number == 0:
                    empty_pos = pos
                    continue
                distancia = self.distancia(pos, number - 1)
                cost += distancia
                if distancia > 0:
                    incorrect.append(pos)
        cost += self.conflito_linear(puzzle) * 2
        print("Min_dist: " + str(self.min_dist_error(empty_pos, incorrect)))
        cost += 2 * max(self.min_dist_error(empty_pos, incorrect) - 1, 0)
        return cost
    
    # Distância dos blocos de sua linha e coluna correta + 2 . (número de conflitos lineares) + (distância do vazio até o bloco em posição incorreta mais distante - 1)
    def h_a3(self, puzzle): # Inválido conforme 023156478
        cost = 0
        incorrect = []
        empty_pos = 0
        for i in range(3):
            for j in range(3):
                pos = i * 3 + j
                number = int(puzzle[pos])
                if number == 0:
                    empty_pos = pos
                    continue
                distancia = self.distancia(pos, number - 1)
                cost += distancia
                if distancia > 0:
                    incorrect.append(pos)
        cost += self.conflito_linear(puzzle) * 2
        print("Max_dist: " + str(self.min_dist_error(empty_pos, incorrect)))
        cost += max(self.max_dist_error(empty_pos, incorrect) - 1, 0)
        return cost

    # Distância dos blocos de sua linha e coluna correta + 2 . (número de conflitos lineares) + 2 . (número de conflitos colunares)
    def h_a4(self, puzzle):
        cost = 0
        for i in range(3):
            for j in range(3):
                pos = i * 3 + j
                number = int(puzzle[pos])
                if number == 0:
                    continue
                distancia = self.distancia(pos, number - 1)
                cost += distancia
        cost += self.conflito_linear(puzzle) * 2
        cost += self.conflito_colunar(puzzle) * 2
        return cost
    
    # Distância dos blocos de sua linha e coluna correta + 2 . (número de conflitos lineares) + 2 . (número de conflitos colunares) + 2.(distância do vazio até o bloco em posição incorreta mais próximo - 1)
    def h_a6(self, puzzle):
        cost = 0
        incorrect = []
        empty_pos = 0
        for i in range(3):
            for j in range(3):
                pos = i * 3 + j
                number = int(puzzle[pos])
                if number == 0:
                    empty_pos = pos
                    continue
                distancia = self.distancia(pos, number - 1)
                cost += distancia
                if distancia > 0:
                    incorrect.append(pos)
        cost += self.conflito_linear(puzzle) * 2
        cost += self.conflito_colunar(puzzle) * 2
        cost += 2 * max(self.min_dist_error(empty_pos, incorrect) - 1, 0)
        return cost