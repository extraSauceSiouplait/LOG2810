class Delivery:
	def __init__(self,origin,destination,weight):
		self.origin = origin
		self.destination = destination
		self.weight = weight
	
class PostalCode:
	def __init__(self,charString):
		self.postalCode = charString

class DeliveryRequest:
	def __init__(self):
		requestQueue = Queue()
	def traiterLesRequetes(self,filename):
		# 
		data = open("./" + filename, "r")
		for line in data:
			temp = line.strip('\n').strip('\n').split(" ")
			if len(temp) != 3:
				print(temp + "is an invalid entry.")
			else:
				if validatePostalCode(temp[0]) and validatePostalCode(temp[1]):
					requestQueue.put(Delivery(temp[0],temp[1],temp[2]))
				else:
					print("Invalid postal code detected")
		return True

class PostalCodeAutomaton:
	possibleStates = ["0","1","2","3","4","5","6"]

	def __init__(self):
		self.name = "Dave"
		self.recognizedPostalCodes = []

	def validatePostalCode(self,postalCode):
		print("validatePostalCode function not implemented")
		return True

	def creerArbreAddresses(self,filename):
		data = open("./" + filename, "r")
		for line in data:
			temp = line.strip('\n').strip('\r').split(" ")
			if len(temp) != 1:
				print("This file contains invalid entries.")
				return (False)
			else:
				self.recognizedPostalCodes.append(temp[0])
		self.recognizedPostalCodes.sort()
		return (True)
		

automaton = PostalCodeAutomaton()
print("Hi, my name is " + automaton.name)
didItWork = automaton.creerArbreAddresses("CodesPostaux.txt")
print("This thing worked: " + str(didItWork))
print(automaton.recognizedPostalCodes)
