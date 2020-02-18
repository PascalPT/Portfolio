# La racine peut être imprécise à cause du nombre d’itérations. Augmenter les itérations régleraient cela .
#Le GUI fonction si le fichier avec les fonctions est nommé Calculatrice_binaire.py

""" # Sans GUI
def sign():
    s = input('Which operation: +, -, x, ÷, ^, √ ')
    #signe de l.opération
    return(s)"""
#def int_bin(question = 'default question (return integer)'): #Sans GUI
def int_bin(x):   # Avec GUI

    #x = str(input(question)) #Sans GUI
    x = str(x) # Avec GUI
    x = str(x).replace(',','.')
    x = str(x).replace(' ','')
    x = float(x)

    if x < 0 :
        w = str('-')
    else:

        w = ''
    if x < 0:
        x = str(x).split('-')[1]
        x = float(x)
    d = 500
    a = ''
    while d >= -500:
        if x >= 2**d:
            x = x - 2**d
            a = str(a) + str(1)
        elif a != str(''):
            a = str(a)+str(0)
        if d == 0:
            a = str(a) + str('.')
        if x == 0 and d < 0:
            d = -500
        d = d - 1
        
    a = str(w) + str(a)
    
    if a == '':
        a = str(0)
    if a.split('.')[0] == '-':
        a = str('-0.')+ str(a.split('.')[1])
    elif a.split('.')[0] == '' :
        a = str('0.') + str(a.split('.')[1])
    if a.split('.')[1] == '':
        a = str(a.split('.')[0]) + str('.0')
        
    return(a)

def bin_int(e):
    
    w = e.find('-')
    l = len(e.split('.')[0])
    ld = -1 * len(e.split('.')[1])
    d = l-1 #L
    c = 0
    e = e.split('.')[0] + e.split('.')[1]
    for i in range (l-ld):
        if e[i] == '1':
            c = c + 2**d
        d = d - 1  
    if w == 0:
        c = str('-') + str(c)
    
    return(c)

def add(a, b):
    zf = ''
    if a.find('-') != b.find('-'):
        if a.find('-') == 0:
            z = sub(a.split('-')[1],b)
            if z.find('-') == 0:
                z = z.replace('-','')
                w = ''
            elif z.find('1') == -1:
                w = ''
            else:
                w = str('-')
        else:
            z = sub(a,b.split('-')[1])
            w = ''            
        zf = str(z)
    elif a.find('-') == 0:
        w = '-'
    else:
        w = ''
    
    for i in range (2):
        while len(a.split('.')[i]) > len(b.split('.')[i]):
            b = (1-i)*str(0) + str(b) + (i)*str(0)
        while len(a.split('.')[i]) < len(b.split('.')[i]):
            a = (1-i)*str(0) + str(a) + (i)*str(0)

    m = len(b.split('.')[1])        
    a = a.split('.')[0] + a.split('.')[1]
    n = len(a)
    b = b.split('.')[0] + b.split('.')[1]
    z = ''
    r = 0
    while n > 0 and zf == '':
        if a[n-1] == '1' and b[n-1] == '1': 
            if r == 1: 
                z = str(1) + str(z)
                r = 1
            else: 
                z = str(0) + str(z)
                r = 1
        elif a[n-1] == '1' or b[n-1] == '1': 
            if r == 1: 
                z = str(0) + str(z)
                r = 1
            else: 
                z = str(1) + str(z)
                r = 0
        else:
            if r == 1: 
                z = str(1) + str(z)
                r = 0
            else: 
                z = str(0) + str(z)
                r = 0
        n = n - 1
    if r == 1:
        z = str(1) + str(z)
        r = 0

    for i in range (len(z)):
        zf = str(zf) + str(z[i])
        if i == len(z)-1-m:
            zf = str(zf) + str('.')
    z = str(w)+str(zf)
    zf = ''
    
    return(z)

