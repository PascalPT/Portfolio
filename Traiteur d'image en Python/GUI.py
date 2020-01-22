import math
from tkinter import *
from tkinter import simpledialog, filedialog

LARGEUR, HAUTEUR = 256, 256

def changer_image():
    from PIL import Image, ImageTk
    global Nouvelle_image, photo_base, image_base, photo_modif, image_modif, photo
    # Pour empecher le 'garbage collector' de détruire l'image.
    """
    Demande à l'utilisateur le chemin d'une nouvelle image et utilise la libraire PIL pour enregistrer
    la nouvelle image sous le nom de Lenna.png et ainsi permettre d'utiliser le tp avec une autre image.
    """
    
    chemin = filedialog.askopenfilename(title = "Select pictures (The closer to 256 x 256 the best it is)",
                                        filetypes=[("Images files","*.png")]) # Demande le chemin vers la nouvelle image.
    
    Nouvelle_image = Image.open(chemin) # Ouvre la nouvelle image.
    Nouvelle_image.save("Lenna.png","PNG")# Enregistre la nouvelle image sous le nom Lena.png par dessus l'ancienne-image. 
    
    photo = PhotoImage(file="Lenna.png") #Affiche l'image maintenant apeller Lena.png.
    image_modif = Label(image=photo)
    image_modif.image = photo
    image_modif.grid(row=0, column=4, columnspan=4)
    image_base = Label(image=photo)
    image_base.image = photo
    image_base.grid(row=0, column=0, columnspan=4)
    
def originale_image():
    from PIL import Image, ImageTk
    global Nouvelle_image, photo_base, image_base, photo_modif, image_modif
    # Pour empecher le garbage collector de détruire l'image.
    """
    Demande à l'utilisateur le chemin d'une nouvelle image et utilise la libraire PIL pour enregistrer
    la nouvelle image sous le nom de Lenna.png et ainsi permettre d'utiliser le tp avec une autre image.
    """
    Nouvelle_image = Image.open("Lenna - Original.png") #Ouvre une image nommer Lenna - Original.png qui est identique à l'image de base.
    Nouvelle_image.save("Lenna.png","PNG") # Enregistre cette image sous le nom de Lenna.png .

    photo = PhotoImage(file="Lenna.png") # Affiche l'image maintenant apeller Lena.png.
    image_modif = Label(image=photo)
    image_modif.image = photo
    image_modif.grid(row=0, column=4, columnspan=4)
    image_base = Label(image=photo)
    image_base.image = photo
    image_base.grid(row=0, column=0, columnspan=4)
    
    
def rvb2hex(r,v,b):
    hex = "#{:02x}{:02x}{:02x}".format(r,v,b)
    return hex

def composante_rouge():

    """
    Parcours chacun des pixels de l'image, de 0 à 256,
    analyse la quantité de rouge, de vert et de bleu de chaque pixel,
    crée un nouveau pixel avec seulement la composante rouge de chaque position et
    remplace le pixel initial par le nouveau.
    """
    
    photo = PhotoImage(file="Lenna.png")

    for i in range (0,256):
        for j in range (0,256):
            (r,v,b) = photo.get(i,j)
            (r1,v1,b1) = (r,0,0)
            t = rvb2hex(r1,v1,b1)
            photo.put(t,(i,j))

    image_modif = Label(image=photo)
    image_modif.image = photo
    image_modif.grid(row=0, column=4, columnspan=4)
    print("composante rouge")


def composante_verte():

    """
    Parcours chacun des pixels de l'image, de 0 à 256,
    analyse la quantité de rouge, de vert et de bleu de chaque pixel,
    crée un nouveau pixel avec seulement la composante verte de chaque position et
    remplace le pixel initial par le nouveau.
    """
    
    photo = PhotoImage(file="Lenna.png")

    for i in range (0,256):
        for j in range (0,256):
            (r,v,b) = photo.get(i,j)
            (r1,v1,b1) = (0,v,0)
            t = rvb2hex(r1,v1,b1)
            photo.put(t,(i,j))

    
    image_modif = Label(image=photo)
    image_modif.image = photo
    image_modif.grid(row=0, column=4, columnspan=4)

    print("composante verte")


def composante_bleue():

    """
    Parcours chacun des pixels de l'image, de 0 à 256,
    analyse la quantité de rouge, de vert et de bleu de chaque pixel,
    crée un nouveau pixel avec seulement la composante bleue de chaque position et
    remplace le pixel initial par le nouveau.
    """
    
    photo = PhotoImage(file="Lenna.png")

    for i in range (0,256):
        for j in range (0,256):
            (r,v,b) = photo.get(i,j)
            (r1,v1,b1) = (0,0,b)
            t = rvb2hex(r1,v1,b1)
            photo.put(t,(i,j))

    image_modif = Label(image=photo)
    image_modif.image = photo
    image_modif.grid(row=0, column=4, columnspan=4)

    print("composante bleue")


