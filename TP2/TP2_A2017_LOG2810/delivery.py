import queue

class Delivery:
    def __init__(self, origin, destination, weight):
        self.origin = origin
        self.destination = destination
        self.weight = int(weight)



class DeliveryRequest:
    def __init__(self):
        self.request_queue = queue.Queue()
        #self.urgency_queue = queue.Queue()

    def traiter_les_requetes(self, filename, automat, fleet, keeper):
        data = open("./" + filename, "r")
        for line in data:
            temp = line.strip('\n').strip('\r').split(" ")
            # print(temp)
            if (automat.validate_postal_code(temp[0], keeper) and automat.validate_postal_code(temp[1], keeper) and (
            temp[2]).isdigit()):
                print("origin: " + temp[0] + "\tDestination: " + temp[1] + "\tWeight: " + temp[2])
                d = Delivery(temp[0], temp[1], temp[2])
                self.request_queue.put(d)
            else:
                print("A request did not meet standards:")
                if (not automat.validate_postal_code(temp[0], keeper)):
                    print("\t" + temp[0] + " is not a valid postal code")
                if (not automat.validate_postal_code(temp[1], keeper)):
                    print("\t" + temp[1] + " is not a valid postal code")
                if (not temp[2].isdigit()):
                    print("\t" + temp[2] + " is not a valid weight")

        print("creating temp queue")
        temp_queue = queue.Queue()

        fleet.summarize_fleet_stats()

        """
        print("verifying priority queue")
        while (not self.urgency_queue.empty()):
            delivery = self.urgency_queue.get()
            if not fleet.assign_delivery_to_drone(delivery):
                fleet.send_a_drone_to(delivery)
                temp_queue.put(delivery)

        # fleet.summarize_fleet_stats()

        """
        print("verifying reqQueue")
        while (not self.request_queue.empty()):
            delivery = self.request_queue.get()
            # print("delivery weight: " + str(delivery.weight))
            if not fleet.assign_delivery_to_drone(delivery):
                if delivery.weight <= max(fleet.types.keys()):
                    # print("delivery not possible at the moment. Sending a drone to pickup location")
                    fleet.send_a_drone_to(delivery)
                    temp_queue.put(delivery)
                else:
                    print("The maximum deliverable weight is " + str(
                        max(fleet.types.keys())) + ". With a weight of " + str(
                        delivery.weight) + ", this delivery is not possible.")
                    keeper.add_invalid_request()

        fleet.summarize_fleet_stats()

        print("transferring contents of temp_queue to request_queue")
        while (not temp_queue.empty()):
            #self.urgency_queue.put(temp_queue.get())
            self.request_queue.put(temp_queue.get())

        print("fleet equilibration")
        fleet.reequilibrate_fleet(automat)

        fleet.summarize_fleet_stats()

        print("package delivery")
        fleet.deliver_packages(keeper)

        fleet.summarize_fleet_stats()

class RecordKeeper:
    def __init__(self):
        self.successful_deliveries = {}
        self.n_processed_requests = 0
        self.n_invalid_requests = 0


    def add_successful_delivery(self, drone_max_load, number_of_packages):

        if drone_max_load not in self.successful_deliveries:
            self.successful_deliveries[drone_max_load] = []

        self.successful_deliveries[drone_max_load].append(number_of_packages)

    def add_request_processed(self):
        self.n_processed_requests += 1

    def add_invalid_request(self):
        self.n_invalid_requests += 1

    def count_delivered_packages_by_model(self,model):
        tot = 0
        for nPackages in self.successful_deliveries[model]:
            tot += nPackages
        return tot

    def count_total_delivered_packages(self):
        tot = 0
        for model in self.successful_deliveries:
            tot += self.count_delivered_packages_by_model(model)
        return tot



    def get_average_n_packages_per_delivery(self, drone_max_load):
        if drone_max_load in self.successful_deliveries:
            tot = 0
            for nPackages in self.successful_deliveries[drone_max_load]:
                tot += nPackages
            return tot/len(self.successful_deliveries[drone_max_load])
        else:
            return 0

    def imprimerLesStatistiques(self):
        #### A MODIFIER #####

        print("Le nombre de livraisons completes a date: " + str(self.count_total_delivered_packages()))
        print("Le nombre de requetes invalides: " + str(self.n_invalid_requests))
        # print le nombre de drones dans chaque quartier
        # print le nombre moyen de colis transportes par un drone a petite capacite
        # print le nombre moyen de colis transportes par un drone a grande capacite


