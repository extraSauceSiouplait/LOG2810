import numpy


def createGraph(str):
    data = open("./" + str, "r")
    chargingStations = []
    weights = []

    for line in data:
        temp = line.strip('\n').split(",")

        if len(temp) == 2:
            temp = [int(x) for x in temp]
            chargingStations.append(temp)

        elif len(temp) == 3:
            temp = [int(x) for x in temp]
            weights.append(temp)

    weightsGraph = numpy.zeros(shape=(len(chargingStations), len(chargingStations)))

    for arc in weights:
        weightsGraph[arc[0] - 1, arc[1] - 1] = arc[2]
        weightsGraph[arc[1] - 1, arc[0] - 1] = arc[2]

    return (weightsGraph, chargingStations)


def convertPointToCity(p):
    if (p > 19 or p < 1):
        return "not in MTL"
    cityNames = ["Ahuntsic-Cartierville",
                 "Anjou",
                 "Cote-des-Neiges-Notre-Dame-de-Grace",
                 "Lachine",
                 "LaSalle",
                 "Le Plateau Mont-Royal",
                 "Le Sud-Ouest",
                 "L'Ile-Bizard-Sainte-Genevieve",
                 "Mercier-Hochelaga-Maisonneuve",
                 "Montreal-Nord",
                 "Outremont",
                 "Pierrefonds-Roxboro",
                 "Riviere-des-Prairies-Pointe-aux-Trembles",
                 "Rosemont-La-Petite-Patrie",
                 "Saint-Laurent",
                 "Saint-Leonard",
                 "Verdun",
                 "Ville-Marie",
                 "Villeray-Saint-Michel-Parc-Extension"]
    return cityNames[p - 1]


def displayGraph(graph):
    for j in range(graph.shape[0]):
        neighbors = "(" + str(convertPointToCity(j + 1)) + ", " + str(j + 1) + ", ("
        for i in range(graph.shape[0]):
            if (graph[j, i] != 0):
                neighbors = neighbors + "(" + str(convertPointToCity(i + 1)) + ", " + str(graph[j, i]) + "min)"
        neighbors = neighbors + ")"
        print(neighbors)
    print("done")


g = createGraph("arrondissements.txt")
displayGraph(g[0])
