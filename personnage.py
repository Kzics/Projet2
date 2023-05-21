from fltk import *

class Personnage:

    def __init__(self, position, niveau,gameManager,tag):
        self.__position = position
        self.__niveau = niveau
        self.gameManager = gameManager
        self.donjon_perso = gameManager.get_actuel_donjon()
        self.tag = tag

    def get_niveau(self):
        return self.__niveau

    def get_position(self):
        return self.__position

    def get_texture(self):
        return "tile/misc/perso.png"

    def montee_de_niveau(self):
        self.__niveau += 1

    def deplacement(self,position):
        self.__position = position

        case = self.gameManager.get_actuel_donjon().get_case_from_tag(f"{position[0]}_{position[1]}")

        efface(f"text{self.tag}")
        efface(self.tag)

        self.dessiner(case.get_positions())

        print("hh",case.get_positions())

        self.rencontre()

    def rencontre(self):
        # Récupère la position et le niveau de l'aventurier
        position_aventurier = self.get_position()
        niveau_aventurier = self.get_niveau()
        dragons = self.donjon_perso.get_dragons()
        actuel_dj = self.gameManager.get_actuel_donjon()

        # Parcourt la liste des dragons
        for dragon in dragons.copy():
            # Récupère la position et le niveau du dragon
            position_dragon = dragon.get_position()
            niveau_dragon = dragon.get_niveau()
            # Vérifie si le dragon se trouve à la même position que l'aventurier
            if position_dragon == position_aventurier:
                # Si oui, compare leurs niveaux
                if int(niveau_dragon) <= int(niveau_aventurier):
                    # Si le niveau du dragon est inférieur ou égal à celui de l'aventurier,
                    # le dragon est retiré de la liste et le niveau de l'aventurier est incrémenté de 1
                    self.montee_de_niveau()
                    print("monté de niveau ")
                    dragons.remove(dragon)

                    actuel_dj.set_dragons(dragons)


                else:
                    # Sinon, l'aventurier est considéré comme mort et la fonction renvoie False
                    return False
        # Si l'aventurier survit à la rencontre avec les dragons, la fonction renvoie True
        return True

    def dessiner(self,perso_case_pos):
        texte(perso_case_pos[0] + 20, perso_case_pos[1] + 20, self.get_niveau(),tag=f"text{self.tag}")
        image(perso_case_pos[0], perso_case_pos[1], self.get_texture(),tag= self.tag)
