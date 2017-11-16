import menuDronesEtPackages
import dejeunerEtDessert


choixMenu = ''

while choixMenu != 'c':
    choixMenu = raw_input("Bienvenue dans le menu principal du TP1 d'Alex, Marc-Andre et Mathieu!\n"
      "A quelle fonctionnalite souhaitez-vous acceder? (a,b ou c)\n\n"
                          "(a) Partie 1: Drones et livraison de paquets\n"
                          "(b) Partie 2: Recettes et diagramme de Hasse\n"
                          "(c) Quitter\n\n")

    if choixMenu == 'a':
        menuDronesEtPackages.menuGlobal()

    elif choixMenu == 'b':
        dejeunerEtDessert.menuGlobal()


print("****** Fin du programme. Au revoir! ******")
