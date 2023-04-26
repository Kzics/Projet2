donjon = [[(False, True, True , False), (False, False, True, False)], [(True , True, False, True ), (True , True , True, False)]]
position = (0,0)
position1 = (1,1)
position2 = (0,1)

aventurier = {
    "position" : (0,1),
    "niveau" : 1
}
dragons = {
    (1, 0): 3
}

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
    def recherche(position, visite):
        # Vérifie si la position actuelle est dans la liste des dragons
        if position in dragons:
            return [position], dragons[position]
        # Vérifie si la position actuelle a déjà été visitée
        if position in visite:
            return None
        visite.add(position)
        resultats = []
        for direction in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nouvelle_position = (position[0] + direction[0], position[1] + direction[1])
            if connecte(donjon, position, nouvelle_position):
                resultat = recherche(nouvelle_position, visite)
                if resultat is not None:
                    resultats.append(resultat)
        # Vérifie si la liste des résultats est vide
        if not resultats:
            return None
        chemin, niveau = max(resultats, key=lambda x: x[1])
        return [position] + chemin, niveau

    resultat = recherche(position, set())
    # Vérifie si le résultat de l'appel à la fonction recherche est None
    if resultat is None:
        return None
    chemin, niveau = resultat
    return chemin

print((donjon[1][1])) 
print(pivoter(donjon, position))
print(connecte(donjon, position1, position2))
print(intention(donjon, position, dragons))