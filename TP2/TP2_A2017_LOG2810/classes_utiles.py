import Queue
import random

class Delivery:
	def __init__(self,origin,destination,weight):
		self.origin = origin
		self.destination = destination
		self.weight = int(weight)
	

class Drone:

	def __init__(self,location,maxLoad):
		self.current_location = location
		self.destination = location
		self.deliveries = []
		self.current_load = 0
		self.remaining_capacity = maxLoad
		self.maximum_load = maxLoad

	def update_weight(self):
            self.current_load = 0
            self.remaining_capacity = self.maximum_load
            for d in self.deliveries:
                self.current_load += d.weight
		self.remaining_capacity -= d.weight

	def delivery_is_possible(self,d):
		if d.weight > self.remaining_capacity:
		    #print("too much weight: Max="+str(self.remaining_capacity)+" weight="+str(d.weight))	
                    return False
		if d.origin != self.current_location:
                    #print("Not at correct starting location")
	    	    return False
		if len(self.deliveries) == 0 and self.destination != self.current_location and d.destination != self.destination:
		    #print("This drone is already assigned to go somewhere")
                    return False
		if len(self.deliveries) > 0 and d.destination != self.deliveries[0].destination:
		    #print("Not going to the same place")
                    return False
		return True

	def add_package(self,d):
		if not self.delivery_is_possible(d):
			#print(str(self.remaining_capacity)+"\tCannot add package to this drone")
			return False
		else:
			self.deliveries.append(d)
			self.update_weight()
			self.destination = d.destination
			return True

	def drone_is_available(self):
                #if the drone has any deliveries in its list
		if len(self.deliveries) > 0:
			return False
                #if the drone's destination differes from its current location
		elif self.current_location != self.destination :
			return False
		else:
			return True

	def deploy_to(self,location):
		self.destination = location

	def deliver(self,keeper):
		if self.current_location != self.destination or len(self.deliveries)>0:
			self.current_location = self.destination
                        if len(self.deliveries)>0:
                            d = self.deliveries[0]
			    self.deliveries.remove(d)
			    self.current_load = self.current_load - d.weight
			    self.remaining_capacity = self.remaining_capacity + d.weight
			    keeper.add_delivery()
			return True
		else:
			#print("No need to move from here")
			if self.current_load != 0.0 or self.remaining_capacity != self.maximum_load or self.destination != self.current_location:
				print("There was a mistake somewhere")
				return False
			else:
				return True

	def display_drone_stats(self):
		print("Max weight: " + str(self.maximum_load))
		print("RemainingCapacity: " + str(self.remaining_capacity))
		print("Current Location: " + self.current_location)
		print("Destination: " + self.destination)

		
