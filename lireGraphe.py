import numpy
#from nested_dict import nested_dict
def creerGraphe(str):

    data = open("./" + str, "r")
    chargingStationsDict = {}
    weightsDict = {} #nested_dict()

    for line in data:
        temp = line.strip('\n').split(",")

        if len(temp) == 2:
			chargingStationsDict[temp[0]] = temp[1]
            #temp = [int(x) for x in temp]
            #chargingStations.append(temp)

        elif len(temp) == 3:
			if (not weightsDict.has_key(temp[0])):
				weightsDict[temp[0]] = {}
			weightsDict[temp[0]][temp[1]] = temp[2]

			if (not weightsDict.has_key(temp[1])):
				weightsDict[temp[1]] = {}
			weightsDict[temp[1]][temp[0]] = temp[2]
				
            #temp = [int(x) for x in temp]
            #weights.append(temp)

    #weightsGraph = numpy.zeros(shape=(len(chargingStations), len(chargingStations)))

    #for arc in weights: 
		#weightsGraph[arc[0]-1,arc[1]-1] = arc[2]
		#weightsGraph[arc[1]-1,arc[0]-1] = arc[2]
		
	#weightsGraph[weightsGraph==0] = -1
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
	for vertex in graph:
		neighbors = "(" + vertex + ", " + vertex + ", ("
		for end in graph[vertex]:
			neighbors = neighbors + "(" + end + ", " + graph[vertex][end] + "mins),"

		neighbors = neighbors[:-1]
		neighbors = neighbors + ")"
		print(neighbors)
		
	#for j in range(graph.shape[0]):
		#neighbors = "(" + str(convertPointToCity(j+1)) + ", " + str(j+1) + ", ("
		#for i in range(graph.shape[0]):
			#if (graph[j,i] != 0):
				#neighbors = neighbors + "(" + str(convertPointToCity(i+1)) + ", " + str(graph[j,i]) + "min)"
		#neighbors = neighbors + ")"
		#print(neighbors)
	#print("done")

#def dijkstra(adjacenceList, start ,end):
	#distances = 
	



weights,chargingStations = creerGraphe("arrondissements.txt")
lireGraphe(weights)

