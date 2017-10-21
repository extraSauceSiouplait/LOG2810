# coding=utf-8
import numpy

def creerGraphe(str):

    try:
        data = open("./" + str, "r")

    except IOError:
        print("Erreur lors de la lecture du fichier: " + str + " . Assurez-vous que celui-ci soit placé à la racine et qu'il ait le bon nom")

    chargingStationsDict = {}
    weightsDict = {}


    for line in data:
        temp = line.strip('\n').strip('\r').split(",")

        if temp.isnumeric():
            for i in range(len(temp)):
                temp[i] = int(temp[i])
                if temp[i] <= 0:
                    raise TypeError("Entier négatif trouvé dans les données de: " + str + " . Assurez vous que celles-ci soit de format:"
                        "x,y,z où les deux premières valeurs sont des ENTIERS POSITIFS et la dernière un RÉEL POSITIF. Ils représentent dans l'ordre, le quartier de départ,"
                        "celui d'arrivée et la distance (en min) entre ceux-ci")
        if len(temp) == 2:
            chargingStationsDict[temp[0]] = temp[1]

        elif len(temp) == 3:

            if (not weightsDict.has_key(temp[0])):
                weightsDict[temp[0]] = {}
            weightsDict[temp[0]][temp[1]] = temp[2]

            if (not weightsDict.has_key(temp[1])):
                weightsDict[temp[1]] = {}
            weightsDict[temp[1]][temp[0]] = temp[2]

    if len(weightsDict) == 0:
        raise TypeError("Aucune donnée de quartiers lues dans le fichier: " + str + " Assurez vous que celles-ci soit de format:"
                        "x,y,z où les deux premières valeurs sont des ENTIERS POSITIFS et la dernière un RÉEL POSITIF. Ils représentent dans l'ordre, le quartier de départ,"
                        "celui d'arrivée et la distance (en min) entre ceux-ci")

    if len(chargingStationsDict) == 0:
        raise TypeError("Aucune station de recharge détectée, la lecture des données de la carte semble toutefois correcte.")


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

def printGraphe(graph):

    for startingVertex, destination in sorted(graph.iteritems()):

        neighbors = "(" + str(startingVertex) + ", " + str(startingVertex) + ", ("

        for destinationVertex, distance in sorted(destination.iteritems()):
            neighbors = neighbors + "(" + str(destinationVertex) + ", " + str(distance) + "mins),"

        neighbors = neighbors[:-1]
        neighbors = neighbors + ")"
        print(neighbors)


def dijkstra(adjacenceList, start, end):

    visited = []
    distances = {}
    predecessors = {}

    if start not in adjacenceList:
        raise TypeError("Le point de départ n\'est pas présent pas dans la carte")
    if end not in adjacenceList:
        raise TypeError("Le point d\'arrivée n\'est pas présent dans la carte")

    #Initialise les coûts (infini pour les
    #sommets non visités
    for vertex in adjacenceList:
        if vertex != start:
            distances[vertex] = float('inf')
            predecessors[vertex] = None

    distances[start] = 0

    while( len(visited) is not len(adjacenceList)):

        #Cherche le sommet non visité avec une distance totale (start --> sommet) minimale
        smallestVertex = min((vertex for vertex in distances if vertex not in visited), key = distances.get)

        if smallestVertex == end:
            return (distances, predecessors)

        visited.append(smallestVertex)

        for voisin, distanceToVoisin in adjacenceList[smallestVertex].items():
            if voisin not in visited:
                newDistance = distances[smallestVertex] + distanceToVoisin
                if newDistance < distances[voisin]:
                    distances[voisin] = newDistance
                    predecessors[voisin] = smallestVertex



def printPath(graph, start, end):


    shortest = dijkstra(graph,start,end)

    path = []
    vertex = end

    while vertex != start:
        path.append(vertex)
        vertex = shortest[1][vertex]

    path.append(start)

    print(list(reversed(path)))


printPath(weights, 1, 3)
printPath(weights, 1, 3)

weights,chargingStations = creerGraphe("arrondissements.txt")
#lireGraphe(weights)
