import numpy


# from nested_dict import nested_dict

def creerGrapheOriente(str, bool, recette={}, ingredient={}):
    data = open("./" + str, "r")  # Ouvrir le fichier en parametre

    for line in data:
        temp = line.strip('\n').strip('\r').split(",")                          # Enlever \n et \r et separer la ligne en 2 autour de la virgule
        if len(temp) == 2:                                                      # Pour ignorer la ligne vide
            temp[0] = int(temp[0])                                              # Convertir string en int
            if any(x.isalpha() for x in temp[1]):                               # Si la deuxieme valeur est alpha, mettre dans recette
                recette[temp[0]] = temp[1]
                # ex: 1, dejeuner
                #    recette[1] = "dejeuner"

            elif temp[1].isdigit():                                             # Si la deuxieme valeur est digit, mettre dans ingredient
                temp[1] = int(temp[1])
                if (not ingredient.has_key(temp[1])):
                    ingredient[temp[1]] = []                                    # Creer une liste pour chaque recette qui contienne des ingredients
                if temp[0] not in ingredient[temp[1]]:                          # Si l'ingredient n'est pas deja dans la liste
                    ingredient[temp[1]].append(temp[0])

    if bool:
        printRecette(recette, ingredient)
    return (recette, ingredient)


def printRecette(recette, ingredient):
    for vertex in sorted(recette):
        # Dejeuner, (1) :
        listeIngredient = recette[vertex] + ", (" + str(vertex) + ") : "
        if ingredient.has_key(vertex):                                          # Si cette recette a des ingredients
            for x in ingredient[vertex]:                                        # Afficher tout les ingredients de la liste
                listeIngredient = listeIngredient + recette[x] + "(" + str(x) + "), "

        print(listeIngredient[:-2])                                             # [:-2] enleve le ", " a la fin du string


def affichage(noeud, recette, ingredient, firstTime):                           # Fonction recursive utiliser pour genererHasse

    listeIngredient = recette[noeud] + " (" + str(noeud) + ") : "               # Affichage de la recette
    if noeud in ingredient:                                                     # Si la recette a des ingredients
        for x in ingredient[noeud]:                                             # Parcourir tout les ingredients
            if x in ingredient and firstTime:                                   # Si l'ingredient a lui meme des ingredients
                if x in ingredient[
                    x]:                                                         # Pour eviter boucle infini, ne repeter qu'une fois si la recette est aussi dans sa propre liste d'ingredient
                    firstTime = 0
                affichage(x, recette, ingredient, firstTime)  # Recursion
            listeIngredient = listeIngredient + recette[x] + " (" + str(x) + "), "
    print(listeIngredient[:-2])


def genererHasse(str):
    # Generer les dictionaires de recette et d'ingredient sans affichage (bool = 0)
    recette, ingredient = creerGrapheOriente(str, 0)
    print("\n"
          "************** DIAGRAMME DE HASSE ***********")

    # Afficher chaque recette avec la fonction recursive affichage
    for x in recette:
        affichage(x, recette, ingredient, 1)
        print("")

        # MAIN
        # Demander a l'utilisateur d'entrer a, b ou c pour ouvrir un menu
        # Si une autre lettres est entrer, demander de nouveau


lettre = ''
while lettre != "c":
    lettre = raw_input("\n----------- MENU GENERAL --------------------\n"
                       "(a) Creer et afficher le graphe des recettes.\n"
                       "(b) Generer et afficher le diagramme de Hasse.\n"
                       "(c) Quitter.\n")
    if lettre == "a":
        creerGrapheOriente("manger.txt", 1)

    elif lettre == "b":
        genererHasse("manger.txt")
