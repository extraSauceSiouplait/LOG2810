import queue

class Delivery:
    def __init__(self, origin, destination, weight):
        self.origin = origin
        self.destination = destination
        self.weight = int(weight)


class DeliveryRequest:
    def __init__(self, defaultLocation):
        self.request_queue = queue.Queue()
        self.priority_queue = queue.Queue()

    def traiter_les_requetes(self, filename, auto, fleet, keeper):
        data = open("./" + filename, "r")
        for line in data:
            temp = line.strip('\n').strip('\r').split(" ")
            # print(temp)
            if (auto.validate_postal_code(temp[0], keeper) and auto.validate_postal_code(temp[1], keeper) and (
            temp[2]).isdigit()):
                print("origin: " + temp[0] + "\tDestination: " + temp[1] + "\tWeight: " + temp[2])
                d = Delivery(temp[0], temp[1], temp[2])
                self.request_queue.put(d)
            else:
                print("A request did not meet standards:")
                if (not auto.validate_postal_code(temp[0], keeper)):
                    print("\t" + temp[0] + " is not a valid postal code")
                if (not auto.validate_postal_code(temp[1], keeper)):
                    print("\t" + temp[1] + " is not a valid postal code")
                if (not temp[2].isdigit()):
                    print("\t" + temp[2] + " is not a valid weight")

        print("creating temp queue")
        temp_queue = queue.Queue()

        # fleet.summarize_fleet_stats()

        print("verifying prioroty queue")
        while (not self.priority_queue.empty()):
            delivery = self.priority_queue.get()
            if not fleet.add_delivery(delivery):
                fleet.send_a_drone_to(delivery)
                temp_queue.put(delivery)

        # fleet.summarize_fleet_stats()

        print("verifying reqQueue")
        while (not self.request_queue.empty()):
            delivery = self.request_queue.get()
            # print("delivery weight: " + str(delivery.weight))
            if not fleet.add_delivery(delivery):
                if delivery.weight <= max(fleet.types.keys()):
                    # print("delivery not possible at the moment. Sending a drone to pickup location")
                    fleet.send_a_drone_to(delivery)
                    temp_queue.put(delivery)
                else:
                    print("The maximum deliverable weight is " + str(
                        max(fleet.types.keys())) + ". With a weight of " + str(
                        delivery.weight) + ", this delivery is not possible.")
                    keeper.add_invalid_request()

        # fleet.summarize_fleet_stats()

        print("transferring contents of temp queue to priorityqueue")
        while (not temp_queue.empty()):
            self.priority_queue.put(temp_queue.get())

        print("fleet equilibration")
        fleet.reequilibrate_fleet(auto)

        # fleet.summarize_fleet_stats()

        print("package delivery")
        fleet.deliver_packages(keeper)

        # fleet.summarize_fleet_stats()

class RecordKeeper:
    def __init__(self):
        self.n_successful_deliveries = 0
        self.n_invalid_requests = 0

    def add_delivery(self):
        self.n_successful_deliveries += 1

    def add_invalid_request(self):
        self.n_invalid_requests += 1

    def getDroneAverageDelivery(self, weight_limit_in_grams, fleet):
        return (self.n_successful_deliveries / fleet.types[weight_limit_in_grams])

    def imprimerLesStatistiques(self):
        print("Le nombre de livraisons completes a date: " + str(self.n_successful_deliveries))
        print("Le nombre de requetes invalides: " + str(self.n_invalid_requests))
        # print le nombre de drones dans chaque quartier
        # print le nombre moyen de colis transportes par un drone a petite capacite
        # print le nombre moyen de colis transportes par un drone a grande capacite
