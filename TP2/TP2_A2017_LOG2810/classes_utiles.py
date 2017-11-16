import Queue


class Delivery:
    def __init__(self, origin, destination, weight):
        self.origin = origin
        self.destination = destination
        self.weight = int(weight)


class Drone:
    def __init__(self, location, max_load):
        self.current_location = location
        self.destination = location
        self.deliveries = []
        self.current_load = 0
        self.remaining_capacity = max_load
        self.maximum_load = max_load

    def update_weight(self, weight):
        self.current_load += weight
        self.remaining_capacity -= weight

    def delivery_is_possible(self, d):
        if d.weight > self.remaining_capacity:
            return False

        if d.origin != self.current_location:
            return False

        if len(
                self.deliveries) == 0 and self.destination != self.current_location and d.destination != self.destination:
            return False

        if len(self.deliveries) > 0 and d.destination != self.deliveries[0].destination:
            return False

        return True

    def add_package(self, d):
        if not self.delivery_is_possible(d):
            print("Cannot add package to this drone")
            return False

        else:
            self.update_weight(d.weight)
            self.deliveries.append(d)
            self.destination = d.destination
            return True

    def drone_is_available(self):
        if len(self.deliveries) > 0:
            return False

        elif self.current_location != self.destination:
            return False

        else:
            return True

    def deploy_to(self, location):
        self.destination = location

    def deliver(self, keeper):
        if self.current_location != self.destination or len(self.deliveries) > 0:

            self.current_location = self.destination
            d = self.deliveries[0]
            self.deliveries.remove(d)

            self.current_load = self.current_load - d.weight
            self.remaining_capacity = self.remaining_capacity + d.weight
            keeper.add_delivery()
            return True

        else:

            # print("No need to move from here")
            if self.current_load != 0.0 or self.remaining_capacity != self.maximum_load \
                    or self.destination != self.current_location:

                print("There was a mistake somewhere")
                return False
            else:
                return True

    def display_drone_stats(self):
        print("Max weight: " + str(self.maximum_load))
        print("remaining_capacity: " + str(self.remaining_capacity))
        print("Current Location: " + self.current_location)
        print("Destination: " + self.destination)


class DroneFleet:
    def __init__(self, starting_location):
        self.units = []
        self.types = {}
        self.home = starting_location

    def add_drone_type(self, weight_limit_grams):
        self.types[weight_limit_grams] = 0

    def add_n_drones(self, weight_limit_grams, n_drones):
        self.types[weight_limit_grams] = self.types[weight_limit_grams] + n_drones

        for x in range(n_drones):
            self.units.append(Drone(self.home, weight_limit_grams))

    def n_drones_available(self, weight_limit_grams):
        count = 0

        for drone in self.units:
            if drone.remaining_capacity == weight_limit_grams:
                count += 1
        return count

    def list_drones_in_fleet(self):
        for model in self.types:
            print("This fleet contains a total of " + str(
                self.types[model]) + " drone that is able to carry a maximum of " + str(model) + " grams.")
            print(str(self.n_drones_available(model)) + " of which are available (not currently assigned to a task)")

    def summarize_fleet_stats(self):
        print("______________________________________________________________________________________")
        print("Available\tLocation\tDestination\tMaxCapacity\tRemainingCap")

        for unit in self.units:
            print(
                str(unit.drone_is_available()) + "\t\t" + unit.current_location + "\t\t" + unit.destination + "\t\t" +
                str(unit.maximum_load) + "\t\t" + str(unit.remaining_capacity))
        print("______________________________________________________________________________________")

    def add_delivery(self, d):
        key_list = self.types.keys()
        key_list.sort()

        for model in key_list:
            for unit in self.units:
                if unit.maximum_load == model:
                    if unit.add_package(d):
                        return True
        return False

    def send_drone_to(self, location):
        key_list = self.types.keys()
        key_list.sort()

        for model in key_list:
            for unit in self.units:
                if unit.maximum_load == model:
                    if unit.drone_is_available():
                        unit.deploy_to(location)
                        return True
        return False

    def deliver_packages(self, keeper):
        for unit in self.units:
            unit.deliver(keeper)

    def reequilibrate_fleet(self, automat):
        list_postal_codes = automat.unorganized_postal_codes

        for unit in self.units:
            if unit.drone_is_available:
                # list_postal_codes.remove
                print("not done yet")


