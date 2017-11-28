import random


class Drone:
    def __init__(self, location, max_load):
        self.current_location = location
        self.destination = location
        self.deliveries = []
        self.urgent_deliveries = []
        self.current_load = 0
        self.remaining_capacity = max_load
        self.maximum_load = max_load

    def getDroneType(self):
        return self.maximum_load

    def update_weight(self):
        self.current_load = 0
        self.remaining_capacity = self.maximum_load
        for d in self.deliveries:
            self.current_load += d.weight
            self.remaining_capacity -= d.weight

    def delivery_is_possible(self, delivery):
        if delivery.weight > self.remaining_capacity:
            # print("too much weight: Max="+str(self.remaining_capacity)+" weight="+str(d.weight))
            return False
        if delivery.origin != self.current_location:
            # print("Not at correct starting location")
            return False
        if len(self.deliveries) == 0 and self.destination != self.current_location and delivery.destination != self.destination:
            # print("This drone is already assigned to go somewhere")
            return False
        if len(self.deliveries) > 0 and delivery.destination != self.deliveries[0].destination:
            # print("Not going to the same place")
            return False
        return True

    def add_package(self, delivery):
        if not self.delivery_is_possible(delivery):
            # print(str(self.remaining_capacity)+"\tCannot add package to this drone")
            return False
        else:
            self.deliveries.append(delivery)
            self.update_weight()
            self.destination = delivery.destination
            return True

    def drone_is_available(self):
        # if the drone has any deliveries in its list
        if len(self.deliveries) > 0:
            return False
        # if the drone's destination differes from its current location
        elif self.current_location != self.destination:
            return False
        else:
            return True

    #def deploy_to(self, location):
    def deploy_to(self, delivery):
        self.urgent_deliveries.append(delivery)
        self.destination = delivery.origin

    def deliver(self, keeper):
        if self.current_location != self.destination or len(self.deliveries) > 0:

            if self.current_location != self.destination and len(self.deliveries) > 0:
                keeper.add_successful_delivery(self.getDroneType(), len(self.deliveries))
                #keeper.add_successful_delivery(self.maximum_load, len(self.deliveries))

            self.current_location = self.destination
            self.urgent_deliveries = []

            if len(self.deliveries) > 0:
                d = self.deliveries[0]
                self.deliveries.remove(d)
                self.current_load = self.current_load - d.weight
                self.remaining_capacity = self.remaining_capacity + d.weight
                keeper.add_request_processed()

            return True
        else:
            # print("No need to move from here")
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

    def has_room(self, delivery):
        weight_of_next_shipment = delivery.weight
        for d in self.urgent_deliveries:
            weight_of_next_shipment += d.weight
        if weight_of_next_shipment <= self.maximum_load and (len(self.urgent_deliveries) == 0 or (delivery.origin == self.urgent_deliveries[0].origin and delivery.destination == self.urgent_deliveries[0].destination)):
            return True
        else:
            return False

class DroneFleet:
    def __init__(self, starting_location):
        self.units = []
        self.types = {}
        self.home = starting_location

    def add_drone_type(self, weight_limit_in_grams):
        self.types[weight_limit_in_grams] = 0

    def add_n_drones(self, weight_limit_in_grams, n_drones):
        self.types[weight_limit_in_grams] = self.types[weight_limit_in_grams] + n_drones
        for x in range(n_drones):
            self.units.append(Drone(self.home, weight_limit_in_grams))

    def n_drones_available(self, weight_limit_in_grams):
        count = 0
        for drone in self.units:
            if drone.remaining_capacity == weight_limit_in_grams:
                count += 1
        return count

    def list_drones_in_fleet(self):
        for model in self.types:
            print("This fleet contains a total of " + str(
                self.types[model]) + " drone that is able to carry a maximum of " + str(model) + " grams.")
            print(str(self.n_drones_available(model)) + " of which are available (not currently assigned to a task)")

    def summarize_fleet_stats(self):
        print("______________________________________________________________________________________")
        print("Available\tLocation\tDestination\tMaxCapacity\tnPackages\tRemainingCap")
        for unit in self.units:
            print(str(
                unit.drone_is_available()) + "\t\t" + unit.current_location + "\t\t" + unit.destination + "\t\t" + str(
                unit.maximum_load) + "\t\t" + str(len(unit.deliveries)) + "\t\t\t" + str(unit.remaining_capacity))
        print("______________________________________________________________________________________")

    def assign_delivery_to_drone(self, delivery):
        key_list = self.types.keys()

        for model in sorted(key_list):
            for unit in self.units:
                if unit.maximum_load == model:
                    # print("Load size = " + str(d.weight) + "\tMax load: " + str(model))
                    if unit.add_package(delivery):
                        return True
        return False

    def send_a_drone_to(self, d):
        # get list of all drone types
        key_list = self.types.keys()

        # put them in numerical order
        for model in sorted(key_list):
            # print("now looking at model #" + str(model))
            for unit in self.units:
                if unit.maximum_load == model:
                    if unit.has_room(d):
                    #if unit.drone_is_available():
                        #if d.weight <= unit.remaining_capacity:
                            # unit.remaining_capacity -= d.weight
                            #unit.deploy_to(d.origin)
                            unit.deploy_to(d)
                            return True
        return False

    def deliver_packages(self, keeper):
        for unit in self.units:
            unit.deliver(keeper)

    def reequilibrate_fleet(self, automat):
        # 1) List all postal codes
        # print("beginning postal_codes")
        list_of_postal_codes = list(automat.unorganized_postal_codes)
        # print(list_of_postal_codes)
        # print(list_of_postal_codes)
        # 2) For each non-available drone
        for unit in self.units:
            # print(str(unit.maximum_load) +"\t" + str(unit.drone_is_available()))
            if not unit.drone_is_available():
                if unit.destination in list_of_postal_codes:
                    # 3) subtract their destination from the list of postal codes
                    # print(unit.destination)
                    list_of_postal_codes.remove(unit.destination)
        # print(list_of_postal_codes)
        # 4) Dispatch them to different locations selected at random
        for unit in self.units:
            if unit.drone_is_available():
                # print(list_of_postal_codes)
                # print("remaining Postal codes:")
                # print(list_of_postal_codes)
                d = random.sample(list_of_postal_codes, 1)[0]
                # print(d)
                unit.destination = d
                list_of_postal_codes.remove(d)
                # print("deploying unit to " + d)
