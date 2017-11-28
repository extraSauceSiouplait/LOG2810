
import random
from delivery import *
from codes_postaux_process import *




#Step1: Create Automaton
dave = PostalCodeAutomaton()

#Step2: Feed automaton postal codes
dave.creer_arbre_addresses("CodesPostaux.txt")

#Step3: Create record keeper
history = RecordKeeper()

#Step4: Create drone fleet
fleet = DroneFleet("H1W1B2")
types = [[5000,5],[1000,10]]
fleet.add_drone_type(5000)
fleet.add_drone_type(1000)
fleet.add_n_drones(types[0][0],types[0][1])
fleet.add_n_drones(types[1][0],types[1][1])

print(fleet.types.keys())

#Step5: Dispatch drones to random places on the map
fleet.reequilibrate_fleet(dave)
fleet.deliver_packages(history)


#print("successful deliveries: " + str(history.n_successful_deliveries))

#Step6: Create DeliveryRequest object to handle requests
requests = DeliveryRequest()

#Step7: Process request
requests.traiter_les_requetes("requetes1.txt",dave,fleet,history)
#print("successful deliveries: " + str(history.n_successful_deliveries))




#Step8: (repeat)
requests.traiter_les_requetes("requetes2.txt",dave,fleet,history)
#print("successful deliveries: " + str(history.n_successful_deliveries))

requests.traiter_les_requetes("requetes3.txt",dave,fleet,history)
#print("successful deliveries: " + str(history.n_successful_deliveries))

requests.traiter_les_requetes("requetes4.txt",dave,fleet,history)
#print("successful deliveries: " + str(history.n_successful_deliveries))
requests.traiter_les_requetes("requetes5.txt",dave,fleet,history)
#print("successful deliveries: " + str(history.n_successful_deliveries))
requests.traiter_les_requetes("requetes6.txt",dave,fleet,history)
#print("successful deliveries: " + str(history.n_successful_deliveries))
requests.traiter_les_requetes("requetes7.txt",dave,fleet,history)
#print("successful deliveries: " + str(history.n_successful_deliveries))
requests.traiter_les_requetes("requetes8.txt",dave,fleet,history)
#print("successful deliveries: " + str(history.n_successful_deliveries))

while( not requests.request_queue.empty()):
    print(requests.request_queue.get()),
"""
for x in range(0,10):
    requests.traiter_les_requetes("r0.txt",dave,fleet,history)
#print("successful deliveries: " + str(history.n_successful_deliveries))
"""

print("\n\nAverage " + str(history.get_average_n_packages_per_delivery(1000)) + "\n\n")
print("\n\nAverage " + str(history.get_average_n_packages_per_delivery(5000)) + "\n\n")
history.imprimerLesStatistiques()

fleet.summarize_fleet_stats()
