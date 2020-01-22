from tkinter import *
from tkinter import messagebox
import Calculatrice_Binaire

class Application(Frame):

    def Calcul(self) :

        x = self.PN.get()
        PNB_txt = Calculatrice_Binaire.int_bin(x)
        self.PNB_txt.set(PNB_txt)
        
        x = self.DN.get()
        DNB_txt = Calculatrice_Binaire.int_bin(x)
        self.DNB_txt.set(DNB_txt)
        
        a = self.PNB.get()
        b = self.DNB.get()
        
        if (self.radioBtn.get() == '1') :
            RPB_txt = Calculatrice_Binaire.add(a,b)
        elif (self.radioBtn.get() == '2') :
            RPB_txt = Calculatrice_Binaire.sub(a,b)
        elif (self.radioBtn.get() == '3') :
            RPB_txt = Calculatrice_Binaire.mul(a,b)
        elif (self.radioBtn.get() == '4') :
            RPB_txt = Calculatrice_Binaire.div(a,b)
        elif (self.radioBtn.get() == '5') :
            RPB_txt = Calculatrice_Binaire.rac(a,b)
        else :
            RPB_txt = Calculatrice_Binaire.exp(a,b)
        self.RPB_txt.set(RPB_txt)

        RP_txt = Calculatrice_Binaire.bin_int(RPB_txt)
        self.RP_txt.set(RP_txt)

    def Binaire(self) :

        x = self.PN.get()
        PNB_txt = Calculatrice_Binaire.int_bin(x)
        self.PNB_txt.set(PNB_txt)
        
        x = self.DN.get()
        DNB_txt = Calculatrice_Binaire.int_bin(x)
        self.DNB_txt.set(DNB_txt)

    def createWidgets(self):
        WIDTH, HEIGHT = 1280, 960

        # Premier Nombre
        self.lblPN = Label(self, text="Premier Nombre")
        self.lblPN.grid(row=0, column=0)
        # Binaire 1
        self.lblPNB = Label(self, text="Binaire 1")
        self.lblPNB.grid(row=1, column=0)
        # Deuxieme Nombre
        self.lblDN = Label(self, text="Deuxieme Nombre")
        self.lblDN.grid(row=2, column=0)
        # Binaire 2
        self.lblDNB = Label(self, text="Binaire 2")
        self.lblDNB.grid(row=3, column=0)
        # Opération
        self.lblO = Label(self, text="Opération")
        self.lblO.grid(row=4, column=0)
        # Réponse 
        self.lblR = Label(self, text="Réponse")
        self.lblR.grid(row=5, column=0)
        # Réponse Binaire
        self.lblRB = Label(self, text="Réponse en Binaire")
        self.lblRB.grid(row=6, column=0)

        # Différentes boites pour les nombres de l'utilisateur, en binaire et les réponses

        
        self.PN = StringVar()
        self.PN.set("0")
        self.PN = Entry(self, textvariable=self.PN, width=100)
        self.PN.grid(row=0, column=1, columnspan=6)
        
        self.PNB_txt = StringVar()
        self.PNB_txt.set("0")
        self.PNB = Entry(self, textvariable=self.PNB_txt, width=100)
        self.PNB.grid(row=1, column=1, columnspan=6)
        self.PNB.config(state=DISABLED)

        self.DN = StringVar()
        self.DN.set("0")
        self.DN = Entry(self, textvariable=self.DN, width=100)
        self.DN.grid(row=2, column=1, columnspan=6)

        self.DNB_txt = StringVar() 
        self.DNB_txt.set("0")
        self.DNB = Entry(self, textvariable=self.DNB_txt, width=100)
        self.DNB.grid(row=3, column=1, columnspan=6)
        self.DNB.config(state=DISABLED)
        
        self.RP_txt = StringVar()
        self.RP_txt.set("0")
        self.R = Entry(self, textvariable=self.RP_txt, width=100)
        self.R.grid(row=5, column=1, columnspan=6)
        self.R.config(state=DISABLED)

        self.RPB_txt = StringVar()
        self.RPB_txt.set("0")
        self.RB = Entry(self, textvariable=self.RPB_txt, width=100)
        self.RB.grid(row=6, column=1, columnspan=6)
        #self.RB.config(state=DISABLED)

       

        # radio choix Opération
        self.radioBtn = StringVar()
        self.RADIO1 = Radiobutton(self, text="Addition", variable=self.radioBtn, value=1)
        self.RADIO2 = Radiobutton(self, text="Soustraction", variable=self.radioBtn, value=2)
        self.RADIO3 = Radiobutton(self, text="Multiplication", variable=self.radioBtn, value=3)
        self.RADIO4 = Radiobutton(self, text="Division", variable=self.radioBtn, value=4)
        self.RADIO5 = Radiobutton(self, text="Racine", variable=self.radioBtn, value=5)
        self.RADIO6 = Radiobutton(self, text="Exposant", variable=self.radioBtn, value=6)
        self.RADIO1.grid(row=4, column=1)
        self.RADIO2.grid(row=4, column=2)
        self.RADIO3.grid(row=4, column=3)
        self.RADIO4.grid(row=4, column=4)
        self.RADIO5.grid(row=4, column=5)
        self.RADIO6.grid(row=4, column=6)
        self.radioBtn.set(1)
		
        # Button Binaire
        self.BINAIRE = Button(self)
        self.BINAIRE["text"] = "Binaire"
        self.BINAIRE["command"] = self.Binaire
        self.BINAIRE.grid(row=8, column=2)

        # Button Calculer
        self.CALCUL = Button(self)
        self.CALCUL["text"] = "Calculer"
        self.CALCUL["command"] = self.Calcul
        self.CALCUL.grid(row=8, column=3)


        # Button quit
        self.QUIT = Button(self)
        self.QUIT["text"] = "Quitter"
        self.QUIT["command"] = root.destroy
        self.QUIT.grid(row=8, column=6)


        


    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.pack()
        self.createWidgets()

root = Tk()
root.title("Calculatrice")
app = Application(master=root)
app.mainloop()
