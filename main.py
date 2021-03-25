import math

from aco import ACO, Graph,_Ant
from plot import plot


def distance(city1: dict, city2: dict):
    return math.sqrt((city1['x'] - city2['x']) ** 2 + (city1['y'] - city2['y']) ** 2)


def main():
    cities = []
    points = []
    pickups = []
    with open('./data/chn31.txt') as f:
        for line in f.readlines():
            city = line.split(' ')
            cities.append(dict(index=city[0], x=int(city[1]), y=int(city[2])))
            points.append((int(city[1]), int(city[2])))
    with open('./data/picdev.txt') as f:
        for line in f.readlines():
            picup = line.split(' ')
            pickups.append((int(picup[0]),int(picup[1])))
    cost_matrix = []
    rank = len(cities)
    # print(pickups)
    # print(rank)
    for i in range(rank):
        row = []
        for j in range(rank):
            row.append(distance(cities[i], cities[j]))
        cost_matrix.append(row)
    aco = ACO(10, 100, 1.0, 10.0, 0.5, 10, 2)
    start = 29
    graph = Graph(cost_matrix, rank, pickups, start)
    path, cost, allowed, prob, cur = aco.solve(graph)
    
    print(prob)
    print('cost: {}, path: {}'.format(cost, path))
    print(allowed)
    
    # m_e =[]
    # for i in range(len(cost_matrix)):
    #     for j in range(len(cost_matrix[i])):
    #         if cost_matrix[i][j] == 0:
    #             break
    #         else:
    #             m_e.append((i,j,cost_matrix[i][j]))
    # print(m_e)
    plot(points, cost_matrix, path)

if __name__ == '__main__':
    main()
