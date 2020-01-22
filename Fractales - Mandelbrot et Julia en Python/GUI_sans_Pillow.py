import fractales_normale
from tkinter import *
from tkinter import simpledialog
from random import *

import cmath

# MODIFIER AU BESOIN :
NB_LIGNES, NB_COLONNES = 400, 400

def affiche_julia():

    pxls = fractales_normale.julia(NB_LIGNES, NB_COLONNES)
    for i in range(NB_LIGNES):
        for j in range(NB_COLONNES):
            pixels.put(pxls[i][j], (i, j))
        
    imgLbl.image = pixels


def affiche_mandelbrot():

    pxls = fractales_normale.mandelbrot(NB_LIGNES, NB_COLONNES)
    for i in range(NB_LIGNES):
        for j in range(NB_COLONNES):
            pixels.put(pxls[i][j], (i, j))
        
    imgLbl.image = pixels


def zoom():
    x = float(simpledialog.askstring("Input", "Coordonnée en x (axe réel) du centre de la région à afficher : ", parent=window))
    y = float(simpledialog.askstring("Input", "Coordonnée en y (axe imaginaire) du centre de la région à afficher : ", parent=window))
    taille = float(simpledialog.askstring("Input", "Taille de la région à afficher : ", parent=window))
    ensemble = simpledialog.askstring("Input", "Ensemble de Julia ou de Mandelbrot (répondre J ou M) :", parent=window)

    pxls = fractales_normale.zoom(NB_LIGNES, NB_COLONNES, x, y, taille, ensemble)
    for i in range(NB_LIGNES):
        for j in range(NB_COLONNES):
            pixels.put(pxls[i][j], (i, j))
        
    imgLbl.image = pixels
    

window = Tk()

pixels = PhotoImage()

for i in range(NB_LIGNES):
    for j in range(NB_COLONNES):
        p = "#{:02x}{:02x}{:02x}".format(255, 255, 255)
        pixels.put(p, (i, j))

imgLbl = Label(image=pixels)
imgLbl.image = pixels
imgLbl.grid(row=0, column=0, columnspan=4)


# bouton julia
BTNJulia = Button(window)
BTNJulia["text"] = "Julia"
BTNJulia["command"] = affiche_julia
BTNJulia.grid(row=1, column=0)

# bouton mandelbrot
BTNMandelbrot = Button(window)
BTNMandelbrot["text"] = "Mandelbrot"
BTNMandelbrot["command"] = affiche_mandelbrot
BTNMandelbrot.grid(row=1, column=1)

# bouton zoom
BTNZoom = Button(window)
BTNZoom["text"] = "Zoom"
BTNZoom["command"] = zoom
BTNZoom.grid(row=1, column=2)

# bouton quit
BTNQuit = Button(window)
BTNQuit ["text"] = "Quit"
BTNQuit ["command"] = quit
BTNQuit.grid(row=1, column=3)


mainloop()
