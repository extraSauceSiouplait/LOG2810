import numpy
import copy

# from nested_dict import nested_dict

def creerGrapheOriente(nomFichier, printCall):

    indicesToRecettes={}
    ingredients={}

    data = open("./" + nomFichier, "r")  # Ouvrir le fichier en parametre

    for line in data:
        temp = line.strip('\n').strip('\r').split(",")                          # Enlever \n et \r et separer la ligne en 2 autour de la virgule

        if len(temp) == 2:                                                      # Pour ignorer la ligne vide
            temp[0] = int(temp[0])                                              # Convertir string en int

            if any(x.isalpha() for x in temp[1]):                               # Si la deuxieme valeur est alpha, mettre dans recette
                indicesToRecettes[temp[0]] = temp[1]
                # ex: 1, dejeuner
                #    recette[1] = "dejeuner"

            elif temp[1].isdigit():                                             # Si la deuxieme valeur est digit, mettre dans ingredient
                temp[1] = int(temp[1])

                if not ingredients.has_key(temp[0]):
                    ingredients[temp[0]] = []                                    # Creer une liste de liste, chaque ingredient a une liste de recette(s) dans lesquelles il est present

                if temp[1] not in ingredients[temp[0]]:                          # Si l'ingredient n'est pas deja dans la liste
                    ingredients[temp[0]].append(temp[1])

    if printCall:
        print("\n*******************************************************************\n"
              "Liste des ingredients et des recettes auxquelles ils sont associes.\n")
        printRecettes(indicesToRecettes, ingredients)
    return (indicesToRecettes, ingredients)


def printRecettes(indicesToRecettes, ingredients):
    for recette in sorted(indicesToRecettes):
        # Dejeuner, (1) :
        listeIngredients = indicesToRecettes[recette] + "(" + str(recette) + ") : "
        if ingredients.has_key(recette):                                          # Si cette recette a des ingredients
            for ingredient in ingredients[recette]:                                        # Afficher tout les ingredients de la liste
                listeIngredients = listeIngredients + indicesToRecettes[ingredient] + "(" + str(ingredient) + "), "

        print(listeIngredients[:-2])                                             # [:-2] enleve le ", " a la fin du string


def hasseRecursif(ingredient, recettesAssociees, ingredients, indiceToRecettes, firstEncounter, listeOutput):

    listeOutput  +=  indiceToRecettes[ingredient] + " (" + str(ingredient) + ") --> "

    for recetteAssociee in recettesAssociees:

        if ingredients.has_key(recetteAssociee):
            hasseRecursif(recetteAssociee, ingredients[recetteAssociee], ingredients, indiceToRecettes, firstEncounter, listeOutput)

        else:
            listeOutput += indiceToRecettes[recetteAssociee] + "(" + str(recetteAssociee) + ") "
            print("Liste " + " : " + listeOutput)


""""
def affichageHasse(ingredient, recettesAssociees, ingredients, indiceToRecettes, firstE):        # Fonction recursive utiliser pour genererHasse

    print("Liste " + str(count) + " : ")



    listeIngredients = ingredient + " (" + indiceToRecettes[ingredient] + ") : "               # Affichage de la recette

    if recettesAssociees != 0:
        for recetteAssociee in recettesAssociees:                                             # Parcourir toutes les recettes associees a l'ingredient

            if  firstTime:                                   # Si l'ingredient a lui meme des ingredients
                if recetteAssociee in ingredients[recetteAssociee]:          # Pour eviter boucle infinie, ne repeter qu'une fois si la recette est aussi dans sa propre liste d'ingredient
                    firstTime = False
                affichageHasse(recetteAssociee, ingredients, indiceToRecettes, firstTime)  # Recursion
            listeIngredients = listeIngredients + indiceToRecettes[x] + " (" + str(x) + "), "
    print(listeIngredients[:-2])
"""

def genererHasse(nomFichier):
    # Generer les dictionaires de recette et d'ingredient sans affichage (printCall = False)
    indicesToRecettes, ingredients = creerGrapheOriente(nomFichier, False)
    print("\n"
          "************** DIAGRAMME DE HASSE ***********")

    # Afficher chaque recette avec la fonction recursive affichage
    ingredientsMinimaux = copy.deepcopy(indicesToRecettes)

    for ingredient in ingredients:

        for recetteAssociee in ingredients[ingredient]:
            if recetteAssociee in ingredientsMinimaux:
                ingredientsMinimaux.pop(recetteAssociee)

    for ingredient in ingredientsMinimaux:
        if ingredients.has_key(ingredient):
            listeOutput = ""
            hasseRecursif(ingredient, ingredients[ingredient], ingredients, indicesToRecettes, True, listeOutput)
            print("")
        else:
            print("Liste : " + indicesToRecettes[ingredient] + "(" + str(ingredient) + ") \n")
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
        creerGrapheOriente("manger.txt", True)

    elif lettre == "b":
        genererHasse("manger.txt")