def luminance():
    
    """
    Parcours chacun des pixels de l'image, de 0 à 256,
    calcule la luminance de chaque pixel,
    soit l'information des niveaux de gris de l'image,
    et ressort l'image en noir et blanc.
    """
    
    photo = PhotoImage(file="Lenna.png")

    for i in range(0, 256):
        for j in range(0, 256):
            (r, v, b) = photo.get(i, j)
            L = 0.299 * r + 0.587 * v + 0.114 * b   #calcul de la luminance
            (r1, v1, b1) = (L,L,L)
            #Ajoute 1 à r1,v1,b1 pour faire l'arrondissement de r1,v1,b1 à l'unité.
            if r1%1 >= 0.5:
                r1 = r1 + 1
            if v1%1 >= 0.5:
                v1 = v1 + 1
            if b1%1 >= 0.5:
                b1 = b1 + 1
            (r2, v2, b2) = (int(r1), int(v1), int(b1))#arrondit r1,v1,b1 à l'unité près
            t = rvb2hex(r2, v2, b2)
            photo.put(t, (i, j))

    image_modif = Label(image=photo)
    image_modif.image = photo
    image_modif.grid(row=0, column=4, columnspan=4)

    print("luminance")


def chrominance1():

    """
    Parcours chacun des pixels de l'image, de 0 à 256,
    calcule la chrominance 1 de chaque pixel,
    soit l'écart entre le niveau de bleu et la luminance,
    et ressort l'image modifiée.
    """
    
    photo = PhotoImage(file="Lenna.png")
    for i in range(0, 256):
        for j in range(0, 256):
            (r, v, b) = photo.get(i, j)
            M = -0.16874 * r - 0.33126 * v + 0.5 * b + 128  #calcul de la chrominance 1
            (r1, v1, b1) = (128, 128 - 0.34413 * (M - 128), 128 + 1.772 * (M - 128))
            #Ajoute 1 à r1,v1,b1 pour faire l'arrondissement de r1,v1,b1 à l'unité.
            if r1%1 >= 0.5:
                r1 = r1 + 1
            if v1%1 >= 0.5:
                v1 = v1 + 1
            if b1%1 >= 0.5:
                b1 = b1 + 1
            (r2, v2, b2) = (max(min(int(r1),255),0), max(min(int(v1),255),0), max(min(255,int(b1)),0))
            #Arrondit r1,v1,b1 à l'unité près et prend la valeur pour la quantité de rouge, bleu ou vert qui est entre 0 ou 255
            #pour empecher la 'parsage d'une couleur innexistante (pour python). Dans le cas d'un nombre plus grand ou plus petit le remplace par 0 ou 255.
            t = rvb2hex(r2, v2, b2)
            photo.put(t, (i, j))
    
    image_modif = Label(image=photo)
    image_modif.image = photo
    image_modif.grid(row=0, column=4, columnspan=4)

    print("chrominance1")

def chrominance2():

    """
    Parcours chacun des pixels de l'image, de 0 à 256,
    calcule la chrominance 2 de chaque pixel,
    soit l'écart entre le niveau de rouge et la luminance,
    et ressort l'image modifiée.
    """
    
    photo = PhotoImage(file="Lenna.png")

    for i in range(0, 256):
        for j in range(0, 256):
            (r, v, b) = photo.get(i, j)
            N = 0.5 * r - 0.41869 * v - 0.08131 * b + 128   #calcul de la chrominance 2
            (r1, v1, b1) = (128 + 1.402 * (N - 128), 128 - 0.71414 * (N - 128), 128)
            #Ajoute 1 à r1,v1,b1 pour faire l'arrondissement de r1,v1,b1 à l'unité.
            if r1%1 >= 0.5:
                r1 = r1 + 1
            if v1%1 >= 0.5:
                v1 = v1 + 1
            if b1%1 >= 0.5:
                b1 = b1 + 1
            (r2, v2, b2) = (int(r1), int(v1), int(b1))#arrondit r1,v1,b1 à l'unité près
            t = rvb2hex(r2, v2, b2)
            photo.put(t, (i, j))
    
    image_modif = Label(image=photo)
    image_modif.image = photo
    image_modif.grid(row=0, column=4, columnspan=4)

    print("chrominance2")


def niveau_gris():

    """
    Appelle la fonction luminance() qui ressort une image au niveau de gris
    """

    luminance()
    print("niveau de gris")

