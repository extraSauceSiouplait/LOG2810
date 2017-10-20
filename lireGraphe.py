import numpy

def creerGraphe(str):

    data = open("./" + str, "r")
    chargingStationsDict = {}
    weightsDict = {}


    for line in data:
        temp = line.strip('\n').strip('\r').split(",")

        if len(temp) == 2:
            for i in range(len(temp)):
                temp[i] = int(temp[i])

            chargingStationsDict[temp[0]] = temp[1]

        elif len(temp) == 3:
            for i in range(len(temp)):
                temp[i] = int(temp[i])

            if (not weightsDict.has_key(temp[0])):
                weightsDict[temp[0]] = {}
            weightsDict[temp[0]][temp[1]] = temp[2]

            if (not weightsDict.has_key(temp[1])):
                weightsDict[temp[1]] = {}
            weightsDict[temp[1]][temp[0]] = temp[2]

    return (weightsDict,chargingStationsDict)

def convertPointToCity(p):
    if(p>19 or p<1):
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
    return cityNames[int(p)-1]

def lireGraphe(graph):
    for startingVertex, destination in sorted(graph.iteritems()):

        neighbors = "(" + str(startingVertex) + ", " + str(startingVertex) + ", ("

        for destinationVertex, distance in sorted(destination.iteritems()):
            neighbors = neighbors + "(" + str(destinationVertex) + ", " + str(distance) + "mins),"
predecessors = {}
        neighbors = neighbors[:-1]
        neighbors = neighbors + ")"
        print(neighbors)


def dijkstra(adjacenceList, start, end, Visited = [], distances = {}, predecessors = {}):


    if start not in adjacenceList:
        raise TypeError("Le point de départ n'est pas présent pas dans la carte")
    if end not in adjacenceList:
        raise  TypeError("Le point d'arrivée n'est pas présent dans la carte")

    #Initialise les coûts (infini pour les
    #sommets non visités
    for vertex in adjacenceList:
        if vertex != start:
            distances[vertex] = float('inf')
            predecessors[vertex] = Null
            notVisited.append(vertex)

    distances[start] = 0

        min(vertex for vertex in distances if vertex not in visited, key= distances.get())

            distances[start] = 0

        for voisin in adjacenceList.items():
            newDistance = distances[]

    #Condition finale si on a trouvé le chemin jusqu'a end
    #On construit le chemin le plus court
    if start == end:

weights,chargingStations = creerGraphe("arrondissements.txt")
lireGraphe(weights)

