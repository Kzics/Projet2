import datetime
import glob
import time

import donjon
from fltk import *
from pbutton import PButton

class Manager:
    """
    Cette classe gère les donjons et les boutons de l'interface utilisateur.
    """

    def __init__(self, resolution: list) -> None:
        """
        Initialise les attributs de la classe Manager.

        :param resolution: La résolution de la fenêtre.
        """
        self.resolution = resolution
        self.buttons = {}
        self.currentPage = 0
        self.lastClicked = None
        self.playing = False
        self.playing_donjon = None
        self.is_at_hub = True

        self.donjons = []

        # Récupère les fichiers de configuration des donjons
        fichiers_config = glob.glob("donjons/config*.txt")

        # Crée les instances de Donjon à partir des fichiers de configuration
        for conf in fichiers_config:
            dj = donjon.Donjon(conf, "desert", self)
            if conf.endswith("3.txt"):
                dj = donjon.Donjon(conf, "ice", self)
            self.donjons.append(dj)

    def lancemenent(self) -> None:
        """
        Lance l'application en ouvrant la fenêtre principale.
        """
        self.ouvrir_fenetre()

    def entrer_donjon(self,position):
        """
        Vérifie si un bouton a été cliqué et entre dans le donjon correspondant.

        :param position: La position du clic de la souris.
        """
        for k,v in self.getBtns().items():
            if v.checkClicked(position[0],position[1]):
                donjon_num = str(k).split()[1]
                dj = self.get_donjons()[int(donjon_num)-1]
                dj.affiche_fltk()
                self.playing = True
                self.set_playing_donjon(dj)
                dj.startedTime = time.time()

    def ouvrir_fenetre(self):
        """
        Ouvre la fenêtre principale et affiche les boutons Jouer et Quitter.
        """
        cree_fenetre(self.resolution[0], self.resolution[1])

        texte(self.resolution[0] / 2 - 100, self.resolution[1] / 4, "THE WALL IS YOU")

        # Crée les boutons Jouer et Quitter
        self.startBtn = PButton("Jouer", self.resolution[0] / 2, self.resolution[1] / 2, self.resolution, "Jouer")
        self.quitBtn = PButton("Quitter", self.resolution[0] / 2, (self.resolution[1] / 2) + 100, self.resolution,
                               "Quitter")

        # Affiche les boutons Jouer et Quitter
        self.startBtn.normalSpawn()
        self.quitBtn.normalSpawn()

        # Ajoute les boutons au dictionnaire des boutons
        self.getBtns()[self.startBtn.getName()] = self.startBtn
        self.getBtns()[self.quitBtn.getName()] = self.quitBtn

    def getBtns(self) -> dict:
      """
      Retourne le dictionnaire des boutons.

      :return: Le dictionnaire des boutons.
      """
      return self.buttons

    def openEndMenu(self):
      """
      Ouvre le menu de fin de partie et affiche les boutons Rejouer, Menu et Parties.
      """
      efface_tout()

      rectangle(self.resolution[0] / 2 + 300, self.resolution[1] / 2 + 200, 100, 200)

      texte(self.resolution[0] * 0.25, self.resolution[1] * 0.3, "Vous avez perdu !",taille=40)

      texte(self.resolution[0] * 0.2 ,self.resolution[1] * 0.5,f"Temps : ")
      self.get_actuel_donjon().drawTimer(self.resolution[0] * 0.35,self.resolution[1] * 0.5)

      # Crée les boutons Rejouer, Menu et Parties
      againBtn = PButton("Rejouer",250,450,self.resolution,"rejouer")
      menuBtn = PButton("Menu",550,450,self.resolution,"menu")
      partiesBtn = PButton("Parties",550,250,self.resolution,"parties")

      # Ajoute les boutons au dictionnaire des boutons
      self.getBtns()[partiesBtn.getName()] = partiesBtn
      self.getBtns()[againBtn.getName()] = againBtn
      self.getBtns()[menuBtn.getName()] = menuBtn

    def get_donjon_btns(self):
      """
      Retourne la liste des boutons pour entrer dans un donjon.

      :return: La liste des boutons pour entrer dans un donjon.
      """
      return list(filter(lambda x: x.startswith("Rentrer"),self.getBtns()))

    def setLastClicked(self,clicked):
      """
      Définit le dernier bouton cliqué.

      :param clicked: Le dernier bouton cliqué.
      """
      self.lastClicked = clicked

    def getLastClicked(self):
      """
      Retourne le dernier bouton cliqué.

      :return: Le dernier bouton cliqué.
      """
      return self.lastClicked

    def get_donjons(self):
      """
      Retourne la liste des donjons.

      :return: La liste des donjons.
      """
      return self.donjons

    def get_page(self):
       """
       Retourne l'index de la page actuelle.

       :return: L'index de la page actuelle.
       """
       return self.currentPage * 3

    def add_page(self,action):
       """
       Incrémente l'index de la page actuelle si l'action est différente du dernier clic.

       :param action: L'action effectuée par l'utilisateur.
       """
       if action ==self.lastClicked:return

       self.currentPage=self.currentPage+1

    def remove_page(self,action):
       """
       Décrémente l'index de la page actuelle si l'action est différente du dernier clic.

       :param action: L'action effectuée par l'utilisateur.
       """
       if action ==self.lastClicked:return

       if (self.currentPage-1)<=0:
           self.currentPage=0
           return

       self.currentPage=self.currentPage-1

    def isPlaying(self):
       """
       Retourne si une partie est en cours ou non.

       :return: True si une partie est en cours sinon False.
       """
       return self.playing

    def get_actuel_donjon(self):
       """
       Retourne le donjon actuellement joué.

       :return: Le donjon actuellement joué.
       """
       return self.playing_donjon

    def set_playing_donjon(self,dj):
       """
       Définit le donjon actuellement joué.

       :param dj: Le donjon actuellement joué.
       """
       self.playing_donjon=dj

    def set_playing(self,state):
       """
       Définit si une partie est en cours ou non.

       :param state: True si une partie est en cours sinon False.
       """
       self.playing=state

    def set_is_at_hub(self,state):
       """
       Définit si l'utilisateur est sur l'écran d'accueil ou non.

       :param state: True si l'utilisateur est sur l'écran d'accueil sinon False.
       """
       self.is_at_hub=state

    def is_at_hub(self):
        """
        Retourne si l'utilisateur est sur l'écran d'accueil ou non.

        :return: True si l'utilisateur est sur l'écran d'accueil sinon False.
        """
        return  self.is_at_hub