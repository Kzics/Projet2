import time

from fltk import *


class ActionInexistante(Exception):
    pass


class PButton:
    text = None

    posX = None

    posY = None

    resolution = None

    longueur, hauteur = None, None

    def __init__(self, text: str, posX, posY, resolution, name, rempli=""):
        self.text = text
        self.posX = posX
        self.posY = posY
        self.tempX = 0
        self.rempli = rempli

        self.resolution = resolution
        self.name = name

    def spawnAnim(self):
        while self.tempX - 50 < self.posX:
            efface(f"txt{self.name}")
            efface(f"btn{self.name}")
            texte(self.tempX, self.posY, self.text, taille="50", ancrage="center", tag=f"txt{self.name}")

            self.longueur, self.hauteur = taille_texte(self.text, taille=50)

            rectangle(self.tempX - self.longueur // 2, self.posY - self.hauteur // 2,
                      self.tempX + self.longueur // 2, self.posY + self.hauteur // 2, tag=f"btn{self.name}",
                      remplissage=self.rempli)

            mise_a_jour()
            self.tempX += 50
            time.sleep(0.05)

    def normalSpawn(self):
        self.tempX = self.posX  # Ajout de cette ligne pour initialiser self.tempX
        efface(f"txt{self.name}")
        efface(f"btn{self.name}")
        texte(self.tempX, self.posY, self.text, taille="30", ancrage="center", tag=f"txt{self.name}")

        self.longueur, self.hauteur = taille_texte(self.text, taille=50)

        rectangle(self.tempX - self.longueur // 2, self.posY - self.hauteur // 2,
                  self.tempX + self.longueur // 2, self.posY + self.hauteur // 2, tag=f"btn{self.name}")

        mise_a_jour()

    def deleteBtn(self):
        efface(f"txt{self.name}")
        efface(f"btn{self.name}")

        mise_a_jour()

    def getName(self):
        return self.text

    def getTagName(self):
        return self.name

    def checkClicked(self, clickedX, clickedY) -> bool:
        print(self.posX - self.longueur // 2, self.posY - self.hauteur // 2, self.posX + self.longueur // 2,
              self.posY + self.hauteur // 2)
        if self.posY - self.hauteur // 2 < clickedY < self.posY + self.hauteur // 2:
            if self.posX - self.longueur // 2 < clickedX < self.posX + self.longueur // 2:
                return True
        return False


class AnimationButton(PButton):
    def __init__(self, text: str, posX, posY, resolution, name, rempli=""):
        super().__init__(text, posX, posY, resolution, name, rempli="")
        texte(self.posX - 200, self.posY, self.text, taille="50", ancrage="center", tag=f"txt{self.name}")

        self.longueur, self.hauteur = taille_texte(self.text, taille=50)

        rectangle(self.posX - self.longueur // 2, self.posY - self.hauteur // 2,
                  self.posX + self.longueur // 2, self.posY + self.hauteur // 2
                  , tag=f"btn{self.name}", remplissage=rempli)

        mise_a_jour()


class MovementButton(PButton):

    def __init__(self, text: str, posX, posY, resolution, name, rempli=""):
        super().__init__(text, posX, posY, resolution, name, rempli="")

        texte(self.posX - 200, self.posY, self.text, taille="50", ancrage="center", tag=f"txt{self.name}")

        self.longueur, self.hauteur = taille_texte(self.text, taille=50)

        rectangle(self.posX - self.longueur // 2, self.posY - self.hauteur // 2,
                  self.posX + self.longueur // 2, self.posY + self.hauteur // 2
                  , tag=f"btn{self.name}", remplissage=rempli)

        mise_a_jour()