def augmente_rouge():

    """
    Parcours chacun des pixels de l'image, de 0 à 256,
    analyse la quantité de rouge, de vert et de bleu de chaque pixel,
    augmente le rouge selon la quantité désirée par l'utilisateur
    et ressort l'image modifiée.
    """
        
    photo = PhotoImage(file="Lenna.png")
    k = float(simpledialog.askstring("Input", "Augmenter le rouge de quelle quantité ? ", parent=window))

    for i in range(0, 256):
        for j in range(0, 256):
            (r, v, b) = photo.get(i, j)
            (r1, v1, b1) = (r + k, v, b)
            if r1 > 255:   #si valeur de rouge > 255, faut la limiter à 255 puisque Python ne peut pas la ressortir
                r1 = 255
            #Ajoute 1 à r1 pour faire l'arrondissement de r1 à l'unité si besoin.
            if r1%1 >= 0.5:
                r1 = r1 + 1
            t = rvb2hex(int(r1), v1, b1) #arrondit r1 si besoin à l'unité.
            photo.put(t, (i, j))
    
    image_modif = Label(image=photo)
    image_modif.image = photo
    image_modif.grid(row=0, column=4, columnspan=4)

    print("augmente rouge")


def augmente_luminosite():

    """
    Parcours chacun des pixels de l'image, de 0 à 256,
    analyse la quantité de rouge, de vert et de bleu de chaque pixel,
    augmente chaque composante RVB avec L qui est la luminance du pixel
    et ressort l'image modifiée
    """
    
    photo = PhotoImage(file="Lenna.png")

    for i in range (0,256):
        for j in range (0,256):
            (r,v,b) = photo.get(i,j)
            L=0.299*r+0.587*v+0.114*b   #formule de la luminance
            (r1, v1, b1) = (r + L*(255-r)/510, v + L*(255-v)/510, b + L*(255-b)/510)   #augmentation de la luminosité
            #Ajoute 1 à r1,v1,b1 pour faire l'arrondissement de r1,v1,b1 à l'unité si besoin.
            if r1%1 >= 0.5:
                r1 = r1 + 1
            if v1%1 >= 0.5:
                v1 = v1 + 1
            if b1%1 >= 0.5:
                b1 = b1 + 1
            (r2, v2, b2) = (int(r1), int(v1), int(b1))   #arrondit à l'unité pour permettre de ressortir l'image finale
            t = rvb2hex(r2, v2, b2)
            photo.put(t, (i, j))
    
    image_modif = Label(image=photo)
    image_modif.image = photo
    image_modif.grid(row=0, column=4, columnspan=4)
    
    print("augmente luminosite")

def reflexion_verticale():

    """
    Parcours chacun des pixels de l'image, de 0 à 256,
    analyse la quantité de rouge, de vert et de bleu de chaque pixel,
    envoie chaque pixel à l'extrémité opposée en x en modifiant leur position
    et ressort l'image modifiée.
    """

    photo_modif = PhotoImage(file="Lenna.png")
    photo = PhotoImage(file="Lenna.png")

    for i in range (0,256):
        for j in range (0,256):
            (r,v,b) = photo.get(i,j)
            x=255-i  #inverse la position des pixels à l'autre extrémité en x de la photo
            t = rvb2hex(r, v, b)
            photo_modif.put(t, (x, j))  #remplace i par la nouvelle position inversée "x"
    photo=photo_modif
    
    image_modif = Label(image=photo)
    image_modif.image = photo
    image_modif.grid(row=0, column=4, columnspan=4)

    print("réflexion verticale")


