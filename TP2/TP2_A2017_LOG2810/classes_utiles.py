import Queue

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

	def updateWeight(self,weight):
		self.currentLoad += weight
		self.remainingCapacity -= weight

	def deliveryIsPossible(self,d):
		if d.weight > self.remainingCapacity:
			return False
		if d.origin != self.currentLocation:
			return False
		if len(self.deliveries) == 0 and self.destination != self.currentLocation and d.destination != self.destination:
			return False
		if len(self.deliveries) > 0 and d.destination != self.deliveries[0].destination:
			return False
		return True

	def addPackage(self,d):
		if not self.deliveryIsPossible(d):
			print("Cannot add package to this drone")
			return False
		else:
			self.updateWeight(d.weight)
			self.deliveries.append(d)
			self.destination = d.destination
			return True

	def droneIsAvailable(self):
		if len(self.deliveries) > 0:
			return False
		elif self.currentLocation != self.destination:
			return False
		else:
			return True

	def deployTo(self,location):
		self.destination = location

	def deliver(self,keeper):
		if self.currentLocation != self.destination or len(self.deliveries)>0:
			self.currentLocation = self.destination
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
			print(str(unit.droneIsAvailable())+ "\t\t" + unit.currentLocation + "\t\t" + unit.destination + "\t\t" + str(unit.maximumLoad)+"\t\t" + str(unit.remainingCapacity))
		print("______________________________________________________________________________________")


	def addDelivery(self,d):
		keyList = self.types.keys()
		keyList.sort()
		for model in keyList:
			for unit in self.units:
				if unit.maximumLoad == model:
					if unit.addPackage(d):
						return True
		return False

	def sendADroneTo(self,location):
		keyList = self.types.keys()
		keyList.sort()
		for model in keyList:
			for unit in self.units:
				if unit.maximumLoad == model:
					if unit.droneIsAvailable():
						unit.deployTo(location)
						return True
		return False

	def deliverPackages(self,keeper):
		for unit in self.units:
			unit.deliver(keeper)

	def reequilibrateFleet(self,automat):
		listOfPostalCodes = automat.unorganizedPostalCodes
		for unit in self.units:
			if unit.droneIsAvailable:
				#listOfPostalCodes.remove
				print("not done yet")


class DeliveryRequest:
	def __init__(self,defaultLocation):
		self.requestQueue = Queue.Queue()
		self.priorityQueue = Queue.Queue()
	def traiterLesRequetes(self,filename,auto,fleet,keeper):
		data = open("./" + filename, "r")
		for line in data:
			temp = line.strip('\n').strip('\r').split(" ")
			print(temp)
			if (auto.validatePostalCode(temp[0],keeper) and auto.validatePostalCode(temp[1],keeper) and (temp[2]).isdigit()):
				print("origin: " + temp[0] + "\tDestination: " + temp[1] + "\tWeight: " + temp[2])
				d = Delivery(temp[0],temp[1],temp[2])
				self.requestQueue.put(d)
			else:
				print("did not meet standards")
				if(not auto.validatePostalCode(temp[0],keeper)):
					print(temp[0] + " is not a valid postal code")
				if(not auto.validatePostalCode(temp[1],keeper)):
					print(temp[0] + " is not a valid postal code")
				if(not temp[2].isdigit()):
					print(temp[2] + " is not a valid weight")

		tempQueue = Queue.Queue()
		while(not self.priorityQueue.empty()):
			delivery = self.priorityQueue.get()
			if not fleet.addDelivery(delivery):
				fleet.sendADroneTo(delivery.origin)
				tempQueue.put(delivery)				

		while(not self.requestQueue.empty()):
			delivery = self.requestQueue.get()
			if not fleet.addDelivery(delivery):
				fleet.sendADroneTo(location)
				tempQueue.put(delivery)
	
		while(not tempQueue.empty()):
			self.requestQueue.put(tempQueue.get())

		fleet.deliverPackages()

		#Equilibrer les drones


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
		

		#return (True)
#class PossibleStates(Enum):
#	state0 = 0
#	state1 = 1
#	state2 = 2
#	state3 = 3
#	state4 = 4
#	state5 = 5
#	state6 = 6

#dave = PostalCodeAutomaton()
#dave.creerArbreAddresses("CodesPostaux.txt")

#print(dave.recognizedPostalCodes)
#print(dave.validatePostalCode("H1Z3E4"))

#q = Queue.Queue()

#requests = DeliveryRequest()
#requests.traiterLesRequetes("requetes1.txt",dave)
#print(requests)
history = RecordKeeper()
fleet = DroneFleet("H1W1B2")
types = [[5000,1],[1000,2]]
fleet.addDroneType(5000)
fleet.addDroneType(1000)
fleet.addNdrones(types[0][0],types[0][1])
fleet.addNdrones(types[1][0],types[1][1])
#fleet.listDronesInFleet()
fleet.addDelivery(Delivery("H1W1B2","H4N2Y8","500"))  
fleet.addDelivery(Delivery("H1W1B2","H4N2Y8","500"))  
#fleet.listDronesInFleet()
#fleet.units[0].displayDroneStats()
#fleet.units[1].displayDroneStats()
#fleet.units[2].displayDroneStats()
fleet.summarizeFleetStats()
fleet.deliverPackages(history)
fleet.summarizeFleetStats()
fleet.deliverPackages(history)
fleet.summarizeFleetStats()
print(history.nSuccessfulDeliveries)


