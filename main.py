import sys

import dungeonspage
from manager import Manager
from fltk import *

started = False
resolution = [1000, 800]
gameManager = Manager(resolution)
gameManager.lancemenent()

while True:
    #   gameManager.getStartButton()

    if not started:
        started = True

    ev = donne_ev()
    tev = type_ev(ev)
    if tev == "ClicGauche":
        if gameManager.getBtns()["Jouer"].checkClicked(abscisse_souris(), ordonnee_souris()):
            dungeonspage.Hub(resolution,gameManager.get_donjons(),gameManager,gameManager.get_page())
        elif gameManager.getBtns()["Quitter"].checkClicked(abscisse_souris(), ordonnee_souris()):
            sys.exit()
        elif gameManager.getBtns()["Précédente"].checkClicked(abscisse_souris(),ordonnee_souris()):
            print("before",gameManager.get_page())
            gameManager.remove_page("precedent")
            efface_tout()
            print("page",gameManager.get_page())

            dungeonspage.Hub(resolution,gameManager.get_donjons(),gameManager,gameManager.get_page())

        elif gameManager.getBtns()["Suivante"].checkClicked(abscisse_souris(),ordonnee_souris()):
            gameManager.add_page("suivant")
            efface_tout()
            dungeonspage.Hub(resolution,gameManager.get_donjons(),gameManager,gameManager.get_page())
            print("page",gameManager.get_page())
        elif gameManager.getBtns()["Rentrer 1"].checkClicked(abscisse_souris(),ordonnee_souris()):
            gameManager.get_donjons()[0].affiche_fltk()
        elif gameManager.getBtns()["Rentrer 2"].checkClicked(abscisse_souris(),ordonnee_souris()):
            print("t'es rentré")
        elif gameManager.getBtns()["Rentrer 3"].checkClicked(abscisse_souris(),ordonnee_souris()):
            print("t'es rentré")
        else:
            print("jsp")

    mise_a_jour()