def lissage():

    """
    Parcours chacun des pixels de l'image, de 0 à 256,
    analyse la quantité de rouge, de vert et de bleu de chaque pixel,
    fait la moyenne des valeurs RVB de chaque pixel autour du pixel initial,
    ce qui crée une image finale plus floue,
    et ressort l'image modifiée.
    """
    
    photo = PhotoImage(file="Lenna.png")
    photo_base = PhotoImage(file="Lenna.png")
    
    (rtot, vtot, btot) = (0, 0, 0) #total des composantes RVB
    (rg, vg, bg) = (0, 0, 0) #pixel gauche
    (rd, vd, bd) = (0, 0, 0) #pixel droit
    (rb, vb, bb) = (0, 0, 0) #pixel bas
    (rh, vh, bh) = (0, 0, 0) #pixel haut
    (rgh, vgh, bgh) = (0, 0, 0) #pixel en diagonal en haut à gauche
    (rgb, vgb, bgb) = (0, 0, 0) #pixel en diagonal en bas à gauche
    (rdh, vdh, bdh) = (0, 0, 0) #pixel en diagonal en haut à droite
    (rdb, vdb, bdb) = (0, 0, 0) #pixel en diagonal en haut à droite

    for i in range (0,256):
        for j in range (0,256):
            (r,v,b) = photo_base.get (i,j)
            if i > 0: #si pixel pas dans première rangée verticale de pixels à gauche, prendre l'autre d'avant
                (rg,vg,bg) = photo_base.get(i-1,j)
            if i < 255: #si pixel pas dans dernière rangée verticale de pixels à droite, prendre l'autre d'après
                (rd,vd,bd) = photo_base.get(i+1,j)
            if j > 0: #si pixel pas dans première rangée horizontale de pixels en haut, prendre l'autre d'avant
                (rb,vb,bb) = photo_base.get(i,j-1)
            if j < 255: #si pixel pas dans dernière rangée verticale de pixels en bas, prendre l'autre d'après
                (rh,vh,bh) = photo_base.get(i,j+1)
            if 0 < i < 255 and 0 < j < 255: #si pixel ne fait pas parti d'aucune première ligne ou colone de l'image
                (rgh, vgh, bgh) = photo_base.get(i - 1, j - 1)
                (rgb, vgb, bgb) = photo_base.get(i - 1, j + 1)
                (rdh, vdh, bdh) = photo_base.get(i + 1, j + 1)
                (rdb, vdb, bdb) = photo_base.get(i + 1, j + 1)

            (rtot, vtot, btot) = ((r/9) + (rg/9) + (rd/9) + (rb/9) + (rh/9) + (rgh/9) + (rgb/9) + (rdh/9) + (rdb/9), #calcul de la moyenne de chaque pixel autour du pixel initial
                                  (v/9) + (vg/9) + (vd/9) + (vb/9) + (vh/9) + (vgh/9) + (vgb/9) + (vdh/9) + (vdb/9),
                                  (b/9) + (bg/9) + (bd/9) + (bb/9) + (bh/9) + (bgh/9) + (bgb/9) + (bdh/9) + (bdb/9))

            if rtot > 255: #si chaque composante RVB > 255, doit limiter à 255 sinon Python peut pas ressortir image finale
                rtot = 255
            if vtot > 255:
                vtot = 255
            if btot > 255:
                btot = 255
            if rtot < 0: #si chaque composante RVB < 0, doit limiter à 0 sinon Python peut pas ressortir image finale
                rtot = 0
            if vtot < 0:
                vtot = 0
            if btot < 0:
                btot = 0

            #Ajoute 1 à rtot,vtot,btot pour faire l'arrondissement de rtot,vtot,btot à l'unité si besoin.
            if rtot%1 >= 0.5:
                rtot = rtot + 1
            if vtot%1 >= 0.5:
                vtot = vtot + 1
            if btot%1 >= 0.5:
                btot = btot + 1

            (r_arrondi,b_arrondi,v_arrondi) = (int(rtot),int(btot),int(vtot)) #arrondit à l'unité pour permettre de ressortir l'image finale
            t = rvb2hex(r_arrondi, v_arrondi, b_arrondi)
            photo.put(t, (i, j))

           
    image_modif = Label(image=photo)
    image_modif.image = photo
    image_modif.grid(row=0, column=4, columnspan=4)
    print("lissage")



def augmente_contraste():

    """
    Parcours chacun des pixels de l'image, de 0 à 256,
    analyse la quantité de rouge, de vert et de bleu de chaque pixel,
    multiplie 5 fois le pixel central et -1 fois ceux en haut, en bas, à gauche et à droite du pixel initial afin d'augmenter les détails
    et ressort l'image finale modifiée.
    """
    
    photo = PhotoImage(file="Lenna.png")
    photo_base = PhotoImage(file="Lenna.png") 

    (rtot, vtot, btot) = (0, 0, 0) #total des composantes RVB
    (rg, vg, bg) = (0, 0, 0) #pixel gauche
    (rd, vd, bd) = (0, 0, 0) #pixel droit
    (rb, vb, bb) = (0, 0, 0) #pixel bas
    (rh, vh, bh) = (0, 0, 0) #pixel haut

    for i in range(0, 256):
        for j in range(0, 256):
            (r, v, b) = photo_base.get(i, j)
            if i > 0: #si pixel pas dans première rangée verticale de pixels à gauche, prendre l'autre d'avant
                (rg, vg, bg) = photo_base.get(i - 1, j)
            if i < 255: #si pixel pas dans dernière rangée verticale de pixels à droite, prendre l'autre d'après
                (rd, vd, bd) = photo_base.get(i + 1, j)
            if j > 0: #si pixel pas dans première rangée horizontale de pixels en haut, prendre l'autre d'avant
                (rb, vb, bb) = photo_base.get(i, j - 1)
            if j < 255: #si pixel pas dans dernière rangée verticale de pixels en bas, prendre l'autre d'après
                (rh, vh, bh) = photo_base.get(i, j + 1)

            (rtot, vtot, btot) = ((5 * r) + (-1 * rg) + (-1 * rd) + (-1 * rb) + (-1 * rh), #multiplication 5 fois du pixel central et -1 fois des pixels en haut, en bas, à gauche et à droite du pixel initial
                                  (5 * v) + (-1 * vg) + (-1 * vd) + (-1 * vb) + (-1 * vh),
                                  (5 * b) + (-1 * bg) + (-1 * bd) + (-1 * bb) + (-1 * bh))

            if rtot > 255: #si chaque composante RVB > 255, doit limiter à 255 sinon Python peut pas ressortir image finale
                rtot = 255
            if vtot > 255:
                vtot = 255
            if btot > 255:
                btot = 255
            if rtot < 0: #si chaque composante RVB < 0, doit limiter à 0 sinon Python peut pas ressortir image finale
                rtot = 0
            if vtot < 0:
                vtot = 0
            if btot < 0:
                btot = 0

            t = rvb2hex(rtot, vtot, btot)
            photo.put(t, (i, j))
    
    image_modif = Label(image=photo)
    image_modif.image = photo
    image_modif.grid(row=0, column=4, columnspan=4)
    print("augmente contraste")



