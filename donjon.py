import random

import dragon
import personnage


class Donjon:
    def __init__(self, fichier):
        """
        Initialise le donjon en chargeant les données depuis un fichier.

        Args:
            fichier (str): Le chemin d'accès au fichier à charger.
        """
        self.agencement = None
        self.personnages = {}

        self.charger(fichier)

    def charger(self, fichier):
        """
        Charge un donjon depuis un fichier texte.

        Args:
            fichier (str): Le chemin d'accès au fichier à charger.
        """
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

        agencement = []
        lignes = parties[0].split("\n")
        for ligne in lignes:
            agencement.append(list(ligne))

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
            ligne = int(elements[1])
            colonne = int(elements[2])
            niveau = 1
            if len(elements) > 3:
                niveau = int(elements[3])

            if nom in self.personnages:
                self.personnages[nom].append({"ligne": ligne, "colonne": colonne, "niveau": niveau})
            else:
                self.personnages[nom] = [{"ligne": ligne, "colonne": colonne, "niveau": niveau}]

        self.agencement = agencement

        print(self.personnages)

    def afficher_agencement(self):
        """
        Affiche l'agencement du donjon.
        """
        if self.agencement is None:
            print("Le donjon n'a pas été chargé.")
            return

        print("Agencement du donjon :")
        for ligne in self.agencement:
            print("".join(ligne))

    def affiche_donjon(self):
        """
        Affiche l'agencement du donjon en utilisant les caractères spéciaux et crée un tuple de 4 éléments pour chaque
        caractère dans le donjon.

        Args:
            donjon (Donjon): L'objet Donjon à afficher.
        """
        if self.agencement is None:
            print("Le donjon n'a pas été chargé.")
            return

        salles = []
        for ligne in self.agencement:
            salles_ligne = []
            for car in ligne:
                if car == " ":
                    pass
                elif car == "╔":
                    salles_ligne.append(tuple((False, False, True, True)))
                elif car == "╦":
                    salles_ligne.append(tuple((True, False, True, True)))
                elif car == "╗":
                    salles_ligne.append(tuple((True, False, False, True)))
                elif car == "╠":
                    salles_ligne.append(tuple((False, True, True, False)))
                elif car == "╬":
                    salles_ligne.append(tuple((True, True, True, True)))
                elif car == "╣":
                    salles_ligne.append(tuple((True, True, False, True)))
                elif car == "╚":
                    salles_ligne.append(tuple((False, True, True, False)))
                elif car == "╩":
                    salles_ligne.append(tuple((True, True, True, False)))
                elif car == "╝":
                    salles_ligne.append(tuple((True, True, False, False)))
                elif car == "║":
                    salles_ligne.append(tuple((True, False, False, True)))
                elif car == "═":
                    salles_ligne.append(tuple((False, True, True, False)))
            salles.append(salles_ligne)
        return salles

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

    def intention(self):
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

    def pivoter(self,position):
        rota_donjon = self.affiche_donjon()[position[0]][position[1]][-1:] + self.affiche_donjon()[position[0]][position[1]][
                                                              :-1]  # Créer une variable qui est l'addition du dernier indice de donjon et ajouter les éléments restants de ce dernier
        return rota_donjon

    def connecte(self,position1,position2):
        y1, x1 = position1
        y2, x2 = position2

        donjon = self.affiche_donjon()

        # Vérification que les coordonnées sont bien dans les limites du donjon
        if not (0 <= y1 < len(donjon) and 0 <= x1 < len(donjon[y1])):
            return False
        if not (0 <= y2 < len(donjon) and 0 <= x2 < len(donjon[y2])):
            return False

        # Vérification que les salles sont adjacentes
        if abs(y1 - y2) + abs(x1 - x2) != 1:
            return False

        # Vérification de la connexion de la première salle vers la deuxième
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

        # Vérification de la connexion de la deuxième salle vers la première
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

        # Si toutes les vérifications ont été passées, les salles sont connectées
        return True

    def fin_partie(self):
        # Vérifie si l'aventurier est mort
        if not self.rencontre():
            return -1
        # Vérifie si tous les dragons ont été tués
        elif len(self.get_dragons()) == 0:
            return 1
        # Si la partie continue
        else:
            return 0


dj = Donjon("config.txt")

print(dj.get_personnage())
