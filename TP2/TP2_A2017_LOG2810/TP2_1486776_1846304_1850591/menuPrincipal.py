import random
from delivery import *
from codes_postaux_process import *


choixMenu = ''
automatecree = False
requests = DeliveryRequest()
automate = PostalCodeAutomaton()
history = RecordKeeper()

def initialize_fleet_TP(fleet, record_keeper):
    types = [[5000, 5], [1000, 10]]
    fleet.add_drone_type(5000)
    fleet.add_drone_type(1000)
    fleet.add_n_drones(types[0][0], types[0][1])
    fleet.add_n_drones(types[1][0], types[1][1])

    fleet.reequilibrate_fleet(automate)
    fleet.deliver_packages(record_keeper)
    record_keeper.reset_stats()

print("Bienvenue dans le menu principal du TP2 d'Alex, Marc-Andre et Mathieu!\n"
      "A quelle fonctionnalite souhaitez-vous acceder? (a,b,c ou d)\n")

while choixMenu != 'e':
    choixMenu = input("(a) Creer l'automate\n"
                          "(b) Traiter des requetes\n"
                          "(c) Éxécuter un cycle sans nouvelles requetes\n"
                          "(d) Afficher les statistiques\n"
                          "(e) Quitter\n")



    if choixMenu == 'a' and automatecree == False:
        try:
            automate.creer_arbre_addresses("CodesPostaux.txt")

            fleet = DroneFleet(automate.unorganized_postal_codes[0])

            initialize_fleet_TP(fleet, history)

            print("\nL'automate a ete cree avec succes\n")

            automatecree = True

        except:
            print("\nLa creation de l'automate a echoue, verifier si le\n"
                  "fichier \"CodesPostaux\" est bien present dans le dossier\n")

    elif choixMenu == 'a' and automatecree == True:
        choix = input("\nL'automate a deja ete cree, voulez-vous le mettre a jour? (o/n)")
        if choix == 'o':
            try:
                nomFichier = input("Entrer le nom du fichier contenant les codes postaux valides:  ")
                automate.creer_arbre_addresses(nomFichier)

                requests.clear_all()
                fleet.reset_all(automate.unorganized_postal_codes[0])

                initialize_fleet_TP(fleet, history)

                print("Automate mise a jour\n")

            except:
                print("\nFichier introuvable ou incompatible\n")
                automatecree = False
        else:
            print("Retour au menu principal\n")



    elif choixMenu == 'b'  and automatecree == False:
        print("\nVeuillez creer l'automate avant de traiter des requetes\n")

    elif choixMenu == 'b' and automatecree == True:

        choixRequete = input("Entrer le nom du fichier contenant la requete: ")

        try:
            requests.traiter_les_requetes(choixRequete, automate, fleet, history)
            history.add_cycle()

        except Exception as e:
            print(str(e) + " Fichier introuvable ou incompatible\n")



    elif choixMenu == 'c' and automatecree == True:
        emptyRequests = open("r0.txt", "r+")
        requests.traiter_les_requetes("r0.txt", automate, fleet, history)
        history.add_cycle()

    elif choixMenu == 'c' and automatecree == False:
        print("\nVeuillez creer l'automate avant de traiter des requetes\n")



    elif choixMenu == 'd'and automatecree == False:
        print("\nVeuillez creer l'automate avant d'afficher les statistiques\n")

    elif choixMenu == 'd' and automatecree == True:

        history.imprimer_statistiques(automate, fleet)
        print("\n")


print("****** Fin du programme. Au revoir! ******")
