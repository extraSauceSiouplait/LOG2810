import Queue
import random

class Delivery:
	def __init__(self,origin,destination,weight):
		self.origin = origin
		self.destination = destination
		self.weight = int(weight)
	

class Drone:

	def __init__(self,location,maxLoad):
		self.currentLocation = location
		self.destination = location
		self.deliveries = []
		self.currentLoad = 0
		self.remainingCapacity = maxLoad
		self.maximumLoad = maxLoad

	def updateWeight(self):
            self.currentLoad = 0
            self.remainingCapacity = self.maximumLoad
            for d in self.deliveries:
                self.currentLoad += d.weight
		self.remainingCapacity -= d.weight

	def deliveryIsPossible(self,d):
		if d.weight > self.remainingCapacity:
		    #print("too much weight: Max="+str(self.remainingCapacity)+" weight="+str(d.weight))	
                    return False
		if d.origin != self.currentLocation:
                    #print("Not at correct starting location")
	    	    return False
		if len(self.deliveries) == 0 and self.destination != self.currentLocation and d.destination != self.destination:
		    #print("This drone is already assigned to go somewhere")
                    return False
		if len(self.deliveries) > 0 and d.destination != self.deliveries[0].destination:
		    #print("Not going to the same place")
                    return False
		return True

	def addPackage(self,d):
		if not self.deliveryIsPossible(d):
			#print(str(self.remainingCapacity)+"\tCannot add package to this drone")
			return False
		else:
			self.deliveries.append(d)
			self.updateWeight()
			self.destination = d.destination
			return True

	def droneIsAvailable(self):
                #if the drone has any deliveries in its list
		if len(self.deliveries) > 0:
			return False
                #if the drone's destination differes from its current location
		elif self.currentLocation != self.destination :
			return False
		else:
			return True

	def deployTo(self,location):
		self.destination = location

	def deliver(self,keeper):
		if self.currentLocation != self.destination or len(self.deliveries)>0:
			self.currentLocation = self.destination
                        if len(self.deliveries)>0:
                            d = self.deliveries[0]
			    self.deliveries.remove(d)
			    self.currentLoad = self.currentLoad - d.weight
			    self.remainingCapacity = self.remainingCapacity + d.weight
			    keeper.addDelivery()
			return True
		else:
			#print("No need to move from here")
			if self.currentLoad != 0.0 or self.remainingCapacity != self.maximumLoad or self.destination != self.currentLocation:
				print("There was a mistake somewhere")
				return False
			else:
				return True

	def displayDroneStats(self):
		print("Max weight: " + str(self.maximumLoad))
		print("RemainingCapacity: " + str(self.remainingCapacity))
		print("Current Location: " + self.currentLocation)
		print("Destination: " + self.destination)

		
