# coding=utf-8
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

            chargingStationsDict[int(temp[0])] = int(temp[1])

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

        neighbors = neighbors[:-1]
        neighbors = neighbors + ")"
        print(neighbors)


def dijkstra(adjacenceList, start, end):

    visited = []
    distances ={}
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





#Input: un dictionnaire de dictionnaire qui detaille les arcs et leur cout
#Output: un dictionnaire de dictionnaires. 
#	Pour chaque paire (start,end), on obtient un int avec la distance (en minutes) et 
#	une liste du de int representant le meilleur chemin entre les deux points
def createDistanceMatrix(graph):
	allDistances = {}
	for start in graph:
		allDistances[start] = {}
		for end in graph:
			d,p = dijkstra(graph,start,end)
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
def directRoutePossible(distanceMatrix,start,end,bigDrone,packageSize,consumption=[[10.0,20.0,40.0],[10.0,15.0,25.0]]):
	dist = distanceMatrix[start][end][0]
	c = consumption[bigDrone][packageSize]/10.0

	remainingCharge = 100.0 - float(dist)*c
	if remainingCharge < 20.0:
		return (False,dist,remainingCharge)
	else:
		return (True,dist,distanceMatrix[start][end][1],remainingCharge)



#Input:		dictionnaire de dictionnaire representant les distance et les path d'un point a un autre
#			un dictionnaire des stations de chargement
#			debut d'un trajet
#			arret a une station de charge
#			fin du trajet
#			un int 0 ou 1 representant si on regarde le trajet d'un drone 3.3A (0) ou un drone 5A (1)
#			un int representant la grosseur du colis a livrer: small(0), medium(1), large(2)
#Output:	Un tuple avec deux valeurs
#				Boolean qui represente si le trajet est possible
#				le meilleur chemin a prendre			
def computeShortestCompoundDistance(distancesMatrix,chargingStations,nStations,a,b,bigDrone,packageSize):
	routes = []
	for cStation in chargingStations:
		if chargingStations[cStation] == 1:
			print("cStation: " + str(cStation))
			route1 = directRoutePossible(distancesMatrix,a,cStation,bigDrone,packageSize)
			route2 = directRoutePossible(distancesMatrix,cStation,b,bigDrone,packageSize)
			if route1[0] and route2[0]:
				routes.append((route1,route2))

	if not routes:
		#recusively call compute shortest routes?
		if nStations == 0:
			print("no possible routes")
			return False
		else:
			print("must dive deeper")
			for cStations in chargingStations:
				if chargingStations == 1:
					print("verifying possible routes passing though charging station " + str(cStation))
					route1 = computeShortestCompoundDistance(distancesMatrix,chargingStations,nStations-1,a,cStations,bigDrone,packageSize)
					route2 = computeShortestCompoundDistance(distancesMatrix,chargingStations,nStations-1,cStations,b,bigDrone,packageSize)
					#if route1[0] and route2[0]:
						#return 
		return False


	print("route possible")
	bestRoute = routes[0]
	for route in routes:
		if (route[0][1] + route[1][1]) < bestRoute[0][1] + bestRoute[1][1]:
			bestRoute = route
	print(bestRoute)
	return (True,bestRoute[0][1]+bestRoute[1][1]+20.0,bestRoute[0][2][:-1]+bestRoute[1][2])
	#returns (possible route , distance + 20 mins , (path a-b, path b-c)



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
	route = directRoutePossible(distanceMatrix,start,end,0,packageSize)
	if route[0]:	
		print("direct route possible")
		print(route)
		return route
		#probably need to return path and total time
	else:
		print("no direct route possible. verifying compound route")
		nChargingStations = sum(x == 1 for x in chargingStations.values())
		route = computeShortestCompoundDistance(distanceMatrix,chargingStations,nChargingStations,start,end,0,packageSize)
		if route[0]:
			print(route)
			return route
		else:
			print("no route") 
			return False




weights,chargingStations = creerGraphe("arrondissements.txt")
#lireGraphe(weights)

allDist = createDistanceMatrix(weights)

point = (8,15)
package = 2

checkForPossibleRoutes(allDist,chargingStations,point[0],point[1],package)[0]

"""
point = (8,12)
print("Distance between " + str(point[0]) + " and " + str(point[1])+ ": " + str(allDist[point[0]][point[1]][0]))
print("path: " + str(allDist[point[0]][point[1]][1]))
print(directRoutePossible(allDist,point[0],point[1],0,2))

point = (8,17)
print("Distance between " + str(point[0]) + " and " + str(point[1])+ ": " + str(allDist[point[0]][point[1]][0]))
print("path: " + str(allDist[point[0]][point[1]][1]))
print(directRoutePossible(allDist,point[0],point[1],0,2))

point = (8,17)
print("Distance between " + str(point[0]) + " and " + str(point[1])+ ": " + str(allDist[point[0]][point[1]][0]))
print("path: " + str(allDist[point[0]][point[1]][1]))
print(directRoutePossible(allDist,point[0],point[1],0,2))
"""




