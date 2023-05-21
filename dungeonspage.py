from fltk import *
import glob

from pbutton import PButton


class Hub:
    def __init__(self, resolution, donjons, manager,start):
        manager.set_is_at_hub(False)

        efface_tout()

        marge_haut = 200  # Ajuste cette valeur pour définir la marge supérieure
        marge_cotes = 0  # Ajuste cette valeur pour définir la marge des côtés
        x1 = marge_cotes
        y1 = marge_haut
        x2 = resolution[0] - marge_cotes
        y2 = resolution[1] - marge_haut

        # Dessin du rectangle sur les deux côtés supérieurs
        rectangle(x1, y1, x2, y2)
        rectangle(x1, resolution[1] - y2, x2, resolution[1] - y1)

        largeur_carre = (x2 - x1) // 3

        # Recherche des fichiers de configuration
        fichiers_config = glob.glob("donjons/config*.txt")

        # Détermination du nombre de donjons en fonction du nombre de fichiers trouvés
        nombre_donjons = min(len(fichiers_config),3)

        # Dessin des lignes verticales pour diviser le rectangle en carrés
        for i in range(1, 3):
            ligne(x1 + i * largeur_carre, y1, x1 + i * largeur_carre, y2)

        # Dessin des images à l'intérieur de chaque carré
        for i in range(nombre_donjons):
            try:
                texte(x1 + (i + 1) * largeur_carre - largeur_carre // 2, y1 - 20, f"{donjons[start+i].get_name()}", ancrage='center')
            except IndexError:
                print("t")
            rectangle(x1 + i * largeur_carre, y1, x1 + (i + 1) * largeur_carre, y2)

            temp_x = x1 + i * largeur_carre + 10
            temp_y = y1 + 10

            image_width = (largeur_carre - 20) // 3
            image_height = (y2 - y1 - 40) // 5

            for row in range(5):
                for col in range(3):
                    image_number = row * 3 + col + 1
                    if image_number <= 15:
                        try:
                            image_path = f"tile/{donjons[start + i].get_type()}/t{image_number}.png"
                            image(temp_x, temp_y, image_path, ancrage='nw',largeur= 144//2,hauteur=144//2)
                        except IndexError:
                            pass
                    temp_x += image_width

                temp_y += image_height
                temp_x = x1 + i * largeur_carre + 10

            # Affichage du texte "Jouer"
            play = PButton(f"Rentrer {start + i+1}", x1 + (i + 1) * largeur_carre - largeur_carre // 2, y2 + 40,
                           manager.resolution,
                           f"enter{start + i+1}")
            play.normalSpawn()
            manager.getBtns()[play.getName()] = play

        # Affichage des liens "Page suivante" et "Page précédente"

        quitBtn = PButton("Précédente", x1 + 180, y2 + 150, manager.resolution,
                          "oldPage")

        nextPage = PButton("Suivante", x2 - 130, y2 + 150, manager.resolution,
                           "nextPage")

        quitBtn.normalSpawn()
        nextPage.normalSpawn()

        manager.getBtns()[quitBtn.getName()] = quitBtn
        manager.getBtns()[nextPage.getName()] = nextPage

        mise_a_jour()
        """
        efface_tout()

        marge_haut = 200  # Ajuste cette valeur pour définir la marge supérieure
        marge_cotes = 0  # Ajuste cette valeur pour définir la marge des côtés
        x1 = marge_cotes
        y1 = marge_haut
        x2 = resolution[0] - marge_cotes
        y2 = resolution[1] - marge_haut

        # Dessin du rectangle sur les deux côtés supérieurs
        rectangle(x1, y1, x2, y2)
        rectangle(x1, resolution[1] - y2, x2, resolution[1] - y1)

        largeur_carre = (x2 - x1) // 3

        # Dessin des lignes verticales pour diviser le rectangle en carrés
        for i in range(1, 3):
            ligne(x1 + i * largeur_carre, y1, x1 + i * largeur_carre, y2)

        # Dessin des images à l'intérieur de chaque carré
        for i in range(3):
            rectangle(x1 + i * largeur_carre, y1, x1 + (i + 1) * largeur_carre, y2)

            temp_x = x1 + i * largeur_carre + 10
            temp_y = y1 + 10

            image_width = (largeur_carre - 20) // 3
            image_height = (y2 - y1 - 20) // 5

            for row in range(5):
                for col in range(3):
                    image_number = row * 3 + col + 1
                    if image_number <= 15:
                        image_path = f"tile/desert/t{image_number}.png"
                        image(temp_x, temp_y, image_path, ancrage='nw')
                    temp_x += image_width

                temp_y += image_height
                temp_x = x1 + i * largeur_carre + 10

        mise_a_jour()"""
