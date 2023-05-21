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
    if not started:
        started = True

    ev = donne_ev()
    tev = type_ev(ev)

    if tev == "ClicGauche":
        if not gameManager.isPlaying() and gameManager.is_at_hub:
            if gameManager.getBtns()["Jouer"].checkClicked(abscisse_souris(), ordonnee_souris()):
                dungeonspage.Hub(resolution, gameManager.get_donjons(), gameManager, gameManager.get_page())
            elif gameManager.getBtns()["Quitter"].checkClicked(abscisse_souris(), ordonnee_souris()):
                sys.exit()
            else:
                pass
        elif not gameManager.isPlaying() and not gameManager.is_at_hub:
            if gameManager.getBtns()["Précédente"].checkClicked(abscisse_souris(), ordonnee_souris()):
                gameManager.remove_page("precedent")
                efface_tout()

                dungeonspage.Hub(resolution, gameManager.get_donjons(), gameManager, gameManager.get_page())

            elif gameManager.getBtns()["Suivante"].checkClicked(abscisse_souris(), ordonnee_souris()):
                gameManager.add_page("suivant")
                efface_tout()
                dungeonspage.Hub(resolution, gameManager.get_donjons(), gameManager, gameManager.get_page())
                print("page", gameManager.get_page())
            elif gameManager.getBtns()["Rentrer 1"].checkClicked(abscisse_souris(), ordonnee_souris()):
                gameManager.get_donjons()[0].affiche_fltk()
                gameManager.set_playing(True)
                gameManager.set_playing_donjon(gameManager.get_donjons()[0])
            elif gameManager.getBtns()["Rentrer 2"].checkClicked(abscisse_souris(), ordonnee_souris()):
                print("t'es rentré")
            elif gameManager.getBtns()["Rentrer 3"].checkClicked(abscisse_souris(), ordonnee_souris()):
                print("t'es rentré")


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
                            ligne(case_position[0], case_position[1], case_2_position[0], case_2_position[1], couleur="red")
                            mise_a_jour()

                        gameManager.get_actuel_donjon().get_personnage().set_chemin_possible(chemin_liste)

                    break
    if tev == "Touche" and gameManager.isPlaying():
        clicked = touche(ev)
        if clicked == "r":
            gameManager.get_actuel_donjon().reset_donjon()
        elif clicked == "Escape":
            dungeonspage.Hub(resolution,gameManager.get_donjons(),gameManager,0)
            gameManager.set_playing(False)
        elif clicked == "space":
            perso = gameManager.get_actuel_donjon().get_personnage()

            chemin_possible = perso.get_chemin_possible()

            perso.deplacement(chemin_possible[len(chemin_possible) - 1])


    mise_a_jour()