def detecte_contours():

    """
    Parcours chacun des pixels de l'image, de 0 à 256,
    analyse la quantité de rouge, de vert et de bleu de chaque pixel,
    multiplie 8 fois le pixel central et -1 fois les pixels autours afin d'observer les endroits où la luminance est maximale
    et ressort l'image finale modifiée.
    """
    
    photo = PhotoImage(file="Lenna.png")
    photo_base = PhotoImage(file="Lenna.png") 

    (rg, vg, bg) = (0, 0, 0)  # pixel gauche
    (rd, vd, bd) = (0, 0, 0)  # pixel droit
    (rb, vb, bb) = (0, 0, 0)  # pixel bas
    (rh, vh, bh) = (0, 0, 0)  # pixel haut
    (rgh, vgh, bgh) = (0, 0, 0)  # pixel en diagonal en haut à gauche
    (rgb, vgb, bgb) = (0, 0, 0)  # pixel en diagonal en bas à gauche
    (rdh, vdh, bdh) = (0, 0, 0)  # pixel en diagonal en haut à droite
    (rdb, vdb, bdb) = (0, 0, 0)  # pixel en diagonal en haut à droite

    for i in range(0, 256):
        for j in range(0, 256):
            (r, v, b) = photo_base.get(i, j)
            L = 0.299 * r + 0.587 * v + 0.114 * b #calcul de la luminance avec les compsoantes RVB du pixel analysé
            L = L * (-8) #multiplication 8 fois de la luminance
            if i > 0: #si pixel pas dans première rangée verticale de pixels à gauche, prendre l'autre d'avant
                (rg, vg, bg) = photo_base.get(i - 1, j)
                L += 0.299 * rg + 0.587 * vg + 0.114 * bg #ajout à la luminance totale de l'image
            if i < 255: #si pixel pas dans dernière rangée verticale de pixels à droite, prendre l'autre d'après
                (rd, vd, bd) = photo_base.get(i + 1, j)
                L += 0.299 * rd + 0.587 * vd + 0.114 * bd
            if j > 0: #si pixel pas dans première rangée horizontale de pixels en haut, prendre l'autre d'avant
                (rb, vb, bb) = photo_base.get(i, j - 1)
                L += 0.299 * rb + 0.587 * vb + 0.114 * bb
            if j < 255: #si pixel pas dans dernière rangée verticale de pixels en bas, prendre l'autre d'après
                (rh, vh, bh) = photo_base.get(i, j + 1)
                L += 0.299 * rh + 0.587 * vh + 0.114 * bh
            if 0 < i < 255 and 0 < j < 255: #si pixel ne fait pas parti d'aucune première ligne ou colone de l'image
                (rgh, vgh, bgh) = photo_base.get(i - 1, j - 1)
                L += 0.299 * rgh + 0.587 * vgh + 0.114 * bgh
                (rgb, vgb, bgb) = photo_base.get(i - 1, j + 1)
                L += 0.299 * rgb + 0.587 * vgb + 0.114 * bgb
                (rdh, vdh, bdh) = photo_base.get(i + 1, j + 1)
                L += 0.299 * rdh + 0.587 * vdh + 0.114 * bdh
                (rdb, vdb, bdb) = photo_base.get(i + 1, j + 1)
                L += 0.299 * rdb + 0.587 * vdb + 0.114 * bdb

            if L > 255: #si luminance totale > 255, doit limiter à 255 sinon Python peut pas ressortir image finale
                L = 255
            if L < 0: #si luminance totale < 0, doit limiter à 0 sinon Python peut pas ressortir image finale
                L = 0
            if L < 150: #si luminance < 150, applique seuil de L à 0 pour de meilleurs résultats
                L = 0
            if L >= 150: #si luminance >= 150, applique seuil de L à 255 pour de meilleurs résultats
                L = 255
            (r1, v1, b1) = (L, L, L)

            #Ajoute 1 à r1,v1,b1 pour faire l'arrondissement de r1,v1,b1 à l'unité si besoin.
            if r1%1 >= 0.5:
                r1 = r1 + 1
            if v1%1 >= 0.5:
                v1 = v1 + 1
            if b1%1 >= 0.5:
                b1 = b1 + 1
            
            (r2, v2, b2) = (int(r1), int(v1), int(b1)) #arrondit à l'unité pour permettre de ressortir l'image finale
            t = rvb2hex(r2, v2, b2)
            photo.put(t, (i, j))

    
    image_modif = Label(image=photo)
    image_modif.image = photo
    image_modif.grid(row=0, column=4, columnspan=4)
    
    print("détecte contours")

