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

    for arc in enumerate(weights):
        weightsGraph[arc[1]][[arc[2]] = arc[3]
        weightsGraph[arc[2]][[arc[1]] = arc[3] 
    
    return weightsGraph
