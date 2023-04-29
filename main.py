import random
import donjon

dj = donjon.Donjon("config.txt")
donjon = dj.affiche_donjon()

print(donjon)
position = (0, 1)
aventurier = dj.get_personnage()
dragons = dj.get_dragons()

def pivoter(donjon, position):
    rota_donjon = donjon[position[0]][position[1]][-1:] + donjon[position[0]][position[1]][
                                                          :-1]  # Créer une variable qui est l'addition du dernier indice de donjon et ajouter les éléments restants de ce dernier
    return rota_donjon


def connecte(donjon, position1, position2):
    y1, x1 = position1
    y2, x2 = position2

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



def intention(donjon, position, dragons):
    # Fonction interne pour effectuer une recherche récursive dans le donjon
    def recherche(position, visite):
        # Vérifie si la position actuelle contient un dragon
        for dragon in dragons:
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
            if connecte(donjon, position, nouvelle_position):
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
    resultat = recherche(position, set())
    if resultat is None:
        return None
    chemin, niveau = resultat
    # Renvoie le chemin menant au dragon le plus proche avec le niveau le plus élevé
    return chemin


def rencontre(aventurier, dragons):
    # Récupère la position et le niveau de l'aventurier
    position_aventurier = aventurier.get_position()
    niveau_aventurier = aventurier.get_niveau()
    # Parcourt la liste des dragons
    for dragon in dragons:
        # Récupère la position et le niveau du dragon
        position_dragon = dragon.get_position()
        niveau_dragon = dragon.get_niveau()
        # Vérifie si le dragon se trouve à la même position que l'aventurier
        if position_dragon == position_aventurier:
            # Si oui, compare leurs niveaux
            if niveau_dragon <= niveau_aventurier:
                # Si le niveau du dragon est inférieur ou égal à celui de l'aventurier,
                # le dragon est retiré de la liste et le niveau de l'aventurier est incrémenté de 1
                aventurier.montee_de_niveau()
                dragons.remove(dragon)
            else:
                # Sinon, l'aventurier est considéré comme mort et la fonction renvoie False
                return False
    # Si l'aventurier survit à la rencontre avec les dragons, la fonction renvoie True
    return True


"""  def appliquer_chemin(aventurier, dragons, chemin):
    # Parcourt la liste des positions du chemin
    for position in chemin:
        # Met à jour la position de l'aventurier
        aventurier.get_position() = position
        # Appelle la fonction rencontre pour vérifier si l'aventurier rencontre un dragon
        rencontre(aventurier, dragons)"""


def fin_partie(aventurier, dragons):
    # Vérifie si l'aventurier est mort
    if not rencontre(aventurier, dragons):
        return -1
    # Vérifie si tous les dragons ont été tués
    elif len(dragons) == 0:
        return 1
    # Si la partie continue
    else:
        return 0


position1 = (0, 2)
print((donjon[1][1]))
print(pivoter(donjon, position))
print(connecte(donjon, position, position1))
print(intention(donjon, position, dragons))
print(rencontre(aventurier, dragons))
