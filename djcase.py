from fltk import *


class Case:
    def __init__(self, x, y, texture, tag, largeur, hauteur):
        image(x, y, texture, largeur=largeur, hauteur=hauteur, ancrage='center', tag=tag)

        self.tag = tag

        self.x = x
        self.y = y

    def get_positions(self):
        return self.x, self.y

    def get_tag(self):
        return self.tag

    def est_dans_case(self, x, y):
        case_x, case_y = self.get_positions()
        # On suppose que la texture de la case a une largeur et une hauteur fixe
        largeur_case = hauteur_case = 144  # Remplacez ces valeurs par les dimensions réelles de la texture de votre case

        # Vérifier si les coordonnées x et y se trouvent à l'intérieur de la case
        if case_x - largeur_case / 2 <= x <= case_x + largeur_case / 2 and \
                case_y - hauteur_case / 2 <= y <= case_y + hauteur_case / 2:
            return True
        else:
            return False
