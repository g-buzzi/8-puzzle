import math

class Evaluator:
    def __init__(self):
        self.__size = 3

    def distance(self, pos_1, pos_2):
        return abs((pos_1 % self.__size) - (pos_2 % self.__size)) + abs((pos_1 // self.__size) - (pos_2 // self.__size))
    
    def linear_conflict(self, puzzle):
        conflicts = 0 
        for i in range(3):
            for j in range(3):
                if(int(puzzle[i * 3 + j]) != 0 and (int(puzzle[i * 3 + j]) - 1)//3 == i):
                    k = j + 1
                    while k < 3:
                        if(int(puzzle[i * 3 + k]) != 0 and (int(puzzle[i * 3 + k]) - 1)//3 == i and int(puzzle[i * 3 + j]) > int(puzzle[i * 3 + k])):
                            puzzle = self.reserse_linear_conflict(puzzle, i * 3 + j, i * 3 + k)
                            conflicts += 1
                        else:
                            k += 1
        return conflicts
    
    def reserse_linear_conflict(self, puzzle, left_pos, right_pos):
        return puzzle[0:left_pos] + puzzle[right_pos] + puzzle[left_pos] + puzzle[left_pos + 1 : right_pos] + puzzle[right_pos + 1:]
    
    def column_conflict(self, puzzle):
        conflicts = 0 
        for j in range(3):
            for i in range(3):
                if(int(puzzle[i * 3 + j]) != 0 and (int(puzzle[i * 3 + j]) - 1)%3 == j):
                    k = i + 1
                    while k < 3:
                        if(int(puzzle[k * 3 + j]) != 0 and (int(puzzle[k * 3 + j]) - 1)%3 == j and int(puzzle[i * 3 + j]) > int(puzzle[k * 3 + j])):
                            conflicts += 1
                            puzzle = self.reverse_column_conflict(puzzle, i * 3 + j, k * 3 + j)
                        else:
                            k += 1
        return conflicts
    
    def reverse_column_conflict(self, puzzle, up_pos, down_pos):
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
            min_dist = min(self.distance(pos, empty_pos), min_dist)
        return min_dist

    def max_dist_error(self, empty_pos: int, incorrect_positions: list): # Inválido conforme 023156478 quando combinado com a distância.
        max_dist = 0
        for pos in incorrect_positions:
            max_dist = max(self.distance(pos, empty_pos), max_dist)
        return max_dist
    
    # Blocos na posição correta
    def h_a_dumb(self, puzzle):
        cost = 0
        for i in range(3):
            for j in range(3):
                number = int(puzzle[i * 3 + j])
                if number == 0:
                    continue
                if number - 1 != i * 3 + j:
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
                cost += self.distance(i * 3 + j, number - 1)
        return cost
    
    # Distância dos blocos de sua linha e coluna correta + 2 . (número de conflitos lineares)
    def h_a1(self, puzzle):
        cost = 0
        for i in range(3):
            for j in range(3):
                number = int(puzzle[i * 3 + j])
                if number == 0:
                    continue
                cost += self.distance(i * 3 + j, number - 1)
        cost += self.linear_conflict(puzzle) * 2
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
                distancia = self.distance(pos, number - 1)
                cost += distancia
                if distancia > 0:
                    incorrect.append(pos)
        cost += self.linear_conflict(puzzle) * 2
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
                distancia = self.distance(pos, number - 1)
                cost += distancia
                if distancia > 0:
                    incorrect.append(pos)
        cost += self.linear_conflict(puzzle) * 2
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
                distancia = self.distance(pos, number - 1)
                cost += distancia
        cost += self.linear_conflict(puzzle) * 2
        cost += self.column_conflict(puzzle) * 2
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
                distancia = self.distance(pos, number - 1)
                cost += distancia
                if distancia > 0:
                    incorrect.append(pos)
        cost += self.linear_conflict(puzzle) * 2
        cost += self.column_conflict(puzzle) * 2
        cost += 2 * max(self.min_dist_error(empty_pos, incorrect) - 1, 0)
        return cost