class DroneFleet:
	def __init__(self,startingLocation):
		self.units = []
		self.types = {}
		self.home = startingLocation
	
	def addDroneType(self,weightLimitInGrams):
		self.types[weightLimitInGrams] = 0
	
	def addNdrones(self,weightLimitInGrams,nDrones):
		self.types[weightLimitInGrams] = self.types[weightLimitInGrams] + nDrones
		for x in range(nDrones):
			self.units.append(Drone(self.home,weightLimitInGrams))
		
	def nDronesAvailable(self,weightLimitInGrams):
		count = 0
		for drone in self.units:
			if drone.remainingCapacity == weightLimitInGrams:
				count += 1
		return count

	def listDronesInFleet(self):
		for model in self.types:
			print("This fleet contains a total of " + str(self.types[model]) + " drone that is able to carry a maximum of " + str(model) + " grams.")
			print(str(self.nDronesAvailable(model)) + " of which are available (not currently assigned to a task)")

	def summarizeFleetStats(self):
		print("______________________________________________________________________________________")
		print("Available\tLocation\tDestination\tMaxCapacity\tRemainingCap")
		for unit in self.units:
			print(str(unit.droneIsAvailable())+"\t\t"+unit.currentLocation+"\t\t"+unit.destination+"\t\t"+str(unit.maximumLoad)+"\t\t"+str(unit.remainingCapacity))
		print("______________________________________________________________________________________")


	def addDelivery(self,d):
		keyList = self.types.keys()
		keyList.sort()
		for model in keyList:
			for unit in self.units:
				if unit.maximumLoad == model:
                                        #print("Load size = " + str(d.weight) + "\tMax load: " + str(model))
					if unit.addPackage(d):
						return True
		return False

	def sendADroneTo(self,d):
                #get list of all drone types
		keyList = self.types.keys()
                
                #put them in numerical order
		keyList.sort()
		
                for model in keyList:
                        #print("now looking at model #" + str(model))
			for unit in self.units:
				if unit.maximumLoad == model:
                                    if unit.droneIsAvailable(): 
					if d.weight <= unit.remainingCapacity:
                                            #unit.remainingCapacity -= d.weight
                                            unit.deployTo(d.origin)
					    return True
		return False

	def deliverPackages(self,keeper):
		for unit in self.units:
			unit.deliver(keeper)

	def reequilibrateFleet(self,automat):
                #1) List all postal codes
                #print("beginning postalCodes")
		listOfPostalCodes = list(automat.unorganizedPostalCodes)
                #print(listOfPostalCodes)
		#print(listOfPostalCodes)
                #2) For each non-available drone
                for unit in self.units:
                        #print(str(unit.maximumLoad) +"\t" + str(unit.droneIsAvailable()))
			if not unit.droneIsAvailable():
                            if unit.destination in listOfPostalCodes:
                                #3) subtract their destination from the list of postal codes
                                #print(unit.destination)
                                listOfPostalCodes.remove(unit.destination)
                #print(listOfPostalCodes)
                #4) Dispatch them to different locations selected at random
                for unit in self.units:
                    if unit.droneIsAvailable():
                        #print(listOfPostalCodes)
                        #print("remaining Postal codes:")
                        #print(listOfPostalCodes)
                        d = random.sample(listOfPostalCodes,1)[0]
                        #print(d)
                        unit.deployTo(d)
                        listOfPostalCodes.remove(d)
                        #print("deploying unit to " + d)
				


class DeliveryRequest:
	def __init__(self,defaultLocation):
		self.requestQueue = Queue.Queue()
		self.priorityQueue = Queue.Queue()
	def traiterLesRequetes(self,filename,auto,fleet,keeper):
		data = open("./" + filename, "r")
		for line in data:
		    temp = line.strip('\n').strip('\r').split(" ")
	            #print(temp)
		    if (auto.validatePostalCode(temp[0],keeper) and auto.validatePostalCode(temp[1],keeper) and (temp[2]).isdigit()):
			print("origin: " + temp[0] + "\tDestination: " + temp[1] + "\tWeight: " + temp[2])
			d = Delivery(temp[0],temp[1],temp[2])
			self.requestQueue.put(d)
		    else:
                        print("A request did not meet standards:")
			if(not auto.validatePostalCode(temp[0],keeper)):
			    print("\t" + temp[0] + " is not a valid postal code")
			if(not auto.validatePostalCode(temp[1],keeper)):
			    print("\t" + temp[1] + " is not a valid postal code")
			if(not temp[2].isdigit()):
			    print("\t" + temp[2] + " is not a valid weight")
                
                print("creating temp queue")
		tempQueue = Queue.Queue()
                
                #fleet.summarizeFleetStats()
                
                print("verifying prioroty queue")
	        while(not self.priorityQueue.empty()):
			delivery = self.priorityQueue.get()
			if not fleet.addDelivery(delivery):
				fleet.sendADroneTo(delivery)
				tempQueue.put(delivery)				
                
                #fleet.summarizeFleetStats()
                
                print("verifying reqQueue")
		while(not self.requestQueue.empty()):
			delivery = self.requestQueue.get()
                        #print("delivery weight: " + str(delivery.weight))
			if not fleet.addDelivery(delivery):
                            if delivery.weight <= max(fleet.types.keys()):
                                #print("delivery not possible at the moment. Sending a drone to pickup location")
			        fleet.sendADroneTo(delivery)
			        tempQueue.put(delivery)
                            else:
                                print("The maximum deliverable weight is "+str(max(fleet.types.keys()))+". With a weight of "+str(delivery.weight)+", this delivery is not possible.")
                                keeper.addInvalidRequest()
	        
                
                #fleet.summarizeFleetStats()
                
                print("transferring contents of temp queue to priorityqueue")
		while(not tempQueue.empty()):
			self.priorityQueue.put(tempQueue.get())

                print("fleet equilibration")
		fleet.reequilibrateFleet(auto)
                
                #fleet.summarizeFleetStats()
                
                print("package delivery")
                fleet.deliverPackages(keeper)
                
                #fleet.summarizeFleetStats()