def pavage():

    """
    Demande la méthode de pavage soit par moyenne ou par 'photomaton' et le nombre de fois que l'utilisateur veut opérer.
    Ensuite, si c'est par moyenne l'image est rétrécis en faisant la moyenne de 4 pixels voisins en un seul. L'image créer
    correspondera à seulement 1/4 de l'image. Celle-ci est copier sur les 3 autres coins. Cela est répéter le nombre de fois
    nécéssaire. Si la méthode est 'photomaton', alors chaques pixels se voit assigner un coin différent de l'imgage
    et est placés dans son coin respectif. L'opération est répéter le nombre de fois nécéssaire.
    """

    #Ouvre une fenêtre qui demande la méthode voulut.
    méthode = simpledialog.askstring("Input", "Type de pavage -> Par Moyenne(m) ou Photomaton(p)", parent=window)
    #Ouvre une fenêtre qui demande le nombre de fois que l'opération doit être faite,
    n = int(simpledialog.askstring("Input", "Nombre de fois que l'image doit être paver (minimum =1)", parent=window))
    photo = PhotoImage(file="Lenna.png")
        
    while n > 0 and méthode == "p": 
        photo_modif = PhotoImage(file="Lenna.png")
        x = -1 #x commence à -1, car il sera additionner 1 avant d'être placer. Il commence donc rellement à 0.
        for i in range(0,256,2):
            x+=1 #x et y correspondent aux emplacementx des pixels qui doivent être assignés dans le coin haut-gauche.
            y=0
            for j in range(0,256,2):#Sépare l'image en 4 en faisant des bonds de 2 pour j et i.
                
                pix = photo.get(i,j) #Prend 4 pixels qui sont collés.
                pixDroit = photo.get(i+1,j)
                pixBas = photo.get(i,j+1)
                pixBasDroit = photo.get(i+1,j+1)
                
                #Sépare les 4 pixels et les placent dans le coin qui lui est assigné dû à sa position. 
                photo_modif.put(rvb2hex(pix[0],pix[1],pix[2]),(x,y))
                photo_modif.put(rvb2hex(pixDroit[0],pixDroit[1],pixDroit[2]),(x+128,y))
                photo_modif.put(rvb2hex(pixBas[0],pixBas[1],pixBas[2]),(x,y+128))
                photo_modif.put(rvb2hex(pixBasDroit[0],pixBasDroit[1],pixBasDroit[2]),(x+128,y+128))
                y+=1

        photo=photo_modif
        n -= 1 # diminue le nombre de fois que l'opération doit avoir lieux par 1.
        

    while n > 0 and méthode == 'm':
        x=-1 #x commence à -1, car il sera additionner 1 avant d'être placer. Il commence donc rellement à 0.
        for i in range (0,255,2):
            x+=1 #x et y correspondent aux emplacementx des pixels qui doivent être assignés dans le coin haut-gauche.
            y = 0
            for j in range (0,255,2): #Sépare l'image en 4 en faisant des bonds de 2 pour j et i.

                pix = photo.get(i,j) #Prend 4 pixels qui sont collés.
                pixDroit=photo.get(i+1,j)
                pixBas=photo.get(i,j+1)
                pixBasDroit=photo.get(i+1,j+1)

                #Fait la moyenne de rouge, vert et bleu de ces 4 pixels
                r = (pix[0]+pixDroit[0]+pixBas[0]+pixBasDroit[0])/4
                v = (pix[1]+pixDroit[1]+pixBas[1]+pixBasDroit[1])/4
                b = (pix[2]+pixDroit[2]+pixBas[2]+pixBasDroit[2])/4

                #Ajoute 1 à r,v,b pour faire l'arrondissement à l'unité si besoin.
                if r%1 >= 0.5:
                     r = r + 1
                if v%1 >= 0.5:
                     v = v + 1
                if b%1 >= 0.5:
                     b = b + 1

                #Place les pixels obtenus par moyenne dans la photo de base      
                t = rvb2hex(min(int(r),255),min(int(v),255),min(int(b),255)) # Prend la valeur la plus petite entre 255 le rouge,
                                                                             #vert et bleu pour que python puissent placer le pixel
                photo.put(t,(x,y))
                y+=1

        #La nouvelle image a été placé dans le coin haut-gauche.
        #Elle est copié dans les 3 autre coins
        for k in range(128):
            for p in range(128):
                c = photo.get(k,p)
                t = rvb2hex(c[0], c[1],c[2])
                photo.put(t,(k+128,p))
                photo.put(t,(k,p+128))
                photo.put(t,(k+128,p+128))
        n-=1 # diminue le nombre de fois que l'opération doit avoir lieux par 1.

    image_modif = Label(image=photo)
    image_modif.image = photo
    image_modif.grid(row=0, column=4, columnspan=4)
        
    print("pavage")
    

