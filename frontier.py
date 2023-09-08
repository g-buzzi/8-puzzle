class Frontier:
    def __init__(self):
        self.__frontier = []
        self.__in_frontier = dict()

    def insert(self, element):
        remove = False
        if(element.puzzle in self.__in_frontier):
            if(element.total_cost >= self.__in_frontier[element.puzzle]):
                return
            remove = True #Estamos assumindo que o custo só aumenta
        self.__in_frontier[element.puzzle] = element.total_cost
        for i in range(len(self.__frontier)):
            if(element.total_cost < self.__frontier[i].total_cost):
                self.__frontier.insert(i, element)
                break
        else:
            self.__frontier.append(element)
        if(remove):
            for i in range(i+1, len(self.__frontier)):
                if(self.__frontier[i].puzzle == element.puzzle):
                    self.__frontier.pop(i)
                    break

    def pop(self):
        element = self.__frontier.pop(0)
        self.__in_frontier.pop(element.puzzle)
        return element
    
    @property
    def size(self):
        return len(self.__frontier)