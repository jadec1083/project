import operator

import networkx as nx
import matplotlib.pyplot as plt


def plot(points, cost_matrix:list, path: list):
    pos = {}
    x2 = []
    x = []
    y = []
    for point in points:
        x.append(point[0])
        x2.append(point[1])
        y.append(point[1])
    # noinspection PyUnusedLocal
    y = list(map(operator.sub, [max(y) for i in range(len(points))], y))
    # plt.plot(x, y, 'co')

    for _ in range(1, len(path)):
        i = path[_ - 1]
        j = path[_]
        # noinspection PyUnresolvedReferences
        # plt.arrow(x[i], y[i], x[j] - x[i], y[j] - y[i], color='b', length_includes_head=True)

    # noinspection PyTypeChecker
    # plt.xlim(0, max(x) * 1.1)
    # noinspection PyTypeChecker
    # plt.ylim(0, max(y) * 1.1)

    for i in range(len(x)):
        pos[path[i]] = [int(x[path[i]]), int(x2[path[i]])]
        #d[i+1] = {x[i]: y[i]}

    G = nx.Graph()

    m_e =[]
    for i in range(len(cost_matrix)):
        for j in range(len(cost_matrix[i])):
            if cost_matrix[i][j] == 0:
                break
            else:
                m_e.append((i,j,cost_matrix[i][j]))

    for i in range(len(m_e)):
        for x in range(len(path)-1):
            if (path[x] == m_e[i][0] and path[x+1] == m_e[i][1]) or (path[x+1] == m_e[i][0] and path[x] == m_e[i][1]):
                wgt = m_e[i][2]
                G.add_edge(path[x], path[x+1], weight=wgt)
        if (path[0] == m_e[i][0] and path[-1] == m_e[i][1]) or (path[-1] == m_e[i][0] and path[0] == m_e[i][1]):
                wgt = m_e[i][2]
                G.add_edge(path[0], path[-1], weight=wgt)

    elarge = [(u, v) for (u, v, d) in G.edges(data=True) if d['weight'] > 0.5]
    esmall = [(u, v) for (u, v, d) in G.edges(data=True) if d['weight'] <= 0.5]

    # pos = nx.spring_layout(G)  # positions for all nodes
    # plt.figure(dpi=300)
    _, ax = plt.subplots()
    # nodes
    nx.draw_networkx_nodes(G, pos, node_size=200)

    # edges
    nx.draw_networkx_edges(G, pos, edgelist=elarge, arrows=True, arrowstyle='-|>',arrowsize=20)
    nx.draw_networkx_edges(G, pos, edgelist=esmall, arrows=True, arrowsize=20,
                        arrowstyle='-|>',alpha=0.5, edge_color='b', style='dashed')

    # labels
    nx.draw_networkx_labels(G, pos, font_size=5, font_family='sans-serif')
    ax.tick_params(left=True, bottom=True, labelleft=True, labelbottom=True)
    plt.show()