def rotation():
    """
    Demande à l'utilisateur dans une fenêtre l'angle de rotation qu'il veut et retotionne l'image selon cette angle.
    """

    #Ouvre un fenêtre et demande l'angle de rotation qui doit suivre les modèles fournient ou être laissé vide.
    a = simpledialog.askstring("Input", "Donner l'angle pour la rotation (Pi, Pi/2, Pi/3, 5Pi/4, etc.) ", parent=window)
    
    g = ''#Création de variable temporaire qui serviront à extraire la valeur fournit et la transformer en nombre (float).
    n = 0 # n est la position dans la chaîne de texte fournie.
    h = ''
    if a == '': #Si a était vide assigne la valeur de 0 à a.
        a = str(0)
    while a[n] != 'P' and a != str(0): # Prend la partie de gauche (Avant le P) de ce qui est fournie et en extrait les chiffres.
        g = str(g) + str(a[n])
        n += 1 # n est augmenté de 1 à chaque nombre trouvé
    if g == '': # Si g était vide lui donne la valeur de 1 pour éviter les divisions par rien ou 0.
        g = 1
    g = float(g)
    while n < len(a) - 3 and a != str(0): # Prend la partie de droite (après la /) de ce qui est fournie et en extrait les chiffres.
        h = str(h) + str(a[n + 3])
        n += 1 # n est augmenté de 1 à chaque nombre trouvé
    if h == '': # Si h était vide lui donne la valeur de 1 pour éviter les divisions par rien ou 0.
        h = 1
    h = float(h)
    b = float(math.pi)
    if a != str(0): # Si a n'était pas vide, il ne sera pas égale à 0 et l'angle peut alors être calculé en nombre réelle (float).
        a = -1 * g * b / h #Le -1 correspond au fait que les rotations se font dans le sens anti-horaire. 
    else:
        a = int(a) # Si a était vide et qu'il a été assigné 0, il est alors transformé de chaines à nombre (int).

    photo = PhotoImage(file="Lenna.png")
    photo_modif = PhotoImage(file="Lenna.png")
    
    for k in range(256):#Parcours l'image à modifier et mets des pixels noirs pour que les pixels dans des positions
                        #'arrondis' et donc inexistante à cause des cos et sin soient noirs.
        for p in range(256):
            t = rvb2hex(0, 0, 0)
            photo_modif.put(t, (k, p))

    for i in range(-127, 127):#Parcous à partir de -127 pour ajuster le centre de l'image comme pivot de rotation.
        for j in range(-127, 127): # Parcours chaque pixels de l'image d'origine et calcule le nouvelle emplacement de chaque pixels.
            x = math.cos(a) * i - math.sin(a) * j + 128 #x et y correspondent aux nouvelles emplacements des pixels
            y = math.sin(a) * i + math.cos(a) * j + 128 #Ajoute 128 pour que le centre de rotation soit dans le milieu de l'image.
            if 0 <= x < 256 and 0 <= y < 256: #Vérifie si l'emplacement est situé dans le carré/l'image de départ, si oui le place, sinon l'ignore.
                
                #Ajoute 1 à x et y pour faire l'arrondissement à l'unité si besoin.
                if y % 1 >= 0.5:
                    y = y + 1
                if x % 1 >= 0.5:
                    x = x + 1
                   
                pix = photo.get(i + 128, j + 128) #Ajoute 128 pour que le centre de rotation soit dans le milieu de l'image.
                t = rvb2hex(pix[0], pix[1], pix[2])#Place les pixels de l'image d'origine dans le nouvelle emplacement sur l'image modifiée  
                photo_modif.put(t, (int(x), int(y))) # Arrondis x et y pour que python puisse les placer.
    photo = photo_modif #Remplace la variable photo pour que python affiche la photo modifée
    
    image_modif = Label(image=photo)
    image_modif.image = photo
    image_modif.grid(row=0, column=4, columnspan=4)
    
    print("rotation")


