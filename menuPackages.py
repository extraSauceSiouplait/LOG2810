import lireGraphe


listeDadjacence = {}


def menuGlobal(listeDadjacence):

    print("Logiciel de calcul du plus court chemin dans une ville"
          "----------------   MENU GLOBAL  -----------------"
          "(1) Mettre a jour la carte."
          "(2) Determiner le plus court chemin securitaire."
          "(3) Quitter.")

    choixGlobal = input("Veuillez entrer votre choix d'option")

def menuMiseAJour(listeDadjacence):

    nomFichier = input("Veuillez entrer le nom du fichier (place dans le repertoire courant) d'ou extraire les donnees"
          "de la carte.")

    try:
        listeDadjacence = lireGraphe.creerGraphe(nomFichier)

    while except TypeError is True:
        print("Le programme a rencontre une erreur lors de la lecture")
        menuMiseAJour(listeDadjacence)


    Print("Carte mise à jour. Voici le résultat:")
    lireGraphe.printGraphe(listeDadjacence)