class DroneFleet:
	def __init__(self,starting_location):
		self.units = []
		self.types = {}
		self.home = starting_location
	
	def add_drone_type(self,weight_limit_in_grams):
		self.types[weight_limit_in_grams] = 0
	
	def add_n_drones(self,weight_limit_in_grams,nDrones):
		self.types[weight_limit_in_grams] = self.types[weight_limit_in_grams] + nDrones
		for x in range(nDrones):
			self.units.append(Drone(self.home,weight_limit_in_grams))
		
	def n_drones_available(self,weight_limit_in_grams):
		count = 0
		for drone in self.units:
			if drone.remaining_capacity == weight_limit_in_grams:
				count += 1
		return count

	def list_drones_in_fleet(self):
		for model in self.types:
			print("This fleet contains a total of " + str(self.types[model]) + " drone that is able to carry a maximum of " + str(model) + " grams.")
			print(str(self.n_drones_available(model)) + " of which are available (not currently assigned to a task)")

	def summarize_fleet_stats(self):
		print("______________________________________________________________________________________")
		print("Available\tLocation\tDestination\tMaxCapacity\tRemainingCap")
		for unit in self.units:
			print(str(unit.drone_is_available())+"\t\t"+unit.current_location+"\t\t"+unit.destination+"\t\t"+str(unit.maximum_load)+"\t\t"+str(unit.remaining_capacity))
		print("______________________________________________________________________________________")


	def add_delivery(self,d):
		key_list = self.types.keys()
		key_list.sort()
		for model in key_list:
			for unit in self.units:
				if unit.maximum_load == model:
                                        #print("Load size = " + str(d.weight) + "\tMax load: " + str(model))
					if unit.add_package(d):
						return True
		return False

	def send_a_drone_to(self,d):
                #get list of all drone types
		key_list = self.types.keys()
                
                #put them in numerical order
		key_list.sort()
		
                for model in key_list:
                        #print("now looking at model #" + str(model))
			for unit in self.units:
				if unit.maximum_load == model:
                                    if unit.drone_is_available(): 
					if d.weight <= unit.remaining_capacity:
                                            #unit.remaining_capacity -= d.weight
                                            unit.deploy_to(d.origin)
					    return True
		return False

	def deliver_packages(self,keeper):
		for unit in self.units:
			unit.deliver(keeper)

	def reequilibrate_fleet(self,automat):
                #1) List all postal codes
                #print("beginning postal_codes")
		list_of_postal_codes = list(automat.unorganized_postal_codes)
                #print(list_of_postal_codes)
		#print(list_of_postal_codes)
                #2) For each non-available drone
                for unit in self.units:
                        #print(str(unit.maximum_load) +"\t" + str(unit.drone_is_available()))
			if not unit.drone_is_available():
                            if unit.destination in list_of_postal_codes:
                                #3) subtract their destination from the list of postal codes
                                #print(unit.destination)
                                list_of_postal_codes.remove(unit.destination)
                #print(list_of_postal_codes)
                #4) Dispatch them to different locations selected at random
                for unit in self.units:
                    if unit.drone_is_available():
                        #print(list_of_postal_codes)
                        #print("remaining Postal codes:")
                        #print(list_of_postal_codes)
                        d = random.sample(list_of_postal_codes,1)[0]
                        #print(d)
                        unit.deploy_to(d)
                        list_of_postal_codes.remove(d)
                        #print("deploying unit to " + d)
				


class DeliveryRequest:
	def __init__(self,defaultLocation):
		self.request_queue = Queue.Queue()
		self.priority_queue = Queue.Queue()
	def traiter_les_requetes(self,filename,auto,fleet,keeper):
		data = open("./" + filename, "r")
		for line in data:
		    temp = line.strip('\n').strip('\r').split(" ")
	            #print(temp)
		    if (auto.validate_postal_code(temp[0],keeper) and auto.validate_postal_code(temp[1],keeper) and (temp[2]).isdigit()):
			print("origin: " + temp[0] + "\tDestination: " + temp[1] + "\tWeight: " + temp[2])
			d = Delivery(temp[0],temp[1],temp[2])
			self.request_queue.put(d)
		    else:
                        print("A request did not meet standards:")
			if(not auto.validate_postal_code(temp[0],keeper)):
			    print("\t" + temp[0] + " is not a valid postal code")
			if(not auto.validate_postal_code(temp[1],keeper)):
			    print("\t" + temp[1] + " is not a valid postal code")
			if(not temp[2].isdigit()):
			    print("\t" + temp[2] + " is not a valid weight")
                
                print("creating temp queue")
		temp_queue = Queue.Queue()
                
                #fleet.summarize_fleet_stats()
                
                print("verifying prioroty queue")
	        while(not self.priority_queue.empty()):
			delivery = self.priority_queue.get()
			if not fleet.add_delivery(delivery):
				fleet.send_a_drone_to(delivery)
				temp_queue.put(delivery)				
                
                #fleet.summarize_fleet_stats()
                
                print("verifying reqQueue")
		while(not self.request_queue.empty()):
			delivery = self.request_queue.get()
                        #print("delivery weight: " + str(delivery.weight))
			if not fleet.add_delivery(delivery):
                            if delivery.weight <= max(fleet.types.keys()):
                                #print("delivery not possible at the moment. Sending a drone to pickup location")
			        fleet.send_a_drone_to(delivery)
			        temp_queue.put(delivery)
                            else:
                                print("The maximum deliverable weight is "+str(max(fleet.types.keys()))+". With a weight of "+str(delivery.weight)+", this delivery is not possible.")
                                keeper.add_invalid_request()
	        
                
                #fleet.summarize_fleet_stats()
                
                print("transferring contents of temp queue to priorityqueue")
		while(not temp_queue.empty()):
			self.priority_queue.put(temp_queue.get())

                print("fleet equilibration")
		fleet.reequilibrate_fleet(auto)
                
                #fleet.summarize_fleet_stats()
                
                print("package delivery")
                fleet.deliver_packages(keeper)
                
                #fleet.summarize_fleet_stats()



