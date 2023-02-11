# -*- coding: utf-8 -*-
"""
Created on Sat Aug 27 13:30:45 2022

@author: Alexis Michaux-kinet
"""

import tkinter
import time
from random import randint, random
from math import sqrt, cos, sin, pi, asin, acos
from classe_animal import *

LARGEUR_FENETRE = 1000
HAUTEUR_FENETRE = 1000
RAFRAICHISSEMENT = 0.01

def animate_ball(animal):
    global canvas, Window
    
    taille = animal.taille
    sprite = canvas.create_oval(animal.position.x - taille,
            animal.position.y - taille,
            animal.position.x + taille,
            animal.position.y + taille,
            fill="Black", outline="Black", 
            width=1)
    
    while True :
        animal.maj_position()        
        canvas.move(sprite, animal.vitesse.x , animal.vitesse.y)   
        Window.update()
        time.sleep(RAFRAICHISSEMENT)

      
l_univers = LARGEUR_FENETRE - 100
h_univers = HAUTEUR_FENETRE - 100
animal = Animal(l_univers, h_univers)


Window = tkinter.Tk()
Window.title("test mouvement aléatoire")
Window.geometry(f'{LARGEUR_FENETRE}x{HAUTEUR_FENETRE}')

canvas = tkinter.Canvas(Window, width = l_univers, height = h_univers, bg = "cyan")
canvas.pack(anchor = tkinter.CENTER, expand=True)

animate_ball(animal)