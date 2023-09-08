class Node:
    def __init__(self, puzzle: str, cost: int, heuristic: int, steps: str):
        self.__puzzle = puzzle
        self.__cost = cost
        self.__heuristic = heuristic
        self.__steps = steps

    @property
    def puzzle(self):
        return self.__puzzle
    
    @property
    def steps(self):
        return self.__steps

    @property
    def total_cost(self):
        return self.__cost + self.__heuristic
    
    def derive(self, heuristic):
        position = self.__puzzle.find("0")
        line = position // 3
        column = position % 3
        derivations = []
        if(line > 0):
            new_puzzle = self.__puzzle[0:position - 3] + "0" + self.__puzzle[position - 2 : position] + self.__puzzle[position-3] + self.__puzzle[position+1:]
            derivations.append(Node(new_puzzle, self.__cost + 1, heuristic(new_puzzle), self.__steps + '↑'))
        if(line < 2):
            new_puzzle = self.__puzzle[0:position] + self.__puzzle[position + 3] + self.__puzzle[position + 1: position + 3] + "0" + self.__puzzle[position+4:]
            derivations.append(Node(new_puzzle, self.__cost + 1, heuristic(new_puzzle), self.__steps + '↓'))
        if(column > 0):
            new_puzzle = self.__puzzle[0:position -1] + "0" + self.__puzzle[position -1] + self.__puzzle[position + 1:]
            derivations.append(Node(new_puzzle, self.__cost + 1, heuristic(new_puzzle), self.__steps + '←' ))
        if(column < 2):
            new_puzzle = self.__puzzle[0:position] + self.__puzzle[position + 1] + "0" + self.__puzzle[position + 2:]
            derivations.append(Node(new_puzzle, self.__cost + 1, heuristic(new_puzzle), self.__steps + '→'))
        return derivations
    
    def print(self):
        print(self.__puzzle[0:3])
        print(self.__puzzle[3:6])
        print(self.__puzzle[6:9])

    def __str__(self) -> str:
        return self.__puzzle + ": " + str(self.total_cost)
