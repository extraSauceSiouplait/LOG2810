# coding=utf-8
from classes_drones import *


class PostalCodeAutomaton:
    possible_states = [0, 1, 2, 3, 4, 5, 6]

    def __init__(self):
        self.name = "Dave"
        self.recognized_postal_codes = {}
        self.unorganized_postal_codes = []

    @staticmethod
    def is_postal_code_format(word):
        """

        :param word: Le string à évaluer
        :return: Retourne un idicateur si "word" est de format X1XX1X
        :rtype: bool
        """
        if len(word) != 6 or not (word[0].isnumeric() or word[1].isalpha() or word[2].isnumeric() or word[3].isalpha or
                                    word[4].isnumeric() or word[5].isalpha):
            print("This file contains invalid entries. " + word + " is not a postal code." +
                  "Un code postal est une chaîne de six caractères alphanumériques, "
                  "qui utilise le format A1B2C3, alternant lettres et chiffres.")
            return False

        else:
            return True

    def validate_postal_code(self, postal_code, keeper):
        """

        :param postal_code: le code postal à valider (chercher dans la liste des codes postaux ajoutés)
        :param keeper: Un registre à fins statistiques
        :return: Indique si le code est valide ou non
        """
        current_state = self.possible_states[0]
        code = list(postal_code)

        while current_state != self.possible_states[6]:

            if current_state == self.possible_states[0]:
                if not code[0] in self.recognized_postal_codes:
                    return False
                else:
                    current_state = self.possible_states[1]

            if current_state == self.possible_states[1]:
                if not code[1] in self.recognized_postal_codes[code[0]]:
                    return False
                else:
                    current_state = self.possible_states[2]

            if current_state == self.possible_states[2]:
                if not code[2] in self.recognized_postal_codes[code[0]][code[1]]:
                    return False
                else:
                    current_state = self.possible_states[3]

            if current_state == self.possible_states[3]:
                if not code[3] in self.recognized_postal_codes[code[0]][code[1]][code[2]]:
                    return False
                else:
                    current_state = self.possible_states[4]

            if current_state == self.possible_states[4]:
                if not code[4] in self.recognized_postal_codes[code[0]][code[1]][code[2]][code[3]]:
                    return False
                else:
                    current_state = self.possible_states[5]

            if current_state == self.possible_states[5]:
                if not code[5] in self.recognized_postal_codes[code[0]][code[1]][code[2]][code[3]][code[4]]:
                    return False
                else:
                    current_state = self.possible_states[6]

        return True

    def creer_arbre_addresses(self, filename):
        """

        :param filename: le fichier.txt d'ou importer les codes postaux
        """
        data = open("./" + filename, "r")
        self.recognized_postal_codes = {}

        for line in data:
            temp = line.strip('\n').strip('\r').strip(' ')
            word = list(temp)

            if self.is_postal_code_format(word):

                if not word[0] in self.recognized_postal_codes:
                    self.recognized_postal_codes[word[0]] = {}

                if not word[1] in self.recognized_postal_codes[word[0]]:
                    self.recognized_postal_codes[word[0]][word[1]] = {}

                if not word[2] in self.recognized_postal_codes[word[0]][word[1]]:
                    self.recognized_postal_codes[word[0]][word[1]][word[2]] = {}

                if not word[3] in self.recognized_postal_codes[word[0]][word[1]][word[2]]:
                    self.recognized_postal_codes[word[0]][word[1]][word[2]][word[3]] = {}

                if not word[4] in self.recognized_postal_codes[word[0]][word[1]][word[2]][word[3]]:
                    self.recognized_postal_codes[word[0]][word[1]][word[2]][word[3]][word[4]] = {}

                if not word[5] in self.recognized_postal_codes[word[0]][word[1]][word[2]][word[3]][word[4]]:
                    self.recognized_postal_codes[word[0]][word[1]][word[2]][word[3]][word[4]][word[5]] = {}

                self.recognized_postal_codes[word[0]][word[1]][word[2]][word[3]][word[4]][word[5]] = temp
                self.unorganized_postal_codes.append(temp)

        data.close()
