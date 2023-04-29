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


dj = Donjon("config.txt")

print(dj.get_personnage())
