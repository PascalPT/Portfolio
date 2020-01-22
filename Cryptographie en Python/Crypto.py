def format(txt):
    
    "1 Normaliser le texte en retirant les accents"    
    import unicodedata
    txt = unicodedata.normalize('NFD', txt).encode('ascii', 'ignore').decode("utf-8")
    #Normaliser le texte en format NFD ( lettre en format code 8-bit suivie du code 8-bit de l’accent, cédille, etc.),puis encodé en
    #format ascii (lettre transformer en leur code 7-bit et on ignore les éléments inconnus de la table ascii comme les codes pour les accents),
    #puis en réencode en format  utf-8 (8-bit), car python utilise ce format pour la gestion de textes.

    "2 Retirer les caractères spéciaux"
    txtf=txt #Création de la variable temporaire qui sera éditée durant la boucle
    txt_enleve = "" 

    #Boucle retirant les caractères spéciaux
    for i in range (0,len(txt)):
        c=ord(txt[i])
        if c < 65:
           txt_enleve = txt_enleve + txt[i]
           b=txt[i]
           txtf = txtf.replace(b,'')
        elif 90 < c and c < 97:
           txt_enleve = txt_enleve + txt[i]
           b=txt[i]
           txtf = txtf.replace(b,'')
        elif  c > 122:
           txt_enleve = txt_enleve + txt[i]
           b=txt[i]
           txtf = txtf.replace(b,'')

    "3 Mettre en minuscule"
    txt=txtf.lower()   
    
    return txt, txt_enleve
    

def cesar(txt):

    #Avancer les lettres de 3 positions (ou reculer de 23 si x,y ou z)
    txt_code=''
    a=len(txt)
    for i in range (0,a):
        c=ord(txt[i])
        if  96 < c and c < 120:
            txt_code =txt_code + chr(c+3)
        elif 120 <= c and c < 123:
            txt_code = txt_code + chr(c-23)
        else :
            txt_code=txt_code+txt[i]
    return txt_code


def vigenere(txt, cle):
    
    "1 Formater cle pour retirer les caractères spéciaux en utilisant format()"
    cle=format(cle)[0]
    txt_code=''
    
    #position de la lettre dans cle
    b = 0

    #Si cle est vide pour éviter de casser le programme -> cle = "a"
    if cle == '':
        cle='a'

    """2 Boucle ajoutant le code (ascii) à la lettre à la position i et qui crée un nouvelle variable pour stocker cette lettre
    Ensuite si le code ascii ne correspond plus à une lettre retirer 26 au code pour faire boucler vers 'a'.
    Créer une chaîne de caractère avec les codes asciis des lettres modifiées."""
    
    for i in range (0,len(txt)):
        ajout=ord(cle[b])-97
        letter_i = ord(txt[i])+ajout
        if letter_i > 122:
            letter_i=letter_i-26
        b = b+1
        if b > len(cle)-1:
            b=0

        txt_code = txt_code+chr(letter_i)   
   
    return txt_code
