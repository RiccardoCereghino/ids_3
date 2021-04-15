from functools import reduce

import networkx as nx
import matplotlib.pyplot as plt
from collections import OrderedDict

players = [
    (1, {"nome": "Perin"}),
    (55, {"nome": "Masiello"}),
    (21, {"nome": "Radovanovic"}),
    (4, {"nome": "Criscito"}),
    (99, {"nome": "Czyborra"}),
    (20, {"nome": " Strootman"}),
    (47, {"nome": " Badelj"}),
    (16, {"nome": "Zajic"}),
    (77, {"nome": "Zappacosta"}),
    (9, {"nome": "Scamacca"}),
    (23, {"nome": "Destro"})
]

dataset = [(1, 55, 21.0), (55, 1, 34.0), (1, 21, 54.0), (21, 1, 43.0), (1, 4, 23.0), (4, 1, 12.0), (4, 55, 56.0),
           (55, 4, 23.0), (21, 55, 10.0), (55, 21, 34.0), (21, 4, 34.0), (4, 21, 44.0), (1, 99, 21.0), (99, 1, 5.0),
           (99, 55, 3.0), (55, 99, 6.0), (99, 21, 47.0), (99, 21, 47.0), (20, 21, 15.0), (20, 47, 80.0), (20, 99, 16.0),
           (20, 77, 35.0), (16, 21, 5.0), (16, 20, 34.0), (16, 47, 45.0), (16, 77, 22.0), (16, 4, 15.0), (16, 9, 15.0),
           (16, 23, 25.0), (16, 21, 12.0), (77, 21, 10.0), (77, 47, 35.0), (77, 9, 28.0), (77, 23, 25.0),
           (77, 16, 25.0), (77, 20, 32.0), (23, 9, 15.0), (9, 23, 12.0), (23, 77, 12.0), (9, 77, 11.0), (9, 16, 15.0),
           (23, 16, 21.0), (23, 20, 2.0), (23, 21, 4.0), (23, 47, 15.0), (23, 99, 11.0), (1, 23, 25.0), (1, 9, 14.0),
           (21, 9, 8.0), (21, 23, 15.0), (4, 9, 5.0), (4, 23, 4.0), (47, 9, 15.0), (47, 23, 15.0)]

if __name__ == '__main__':
    players_dict = dict(players)
    g = nx.DiGraph()

    g.add_weighted_edges_from(dataset)

    nx.draw(g, with_labels=True)
    plt.show()

    in_degree_view = g.in_degree(g.nodes, weight='weight')
    for number, passes in in_degree_view:
        players_dict[number]["in_passes"] = passes

    out_degree_view = g.out_degree(g.nodes, weight='weight')

    for number, passes in out_degree_view:
        players_dict[number]["out_passes"] = passes

    for k, v in players_dict.items():
        print("({}) {} ha passato la palla {} volte ed ha ricevuto la palla {} volte".format(k, v["nome"], v["out_passes"], v["in_passes"]))

    print("In ordine, i giocatori piu' centrali nel gioco:")
    ug = nx.to_undirected(g)
    closeness = [(k, v) for k, v in sorted(nx.closeness_centrality(ug).items(), key=lambda item: item[1], reverse=True)]
    for number, rate in closeness:
        print("({}) {}".format(number, players_dict[number]["nome"]))

    print("In ordine, i giocatori che facilitano di piu' il passaggio di palla:")
    betweenness = [(k, v) for k, v in sorted(nx.betweenness_centrality(ug).items(), key=lambda item: item[1], reverse=True)]
    for number, rate in betweenness:
        print("({}) {}".format(number, players_dict[number]["nome"]))


    d_g = g.subgraph([1, 4, 21, 55])
    d_passes = reduce(lambda r, x: r + x, [x[2] for x in d_g.edges.data('weight')], 0)

    c_g = g.subgraph([99, 20, 47, 16, 77])
    c_passes = reduce(lambda r, x: r + x, [x[2] for x in c_g.edges.data('weight')], 0)

    a_g = g.subgraph([9, 23])
    a_passes = reduce(lambda r, x: r + x, [x[2] for x in a_g.edges.data('weight')], 0)

    print("Difesa ha passato: {}, centrocampo: {} e attacco {}", d_passes, c_passes, a_passes)

    print("Pagerank, valore piu alto implica che il gioctore ha ricevuto la palla piu volte di quella che l'ha passata.")
    print(nx.pagerank(g))
