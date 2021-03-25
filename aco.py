import random


class Graph(object):
    def __init__(self, cost_matrix: list, rank: int, pick_del: list, start: int):
        """
        :param cost_matrix:
        :param rank: rank of the cost matrix
        """
        st = (-1, start)
        pick_del.insert(0, st)
        self.matrix = cost_matrix
        self.rank = rank
        self.pickup = pick_del
        # noinspection PyUnusedLocal
        self.pheromone = [[1 / (rank * rank) for j in range(rank)] for i in range(rank)]


class ACO(object):
    def __init__(self, ant_count: int, generations: int, alpha: float, beta: float, rho: float, q: int,
                 strategy: int):
        """
        :param ant_count:
        :param generations:
        :param alpha: relative importance of pheromone
        :param beta: relative importance of heuristic information
        :param rho: pheromone residual coefficient
        :param q: pheromone intensity
        :param strategy: pheromone update strategy. 0 - ant-cycle, 1 - ant-quality, 2 - ant-density
        """
        self.Q = q
        self.rho = rho
        self.beta = beta
        self.alpha = alpha
        self.ant_count = ant_count
        self.generations = generations
        self.update_strategy = strategy

    def _update_pheromone(self, graph: Graph, ants: list):
        for i, row in enumerate(graph.pheromone):
            for j, col in enumerate(row):
                graph.pheromone[i][j] *= self.rho
                for ant in ants:
                    graph.pheromone[i][j] += ant.pheromone_delta[i][j]

    # noinspection PyProtectedMember
    def solve(self, graph: Graph):
        """
        :param graph:
        """
        best_cost = float('inf')
        best_solution = []
        allow = []
        prob = []
        cur = []
        for gen in range(self.generations):
            # noinspection PyUnusedLocal
            ants = [_Ant(self, graph) for i in range(self.ant_count)]
            for ant in ants:
                # for i in range(14 - 1):
                #     ant._select_next()
                ant._select_next()
                ant.total_cost += graph.matrix[ant.tabu[-1][1]][ant.tabu[0][1]]
                if ant.total_cost < best_cost:
                    best_cost = ant.total_cost
                    best_solution = [] + ant.tabu
                    allow = [] + ant.allowed
                    prob = [] + ant.probabilities
                    cur = ant.current
                # update pheromone
                ant._update_pheromone_delta()
            self._update_pheromone(graph, ants)
            # print('generation #{}, best cost: {}, path: {}'.format(gen, best_cost, best_solution))
        return best_solution, best_cost, allow, prob, cur


class _Ant(object):
    def __init__(self, aco: ACO, graph: Graph):
        self.colony = aco
        self.graph = graph
        self.probabilities = []
        self.total_cost = 0.0
        self.tabu = []  # tabu list
        self.pheromone_delta = []  # the local increase of pheromone
        self.allowed = graph.pickup  # nodes which are allowed for the next selection
        self.eta = [[0 if i == j else 1 / graph.matrix[i][j] for j in range(graph.rank)] for i in
                    range(graph.rank)]  # heuristic information
        start = (-1,29) #random.randint(0, graph.rank - 1)  # start from any node
        self.tabu.append(start)
        self.current = start
        if start[0] != -1:
            self.allowed.remove(start)

    def _select_next(self):
        denominator = 0
        denominator1 = 0
        for i in range(len(self.allowed)):
            denominator += self.graph.pheromone[self.current[1]][self.allowed[i][0]] ** self.colony.alpha * self.eta[self.current[1]][self.allowed[i][0]] ** self.colony.beta
            denominator1 += self.graph.pheromone[self.allowed[i][0]][self.allowed[i][1]] ** self.colony.alpha * self.eta[self.allowed[i][0]][self.allowed[i][1]] ** self.colony.beta
        # noinspection PyUnusedLocal
        probabilities = [0 for i in range(len(self.allowed))]  # probabilities for moving to a node in the next step
        for i in range(len(self.allowed)):
            try:
                # self.allowed.index(i)  # test if allowed list contains i
                probabilities[i] = (self.graph.pheromone[self.current[1]][self.allowed[i][0]] ** self.colony.alpha * \
                    self.eta[self.current[1]][self.allowed[i][0]] ** self.colony.beta) * (self.graph.pheromone[self.allowed[i][0]][self.allowed[i][1]] ** self.colony.alpha * \
                    self.eta[self.allowed[i][0]][self.allowed[i][1]] ** self.colony.beta) / denominator * denominator1
            except ValueError:
                pass  # do nothing
        # select next node by probability roulette
        selected = (-1, 29)
        rand = random.random()
        for i, probability in enumerate(probabilities):
            rand -= probability
            if rand <= 0:
                selected = self.allowed[i]
                break
        print("selected =", selected)
        print("allowed =", self.allowed)
        self.allowed.remove(selected)
        self.tabu.append(selected)
        self.total_cost += self.graph.matrix[self.current[1]][selected[0]] + self.graph.matrix[selected[0]][selected[1]]
        self.current = selected
                

    # noinspection PyUnusedLocal
    def _update_pheromone_delta(self):
        self.pheromone_delta = [[0 for j in range(self.graph.rank)] for i in range(self.graph.rank)]
        tabu_raw = [item for sublist in self.tabu for item in sublist]
        tabu_raw.remove(-1)
        for _ in range(1, len(tabu_raw)):
            i = tabu_raw[_ - 1]
            j = tabu_raw[_]
            if self.colony.update_strategy == 1:  # ant-quality system
                self.pheromone_delta[i][j] = self.colony.Q
            elif self.colony.update_strategy == 2:  # ant-density system
                # noinspection PyTypeChecker
                self.pheromone_delta[i][j] = self.colony.Q / self.graph.matrix[i][j]
            else:  # ant-cycle system
                self.pheromone_delta[i][j] = self.colony.Q / self.total_cost
