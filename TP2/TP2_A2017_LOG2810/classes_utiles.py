import Queue

class Delivery:
	def __init__(self,origin,destination,weight):
		self.origin = origin
		self.destination = destination
		self.weight = int(weight)
	
class PostalCode:
	def __init__(self,charString):
		self.postalCode = charString

class DeliveryRequest:
	def __init__(self):
		self.requestQueue = Queue.Queue()
	def traiterLesRequetes(self,filename,auto):
		data = open("./" + filename, "r")
		for line in data:
			#print(line)
			temp = line.strip('\n').strip('\r').split(" ")
			print(temp)
			if (auto.validatePostalCode(temp[0]) and auto.validatePostalCode(temp[1]) and (temp[2]).isdigit()):
				print("origin: " + temp[0] + "\tDestination: " + temp[1] + "\tWeight: " + temp[2])
				d = Delivery(temp[0],temp[1],temp[2])
				self.requestQueue.put(d)
			else:
				print("did not meet standards")
				if(not auto.validatePostalCode(temp[0])):
					print(temp[0] + " is not a valid postal code")
				if(not auto.validatePostalCode(temp[1])):
					print(temp[0] + " is not a valid postal code")
				if(not temp[2].isdigit()):
					print(temp[2] + " is not a valid weight")

class PostalCodeAutomaton:
	possibleStates = [0,1,2,3,4,5,6]

	def __init__(self):
		self.name = "Dave"
		self.recognizedPostalCodes = {}

	def validatePostalCode(self,postalCode):
		currentState = self.possibleStates[0]
		code = list(postalCode)
		while(currentState != self.possibleStates[6]):
			if (currentState == self.possibleStates[0]):
				if (not code[0] in self.recognizedPostalCodes):
					#print(str(code[0]) + "not in dictionnary")
					return False
				else:
					currentState = self.possibleStates[1]
			if (currentState == self.possibleStates[1]):
				if (not code[1] in self.recognizedPostalCodes[code[0]]):
					#print(str(code[1]) + "not in dictionnary")
					return False
				else:
					currentState = self.possibleStates[2]
			if (currentState == self.possibleStates[2]):
				if (not code[2] in self.recognizedPostalCodes[code[0]][code[1]]):
					#print(str(code[2]) + "not in dictionnary")
					return False
				else:
					currentState = self.possibleStates[3]
			if (currentState == self.possibleStates[3]):
				if (not code[3] in self.recognizedPostalCodes[code[0]][code[1]][code[2]]):
					#print(str(code[3]) + "not in dictionnary")
					return False
				else:
					currentState = self.possibleStates[4]
			if (currentState == self.possibleStates[4]):
				if (not code[4] in self.recognizedPostalCodes[code[0]][code[1]][code[2]][code[3]]):
					#print(str(code[4]) + "not in dictionnary")
					return False
				else:
					currentState = self.possibleStates[5]
			if (currentState == self.possibleStates[5]):
				if (not code[5] in self.recognizedPostalCodes[code[0]][code[1]][code[2]][code[3]][code[4]]):
					#print(code[5])
					#print(self.recognizedPostalCodes[code[0]][code[1]][code[2]][code[3]][code[4]])
					#print("last char not in dictionnary")
					return False
				else:
					currentState = self.possibleStates[6]

		return True

	def creerArbreAddresses(self,filename):
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
				
		

		#return (True)
#class PossibleStates(Enum):
#	state0 = 0
#	state1 = 1
#	state2 = 2
#	state3 = 3
#	state4 = 4
#	state5 = 5
#	state6 = 6

dave = PostalCodeAutomaton()
dave.creerArbreAddresses("CodesPostaux.txt")

print(dave.recognizedPostalCodes)
print(dave.validatePostalCode("H1Z3E4"))

q = Queue.Queue()

requests = DeliveryRequest()
requests.traiterLesRequetes("requetes1.txt",dave)
print(requests)
