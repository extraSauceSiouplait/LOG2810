from delivery import *
from classes_drones import *
from codes_postaux_process import *

# class possible_states(Enum):
#	state0 = 0
#	state1 = 1
#	state2 = 2
#	state3 = 3
#	state4 = 4
#	state5 = 5
#	state6 = 6

# dave = postal_codeAutomaton()
# dave.creer_arbre_addresses("CodesPostaux.txt")

# print(dave.recognized_postal_codes)
# print(dave.validate_postal_code("H1Z3E4"))

# q = Queue.Queue()

# requests = DeliveryRequest()
# requests.process_requests("requetes1.txt",dave)
# print(requests)
history = RecordKeeper()
fleet = DroneFleet("H1W1B2")
types = [[5000, 1], [1000, 2]]
fleet.add_drone_type(5000)
fleet.add_drone_type(1000)
fleet.add_n_drones(types[0][0], types[0][1])
fleet.add_n_drones(types[1][0], types[1][1])
# fleet.list_drones_in_fleet()
fleet.add_delivery(Delivery("H1W1B2", "H4N2Y8", "500"))
fleet.add_delivery(Delivery("H1W1B2", "H4N2Y8", "500"))
# fleet.list_drones_in_fleet()
# fleet.units[0].display_drone_stats()
# fleet.units[1].display_drone_stats()
# fleet.units[2].display_drone_stats()
fleet.summarize_fleet_stats()
fleet.deliver_packages(history)
fleet.summarize_fleet_stats()
fleet.deliver_packages(history)
fleet.summarize_fleet_stats()
print(history.n_successful_deliveries)
