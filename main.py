import sys

import dungeonspage
from manager import Manager
from fltk import *

started = False
resolution = [800, 800]
gameManager = Manager(resolution)
gameManager.lancemenent()

donjons = gameManager.get_donjons()

while True:
    #   gameManager.getStartButton()

    if not started:
        started = True

    ev = donne_ev()
    tev = type_ev(ev)

    if tev == "ClicGauche":
        if not gameManager.isPlaying():
            if gameManager.getBtns()["Jouer"].checkClicked(abscisse_souris(), ordonnee_souris()):
                dungeonspage.Hub(resolution, gameManager.get_donjons(), gameManager, gameManager.get_page())
            elif gameManager.getBtns()["Quitter"].checkClicked(abscisse_souris(), ordonnee_souris()):
                sys.exit()
            elif gameManager.getBtns()["Précédente"].checkClicked(abscisse_souris(), ordonnee_souris()):
                print("before", gameManager.get_page())
                gameManager.remove_page("precedent")
                efface_tout()
                print("page", gameManager.get_page())

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
            else:
                pass

        if gameManager.isPlaying():
            dj_actuel = gameManager.get_actuel_donjon()
            for c in gameManager.get_actuel_donjon().cases:
                if c.est_dans_case(abscisse_souris(), ordonnee_souris()):
                    position = c.get_tag().split("_")
                    print(position)
                    dj_actuel.pivoter(tuple((int(position[1]), int(position[0]))))

                    chemin_liste = dj_actuel.intention()

                    print(chemin_liste)

                    print(dj_actuel.get_personnage().get_position())

                    if chemin_liste is not None:
                        for i in range(len(chemin_liste) - 1):
                            case = dj_actuel.get_case_from_tag(f"{chemin_liste[i][0]}_{chemin_liste[i][1]}")
                            case_2 = dj_actuel.get_case_from_tag(f"{chemin_liste[i + 1][0]}_{chemin_liste[i + 1][1]}")
                            case_position = case.get_positions()
                            case_2_position = case_2.get_positions()
                            ligne(case_position[0], case_position[1], case_2_position[0], case_2_position[1], couleur="red")
                            mise_a_jour()

                        print("il va",chemin_liste[len(chemin_liste)-1])
                        dj_actuel.get_personnage().deplacement(chemin_liste[len(chemin_liste)-1])

                    break

    mise_a_jour()
