import datetime
import sys
import time
from collections import deque

import djcase
from fltk import *
import random

import dragon
import personnage


class Donjon:
    def __init__(self, fichier, type, manager):
        self.dragons = None
        self.personnage = None
        self.fichier = fichier
        self.startedTime = None
        self.agencement = None
        self.personnages = {}
        self.nom = None
        self.donjon = None
        self.type = type
        self.cases = []
        self.manager = manager
        self.playing = True

        self.charger(fichier)

    def charger(self, fichier):
        """
        Charge les données à partir d'un fichier spécifié.
        (joueur,dragons,cases)

        :param fichier: Le chemin du fichier à charger.
        :type fichier: str
        """
        try:
            with open(fichier, "r", encoding='utf-8') as f:
                contenu = f.read()
        except FileNotFoundError:
            print(f"Le fichier '{fichier}' n'existe pas.")
            return

        parties = contenu.split("\n\n")
        if len(parties) != 2:
            print("Le fichier n'est pas correctement formaté.")
            return

        agencement = [list(ligne) for ligne in parties[0].split("\n")]

        self.personnages = {}

        infos = parties[1].split("\n")


        for info in infos:
            if len(info) == 0:
                continue
            elements = info.split()
            if len(elements) < 3:
                print("Le fichier n'est pas correctement formaté.")
                return
            nom = elements[0]
            ligne = elements[1]
            colonne = elements[2]
            niveau = elements[3] if len(elements) > 3 else 1
            if nom == "N":
                self.nom = colonne
                continue
            self.personnages.setdefault(nom, []).append({"ligne": ligne, "colonne": colonne, "niveau": niveau})
        self.agencement = agencement



    def get_type(self):
        """
        Retourne le type du donjon (parmi ice et desert)
        :return: str
        """
        return self.type

    def drawTimer(self,posX,posY):
        """
        Cette fonction permet de dessiner le timer dans la fenetre
        """
        efface("timer")
        texte(posX, posY, datetime.datetime.utcfromtimestamp(self.getTimer()).strftime("%M:%S"), tag="timer")
    def getTimer(self) -> float:
        """
        Cette fonction recupere le temps de la partie actuel.

        En comparant le temps unix du lancement de la partie au temps durant la partie
        """
        return time.time() - self.startedTime
    def get_fichier_path(self):
        """
        Cette fonction retourne le fichier auquel on a chargé le donjon.
        :return: str
        """
        return self.fichier

    def reset_donjon(self):
        """
        Cette fonction permet de réinitialiser le donjon à son état d'origine.
        Avant tout changement effectué par le joueur.
        :return: void
        """
        self.donjon = None
        self.personnage = None
        self.dragons = None

        texte(0, 0, "", ancrage='center')

        self.affiche_fltk()

    def affiche_donjon(self):
        """
        Cette fonction permet de retourner une liste de liste de la composition du donjon.
        Sois en la recuperant directement dans le fichier config sois en recuperant dans le cache.
        :return: list
        """
        if self.agencement is None:
            print("Le donjon n'a pas été chargé.")
            return

        if self.donjon is not None:
            return self.donjon

        salles = []
        for ligne in self.agencement:
            salles_ligne = []
            for car in ligne:
                if car == " ":
                    pass
                else:
                    salles_ligne.append(self.get_salle(car))
            salles.append(salles_ligne)

        self.donjon = salles
        return salles

    def get_salle(self, car):
        """
        Cette fonction peremt de convertir un caractère à sa case associé.

        Exemple: get_salle(╔)
        >>>(False, True, True, False)

        :param car: 
        :return: 
        """
        salles_dict = {
            " ": None,
            "╔": (False, True, True, False),
            "╦": (False, True, True, True),
            "╗": (False, False, True, True),
            "╠": (True, True, True, False),
            "╬": (True, True, True, True),
            "╣": (True, False, True, True),
            "╚": (True, True, False, False),
            "╩": (True, True, False, True),
            "╝": (True, False, False, True),
            "║": (True, False, True, False),
            "═": (False, True, False, True),
            "╨": (True, False, False, False),
            "╡": (False, False, False, True),
            "╥": (False, False, True, False),
            "╞": (False, True, False, False)
        }
        return salles_dict.get(car, None)

    def get_donjon(self):
        """
        Cette fonction permet de recuperer la composition du donjon
        :return: obj
        """
        return self.donjon

    def affiche_fltk(self):
        """
        Cette fonction permet de retranscrire la composition du donjon en un affichage
        réel dans une interface de jeu.

        La fonction retranscris également le positionnement du joueur et des dragons
        :return: void
        """
        efface_tout()

        images = {
            (False, True, True, False): f"tile/{self.type}/t1.png",
            (False, True, True, True): f"tile/{self.type}/t8.png",
            (False, False, True, True): f"tile/{self.type}/t2.png",
            (True, True, True, False): f"tile/{self.type}/t7.png",
            (True, True, True, True): f"tile/{self.type}/t9.png",
            (True, False, True, True): f"tile/{self.type}/t5.png",
            (True, True, False, False): f"tile/{self.type}/t4.png",
            (True, True, False, True): f"tile/{self.type}/t6.png",
            (True, False, False, True): f"tile/{self.type}/t3.png",
            (True, False, True, False): f"tile/{self.type}/t11.png",
            (False, True, False, True): f"tile/{self.type}/t10.png",
            (False, False, True, False): f"tile/{self.type}/t12.png",
            (False, False, False, True): f"tile/{self.type}/t13.png",
            (True, False, False, False): f"tile/{self.type}/t14.png",
            (False, True, False, False): f"tile/{self.type}/t15.png",
        }

        if self.agencement is None:
            print("Le donjon n'a pas été chargé.")
            return

        donjon = self.affiche_donjon()

        largeur_case = 130
        hauteur_case = 130

        nb_cases_largeur = 900 // largeur_case
        nb_cases_hauteur = 800 // hauteur_case

        marge_x = (900 - nb_cases_largeur * largeur_case) // 2 + largeur_case // 2
        marge_y = (800 - nb_cases_hauteur * hauteur_case) // 2 + hauteur_case // 2

        temp_x = marge_x - 55
        temp_y = marge_y
        tag_c = {"x": 0, "y": 0}

        for l in donjon:
            for case in l:
                image_path = images.get(case)
                if image_path is not None:
                    self.cases.append(
                        djcase.Case(temp_x, temp_y, image_path, str(tag_c["x"]) + "_" + str(tag_c["y"]), largeur_case,
                                    hauteur_case))
                    tag_c["x"] += 1
                    temp_x += largeur_case

            temp_y += hauteur_case
            temp_x = marge_x - 55
            tag_c["y"] += 1
            tag_c["x"] = 0

        perso = self.get_personnage()
        perso_pos = perso.get_position()

        perso_case = self.get_case_from_tag(f"{perso_pos[0]}_{perso_pos[1]}")
        perso_case_pos = perso_case.get_positions()

        perso.dessiner(perso_case_pos)

        for d in self.get_dragons():
            d_pos = d.get_position()

            d_case = self.get_case_from_tag(f"{d_pos[0]}_{d_pos[1]}")
            d_case_pos = d_case.get_positions()

            d.dessin(d_case_pos)

        mise_a_jour()

    def get_case_from_tag(self, tag) -> djcase:
        """
        Cette fonction retourne la case associé à son tag.
        Car chaque case à un tag associé
        :param tag:
        :return: str
        """
        for c in self.cases:
            if c.get_tag() == tag:
                return c

        return None

    def afficher_personnages(self):
        """
        Permet d'afficher les informations sur le personnage et les dragons du donjon
        :return:void
        """
        if self.personnages is None:
            print("Le donjon n'a pas été chargé.")
            return

        for nom, personnages in self.personnages.items():
            print(f"Informations pour {nom}:")
            for perso in personnages:
                print(f"Coordonnées: ({perso['ligne']}, {perso['colonne']})")
                print(f"Niveau: {perso['niveau']}")

    def get_personnage(self):
        """
        Permet de recuperer l'instance de l'objet Personnage
        :return: obj
        """
        if self.personnage is not None:
            return self.personnage

        position = None
        niveau = None

        for nom, personnages in self.personnages.items():
            if nom == "A":
                position = (int(personnages[0]['ligne']), int(personnages[0]['colonne']))
                niveau = personnages[0]['niveau']
        self.personnage = personnage.Personnage(position, niveau, self.manager, "perso")

        return self.personnage

    def get_dragons(self):
        """
        Permet de recuperer la liste des instances des dragons du donjon
        :return: list
        """
        if self.dragons is not None:
            return self.dragons

        dragons = []
        count = 0
        for nom, personnages, in self.personnages.items():
            if nom == "D":
                for drag in personnages:
                    position = (int(drag['ligne']), int(drag['colonne']))
                    niveau = drag['niveau']

                    dragons.append(dragon.Dragon(position, niveau, count))
                    count += 1

        self.dragons = dragons
        return dragons

    def set_dragons(self, drags):
        """
        Cette fonction permet de changer le nombre de dragon présent dans le donjon
        :param drags:
        :return: void
        """
        self.dragons = drags

    def get_name(self):
        """
        Cette fonction permet de retourner le nom du donjon émis dans la configuration
        :return: str
        """
        return self.nom

    def intention(self):
        """
        Cette fonction est une fonction recursive qui prédit l'intention du joueur (son chemin)
        Si cela est possible alors on va retourner la liste des cases pour arriver au dragon.
        Autrement on retournera None
        :return: list
        """
        # Fonction interne pour effectuer une recherche récursive dans le donjon
        def recherche(position, visite):
            # Vérifie si la position actuelle contient un dragon
            for dragon in self.get_dragons():
                if position == dragon.get_position():
                        # Si oui, renvoie le chemin menant à cette position et le niveau du dragon
                        return [position], dragon.get_niveau()
            # Si la position a déjà été visitée, renvoie None
            if position in visite:
                return None
            # Ajoute la position actuelle aux positions visitées
            visite.add(position)
            # Liste pour stocker les résultats des recherches récursives
            resultats = []
            # Parcourt les positions voisines connectées à la position actuelle
            for direction in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                nouvelle_position = (position[0] + direction[0], position[1] + direction[1])
                if nouvelle_position[0] <0:
                    nouvelle_position = (0,nouvelle_position[1])
                elif nouvelle_position[1]< 0:
                    nouvelle_position = (nouvelle_position[0],0)
                if nouvelle_position in visite:
                    continue

                if self.connecte(position, nouvelle_position):
                    # Effectue une recherche récursive à partir de la nouvelle position
                    resultat = recherche(nouvelle_position, visite)
                    if resultat is not None:
                        resultats.append(resultat)
            # Si aucun résultat n'a été trouvé, renvoie None
            if not resultats:
                return None
            # Sélectionne le résultat avec le niveau de dragon le plus élevé
            niveau_max = max(resultats, key=lambda x: x[1])[1]
            resultats = [resultat for resultat in resultats if resultat[1] == niveau_max]
            chemin, niveau = random.choice(resultats)
            # Renvoie le chemin menant à la position du dragon et son niveau
            return [position] + chemin, niveau

        # Effectue une recherche récursive à partir de la position initiale de l'aventurier
        resultat = recherche(self.get_personnage().get_position(), set())
        if resultat is None:
            return None
        chemin, niveau = resultat
        # Renvoie le chemin menant au dragon le plus proche avec le niveau le plus élevé
        return chemin

    def connecte(self, position1, position2):
        """
        Cette fonction permet de verifier si 2 cases sont connecté par un passage.
        Si cela est possible on retournera True autrement False
        :param position1:
        :param position2:
        :return: bool
        """
        donjon = self.affiche_donjon()
        print(donjon)
        y1, x1 = position1
        y2, x2 = position2

        num_lignes = len(donjon)
        num_colonnes = len(donjon[0])

        if x1 == x2 and y1 == y2 + 1:
            if 0 <= x1 < num_lignes and 0 <= y1 < num_colonnes and 0 <= x2 < num_lignes and 0 <= y2 < num_colonnes:
                return donjon[x1][y1][3] and donjon[x2][y2][1]
        elif x1 == x2 and y1 == y2 - 1:
            if 0 <= x1 < num_lignes and 0 <= y1 < num_colonnes and 0 <= x2 < num_lignes and 0 <= y2 < num_colonnes:
                return donjon[x1][y1][1] and donjon[x2][y2][3]
        elif x1 == x2 + 1 and y1 == y2:
            if 0 <= x1 < num_lignes and 0 <= y1 < num_colonnes and 0 <= x2 < num_lignes and 0 <= y2 < num_colonnes:
                return donjon[x1][y1][0] and donjon[x2][y2][2]
        elif x1 == x2 - 1 and y1 == y2:
            if 0 <= x1 < num_lignes and 0 <= y1 < num_colonnes and 0 <= x2 < num_lignes and 0 <= y2 < num_colonnes:
                print("tt", y1, x1, y2, x2)
                return donjon[x1][y1][2] and donjon[x2][y2][0]
        else:
            return False

    def pivoter(self, position):
        """
        Cette fonction permet de faire pivoter une case en décalant sa composition dans le sens d'une
        aiguille de montre.
        Puis on actualise le donjon.
        :param position:
        :return:
        """
        donjon = self.affiche_donjon()
        case = donjon[position[0]][position[1]]
        correspondances = {
            (False, True, True, False): (False, False, True, True),
            (False, True, True, True): (True, False, True, True),
            (False, False, True, True): (True, False, False, True),
            (True, True, True, False): (False, True, True, True),
            (True, True, True, True): (True, True, True, True),
            (True, False, True, True): (True, True, False, True),
            (True, True, False, False): (False, True, True, False),
            (True, True, False, True): (True, True, True, False),
            (True, False, False, True): (True, True, False, False),
            (True, False, True, False): (False, True, False, True),
            (False, True, False, True): (True, False, True, False),
            (False, False, True, False): (False, False, False, True),
            (False, False, False, True): (True, False, False, False),
            (True, False, False, False): (False, True, False, False),
            (False, True, False, False): (False, False, True, False),
        }
        donjon[position[0]][position[1]] = correspondances[case]
        print(donjon[position[0]][position[1]])

        self.affiche_fltk()

    def fin_partie(self):
        """Cette fonction permet de verifier si le donjon est completé """
        if len(self.dragons) == 0:
            sys.exit()
