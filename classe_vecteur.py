# -*- coding: utf-8 -*-
"""
Created on Tue Aug 30 15:39:51 2022

@author: Alexis Michaux-kinet 
"""
from math import sqrt, cos, sin, acos, asin, atan2, pi

class Vecteur:
    """
    Une classe pour gérer plus facilement les opérations sur les vecteurs (en 2 dimensions)
    Attributs :
        x flottant, coordonnée du vecteur suivant (Ox)
        y flottant, coordonnée du vecteur suivant (Oy)
    
    Méthodes :
        est_nul() :     renvoie un booléne Vrai si le vecteur est nul et faux sinon
        vect_nul() :    met les coordonnées du vecteur à 0
        norme() :       renvoie la norme du vecteur (sa longueur)
        somme(v) :      transforme le vecteur courant self en self + v (ajout de vecteurs)
        diff(v) :       transforme le vecteur courant self en self - v (soustraction de vecteurs)
        oppose() :      transforme le vecteur courant self en -self
        prodk(k):       transforme le vecteur courant self en k*self (produit d'un vecteur par une constante)
        affectation(v): Affecte les coordonnées de v à celle du vecteur courant self
        est_egal(v) :   Renvoie un booléen Vrai si les deux vecteurs sont égaux
        normalisation(): transforme le vecteur courant self en un vecteur de même sens et direction,
                        mais de norme 1. Le vecteur doit avoir une norme non nulle.
                        Méthode : on divise les coordonnées du vecteur par sa norme
        prod_scal(v) : renvoie le produit scalaire self.v = x.x' + y.y'
        angle(v) :       renvoie l'angle orienté (self, v) sur l'intervalle [0, 359[
    """
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def est_nul(self):
        if self.x == 0 and self.y == 0: 
            return True
        else :
            return False
    
    def vect_nul(self):
        self.x = 0
        self.y = 0
        return self.x, self.y

    def norme(self):
        return sqrt(self.x**2 + self.y**2)
        
    def somme(self, v):
        self.x = self.x + v.x
        self.y = self.y + v.y
        return self.x, self.y
    
    def diff(self, v):
        self.x = self.x - v.x
        self.y = self.y - v.y
        return self.x, self.y
    
    def oppose(self):
        self.x = -self.x 
        self.y = -self.y 
        return self.x, self.y

    def prodk(self, k):
        self.x = self.x * k
        self.y = self.y * k
        return self.x, self.y

    def affectation(self, v):
        self.x = v.x  
        self.y = v.y 
        return self.x, self.y 
    
    def est_egal(self, v):
        return self.x == v.x and self.y == v.y
    
    def normalisation(self):
        # Transforme le vecteur courant en un vecteur de norme 1. Opération très courante
        # même s'il est probable que c'est la première fois que vous entendez ce terme
        # Si le vecteur est nul, on ne peut pas le normaliser. On renvoie une
        # erreur dans ce cas. Si on veut arreter le programme)on peut remplacer le test par : 
        # assert norme != 0 , "ERREUR : erreur de normalisation, vecteur nul" 
        # ou encore
        # if norme == 0 : 
        #   raise ValueError('ERREUR : erreur de normalisation, vecteur nul')
        norme = self.norme()
        if norme == 0 :
            print("AVERTISSEMENT : erreur de normalisation, vecteur nul")
        else :
            self.x = self.x/norme
            self.y = self.y/norme
    
    def prod_scal(self, v):
        # Renvoie le produit scalaire du vecteur courant (self) avec un autre vecteur v
        return self.x * v.x + self.y*v.y
        
    def angle(self, v):
        # Calcule l'angle en degrés entre le vecteur courant (self) et un autre vecteur v
        # C'est la méthode la plus efficace, qui donne un angle orienté. On l'a ici renvoyé en
        # mesure entre entre 0 et 360°
        # On calcule l'arctangente du rapport y/x, où x et y sont les deux arguments
        # Le 1er argument de atan2 provient du produit vectoriel de u et v, que vous utiliserez
        # dans le supérieur, et le 2ème : vous connaissez, qu'est-ce ?
        angle = atan2(self.x * v.y - self.y * v.x, self.x * v.x + self.y * v.y)
        return (angle*180/pi) % 360
    
    def __repr__(self):
        return "(" + str(self.x) + " , " + str(self.y) + ")"

def tests():    
    u = Vecteur(1, 2)
    v = Vecteur(3, 4)
    print("vecteur u : ", u)
    print("vecteur v : ", v)
    u.somme(v)
    print("somme u + v : ", u)
    u.prodk(3)
    print("produit 3u : ", u)
    print("Norme de v : ", v.norme())
    print("u est-il nul : ",u.est_nul())
    print("Peroduit scalaire 3u x v : ",u.prod_scal(v))
    u.vect_nul()
    print("Test de la mise au vecteur nul de u : ", u.est_nul())
    u.affectation(v)
    print("Vecteur u après lui avoir affecté v : ", u)
    u.oppose()
    print("Opposé de u :", u)
    u.diff(v)
    print("Calcul u - v : ", u)
    v = Vecteur(2, 2)
    print("Vecteur v", v)
    v.normalisation()
    print("Vecteur v normalisé :", v)
