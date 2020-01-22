import cmath
import PIL
from PIL import Image

global valeur_pas_claire_de_départ

valeur_pas_claire_de_départ = 0
""" À changer pour -1, si l'image finale n'est pas celle attendue, mais le cercle rouge de l'ensemble
de Julia et de Mandelbrot devrait être exactement le même vue qu'il est à la limite de 2 de distance avec
(0,0). Pour obtenir la même image qu'en exemple pour Julia la valeur de départ devrait être -1."""

def rvb2hex(r,v,b):
    hex = "#{:02x}{:02x}{:02x}".format(r,v,b)
    return hex 

def matrice_nulle(nb_lig, nb_col):
    A = [[0 for x in range(nb_col)] for y in range(nb_lig)]
    return A

def evalue_couleur(z , c):
    for i in range(valeur_pas_claire_de_départ,73):
        """Évalue la distance entre un point z et (0;0). Si la distance est de moins
        de 2, alors z devient z**2+c. Si la distance est de plus de 2, assigne des valeurs
        à une matrice de couleur r,v,b -> p dépendamment du nombre d'itérations nécessaires
        pour dépasser 2 de distance. La fonctionne retourne la matrice p."""
        if abs(z) > 2 or i == 72:
            if i < 1:
                p = (0,0,0)
            elif i < 11:
                p = (255,0,0)
            elif i < 16:
                p = (0,255,0)
            elif i < 21:
                p = (0,0,255)
            elif i < 26:
                p = (0,255,255)
            elif i < 31:
                p = (255,0,255)
            elif i < 36:
                p = (255,255,0)
            elif i < 41:
                p = (25,25,25)
            elif i < 46:
                p = (100,100,0)
            elif i < 51:
                p = (0,100,100)
            elif i < 56:
                p = (100,0,100)
            elif i < 61:
                p = (0,0,100)
            elif i < 66:
                p = (0,100,0)
            elif i < 71:
                p = (100,0,0)
            else:
                p = (255,255,255)
            break
        z = z ** 2 + c
    return p


def julia(l, c):
    
    """ Assigne la valeur de base pour le coin en haut à gauche et le zoom de l'image."""
    z = complex(-2, 2)
    t = 4
    
    if l != c:
        """ l et c ne devraient être différent que lorsque la fonction zoom est utilisée. Celle-ci,
        transmet le nouveau z (coin) en utilisant c et assemble la largeur (résolution) et la taille
        ensemble en créant un nombre complexe avec les 2. Pour les extraire, l est transformé en string
        de texte et les valeurs pour l et t sont, alors, extraites. Par la suite, les valeurs sont assignées
        aux bonnes variables."""
        ltmp = int(str(l).split('+')[0][1::])
        t = float(str(l).split('+')[1].split('j')[0])
        l = ltmp
        z = c
        c = l #L

    """Création de l'image qui sera modifiée selon les résultats de l'évaluation de la couleur
    pour un point donné. Celle-ci sera créée en format rvb, car evalue_couleur utilise ce format."""     
    image = Image.new('RGB',(l,c))

    """ Création des variables correspondants à la distance en x et y entre chaque pixel."""
    xp = t/l #L minuscule
    ym = complex(0, t/c)


    """Parcours toute l'image de gauche à droite et de haut vers le bas. zo est modifié pour être de
    la valeur du point/pixel et à chacun de ces points/pixels utilise la fonction evalue_couleur pour
    déterminer la couleur du pixel, puis ce pixel est placé dans l'image."""  
    for i in range (0,l): #L minuscule
        for k in range (0,c):
            zo = z+xp*i-ym*k
            pix = evalue_couleur(zo,(-0.8 + 0.156j))
            image.putpixel((i,k), pix)

    """Enregistre l'image en format PNG qui sera ouverte dans la fenêtre."""
    image.save("image.png","PNG")


def mandelbrot(l, c):
    
    """ Assigne la valeur de base pour le coin en haut à gauche et le zoom de l'image."""
    z = complex(-2, 2)
    t = 4

    if l != c:
        """ l et c ne devraient être différent que lorsque la fonction zoom est utilisée. Celle-ci,
        transmet le nouveau z (coin) en utilisant c et assemble la largeur (résolution) et la taille
        ensemble en créant un nombre complexe avec les 2. Pour les extraire, l est transformé en string
        de texte et les valeurs pour l et t sont, alors extraites. Par la suite, les valeurs sont assignées
        aux bonnes variables."""
        ltmp = int(str(l).split('+')[0][1::])
        t = float(str(l).split('+')[1].split('j')[0])
        l = ltmp
        z = c
        c = l #L
        
    """Création de l'image qui sera modifiée selon les résultats de l'évaluation de la couleur
    pour un point donné. Celle-ci sera créée en format rvb, car evalue_couleur utilise ce format.""" 
    image = Image.new('RGB',(l,c))

    """ Création des variables correspondants à la distance en x et y entre chaque pixel."""
    xp = t/l #L minuscule
    ym = complex(0, t/c)

    """Parcours toute l'image de gauche à droite et de haut vers le bas. zo est modifié pour être de
    la valeur du point/pixel et à chacun de ces points/pixels utilise la fonction evalue_couleur pour
    déterminer la couleur du pixel, puis ce pixel est placé dans l'image."""  
    for i in range (0,l): #L minuscule
        for k in range (0,c):
            ztemp = z+xp*i-ym*k
            zo = ztemp

            if valeur_pas_claire_de_départ == -1:
                """Le if s'assure simplement que l'image transmise pour mandelbrot soit la même peut importe la valeur """
                zo = 0              

            pix = evalue_couleur(zo,ztemp)
            image.putpixel((i,k), pix)

    """Enregistre l'image en format PNG qui sera ouverte dans la fenêtre."""
    image.save("image.png","PNG")



def zoom(l, c, x, y, t, e):

    """Calcul le nouveau z qui correspond au nouveau coin en haut à gauche."""
    z = complex(x - t/2, y + t/2)

    """Assemble l et t ensemble en nombre complex pour être séparés plus tard dans les fonctions qui seront appelées."""
    l = complex(l, t)

    """Appelle les fonctions dépendamment de l'ensemble demandé."""
    if e == 'J':
        julia(l,z)
    elif e == 'M':
        mandelbrot(l,z)
