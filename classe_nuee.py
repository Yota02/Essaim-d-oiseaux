#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Sep 23 09:35:42 2022

@author: Alexis Michaux-kinet
"""
from classe_animal import *
from classe_vecteur import *
from random import random, randint

class Nuee:
    """
    Attribut de classe :
        vecteur_nul : comme son nom l'indique, objet de type Vecteur égal au vecteur nul
        max_voisins : nombre maximum de voisins. Non utilisé
    Attributs :
        essaim : liste d'objets de type Animal. Le nombre est donné en paramètre du constructeur
        l_univers, h_univers : entiers, largeur et hauteur 
            de l'univers/la grille (en pixels) dans laquelle évolue la nuée
        force_vent : une force qui change de temps en temps, qui exprime un vent 
                ou une direction dominante à suivre pour l'essaim
    Méthodes :
        mouvement :
            Met à jour la position de tous les animaux de la nuée
        regles :
            Applique à chaque animal les réègles de séparation, cohésion et alignement
        voisins :
            Etant donnée une distance de voisinage, renvoie trois listes de tous 
            les voisins de chaque animal. Il y a une liste par distance de perception :
            une pour la distance de séparation, une pour la distance d'alignement, et 
            une pour la distance de cohésion.
            Ces listes sont sous la forme d'une liste de liste de
            booléens : booléen[i][j] est vrai si l'animal i a pour voisin j.
            Attention ces matrices ns pas symétriques, si l'on considère que
            les animaux ont un champ de vision de moins de 360 degrés.
        separation : permet aux animaux de ne pas s'approcher trop près. Pour
            chaque animal, l'éloigne des animaux trop proches
        alignement : permet aux animaux d'aller dans la même direction. 
            Chaque animal se rapproche de la direction moyenne de ses voisins
        cohesion : permet aux animaux de se rapprocher.
            Chaque animal se rapproche de la position moyenne de ses voisins
        centripete : modifie les vitesses des animaux.
        fuite : en présence d'un prédateur, le fuit à un angle aléatoire entre 
            -90 et +90 degrés. Annule toutes les modifications dues aux fonctions
            séparation, alignement et cohésion
        
    """
    max_voisins = 10
    vecteur_nul = Vecteur(0, 0)
    
    def __init__(self,nombre, l_univers, h_univers):
        self.essaim = []
        self.l_univers = l_univers
        self.h_univers = h_univers
        
        for i in range(nombre):
            self.essaim.append(Animal(self.l_univers, self.h_univers, i))
    
    def mouvement(self):
        for i in range(len(self.essaim)):
            self.regles(self.essaim[i])
        for k in range(len(self.essaim)):
            self.essaim[k].maj_position()
        return self.essaim

    def regles(self, animal):
        sep, align, coh = self.voisins()
        for k in range(len(self.essaim)):
            liste_aligne = []
            liste_sepa = []
            liste_cohe = []
            
            for i in range(k, len(align[k])):
                if align[k][i]:
                    liste_aligne.append(self.essaim[i])
                    
                if sep[k][i]:
                    liste_sepa.append(self.essaim[i])
                    
                if coh[k][i]:
                    liste_cohe.append(self.essaim[i])
              
            if self.essaim[k].danger:
                for index, cote in enumerate(self.essaim[k].zone_danger(50)):    
                    if cote == 1:
                        if index == 0:
                            self.essaim[i].vitesse.y *= -1
                        elif index == 1:
                            self.essaim[i].vitesse.x *= -1
                        elif index == 0:
                            self.essaim[i].vitesse.y *= -1
                        elif index == 0:
                            self.essaim[i].vitesse.x *= -1 
            
            elif len(liste_sepa) != 0:
                self.essaim[k].force.affectation(self.separation(self.essaim[k], liste_sepa))
                
            elif len(liste_aligne) != 0:
                self.essaim[k].force.affectation(self.alignement(self.essaim[k], liste_aligne))

            elif len(liste_cohe) != 0:
                self.essaim[k].force.affectation(self.cohesion(self.essaim[k], liste_cohe))

    def voisins(self) :
        vois_sep = []
        vois_align = []
        vois_coh = []
        
        for i in range(len(self.essaim)):
            vois_align.append([])
            vois_sep.append([])
            vois_coh.append([])
            
            for j in range(len(self.essaim)):
                if self.essaim[i].distance(self.essaim[j]) <= self.essaim[i].perception[0] and j != self.essaim[i].id:
                    vois_sep[i].append(True)
                else:
                    vois_sep[i].append(False)
                    
                if self.essaim[i].distance(self.essaim[j]) < self.essaim[i].perception[1] and self.essaim[i].distance(self.essaim[j]) > self.essaim[i].perception[0] and j != self.essaim[i].id:
                    vois_align[i].append(True)
                else:
                    vois_align[i].append(False)
                
                if self.essaim[i].distance(self.essaim[j]) <= self.essaim[i].perception[2] and self.essaim[i].distance(self.essaim[j]) >= self.essaim[i].perception[1] and j != self.essaim[i].id:
                    vois_coh[i].append(True)
                else:
                    vois_coh[i].append(False)

        return vois_sep, vois_align, vois_coh
            
    def alignement(self, animal, liste_vois) :
        force_alignement = Vecteur(0, 0)
        if len(liste_vois) == 0:
            return force_alignement
        
        for i in range(len(liste_vois)):
            force_alignement.somme(liste_vois[i].vitesse)
            
        force_alignement.prodk(1/len(liste_vois))
        force_alignement.diff(animal.vitesse)
        force_alignement.prodk(1/8)
        return force_alignement
    
    def separation(self, animal, liste_vois):
        force_separation = Vecteur(0, 0)
        if liste_vois == 0:
            return force_separation
        for i in range(len(liste_vois)):
            forceX = animal.position.x - liste_vois[i].position.x 
            forceY = animal.position.y - liste_vois[i].position.y
            force_separation.x += forceX
            force_separation.y += forceY
        
        force_separation.prodk(1/10)
        return force_separation
    
    def cohesion(self, animal, liste_vois):
        force_cohesion = Vecteur(0, 0)
        if len(liste_vois) == 0:
            return force_cohesion
        
        for i in range(len(liste_vois)):
            force_cohesion.somme(liste_vois[i].position)
        
        force_cohesion.prodk(1/len(liste_vois))
        force_cohesion.diff(animal.position)
        force_cohesion.prodk(1/100)

        return force_cohesion
        
    def centripete(self, animal):
        force_centripete = Vecteur(-animal.vitesse.x, -animal.vitesse.y)
        return force_centripete
    