class RecordKeeper:
	def __init__(self):
		self.nSuccessfulDeliveries = 0
		self.nInvalidRequests = 0
	def addDelivery(self):
		self.nSuccessfulDeliveries += 1
	def addInvalidRequest(self):
		self.nInvalidRequests += 1
	def getDroneAverageDelivery(self,weightLimitInGrams,fleet):
		return (self.nSuccessfulDeliveries/fleet.types[weightLimitInGrams])
        def imprimerLesStatistiques(self):
                print("Le nombre de livraisons completes a date: "+str(self.nSuccessfulDeliveries))
                print("Le nombre de requetes invalides: " + str(self.nInvalidRequests))
                #print le nombre de drones dans chaque quartier
                #print le nombre moyen de colis transportes par un drone a petite capacite
                #print le nombre moyen de colis transportes par un drone a grande capacite

class PostalCodeAutomaton:
	possibleStates = [0,1,2,3,4,5,6]

	def __init__(self):
		self.name = "Dave"
		self.recognizedPostalCodes = {}
		self.unorganizedPostalCodes = []

	def validatePostalCode(self,postalCode,keeper):
		currentState = self.possibleStates[0]
		code = list(postalCode)
		while(currentState != self.possibleStates[6]):
			if (currentState == self.possibleStates[0]):
				if (not code[0] in self.recognizedPostalCodes):
					#print(str(code[0]) + "not in dictionnary")
					keeper.addInvalidRequest()
					return False
				else:
					currentState = self.possibleStates[1]
			if (currentState == self.possibleStates[1]):
				if (not code[1] in self.recognizedPostalCodes[code[0]]):
					#print(str(code[1]) + "not in dictionnary")
					keeper.addInvalidRequest()
					return False
				else:
					currentState = self.possibleStates[2]
			if (currentState == self.possibleStates[2]):
				if (not code[2] in self.recognizedPostalCodes[code[0]][code[1]]):
					#print(str(code[2]) + "not in dictionnary")
					keeper.addInvalidRequest()
					return False
				else:
					currentState = self.possibleStates[3]
			if (currentState == self.possibleStates[3]):
				if (not code[3] in self.recognizedPostalCodes[code[0]][code[1]][code[2]]):
					#print(str(code[3]) + "not in dictionnary")
					keeper.addInvalidRequest()
					return False
				else:
					currentState = self.possibleStates[4]
			if (currentState == self.possibleStates[4]):
				if (not code[4] in self.recognizedPostalCodes[code[0]][code[1]][code[2]][code[3]]):
					#print(str(code[4]) + "not in dictionnary")
					keeper.addInvalidRequest()
					return False
				else:
					currentState = self.possibleStates[5]
			if (currentState == self.possibleStates[5]):
				if (not code[5] in self.recognizedPostalCodes[code[0]][code[1]][code[2]][code[3]][code[4]]):
					#print(code[5])
					#print(self.recognizedPostalCodes[code[0]][code[1]][code[2]][code[3]][code[4]])
					#print("last char not in dictionnary")
					keeper.addInvalidRequest()
					return False
				else:
					currentState = self.possibleStates[6]

		return True

	def creerArbreAddresses(self,filename):
		self.recognizedPostalCodes = {}
		data = open("./" + filename, "r")
		for line in data:
			temp = line.strip('\n').strip('\r').strip(' ')
			word = list(temp)
			if len(word) != 6:
				print("This file contains invalid entries.")
			else:
				if (not word[0] in self.recognizedPostalCodes):
					self.recognizedPostalCodes[word[0]] = {}
				if (not word[1] in self.recognizedPostalCodes[word[0]]):
					self.recognizedPostalCodes[word[0]][word[1]] = {}
				if (not word[2] in self.recognizedPostalCodes[word[0]][word[1]]):
					self.recognizedPostalCodes[word[0]][word[1]][word[2]] = {}
				if (not word[3] in self.recognizedPostalCodes[word[0]][word[1]][word[2]]):
					self.recognizedPostalCodes[word[0]][word[1]][word[2]][word[3]] = {}
				if (not word[4] in self.recognizedPostalCodes[word[0]][word[1]][word[2]][word[3]]):
					self.recognizedPostalCodes[word[0]][word[1]][word[2]][word[3]][word[4]] = {}
				if (not word[5] in self.recognizedPostalCodes[word[0]][word[1]][word[2]][word[3]][word[4]]):
					self.recognizedPostalCodes[word[0]][word[1]][word[2]][word[3]][word[4]][word[5]] = {}
				self.recognizedPostalCodes[word[0]][word[1]][word[2]][word[3]][word[4]][word[5]] = temp
				self.unorganizedPostalCodes.append(temp)		
		
