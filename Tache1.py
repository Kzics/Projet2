import random
donjon = [[(False, True, True , False), (False, False, True, False)], [(True , True, False, True ), (True , True , True, False)]]
position = (0,0)
position1 = (1,1)
position2 = (0,1)

aventurier = {
    "position" : (0,1),
    "niveau" : 1
}
dragons = [
    {"position": (0,1), "niveau": 0},
    {"position": (1,0), "niveau": 1}
]

def pivoter(donjon, position):
    rota_donjon = donjon[position[0]][position[1]][-1:] + donjon[position[0]][position[1]][:-1] #Créer une variable qui est l'addition du dernier indice de donjon et ajouter les éléments restants de ce dernier
    return rota_donjon

def connecte(donjon, position1, position2):
    n = len(donjon)
    m = len(donjon[0])
    x1, y1 = position1
    x2, y2 = position2
    # Vérifie si les positions sont valides dans le donjon
    if not (0 <= x1 < n and 0 <= y1 < m and 0 <= x2 < n and 0 <= y2 < m):
        return False
    # Vérifie si les positions sont adjacentes
    if (y1 > y2 and y1 - y2 > 1) or (y2 > y1 and y2 - y1 > 1) or (x1 > x2 and x1 - x2 > 1) or (x2 > x1 and x2 - x1 > 1):
        return False
    # Vérifie si les positions sont dans la même ligne
    elif x1 == x2:
        # Vérifie si les positions sont connectées horizontalement
        if (donjon[x1][y1][1] == donjon[x2][y2][3] and donjon[x1][y1][1] == True) or (donjon[x1][y1][3] == donjon[x2][y2][1] and donjon[x1][y1][3] == True):
            return True
        else:
            return False
    # Vérifie si les positions sont dans la même colonne
    elif y1 == y2:
        # Vérifie si les positions sont connectées verticalement
        if (donjon[x1][y1][0] == donjon[x2][y2][2] and donjon[x1][y1][0] == True) or (donjon[x1][y1][2] == donjon[x2][y2][0] and donjon[x1][y1][2] == True):
            return True
        else:
            return False

def intention(donjon, position, dragons):
    # Fonction interne pour effectuer une recherche récursive dans le donjon
    def recherche(position, visite):
        # Vérifie si la position actuelle contient un dragon
        for dragon in dragons:
            if position == dragon['position']:
                # Si oui, renvoie le chemin menant à cette position et le niveau du dragon
                return [position], dragon['niveau']
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
    position_aventurier = aventurier['position']
    niveau_aventurier = aventurier['niveau']
    # Parcourt la liste des dragons
    for dragon in dragons:
        # Récupère la position et le niveau du dragon
        position_dragon = dragon['position']
        niveau_dragon = dragon['niveau']
        # Vérifie si le dragon se trouve à la même position que l'aventurier
        if position_dragon == position_aventurier:
            # Si oui, compare leurs niveaux
            if niveau_dragon <= niveau_aventurier:
                # Si le niveau du dragon est inférieur ou égal à celui de l'aventurier,
                # le dragon est retiré de la liste et le niveau de l'aventurier est incrémenté de 1
                aventurier['niveau'] += 1
                dragons.remove(dragon)
            else:
                # Sinon, l'aventurier est considéré comme mort et la fonction renvoie False
                return False
    # Si l'aventurier survit à la rencontre avec les dragons, la fonction renvoie True
    return True

def appliquer_chemin(aventurier, dragons, chemin):
    # Parcourt la liste des positions du chemin
    for position in chemin:
        # Met à jour la position de l'aventurier
        aventurier['position'] = position
        # Appelle la fonction rencontre pour vérifier si l'aventurier rencontre un dragon
        rencontre(aventurier, dragons)

def fin_partie(aventurier, dragons):
    if not dragons:
        # Si tous les dragons ont été tués, la partie est gagnée
        return 1
    elif 'vivant' in aventurier and not aventurier['vivant']:
        # Si l'aventurier a été tué, la partie est perdue
        return -1
    else:
        # Sinon, la partie continue
        return 0

print((donjon[1][1])) 
print(pivoter(donjon, position))
print(connecte(donjon, position1, position2))
print(intention(donjon, position, dragons))
print(rencontre(aventurier, dragons))