class DeliveryRequest:
    def __init__(self, default_location):
        self.requestQueue = Queue.Queue()
        self.priority_queue = Queue.Queue()

    def process_requests(self, filename, auto, fleet, keeper):
        data = open("./" + filename, "r")

        for line in data:
            temp = line.strip('\n').strip('\r').split(" ")
            print(temp)

            if (auto.validate_postal_code(temp[0], keeper) and auto.validate_postal_code(temp[1], keeper) and (
                    temp[2]).isdigit()):
                print("origin: " + temp[0] + "\tDestination: " + temp[1] + "\tWeight: " + temp[2])
                d = Delivery(temp[0], temp[1], temp[2])
                self.requestQueue.put(d)

            else:
                print("did not meet standards")

                if not auto.validate_postal_code(temp[0], keeper):
                    print(temp[0] + " is not a valid postal code")

                if not auto.validate_postal_code(temp[1], keeper):
                    print(temp[0] + " is not a valid postal code")

                if not temp[2].isdigit():
                    print(temp[2] + " is not a valid weight")

        temp_queue = Queue.Queue()
        
        while not self.priority_queue.empty():
            delivery = self.priority_queue.get()

            if not fleet.add_delivery(delivery):
                fleet.send_drone_to(delivery.origin)
                temp_queue.put(delivery)

        while not self.requestQueue.empty():
            delivery = self.requestQueue.get()

            if not fleet.add_delivery(delivery):
                fleet.send_drone_to(delivery.origin)
                temp_queue.put(delivery)

        while not temp_queue.empty():
            self.priority_queue.put(temp_queue.get())

        fleet.deliver_packages()

        # Equilibrer les drones


class RecordKeeper:
    def __init__(self):
        self.n_successful_deliveries = 0
        self.n_invalid_requests = 0

    def add_delivery(self):
        self.n_successful_deliveries += 1

    def add_invalid_request(self):
        self.n_invalid_requests += 1

    # 
    # A CHANGER WARNING WARNING
    #
    def get_drone_average_delivery(self, weight_limit_grams, fleet):
        return self.n_successful_deliveries / fleet.types[weight_limit_grams]


class PostalCodeAutomaton:

    possible_states = [0, 1, 2, 3, 4, 5, 6]

    def __init__(self):
        self.name = "Dave"
        self.recognized_postal_codes = {}
        self.unorganized_postal_codes = []

    def validate_postal_code(self, postal_code, keeper):
        current_state = self.possible_states[0]
        code = list(postal_code)
        while current_state != self.possible_states[6]:

            if current_state == self.possible_states[0]:

                if not code[0] in self.recognized_postal_codes:
                    # print(str(code[0]) + "not in dictionnary")
                    keeper.add_invalid_request()
                    return False
                else:
                    current_state = self.possible_states[1]

            if current_state == self.possible_states[1]:
                if code[1] in self.recognized_postal_codes[code[0]]:
                    # print(str(code[1]) + "not in dictionnary")
                    keeper.add_invalid_request()
                    return False
                else:
                    current_state = self.possible_states[2]

            if current_state == self.possible_states[2]:

                if not code[2] in self.recognized_postal_codes[code[0]][code[1]]:
                    # print(str(code[2]) + "not in dictionnary")
                    keeper.add_invalid_request()
                    return False
                else:
                    current_state = self.possible_states[3]

            if current_state == self.possible_states[3]:

                if not code[3] in self.recognized_postal_codes[code[0]][code[1]][code[2]]:
                    # print(str(code[3]) + "not in dictionnary")
                    keeper.add_invalid_request()
                    return False
                else:
                    current_state = self.possible_states[4]

            if current_state == self.possible_states[4]:

                if not code[4] in self.recognized_postal_codes[code[0]][code[1]][code[2]][code[3]]:
                    # print(str(code[4]) + "not in dictionnary")
                    keeper.add_invalid_request()
                    return False
                else:
                    current_state = self.possible_states[5]

            if current_state == self.possible_states[5]:

                if not code[5] in self.recognized_postal_codes[code[0]][code[1]][code[2]][code[3]][code[4]]:
                    # print(code[5])
                    # print(self.recognized_postal_codes[code[0]][code[1]][code[2]][code[3]][code[4]])
                    # print("last char not in dictionnary")
                    keeper.add_invalid_request()
                    return False
                else:
                    current_state = self.possible_states[6]

        return True

    def creer_arbre_addresses(self, filename):
        self.recognized_postal_codes = {}
        data = open("./" + filename, "r")

        for line in data:
            temp = line.strip('\n').strip('\r').strip(' ')
            word = list(temp)

            if len(word) != 6:
                print("This file contains invalid entries.")
            else:
                if not word[0] in self.recognized_postal_codes:
                    self.recognized_postal_codes[word[0]] = {}

                if not word[1] in self.recognized_postal_codes[word[0]]:
                    self.recognized_postal_codes[word[0]][word[1]] = {}

                if not word[2] in self.recognized_postal_codes[word[0]][word[1]]:
                    self.recognized_postal_codes[word[0]][word[1]][word[2]] = {}

                if not word[3] in self.recognized_postal_codes[word[0]][word[1]][word[2]]:
                    self.recognized_postal_codes[word[0]][word[1]][word[2]][word[3]] = {}

                if not word[4] in self.recognized_postal_codes[word[0]][word[1]][word[2]][word[3]]:
                    self.recognized_postal_codes[word[0]][word[1]][word[2]][word[3]][word[4]] = {}

                if not word[5] in self.recognized_postal_codes[word[0]][word[1]][word[2]][word[3]][word[4]]:
                    self.recognized_postal_codes[word[0]][word[1]][word[2]][word[3]][word[4]][word[5]] = {}

                self.recognized_postal_codes[word[0]][word[1]][word[2]][word[3]][word[4]][word[5]] = temp
                self.unorganized_postal_codes.append(temp)


                # return (True)


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