class RecordKeeper:
	def __init__(self):
		self.n_successful_deliveries = 0
		self.n_invalid_requests = 0
	def add_delivery(self):
		self.n_successful_deliveries += 1
	def add_invalid_request(self):
		self.n_invalid_requests += 1
	def getDroneAverageDelivery(self,weight_limit_in_grams,fleet):
		return (self.n_successful_deliveries/fleet.types[weight_limit_in_grams])
        def imprimerLesStatistiques(self):
                print("Le nombre de livraisons completes a date: "+str(self.n_successful_deliveries))
                print("Le nombre de requetes invalides: " + str(self.n_invalid_requests))
                #print le nombre de drones dans chaque quartier
                #print le nombre moyen de colis transportes par un drone a petite capacite
                #print le nombre moyen de colis transportes par un drone a grande capacite

class PostalCodeAutomaton:
	possible_states = [0,1,2,3,4,5,6]

	def __init__(self):
		self.name = "Dave"
		self.recognized_postal_codes = {}
		self.unorganized_postal_codes = []

	def validate_postal_code(self,postal_code,keeper):
		current_state = self.possible_states[0]
		code = list(postal_code)
		while(current_state != self.possible_states[6]):
			if (current_state == self.possible_states[0]):
				if (not code[0] in self.recognized_postal_codes):
					#print(str(code[0]) + "not in dictionnary")
					keeper.add_invalid_request()
					return False
				else:
					current_state = self.possible_states[1]
			if (current_state == self.possible_states[1]):
				if (not code[1] in self.recognized_postal_codes[code[0]]):
					#print(str(code[1]) + "not in dictionnary")
					keeper.add_invalid_request()
					return False
				else:
					current_state = self.possible_states[2]
			if (current_state == self.possible_states[2]):
				if (not code[2] in self.recognized_postal_codes[code[0]][code[1]]):
					#print(str(code[2]) + "not in dictionnary")
					keeper.add_invalid_request()
					return False
				else:
					current_state = self.possible_states[3]
			if (current_state == self.possible_states[3]):
				if (not code[3] in self.recognized_postal_codes[code[0]][code[1]][code[2]]):
					#print(str(code[3]) + "not in dictionnary")
					keeper.add_invalid_request()
					return False
				else:
					current_state = self.possible_states[4]
			if (current_state == self.possible_states[4]):
				if (not code[4] in self.recognized_postal_codes[code[0]][code[1]][code[2]][code[3]]):
					#print(str(code[4]) + "not in dictionnary")
					keeper.add_invalid_request()
					return False
				else:
					current_state = self.possible_states[5]
			if (current_state == self.possible_states[5]):
				if (not code[5] in self.recognized_postal_codes[code[0]][code[1]][code[2]][code[3]][code[4]]):
					#print(code[5])
					#print(self.recognized_postal_codes[code[0]][code[1]][code[2]][code[3]][code[4]])
					#print("last char not in dictionnary")
					keeper.add_invalid_request()
					return False
				else:
					current_state = self.possible_states[6]

		return True

	def creer_arbre_addresses(self,filename):
		self.recognized_postal_codes = {}
		data = open("./" + filename, "r")
		for line in data:
			temp = line.strip('\n').strip('\r').strip(' ')
			word = list(temp)
			if len(word) != 6:
				print("This file contains invalid entries.")
			else:
				if (not word[0] in self.recognized_postal_codes):
					self.recognized_postal_codes[word[0]] = {}
				if (not word[1] in self.recognized_postal_codes[word[0]]):
					self.recognized_postal_codes[word[0]][word[1]] = {}
				if (not word[2] in self.recognized_postal_codes[word[0]][word[1]]):
					self.recognized_postal_codes[word[0]][word[1]][word[2]] = {}
				if (not word[3] in self.recognized_postal_codes[word[0]][word[1]][word[2]]):
					self.recognized_postal_codes[word[0]][word[1]][word[2]][word[3]] = {}
				if (not word[4] in self.recognized_postal_codes[word[0]][word[1]][word[2]][word[3]]):
					self.recognized_postal_codes[word[0]][word[1]][word[2]][word[3]][word[4]] = {}
				if (not word[5] in self.recognized_postal_codes[word[0]][word[1]][word[2]][word[3]][word[4]]):
					self.recognized_postal_codes[word[0]][word[1]][word[2]][word[3]][word[4]][word[5]] = {}
				self.recognized_postal_codes[word[0]][word[1]][word[2]][word[3]][word[4]][word[5]] = temp
				self.unorganized_postal_codes.append(temp)		
		