#256x256 les images pas 512

window = Tk()
photo_base = PhotoImage(file="Lenna.png")
photo_modif = PhotoImage(file="Lenna.png")

image_base = Label(image=photo_base)
image_base.grid(row=0, column=0, columnspan=4)

image_modif = Label(image=photo_modif)
image_modif.grid(row=0, column=4, columnspan=4)

# bouton Changer d'image
"""
Apelle la fonction changer_image qui permet de changer l'image. 
"""
BTNR = Button(window)
BTNR["text"] = "Autre Photo"
BTNR["command"] = changer_image
BTNR.grid(row=1, column=0)

# bouton Photo original
"""
Apelle la fonction originale_image qui permet de remettre l'image de base.
"""
BTNR = Button(window)
BTNR["text"] = "Photo de base"
BTNR["command"] = originale_image
BTNR.grid(row=1, column=1)

# bouton Rouge
BTNR = Button(window)
BTNR["text"] = "Rouge"
BTNR["command"] = composante_rouge
BTNR.grid(row=1, column=2)

# bouton Vert
BTNG = Button(window)
BTNG["text"] = "Vert"
BTNG["command"] = composante_verte
BTNG.grid(row=1, column=3)

# bouton Bleu
BTNB = Button(window)
BTNB["text"] = "Bleu"
BTNB["command"] = composante_bleue
BTNB.grid(row=1, column=4)

# bouton Luminance
BTNL = Button(window)
BTNL["text"] = "Luminance"
BTNL["command"] = luminance
BTNL.grid(row=1, column=5)

# bouton Chrominance1
BTNC1 = Button(window)
BTNC1["text"] = "Chrominance 1"
BTNC1["command"] = chrominance1
BTNC1.grid(row=1, column=6)

# bouton Chrominance2
BTNC2 = Button(window)
BTNC2["text"] = "Chrominance 2"
BTNC2["command"] = chrominance2
BTNC2.grid(row=1, column=7)

# bouton gris
BTNGr = Button(window)
BTNGr["text"] = "Niveau de gris"
BTNGr["command"] = niveau_gris
BTNGr.grid(row=1, column=8)

# bouton augmenter rouge
BTNAr = Button(window)
BTNAr["text"] = "Augmente rouge"
BTNAr["command"] = augmente_rouge
BTNAr.grid(row=2, column=0)

# bouton augmenter luminosité
BTNAl = Button(window)
BTNAl["text"] = "Augmente luminosité"
BTNAl["command"] = augmente_luminosite
BTNAl.grid(row=2, column=1)

# bouton reflexion verticale
BTNRV = Button(window)
BTNRV["text"] = "Réflexion verticale"
BTNRV["command"] = reflexion_verticale
BTNRV.grid(row=2, column=2)

# bouton lissage
BTNLiss = Button(window)
BTNLiss["text"] = "Lissage"
BTNLiss["command"] = lissage
BTNLiss.grid(row=2, column=3)

# bouton augmenter contraste
BTNContraste = Button(window)
BTNContraste["text"] = "Augmenter contraste"
BTNContraste["command"] = augmente_contraste
BTNContraste.grid(row=2, column=4)

# bouton détecter contours
BTNContour = Button(window)
BTNContour["text"] = "Détecter contours"
BTNContour["command"] = detecte_contours
BTNContour.grid(row=2, column=5)

# bouton pavage
BTNPavage = Button(window)
BTNPavage["text"] = "Effet pavage"
BTNPavage["command"] = pavage
BTNPavage.grid(row=2, column=6)

# bouton rotation
BTNRotation = Button(window)
BTNRotation["text"] = "Rotation"
BTNRotation["command"] = rotation
BTNRotation.grid(row=2, column=7)

# bouton quit
BTNQuit = Button(window)
BTNQuit ["text"] = "QUIT"
BTNQuit ["command"] = quit
BTNQuit.grid(row=2, column=8)


mainloop()
