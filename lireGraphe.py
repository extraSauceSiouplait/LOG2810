# coding=utf-8
import numpy


## @package Utils.GraphInterpretation
#   Ensemble des fonctions utilitaires qui creent le graphe de la ville et
#   calculent le plus court chemin entre deux points.

## isNumeric
#  Verifie si une liste donnee ne contient que des nombres.
#
#  @param list La liste
#
#  @return Un booléen indiquant la réponse
def isNumeric(list):
    for elem in list:
        if not elem.isdigit():
            return False
        else:
            return True


## creerGraphe
#  Extrait d'un fichier texte: les donnes des stations de recharges et celles des quartier de la ville et de la distance entre eux.
#
#  @param str le nom du fichier a lire.
#
#  @return Un tuple contenant la liste d'adjacence du graphe (un dictionnaire) et un dictionnaire des stations de recharge
#
def creerGraphe(str):

    try:
        data = open("./" + str, "r")

    except IOError:
        print("Erreur lors de la lecture du fichier: " + str + " . Assurez-vous que celui-ci soit placé à la racine et qu'il ait le bon nom")

    chargingStationsDict = {}
    weightsDict = {}


    for line in data:
        temp = line.strip('\n').strip('\r').split(",")

        if isNumeric(temp):
            for i in range(len(temp)):
                temp[i] = int(temp[i])
                if temp[i] < 0:
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


## convertPointToCity
#  Converti le nombre representant un quartier en son nom complet.
#
#  @param p L'entier positif representant le quartier a interpreter
#
#  @return Un string contenant le nom du quartier
#
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


## printGraphe
#  Imprime dans STDOUT la representation d'un graphe
#
#  @param graph La liste d'adjacence a imprimer
#
def printGraphe(graph):

    for startingVertex, destination in sorted(graph.iteritems()):

        neighbors = "(" + str(startingVertex) + ", " + str(startingVertex) + ", ("

        for destinationVertex, distance in sorted(destination.iteritems()):
            neighbors = neighbors + "(" + str(destinationVertex) + ", " + str(distance) + "mins),"

        neighbors = neighbors[:-1]
        neighbors = neighbors + ")"
        print(neighbors)

## dijkstra
#  Calcule le plus court chemin entre 2 points d'un graphe A MODIFIER!!!
#
#  @param adjacenceList La liste d'adjacence d'ou tirer les donnees
#  @param start Le point de depart du chemin
#  @param end Le point d'arrivee du chemin
#
#  @return A MODIFIER!!
#
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


## printPath
#  Imprime dans STDOUT le plus court chemin entre deux point d'un graphe
#
#  @param graph La liste d'adjacence d'ou tirer les donnees
#  @param start Le point de depart du chemin
#  @param end Le point d'arrivee du chemin
#
def printShortestPath(graph, start, end):


    shortest = dijkstra(graph,start,end)

    path = []
    vertex = end

    while vertex != start:
        path.append(vertex)
        vertex = shortest[1][vertex]

    path.append(start)

    print(list(reversed(path)))

graphe, stations = creerGraphe("arrondissements.txt")

printShortestPath(graphe, 2, 8)
