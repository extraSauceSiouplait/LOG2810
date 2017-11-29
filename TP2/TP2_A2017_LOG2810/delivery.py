import queue


class Delivery:
    def __init__(self, origin, destination, weight):
        self.origin = origin
        self.destination = destination
        self.weight = int(weight)


class DeliveryRequest:
    def __init__(self):
        self.request_queue = queue.Queue()

    def clear_all(self):
        self.request_queue.queue.clear()

    def traiter_les_requetes(self, filename, automat, fleet, keeper):
        """

        :param filename: Le fichier.txt de requete à traiter
        :param automat:  La machine à état validant les codes postaux
        :param fleet:   Une flotte de drones
        :param keeper:  Le registre des stats
        """
        data = open("./" + filename, "r")
        print("\n")

        for line in data:
            temp = line.strip('\n').strip('\r').split(" ")

            if (automat.validate_postal_code(temp[0], keeper) and automat.validate_postal_code(temp[1], keeper) and (
                    temp[2]).isdigit()):
                if temp[0] == temp[1]:
                    print("\nA request did not meet standards: \n\t" +
                          temp[0] + " is the origin and the destination of the request. \n\tIt does'nt need to be processed by "
                          "drone delivery.\n\tWill be counted as a process delivery.\n")

                    keeper.add_request_processed()
                print("origin: " + temp[0] + "\tDestination: " + temp[1] + "\tWeight: " + temp[2])
                d = Delivery(temp[0], temp[1], temp[2])
                self.request_queue.put(d)

            else:
                print("\nA request did not meet standards:")
                keeper.add_invalid_request()

                if not automat.validate_postal_code(temp[0], keeper):
                    print("\t" + temp[0] + " is not a valid postal code\n")

                if not automat.validate_postal_code(temp[1], keeper):
                    print("\t" + temp[1] + " is not a valid postal code\n")

                if not temp[2].isdigit():
                    print("\t" + temp[2] + " is not a valid weight\n")

        temp_queue = queue.Queue()

        while not self.request_queue.empty():

            delivery = self.request_queue.get()

            if not fleet.assign_delivery_to_drone(delivery):

                if delivery.weight <= max(fleet.types.keys()):
                    fleet.send_a_drone_to(delivery)
                    temp_queue.put(delivery)
                else:
                    print("The maximum deliverable weight is " + str(
                        max(fleet.types.keys())) + ". With a weight of " + str(
                        delivery.weight) + ", this delivery is not possible.")
                    keeper.add_invalid_request()

        while not temp_queue.empty():
            self.request_queue.put(temp_queue.get())

        print("fleet equilibration")
        fleet.reequilibrate_fleet(automat)

        print("package delivery\n\n")
        fleet.deliver_packages(keeper)

        data.close()


class RecordKeeper:
    def __init__(self):
        self.successful_deliveries = {}
        self.n_processed_requests = 0
        self.n_invalid_requests = 0
        self.n_completed_cycles = 0

    def reset_stats(self):
        self.successful_deliveries.clear()
        self.n_processed_requests = 0
        self.n_processed_requests = 0
        self.n_completed_cycles = 0

    def add_cycle(self):
        self.n_completed_cycles += 1

    def add_successful_delivery(self, drone_max_load, number_of_packages):

        """

        :param drone_max_load: le type de drone que l'on souhaite affecter
        :param number_of_packages: le nombre de paquets dans la livraison
        """
        if drone_max_load not in self.successful_deliveries:
            self.successful_deliveries[drone_max_load] = []

        self.successful_deliveries[drone_max_load].append(float(number_of_packages))

    def add_request_processed(self):
        self.n_processed_requests += 1

    def add_invalid_request(self):
        self.n_invalid_requests += 1

    def count_delivered_packages_by_model(self, drone_max_load):
        """

        :param drone_max_load: le type de drone qui nous interesse
        :return: nombre de paquets totaux délivrés par ce type de drone
        """
        tot = 0
        for nPackages in self.successful_deliveries[drone_max_load]:
            tot += nPackages
        return tot

    def count_total_delivered_packages(self):
        tot = 0
        for model in self.successful_deliveries:
            tot += self.count_delivered_packages_by_model(model)
        return tot

    @staticmethod
    def n_drones_in_neighborhoods(postal_code_list, fleet):
        """

        :param postal_code_list: Liste de codes postaux des stations de dépot
        :param fleet: FLotte de drone
        """
        for postal_code in postal_code_list:
            n = 0
            for unit in fleet.units:
                if unit.current_location == postal_code:
                    n += 1
            print(postal_code + ": " + str(n) + " drones")

    def get_average_n_packages_per_delivery(self, drone_max_load):
        """

        :param drone_max_load: Type de drone qui nous intéresse
        :return:
        """
        if drone_max_load in self.successful_deliveries:
            tot = 0.0

            for nPackages in self.successful_deliveries[drone_max_load]:
                tot += nPackages

            return tot / float(len(self.successful_deliveries[drone_max_load]))

        else:
            return 0

    def imprimer_statistiques(self, automat, fleet):

        """

        :param automat: Machine à état validant les codes postaux des stations
        :param fleet: Flotte de drone
        """
        print("************************* STATS ****************************")
        print("\nLe nombre de livraisons completes a date: " + str(self.n_processed_requests))
        print("Le nombre de requetes invalides: " + str(self.n_invalid_requests))
        print("\nNombre moyen de paquets transporte lors de livraisons par les petits drones: " + str(
            self.get_average_n_packages_per_delivery(1000)))
        print("\nNombre moyen de paquets transporte lors de livraisons par les grands drones: " + str(
            self.get_average_n_packages_per_delivery(5000)) + "\n")

        print("****************************************\nNombre de drone(s) dans chaque(s) quartier(s) apres " + str(
            self.n_completed_cycles) + " cycle(s).\n")
        self.n_drones_in_neighborhoods(automat.unorganized_postal_codes, fleet)
