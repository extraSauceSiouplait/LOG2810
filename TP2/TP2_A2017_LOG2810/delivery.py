import Queue


class Delivery:
    def __init__(self, origin, destination, weight):
        self.origin = origin
        self.destination = destination
        self.weight = int(weight)


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