#def main:


#Step1: Create Automaton
#dave = PostalCodeAutomaton()

#Step2: Feed automaton postal codes
#dave.creer_arbre_addresses("CodesPostaux.txt")

#Step3: Create record keeper
#history = RecordKeeper()

#Step4: Create drone fleet
#fleet = DroneFleet("H1W1B2")
#types = [[5000,5],[1000,10]]
#fleet.add_drone_type(5000)
#fleet.add_drone_type(1000)
#fleet.add_n_drones(types[0][0],types[0][1])
#fleet.add_n_drones(types[1][0],types[1][1])

#print(fleet.types.keys())

#Step5: Dispatch drones to random places on the map
#fleet.reequilibrate_fleet(dave)
#fleet.deliver_packages(history)


#print("successful deliveries: " + str(history.n_successful_deliveries))

#Step6: Create DeliveryRequest object to handle requests
#requests = DeliveryRequest("H3S2B2")

#Step7: Process request
#requests.traiter_les_requetes("requetes1.txt",dave,fleet,history)
#print("successful deliveries: " + str(history.n_successful_deliveries))

#Step8: (repeat)
#requests.traiter_les_requetes("requetes2.txt",dave,fleet,history)
#print("successful deliveries: " + str(history.n_successful_deliveries))

#requests.traiter_les_requetes("requetes3.txt",dave,fleet,history)
#print("successful deliveries: " + str(history.n_successful_deliveries))

#requests.traiter_les_requetes("requetes4.txt",dave,fleet,history)
#print("successful deliveries: " + str(history.n_successful_deliveries))
#requests.traiter_les_requetes("requetes5.txt",dave,fleet,history)
#print("successful deliveries: " + str(history.n_successful_deliveries))
#requests.traiter_les_requetes("requetes6.txt",dave,fleet,history)
#print("successful deliveries: " + str(history.n_successful_deliveries))
#requests.traiter_les_requetes("requetes7.txt",dave,fleet,history)
#print("successful deliveries: " + str(history.n_successful_deliveries))
#requests.traiter_les_requetes("requetes8.txt",dave,fleet,history)
#print("successful deliveries: " + str(history.n_successful_deliveries))
#for x in range(0,10):
    #requests.traiter_les_requetes("r0.txt",dave,fleet,history)
    #print("successful deliveries: " + str(history.n_successful_deliveries))
