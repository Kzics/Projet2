import sys

import dungeonspage
from manager import Manager
from fltk import *

started = False
resolution = [792, 790]
gameManager = Manager(resolution)
gameManager.lancemenent()

donjons = gameManager.get_donjons()

while True:
    # Vérifie si le jeu a démarré
    if not started:
        started = True

    # Récupère l'événement en cours
    ev = donne_ev()
    tev = type_ev(ev)

    # Si l'événement est un clic gauche de la souris
    if tev == "ClicGauche":
        # Si le jeu n'est pas en cours et que le joueur est dans le hub
        if not gameManager.isPlaying() and gameManager.is_at_hub:
            # Vérifie si le bouton "Jouer" a été cliqué
            if gameManager.getBtns()["Jouer"].checkClicked(abscisse_souris(), ordonnee_souris()):
                # Ouvre la page du hub des donjons
                dungeonspage.Hub(resolution, gameManager.get_donjons(), gameManager, gameManager.get_page())
            # Vérifie si le bouton "Quitter" a été cliqué
            elif gameManager.getBtns()["Quitter"].checkClicked(abscisse_souris(), ordonnee_souris()):
                # Quitte le jeu
                sys.exit()
            else:
                pass
        # Si le jeu n'est pas en cours et que le joueur n'est pas dans le hub
        elif not gameManager.isPlaying() and not gameManager.is_at_hub:
            # Vérifie si le bouton "Précédente" a été cliqué
            if gameManager.getBtns()["Précédente"].checkClicked(abscisse_souris(), ordonnee_souris()):
                # Passe à la page précédente
                gameManager.remove_page("precedent")
                efface_tout()
                dungeonspage.Hub(resolution, gameManager.get_donjons(), gameManager, gameManager.get_page())
            # Vérifie si le bouton "Suivante" a été cliqué
            elif gameManager.getBtns()["Suivante"].checkClicked(abscisse_souris(), ordonnee_souris()):
                # Passe à la page suivante
                gameManager.add_page("suivant")
                efface_tout()
                dungeonspage.Hub(resolution, gameManager.get_donjons(), gameManager, gameManager.get_page())
            else:
                # Entre dans un donjon
                gameManager.entrer_donjon((abscisse_souris(), ordonnee_souris()))

        # Si le jeu est en cours
        if gameManager.isPlaying():
            dj_actuel = gameManager.get_actuel_donjon()
            for c in gameManager.get_actuel_donjon().cases:
                if c.est_dans_case(abscisse_souris(), ordonnee_souris()):
                    position = c.get_tag().split("_")
                    dj_actuel.pivoter(tuple((int(position[1]), int(position[0]))))

                    chemin_liste = dj_actuel.intention()

                    if chemin_liste is not None:
                        for i in range(len(chemin_liste) - 1):
                            case = dj_actuel.get_case_from_tag(f"{chemin_liste[i][0]}_{chemin_liste[i][1]}")
                            case_2 = dj_actuel.get_case_from_tag(f"{chemin_liste[i + 1][0]}_{chemin_liste[i + 1][1]}")
                            case_position = case.get_positions()
                            case_2_position = case_2.get_positions()
                            ligne(case_position[0], case_position[1], case_2_position[0], case_2_position[1],
                                  couleur="red")
                            mise_a_jour()

                        gameManager.get_actuel_donjon().get_personnage().set_chemin_possible(chemin_liste)

                    break
    # Si l'événement est une touche du clavier et que le jeu est en cours
    if tev == "Touche" and gameManager.isPlaying():
        clicked = touche(ev)
        if clicked == "r":
            # Réinitialise le donjon actuel
            gameManager.get_actuel_donjon().reset_donjon()
        elif clicked == "Escape":
            # Retourne au hub des donjons
            dungeonspage.Hub(resolution, gameManager.get_donjons(), gameManager, 0)
            gameManager.set_playing(False)
        elif clicked == "space":
            perso = gameManager.get_actuel_donjon().get_personnage()

            chemin_possible = perso.get_chemin_possible()

            perso.deplacement(chemin_possible[len(chemin_possible) - 1])

    mise_a_jour()