def mul(a, b):
    
    w = ''
    if a.find('-') != b.find('-'):
        w = str('-')
        if a.find('-') == 0:
            a = a.split('-')[1]
        else:
            b = b.split('-')[1]
    elif a.find('-') == 0:
        a = a.split('-')[1]
        b = b.split('-')[1]
        

    for i in range (2):
        while len(a.split('.')[i]) > len(b.split('.')[i]):
            b = (1-i)*str(0) + str(b) + (i)*str(0)
        while len(a.split('.')[i]) < len(b.split('.')[i]):
            a = (1-i)*str(0) + str(a) + (i)*str(0)

    n = len(b.split('.')[1])
    a = a.split('.')[0] + a.split('.')[1]
    b = b.split('.')[0] + b.split('.')[1]
    m = len(a)
    y = ''
    yf = ''
    p = ''
    q = 0
    while m > 0:
        if b[m-1] == '1':
            if y == '':
                y = str(a) + q * str(0)
            else:
                p = str(a) + q * str(0)
                y = add(str(y)+str(".0"), str(p)+str(".0"))
                y = y.split('.')[0]
        q = q + 1
        m = m - 1
    if y == '':
        y = str(0.0)
    y = y.split('.')[0]

    while  len(y)-1-2*n < 0:
        y = str(0)+str(y)        
    for i in range (len(y)):
        yf = str(yf) + str(y[i])
        if i == len(y)-1-2*n:
            yf = str(yf) + str('.')
    y = str(yf)
    yf = ''

    
    while y[0] == '0':
        for i in range (len(y)-1):
            yf = yf + y[i+1]
        y = yf
        yf = ''
    while y[-len(y)] == '0':
        for i in range (-len(y)+1):
            yf = yf + y[-i-2]
        y = yf
        yf = ''

    while y[0] == '0':
        for i in range (len(y.split('.')[0])-1):
            yf = yf + y[i+1]
        y = yf + str('.') + y.split('.')[1]
        yf = ''
    if y.split('.')[0] == '':
        y = str('0') + str(y)

    while (y[-1]) == '0':
        for i in range (len(y.split('.')[1])-1):
            yf = yf + y[-i-1]
        y = y.split('.')[0] + str('.') + yf
        yf = ''
    
    if y.split('.')[1] == '':
        y = str(y) + str('0')

    y = str(w) + str(y)
    
    return(y)

def sub(a, b):

    w =''    
    if a.find('-') != b.find('-'):
        if a.find('-') == 0:
            w = str('-')
            z = add((a.split('-')[1]),b)
        else:
            w = str('')
            z = add(b.split('-')[1],a)
    elif a.find('-') == 0:
        w = str('-')
        a = a.split('-')[1]
        b = b.split('-')[1]
        z =''
    else :
        z = ''

    for i in range (2):
        while len(a.split('.')[i]) > len(b.split('.')[i]):
            b = (1-i)*str(0) + str(b) + (i)*str(0)
        while len(a.split('.')[i]) < len(b.split('.')[i]):
            a = (1-i)*str(0) + str(a) + (i)*str(0)
              
    aI = str(a)
    bI = str(b)
    m = len(b.split('.')[1])
    a = a.split('.')[0] + a.split('.')[1]
    b = b.split('.')[0] + b.split('.')[1]   
    n = len(a)
    
    zf = ''
    r = 0
    if z != '':
        n = 0
    while n > 0:
        if (a[-n] == b[-n]):
            z = str(z) +str(0)
        elif (a[-(n)] == '1' and b[-(n)] == '0'): 
            z = str(z) + str(1)
        elif a[-(n)] == '0' and b[-(n)] == '1':
            r = -1
            i = 0
            while r == -1 and i < len(z):
                r = z.find('1',len(z)-1-i,len(z)-i)
                i = i + 1
            for i in range (r+1):
                if i < r:
                    zf = str(zf) + str(z[i])
                elif i == r:
                    zf = str(zf) + str(0) + (len(z)-r)*str(1)
                    z = str(zf)
                    zf = ''
            if r == -1:
                n = 0
                z = sub(bI,aI)
                if w == str('-'):
                    w = ''
                else:
                    w = str('-')
        n = n - 1
        
    if z.find('1') == -1:
        w = ''
    if z.find('.') != -1:
        z = str(z)
    else:
        for i in range (len(z)):
            zf = str(zf) + str(z[i])
            if i == len(z)-1-m:
                zf = str(zf) + str('.')
        z = str(zf)
        zf = ''

    
    while z[0] == '0':
        for i in range (len(z.split('.')[0])-1):
            zf = zf + z[i+1]
        z = zf + str('.') + z.split('.')[1]
        zf = ''
    if z.split('.')[0] == '':
        z = str('0') + str(z)

    while (z[-1]) == '0':
        for i in range (len(z.split('.')[1])-1):
            zf = zf + z[-i-1]
        z = z.split('.')[0] + str('.') + zf
        zf = ''
    
    if z.split('.')[1] == '':
        z = str(z) + str('0')

    z = str(w) + str(z)
    
    return(z)

