import cmath

def rvb2hex(r,v,b):
    hex = "#{:02x}{:02x}{:02x}".format(r,v,b)
    return hex 


def matrice_nulle(nb_lig, nb_col):
    A = [[0 for x in range(nb_col)] for y in range(nb_lig)]
    return A


def evalue_couleur(z, c):

    for i in range(-1,73):
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
        
    return p[0],p[1],p[2]


def julia(l, c):
    z = -2 + 2j
    t = 4
    
    if l != c:
        ltmp = int(str(l).split('+')[0][1::])
        t = float(str(l).split('+')[1].split('j')[0])
        l = ltmp
        z = c
        c = l #L
    
    pixels = matrice_nulle(l, c)
    xp = t/l
    ym = complex(0, t/c)
    for i in range(l):
        for k in range(c):
            pix = evalue_couleur((z+xp*i-ym*k),(-0.8 + 0.156j)) #C fixé
            pixels[i][k]=rvb2hex(pix[0],pix[1],pix[2])
    
    return pixels



def mandelbrot(l, c):    
    z = -2 + 2j
    t = 4

    if l != c:
        ltmp = int(str(l).split('+')[0][1::])
        t = float(str(l).split('+')[1].split('j')[0])
        l = ltmp
        z = c
        c = l #L
    
    pixels = matrice_nulle(l, c)
    xp = t/l
    ym = complex(0, t/c)
    for i in range(l):
        for k in range(c):
            ztmp = z+xp*i-ym*k 
            pix = evalue_couleur((0),(ztmp))
            pixels[i][k]=rvb2hex(pix[0],pix[1],pix[2])
    
    return pixels



def zoom(l, c, x, y, t, e):

    z = complex(x - t/2, y + t/2)
    l = complex(l, t)
    if e == 'J':
        pixels = julia(l,z)
    elif e == 'M':
        pixels = mandelbrot(l,z)
    
    return pixels


