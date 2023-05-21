from fltk import *

class Dragon:
    def __init__(self, position, niveau,tag_num):
        self.__position = position
        self.__niveau = niveau
        self.tag = tag_num

    def get_position(self):
        return self.__position

    def get_niveau(self):
        return self.__niveau

    def get_texture(self):
        return "tile/misc/dragon.png"

    def dessin(self,d_case_pos):
        texte(d_case_pos[0] + 20, d_case_pos[1] + 20, self.get_niveau())

        image(d_case_pos[0], d_case_pos[1], self.get_texture(),tag=f"dragon{self.tag}")