def div(a, b):
    w = ''
    if a.find('-') != b.find('-'):                                              
        w = '-'
        if a.find('-')== 0:
            a = a.split('-')[1]
        else:
            b = b.split('-')[1]
    elif a.find('-') == 0:
        a = a.split('-')[1]
        b = b.split('-')[1]
        
    d = b.split('.')[0]
    b = b.split('.')[0]+b.split('.')[1] + str(0) * ( len(a.split('.')[0])-1) + str('.0')    
    e = len(b) - 4
    
    y = ''
    yf = ''
    m = 0
    while m < 65:         
        z = sub(a,b)
        if z.find('-')== -1:
            a = str(z)
            y = str(y)+ str(1)
        elif y != '' or (a.find('1') == -1 and y != ''):
            y = str(y) + str(0)
        bf = ''
        if b.split('.')[0] == str(d):
                y = str(y) + str('.')
        b = b.split('.')[0] + b.split('.')[1]
        for i in range (len(b)):
            bf = str(bf)+str(b[i])
            if i == e:
                bf = str(bf)+str('.')
                e = e - 1
        b = str(bf)
        if a.find('1') == -1 and y.find('.') != -1:
            m = 65
        if b.find('.') == -1:
            b = str('0.')+str(b)
        m = m + 1

    if y == '':
        y = '0.0'
    if y.find('.') != -1:
        if y.split('.')[1] == '':
            y = str(y)+str('0')
        y = str(y)

    while y[0] == '0':
        for i in range (len(y)-1):
            yf = yf + y[i+1]
        y = yf
        yf = ''
    while y[-len(y)] == '0':
        for i in range (-len(y)+1):
            yf = yf + y[-i-2]
        y = yf
        yf = ''

    while y[0] == '0':
        for i in range (len(y.split('.')[0])-1):
            yf = yf + y[i+1]
        y = yf + str('.') + y.split('.')[1]
        yf = ''
    if y.split('.')[0] == '':
        y = str('0') + str(y)

    while (y[-1]) == '0':
        for i in range (len(y.split('.')[1])-1):
            yf = yf + y[-i-1]
        y = y.split('.')[0] + str('.') + yf
        yf = ''
    
    if y.split('.')[1] == '':
        y = str(y) + str('0')

    y = str(w) + str(y)
    
    return(y)

def rac(a, b):
    m = 0
    y1 = ''
    y = add(sub(b,'1.0'),div(a,b))

    while  m < 30 and y1 != y:
        y1 = str(y)
        y = div(add(mul(sub(b,'1.0'),y),div(a,exp(y,sub(b,'1.0')))),b)
        m = m +1
    return (y)

def exp (a,b):
    
    if a.find('-') == 0:
        a = a.split('-')[1]
        w = str('-')
    else:
        w = ''
    A = str(a)
    c = '0'
    y = '1.0'

    while b.find('1') != -1:
        if b.find('-') == -1:
            b = sub(b,'1.0')
        else:
            b = add(b,'1.0')
            c = '1'
        y = A            
        A = mul(A,a)
    if c =='1':
        y = div('1.0',y)
    y = str(w) + str(y)
    return(y)

# Avec Gui laissez ceci en commentaire
"""
while True:
    a = int_bin('Give an integer: ')
    print('Your integer in binary is: ' + a)
    s = sign()
    print('Your operation is: ' + s)
    b = int_bin('Give another integer: ')
    print('Your integer in binary is: ' + b)
    if s == '+':
        z = add(a, b)
        print('The result of the addition in binary is: ' + z)
        c = bin_int(z)
        print('The result of the addition in decimal is: ' + str(c))
    elif s == '-':
        x = sub(a, b)
        print('The result of the substraction in binary is: ' + x)
        c = bin_int(x)
        print('The result of the substraction in decimal is: ' + str(c))
    elif s == 'x' or s =='*':
        y = mul(a, b)
        print('The result of the multiplication in binary is: ' + y)
        c = bin_int(y)
        print('The result of the multiplication in decimal is: ' + str(c))
    elif s == '÷' or s == '/':
        w = div(a, b)
        print('The result of the division in binary is: ' + w)
        c = bin_int(w)
        print('The result of the division in decimal is: ' + str(c))
    elif s == '√' or s == 'r':
        w = rac(a, b)
        print('The result of the racine in binary is: ' + w)
        c = bin_int(w)
        print('The result of the racine in decimal is: ' + str(c))
    elif s == '^' or s == 'e':
        w = exp(a, b)
        print('The result of the exposant in binary is: ' + w)
        c = bin_int(w)
        print('The result of the exposant in decimal is: ' + str(c))

    continue
"""

