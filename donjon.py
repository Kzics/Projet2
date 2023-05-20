from fltk import *
import random

import dragon
import personnage

class Donjon:
    def __init__(self, fichier, type):
        self.agencement = None
        self.personnages = {}
        self.nom = None
        self.donjon = None
        self.type = type

        self.charger(fichier)

    def charger(self, fichier):
        try:
            with open(fichier, "r", encoding='utf-8') as f:
                contenu = f.read()
                print(contenu)
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

        print(infos)

        for info in infos:
            if len(info) == 0:
                print("er")
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

    def afficher_agencement(self):
        if self.agencement is None:
            print("Le donjon n'a pas été chargé.")
            return

        print("Agencement du donjon :")
        for ligne in self.agencement:
            print("".join(ligne))

    def get_type(self):
        return self.type

    def affiche_donjon(self):
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
        return self.donjon

    def affiche_fltk(self):

        efface_tout()

        images = {
            (False, True, True, False): "tile/desert/t1.png",
            (False, True, True, True): "tile/desert/t8.png",
            (False, False, True, True): "tile/desert/t2.png",
            (True, True, True, False): "tile/desert/t7.png",
            (True, True, True, True): "tile/desert/t9.png",
            (True, False, True, True): "tile/desert/t5.png",
            (True, True, False, False): "tile/desert/t4.png",
            (True, True, False, True): "tile/desert/t6.png",
            (True, False, False, True): "tile/desert/t3.png",
            (True, False, True, False): "tile/desert/t11.png",
            (False, True, False, True): "tile/desert/t10.png",
            (False, False, True, False): "tile/desert/t12.png",
            (False, False, False, True): "tile/desert/t13.png",
            (True, False, False, False): "tile/desert/t14.png",
            (False, True, False, False): "tile/desert/t15.png",
        }

        if self.agencement is None:
            print("Le donjon n'a pas été chargé.")
            return

        donjon = self.affiche_donjon()

        temp_x = 500
        temp_y = 200
        for l in donjon:
            for case in l:
                image_path = images.get(case)
                if image_path is not None:
                    image(temp_x, temp_y, image_path, ancrage='center', tag='im')
                    temp_x += 50

            temp_y += 50
            temp_x = 500

        mise_a_jour()

    def afficher_personnages(self):
        """
        Affiche les informations sur les personnages.
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
        position = None
        niveau = None

        for nom, personnages in self.personnages.items():
            if nom == "A":
                position = (personnages[0]['ligne'], personnages[0]['colonne'])
                niveau = personnages[0]['niveau']
        return personnage.Personnage(position, niveau)

    def get_dragons(self):
        dragons = []

        for nom, personnages, in self.personnages.items():
            if nom == "D":
                for drag in personnages:
                    position = (drag['ligne'], drag['colonne'])
                    niveau = drag['niveau']

                    dragons.append(dragon.Dragon(position, niveau))

        return dragons

    def get_name(self):
        return self.nom

    def intention(self):
        def recherche(position, visite):
            for dragon in self.get_dragons():
                if position == dragon.get_position():
                    return [position], dragon.get_niveau()
            if position in visite:
                return None
            visite.add(position)
            resultats = []
            for direction in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                nouvelle_position = (position[0] + direction[0], position[1] + direction[1])
                if self.connecte(position, nouvelle_position):
                    resultat = recherche(nouvelle_position, visite)
                    if resultat is not None:
                        resultats.append(resultat)
            if not resultats:
                return None
            niveau_max = max(resultats, key=lambda x: x[1])[1]
            resultats = [resultat for resultat in resultats if resultat[1] == niveau_max]
            chemin, niveau = random.choice(resultats)
            return [position] + chemin, niveau

        resultat = recherche(self.get_personnage().get_position(), set())
        if resultat is None:
            return None
        chemin, niveau = resultat
        return chemin

    def rencontre(self):
        # Récupère la position et le niveau de l'aventurier
        position_aventurier = self.get_personnage().get_position()
        niveau_aventurier = self.get_personnage().get_niveau()
        # Parcourt la liste des dragons
        for dragon in self.get_dragons():
            # Récupère la position et le niveau du dragon
            position_dragon = dragon.get_position()
            niveau_dragon = dragon.get_niveau()
            # Vérifie si le dragon se trouve à la même position que l'aventurier
            if position_dragon == position_aventurier:
                # Si oui, compare leurs niveaux
                if niveau_dragon <= niveau_aventurier:
                    # Si le niveau du dragon est inférieur ou égal à celui de l'aventurier,
                    # le dragon est retiré de la liste et le niveau de l'aventurier est incrémenté de 1
                    self.get_personnage().montee_de_niveau()
                    self.get_dragons().remove(dragon)
                else:
                    # Sinon, l'aventurier est considéré comme mort et la fonction renvoie False
                    return False
        # Si l'aventurier survit à la rencontre avec les dragons, la fonction renvoie True
        return True

    def pivoter(self, position):
        donjon = self.affiche_donjon()
        case = donjon[position[0]][position[1]]
        print(tuple(case))
        correspondances = {
            (False, True, True, False): (False, False, True, True),
            (False, True, True, True): (True, False, True, True),
            (False, False, True, True): (True, False, False, True),
            (True, True, True, False): (False, True, True, True),
            (True, True, True, True): (False, False, True, True),
            (True, False, True, True): (True, True, True, False),
            (True, True, False, False): (True, True, True, False),
            (True, True, False, True): (True, True, False, False),
            (True, False, False, True): (True, False, True, False),
            (True, False, True, False): (True, False, True, True),
            (False, True, False, True): (True, True, False, True),
            (True, False, False, False): (False, False, True, False),
            (False, True, False, False): (False, True, True, False),
            (False, False, True, False): (True, True, False, False),
            (False, False, False, True): (True, False, False, True)
        }
        donjon[position[0]][position[1]] = correspondances[case]
        self.affiche_fltk()

    def connecte(self, position1, position2):
        y1, x1 = position1
        y2, x2 = position2
        donjon = self.affiche_donjon()
        if not (0 <= y1 < len(donjon) and 0 <= x1 < len(donjon[y1])) or not (
                0 <= y2 < len(donjon) and 0 <= x2 < len(donjon[y2])):
            return False
        if abs(y1 - y2) + abs(x1 - x2) != 1:
            return False
        if x1 < x2:
            if not donjon[y1][x1][1] or not donjon[y2][x2][3]:
                return False
        elif x1 > x2:
            if not donjon[y1][x1][3] or not donjon[y2][x2][1]:
                return False
        elif y1 < y2:
            if not donjon[y1][x1][2] or not donjon[y2][x2][0]:
                return False
        elif y1 > y2:
            if not donjon[y1][x1][0] or not donjon[y2][x2][2]:
                return False
        if x1 < x2:
            if not donjon[y2][x2][1] or not donjon[y1][x1][3]:
                return False
        elif x1 > x2:
            if not donjon[y2][x2][3] or not donjon[y1][x1][1]:
                return False
        elif y1 < y2:
            if not donjon[y2][x2][0] or not donjon[y1][x1][2]:
                return False
        elif y1 > y2:
            if not donjon[y2][x2][2] or not donjon[y1][x1][0]:
                return False
        return True

    def fin_partie(self):
        if not self.rencontre():
            return -1
        elif len(self.get_dragons()) == 0:
            return 1
        else:
            return 0
