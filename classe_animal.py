#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep 14 11:19:12 2022

@author: Alexis Michaux-kinet
"""
from classe_vecteur import *
from random import random, randint, uniform

class Animal:
    """
    Attribut de classe :
        v_max : norme maximale du vecteur vitesse
        v_init : norme du vecteur vitesse lors de la création de l'objet
        force_max = force maximale s'exerçant sur l'animal. Pour un comportement réaliste, 
                    un animal ne peut pas par exemple faire un demi-tour immédiatement
    Attributs :
        
        position :      vecteur de coordonnées x, y aléatoires, dans les limites de la fenêtre d'affichage
        vitesse :       vecteur  sous la forme d'une liste de flottants
        taille :        rayon en pixels de l'animal. C'est comme en physique, tout est
                         une sphère parfaite (ici un cercle puisqu'en 2D)
        perception :    liste des rayons de perception de l'animal. Noter que l'animal ne
            perçoit pas ce qui se passe derrière lui. On suppose qu'il a une
            vision à 300 degrés, soit +/- 150 degrés par rapport à sa direction.
            La liste comprend 3 éléments qui correspondent aux trois règles de déplacement.
            
    Méthodes :
        force_alea : crée une force de déplacement aléatoire qui va 
                    s'appliquer sur l'animal
        maj_position : déplace l'animal suivant sa vitesse.
        distance : revoie la distance avec un autre Animal
        zone_danger : revoie une liste donnant si l'Animal dans la zone de danger
        
    """
    v_max = 6
    v_init = 3
    force_max = 0.2
    
    def __init__(self, l_univers, h_univers, id):
        self.taille = 2
        self.l_univers = l_univers
        self.h_univers = h_univers
        self.id = id
        self.danger = False
        # Modifier les deux lignes suivantes
        self.x = randint(0, 600)
        self.y = randint(0, 600)
        self.position = Vecteur(self.x, self.y)
        self.vitesse = Vecteur(0, 0)
        # Modifier les deux lignes après le while
        while self.vitesse.est_nul() :          # génération d'une vitesse aléatoire
            self.vitesse.x = uniform(-1,1)
            self.vitesse.y = uniform(-1,1)
        self.vitesse.prodk(self.v_init/self.vitesse.norme()) 
        self.perception = [25, 50, 100]     # separation, alignement, cohesion
        self.force = Vecteur(0, 0)
        
    def force_alea(self):
        
        self.force.x =  randint(1, 10)
        self.vitesse.y = randint(1, 10)

        
        if self.force.norme() != 0 :
            self.force.prodk(self.force_max/self.force.norme())
            
    def zone_danger(self, marge):
        zone = [0,0,0,0]
        self.danger = False
        if self.position.x < marge :
            zone.pop(0)
            zone.insert(0,1)
            self.danger = True
        elif self.position.x > self.l_univers - marge :
            zone.pop(2)
            zone.insert(2,1)
            self.danger = True
        elif self.position.y < marge :
            zone.pop(3)
            zone.insert(3,1)
            self.danger = True
        elif self.position.y > self.h_univers - marge :
            zone.pop(1)
            zone.insert(1,1)
            self.danger = True
        return zone
    
    def maj_position(self):
     
        self.vitesse.somme(self.force)
    
        if self.vitesse.norme() > self.v_max:
            self.vitesse.x = (self.vitesse.x/self.vitesse.norme()) * self.v_max
            self.vitesse.y = (self.vitesse.y/self.vitesse.norme()) * self.v_max
        
        if self.vitesse.norme() < self.v_init:
            self.vitesse.x = (self.vitesse.x/self.vitesse.norme()) * self.v_init
            self.vitesse.y = (self.vitesse.y/self.vitesse.norme()) * self.v_init
        
        if self.position.x > self.l_univers - 50 or self.position.x < 50:
            self.vitesse.x = -1 * self.vitesse.x
        
        if self.position.y > self.h_univers - 50 or self.position.y < 50: 
            self.vitesse.y = -1 * self.vitesse.y
            
        self.position.somme(self.vitesse)
                               
    def distance(self, autre):
        dist = sqrt((autre.position.x - self.position.x)**2 + (autre.position.y - self.position.y)**2)
        return dist
        
    def __repr__(self):
        chaine = "Position : (" + str(self.position.x) + " , " + str(self.position.y) + ")\n"
        chaine += "Vitesse : (" + str(self.vitesse.x)  + " , " + str(self.vitesse.y) + ")\n"
        chaine += "Acceleration/force : (" + str(self.force.x)  + " , " + str(self.force.y) + ")\n"
        return chaine