#def main:


#Step1: Create Automaton
#dave = PostalCodeAutomaton()

#Step2: Feed automaton postal codes
#dave.creerArbreAddresses("CodesPostaux.txt")

#Step3: Create record keeper
#history = RecordKeeper()

#Step4: Create drone fleet
#fleet = DroneFleet("H1W1B2")
#types = [[5000,5],[1000,10]]
#fleet.addDroneType(5000)
#fleet.addDroneType(1000)
#fleet.addNdrones(types[0][0],types[0][1])
#fleet.addNdrones(types[1][0],types[1][1])

#print(fleet.types.keys())

#Step5: Dispatch drones to random places on the map
#fleet.reequilibrateFleet(dave)
#fleet.deliverPackages(history)


#print("successful deliveries: " + str(history.nSuccessfulDeliveries))

#Step6: Create DeliveryRequest object to handle requests
#requests = DeliveryRequest("H3S2B2")

#Step7: Process request
#requests.traiterLesRequetes("requetes1.txt",dave,fleet,history)
#print("successful deliveries: " + str(history.nSuccessfulDeliveries))

#Step8: (repeat)
#requests.traiterLesRequetes("requetes2.txt",dave,fleet,history)
#print("successful deliveries: " + str(history.nSuccessfulDeliveries))

#requests.traiterLesRequetes("requetes3.txt",dave,fleet,history)
#print("successful deliveries: " + str(history.nSuccessfulDeliveries))

#requests.traiterLesRequetes("requetes4.txt",dave,fleet,history)
#print("successful deliveries: " + str(history.nSuccessfulDeliveries))
#requests.traiterLesRequetes("requetes5.txt",dave,fleet,history)
#print("successful deliveries: " + str(history.nSuccessfulDeliveries))
#requests.traiterLesRequetes("requetes6.txt",dave,fleet,history)
#print("successful deliveries: " + str(history.nSuccessfulDeliveries))
#requests.traiterLesRequetes("requetes7.txt",dave,fleet,history)
#print("successful deliveries: " + str(history.nSuccessfulDeliveries))
#requests.traiterLesRequetes("requetes8.txt",dave,fleet,history)
#print("successful deliveries: " + str(history.nSuccessfulDeliveries))
#for x in range(0,10):
    #requests.traiterLesRequetes("r0.txt",dave,fleet,history)
    #print("successful deliveries: " + str(history.nSuccessfulDeliveries))
