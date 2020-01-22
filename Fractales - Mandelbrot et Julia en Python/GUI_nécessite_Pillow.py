import fractales_Pillow
#import fractales_normale
from tkinter import *
from tkinter import simpledialog
from random import *
from PIL import ImageTk, Image
import cmath

# MODIFIER AU BESOIN :
NB_LIGNES, NB_COLONNES = 400, 400

image = Image.new('RGB',(NB_LIGNES,NB_COLONNES))
image.save("image.png","PNG")


def affiche_julia():
    global img
    fractales_Pillow.julia(NB_LIGNES, NB_COLONNES)
    #fractales_normale.julia(NB_LIGNES, NB_COLONNES)
    
    img = ImageTk.PhotoImage(Image.open("image.png"))
    canvas.create_image(0, 0, anchor=NW, image=img)

def affiche_mandelbrot():
    global img
    fractales_Pillow.mandelbrot(NB_LIGNES, NB_COLONNES)
    #fractales_normale.mandelbrot(NB_LIGNES, NB_COLONNES)
    img = ImageTk.PhotoImage(Image.open("image.png"))
    canvas.create_image(0, 0, anchor=NW, image=img)


def zoom():
    global img
    x = float(simpledialog.askstring("Input", "Coordonnée en x (axe réel) du centre de la région à afficher : ", parent=window))
    y = float(simpledialog.askstring("Input", "Coordonnée en y (axe imaginaire) du centre de la région à afficher : ", parent=window))
    taille = float(simpledialog.askstring("Input", "Taille de la région à afficher : ", parent=window))
    ensemble = simpledialog.askstring("Input", "Ensemble de Julia ou de Mandelbrot (répondre J ou M) :", parent=window)

    fractales_Pillow.zoom(NB_LIGNES, NB_COLONNES, x, y, taille, ensemble)
    #pxls = fractales._normale.zoom(NB_LIGNES, NB_COLONNES, x, y, taille, ensemble)
    img = ImageTk.PhotoImage(Image.open("image.png"))
    canvas.create_image(0,0, anchor=NW, image=img)    

window = Tk()

# affichage de l'image
canvas = Canvas(window, width = NB_LIGNES, height = NB_COLONNES)
canvas.grid(row=0, column=0, columnspan=4)
img = ImageTk.PhotoImage(Image.open("image.png"))
canvas.create_image(0, 0, anchor=NW, image=img)


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
