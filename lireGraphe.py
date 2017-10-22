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
#  Calcule le plus court chemin entre 1 point d'un graphe et tous les autres points
#
#  @param adjacenceList La liste d'adjacence d'ou tirer les donnees
#  @param start Le point de depart
#
#  @return La liste des distances minimales et le parcours entre le point de départ et tous les points du graphe
#
def dijkstra(adjacenceList, start):

    visited = []
    distances = {}
    predecessors = {}

    if start not in adjacenceList:
        raise TypeError("Le point de départ n\'est pas présent pas dans la carte")

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

        visited.append(smallestVertex)

        for voisin, distanceToVoisin in adjacenceList[smallestVertex].items():
            if voisin not in visited:
                newDistance = distances[smallestVertex] + distanceToVoisin
                if newDistance < distances[voisin]:
                    distances[voisin] = newDistance
                    predecessors[voisin] = smallestVertex

    return (distances, predecessors)

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


#Input: un dictionnaire de dictionnaire qui detaille les arcs et leur cout
#Output: un dictionnaire de dictionnaires.
#	Pour chaque paire (start,end), on obtient un int avec la distance (en minutes) et
#	une liste du de int representant le meilleur chemin entre les deux points
def createDistanceMatrix(graph):
    allDistances = {}
    for start in graph:
        d,p = dijkstra(graph, start)
        allDistances[start] = {}

        for end in graph:
            allDistances[start][end] = convertDistanceAndPath(d,p,start,end)

    return allDistances



#Input: un dictionnaire representant le vecteur obtenue par la fonction dijkstra
#		un dictionnaire representant les meilleur path obtenues par la fonction dijkstra
#		le debut du chemin
#		la fin du chemin
#Output:un tuple representant la distance la plus courte entre deux points (int) et le meilleur chemin (liste de int)
def convertDistanceAndPath(distances,predecessors,start,end):
    d = distances[end]
    path = []
    vertex = end
    while vertex != start:
        path.append(vertex)
        vertex = predecessors[vertex]
    path.append(start)
    path.reverse()
    return d,path



#Input: un dictionnaire de dictionnaires representant les distance et les path d'un point a un autre
#		le debut du chemin
#		la fin du chemin
#		un int 0 ou 1 representant si on regarde le trajet d'un drone 3.3A (0) ou un drone 5A (1)
#		un int representant la grosseur du colis a livrer: small(0), medium(1), large(2)
#Output:	un tuple ayant 3 valeurs:
#				Si le trajet est possible
#				La duree du trajet en minutes
#				la charge qui reste dans la pile (float qui peut etre negatif dans le cas ou le trajet est impossible)
def directRoute(distanceMatrix,start,end,bigDrone,packageSize,consumption=[[10.0,20.0,40.0],[10.0,15.0,25.0]]):
    dist = distanceMatrix[start][end][0]
    c = consumption[bigDrone][packageSize]/10.0

    remainingCharge = 100.0 - float(dist)*c
    if remainingCharge < 20.0:
        return (False,dist,distanceMatrix[start][end][1])
    else:
        return (True,dist,distanceMatrix[start][end][1])


#Inputs:	dictionnaire de dictionnaires qui represente toutes les distances directes et les paths entre deux points
#			dictionnaire des stations de charge qui definit quelles arrets sont des stations de charge
#			debut du chemin
#			fin de chemin
#			dimension du colis
#Outputs:	une tuple qui indique
#				Si le transport sera possible
#				Le temps de transport
#				Le parcours optmial
#				L'energie qu'il reste dans la pile
def checkForPossibleRoutes(distanceMatrix,chargingStations,start,end,packageSize):
	path = getRoute(distanceMatrix,withoutValues(chargingStations,[0]),start,end,0,packageSize)
	if path[0]:
		return (path,0)
	else:
		path = getRoute(distanceMatrix,withoutValues(chargingStations,[0]),start,end,1,packageSize)
		if path[0]:
			return (path,1)
		else:
			return (path,-1)



