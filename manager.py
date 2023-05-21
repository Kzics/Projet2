import glob

import donjon
from fltk import *
from pbutton import PButton


class Manager:

    def __init__(self, resolution: list) -> None:
        self.resolution = resolution
        self.buttons = {}
        self.currentPage = 0
        self.lastClicked = None
        self.playing = False
        self.playing_donjon = None

        self.donjons = []

        fichiers_config = glob.glob("donjons/config*.txt")

        for conf in fichiers_config:
            dj = donjon.Donjon(conf, "desert",self)
            if conf.endswith("3.txt"):
                dj = donjon.Donjon(conf,"ice",self)
            self.donjons.append(dj)

    def lancemenent(self) -> None:
        self.ouvrir_fenetre()

    def ouvrir_fenetre(self):
        cree_fenetre(self.resolution[0], self.resolution[1])

        texte(self.resolution[0] / 2 - 100, self.resolution[1] / 4, "THE WALL IS YOU")

        self.startBtn = PButton("Jouer", self.resolution[0] / 2, self.resolution[1] / 2, self.resolution, "Jouer")
        self.quitBtn = PButton("Quitter", self.resolution[0] / 2, (self.resolution[1] / 2) + 100, self.resolution,
                               "Quitter")

        self.startBtn.normalSpawn()
        self.quitBtn.normalSpawn()

        self.getBtns()[self.startBtn.getName()] = self.startBtn
        self.getBtns()[self.quitBtn.getName()] = self.quitBtn

    def getBtns(self) -> dict:
        return self.buttons

    def setLastClicked(self, clicked):
        self.lastClicked = clicked

    def getLastClicked(self):
        return self.lastClicked

    def get_donjons(self):
        return self.donjons

    def get_page(self):
        return self.currentPage * 3

    def add_page(self, action):
        if action == self.lastClicked: return

        self.currentPage = self.currentPage + 1

    def remove_page(self, action):
        if action == self.lastClicked: return

        if self.currentPage - 1 <= 0:
            self.currentPage = 0
            return

        self.currentPage = self.currentPage - 1

    def isPlaying(self):
        return self.playing

    def get_actuel_donjon(self):
        return self.playing_donjon

    def set_playing_donjon(self,dj):
        self.playing_donjon = dj

    def set_playing(self,state):
        self.playing = state

