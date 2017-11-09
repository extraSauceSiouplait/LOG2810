import lireGraphe


def menuGlobal():

    firstRun = True
    listeDadjacence = {}
    allDist = {}
    choix = ''

    while choix != 'c':

        print("\n***********************************************************"
              "\n\nLogiciel de calcul du plus court chemin dans une ville\n")
        if firstRun:
            try:
                listeDadjacence, chargingStations = lireGraphe.creerGraphe("arrondissements.txt")
                allDist = lireGraphe.createDistanceMatrix(listeDadjacence)
                firstRun = False
                print("*Le fichier de carte par defaut \"arrondissements.txt\" a ete trouve dans le dossier. Carte mise a jour.*\n"
                      "Voici le graphe resultant: \n")
                lireGraphe.printGraphe(listeDadjacence)
                print("\n\n")

            except:
                print("Le fichier de carte par defaut, \"arrondissements.txt\" n'a pas ete trouve dans le dossier. Veuillez \n"
                      "mettre a jour la carte en utilisant l'option 1.\n\n")

        print("----------------   MENU DRONES ET PAQUETS  -----------------\n"
              "(a) Mettre a jour la carte.\n"
              "(b) Determiner le plus court chemin securitaire pour mon paquet.\n"
              "(c) Quitter.\n")


        choix = raw_input("Veuillez entrer votre choix d'option: ")


        if choix == 'a':
            print("------- Menu mise a jour de la carte -----------")

            try:
                listeDadjacence, chargingStations = menuMiseAJour()

            except Exception:
                print("Erreur: Carte non mise a jour.")

            else:
                allDist = lireGraphe.createDistanceMatrix(listeDadjacence)

        elif choix == 'b':
            menuPlusCourtChemin(listeDadjacence,chargingStations, allDist)


    print("Retour au menu principal\n")




def menuPlusCourtChemin(listeDadjacence, chargingStations, allDistanceMatrix):

    isError = True
    exitCall = False

    while not exitCall and isError:

        #
        #Entree de la zone de depart
        #
        zoneDepart = ""

        while zoneDepart not in listeDadjacence:
            zoneDepart = raw_input("\nVeuillez entrer l'entier representant la zone de depart du paquet: ")

            while not zoneDepart.isdigit():
                zoneDepart = raw_input("Ceci n'est pas un entier, veuillez reessayer: ")

            zoneDepart = int(zoneDepart)

            if zoneDepart not in listeDadjacence:
                exitCall = raw_input("Ce point n'est pas dans la carte. Voulez-vous reessayer? (o/n):")

                while exitCall not in ['o' , 'n']:
                    exitCall = raw_input("Cette reponse n'est pas valide. Voulez vous reessayer? (o/n): ")

                if exitCall == 'n':
                    break


        if exitCall == 'n':     #On sort du menuPlusCourtChemin
            break

        #
        #Entree de la zone d'arrivee
        #
        zoneArrivee = ""

        while zoneArrivee not in listeDadjacence:
            zoneArrivee = raw_input("\nVeuillez entrer l'entier representant la zone d'arrivee du paquet: ")

            while not zoneArrivee.isdigit():
                zoneArrivee = raw_input("Ceci n'est pas un entier, veuillez reessayer: ")

            zoneArrivee = int(zoneArrivee)

            if zoneArrivee not in listeDadjacence:
                exitCall = raw_input("Ce point n'est pas dans la carte. Voulez-vous reessayer? (o/n):")

                while exitCall not in ['o' , 'n']:
                    exitCall = raw_input("Cette reponse n'est pas valide. Voulez vous reessayer? (o/n): ")
                if exitCall == 'n':
                    break


        if exitCall == 'n':     #On sort du menuPlusCourtChemin
            break


        #
        #Entree du type de Paquet
        #
        packageType = ""

        while packageType not in [1,2,3]:
            packageType = raw_input("\nVeuillez entrer l'entier representant la taille du paquet (1: petit, 2: moyen, 3: gros): ")

            while not packageType.isdigit():
                packageType  = raw_input("Ceci n'est pas un entier, veuillez reessayer: ")

            packageType  = int(packageType)

            if packageType not in [1,2,3]:
                exitCall = raw_input("Ceci ne correspond pas a une taille de paquet. Voulez-vous reessayer? (o/n):")

                while exitCall not in ['o' , 'n']:
                    exitCall = raw_input("Cette reponse n'est pas valide. Voulez vous reessayer? (o/n): ")

                if exitCall == 'n':
                    break


        if exitCall == 'n':     #On sort du menuPlusCourtChemin
            break


        print("Les donnees d'entree sont conformes. Calcul en cours...\n")


        lireGraphe.afficherParcours(lireGraphe.checkForPossibleRoutes(allDistanceMatrix,chargingStations,
                                                                      zoneDepart, zoneArrivee, packageType-1), packageType-1)
        exitCall = True



def menuMiseAJour():

    isError = True
    exitCall = False
    newListeDadjacence = {}


    while isError and not exitCall:

        nomFichier = raw_input("\nVeuillez entrer le nom du fichier (place dans le repertoire courant) d'ou extraire les donnees "
              "de la carte.\n")

        try:
            newListeDadjacence, charginStations = lireGraphe.creerGraphe(nomFichier)
            isError = False

        except Exception:
            exitCall = raw_input("\nCe fichier n'existe pas ou ne respecte pas le format demande voulez vous reessayer? (o/n)\n")

            while exitCall not in ['o','n']:
                exitCall = raw_input("Reponse non valide, voulez-vous entrer un autre fichier? (o/n)")

            if exitCall == 'n':
                exitCall = True

            else:
                exitCall = False
                continue

    if exitCall:
        raise Exception()

    else:
        print("Carte mise a jour. Voici le resultat:\n")
        lireGraphe.printGraphe(newListeDadjacence)

        return newListeDadjacence, charginStations