#Inputs: les deux chemins a combiner
#Output: un tuple avec
#				un bool qui indique le respect des conditions
#				le temps requis pour completer le trajet (temps route1 + temps route2 + 20)
#				le chemin complet
def combineRoutes(route1,route2):
	conditionsRespected = route1[0] and route2[0]
	if conditionsRespected:
		timeInMins = route1[1] + route2[1] + 20
	else:
		timeInMins = float("inf")
	path = route1[2] + route2[2]
	return (conditionsRespected, timeInMins, path)



#Input	distanceMatrix
#		la liste des stations de chargement
#		le debut du trajet
#		la fin du trajet
#		le modele de drone
#		la taille du colis
#Output	un tuple indiquant
#			un bool qui indique si le trajet est possible avec les conditions donnees
#			le temps requis au trajet
#			le chemin pris (lorsqu'il y a des doublons, ca represente les arrets aux stations de chargement)
def getRoute(distanceMatrix,chargingStations,start,end,bigDrone,packageSize):
	path = directRoute(distanceMatrix,start,end,bigDrone,packageSize)
	if path[0]:
		return path
	else:
		routes = []
		for c in chargingStations:
			route1 = getRoute(distanceMatrix,withoutKeys(chargingStations,[c]),start,c,bigDrone,packageSize)
			route2 = getRoute(distanceMatrix,withoutKeys(chargingStations,[c]),c,end,bigDrone,packageSize)
			r = combineRoutes(route1,route2)
			if r[0]:
				routes.append(r)
		if not routes:
			return path
		else:
			bestRoute = (True,float("inf"),[])
			for route in routes:
				if route[0] and (route[1] < bestRoute[1]):
					bestRoute = route
			return bestRoute



#Input	un dictionnaire
#		une liste de valeurs a enlever
#Output	une copie du dictinnaire sans les pairs qui contiennent cette valeur
def withoutValues(dic,vals):
	copy = {}
	for e in dic:
		for val in vals:
			if dic[e] != val:
				copy[e] = dic[e]
	return copy


#Input	un dictionnaire
#		une liste de keys a enlever
#Output	une copie du dictionnaire sans les pairs ayant ces keys
def withoutKeys(dic,keys):
	copy = {}
	for e in dic:
		for key in keys:
			if not (e == key):
				copy[e] = dic[e]
	return copy
	

def afficherParcours(path,taille):
	if path[0][2][0] == path[0][2][-1]:
		print("Le debut et la fin fin sont au meme endroit. Une livraison n'est donc pas necessaire...")
	elif not path[0][0]:
		print("Il est impossible de completer securitairement cette livraison.")
	else:
		if taille == 0:
			t = "petit"
		elif taille == 1:
			t = "moyen"
		else:
			t = "large"
		print("Taille du colis: " + t)
		print("De " + str(path[0][2][0]) + " a " + str(path[0][2][-1]))
		print("Duree totale: " + str(path[0][1]) + " minutes")
		print("Le trajet a suivre: ")
		previous = path[0][2][-1]
		trajet = str(path[0][2][0])
		for city in path[0][2][1:]:
			if city == previous:
				trajet += " (arret de recharge)"
			else:
				trajet = trajet + " -> " + str(city)
			previous = city
		print(trajet)
		if path[1] == 1:
			print("Il serait necessaire d'utiliser le drone a 5A.")
		else:
			print("Il est possible d'utiliser le drone a 3.3A.")

weights,chargingStations = creerGraphe("arrondissements.txt")
#lireGraphe(weights)

allDist = createDistanceMatrix(weights)

trip = (8,18)		#	(a,b) le trajet du point a au point b
package = 1			#	small(0), medium(1), large(2)

afficherParcours(checkForPossibleRoutes(allDist,chargingStations,trip[0],trip[1],package),package)


"""
for start in range(1,19+1):
	for end in range(1,19+1):
		trip = (start,end)
		#print("from " + str(start) + " to " + str(end))
		for package in range(3):
			#print("\tpackage size: "+str(package))
			#print("\t\t" + str(checkForPossibleRoutes(allDist,chargingStations,trip[0],trip[1],package)))
			afficherParcours(checkForPossibleRoutes(allDist,chargingStations,trip[0],trip[1],package),package)
"""




