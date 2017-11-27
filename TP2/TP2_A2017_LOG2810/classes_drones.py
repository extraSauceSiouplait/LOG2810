
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
        """

        :type automat: Un object de classe PostalCodeAutomaton
        """
        list_postal_codes = automat.unorganized_postal_codes

        for unit in self.units:
            if unit.drone_is_available:
                # list_postal_codes.remove
                print("not done yet")
