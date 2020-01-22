from tkinter import *
from tkinter import messagebox
import Crypto

class Application(Frame):

    def encodage(self):
        if(self.radioBtn.get() == '1') :
            self.cesar()
        else :
            self.vigenere(self.MOTCLE.get())

    def format(self) :
        txt = self.txt_clair.get()
        txt_format, txt_enleve = Crypto.format(txt)
        messagebox.showinfo("Formatage", "Texte enlevé : " + txt_enleve)
        self.txt_clair.set(txt_format)
        
    def cesar(self) :
        txt = self.txt_clair.get()
        txt_code = Crypto.cesar(txt)
        self.txt_code.set(txt_code)

    def vigenere(self, cle) :
        txt = self.txt_clair.get()
        txt_code = Crypto.vigenere(txt, cle)
        self.txt_code.set(txt_code)


    def createWidgets(self):
        WIDTH, HEIGHT = 640, 480

        # label clair
        self.lblCLAIR = Label(self, text="TEXTE CLAIR")
        self.lblCLAIR.grid(row=0, column=0)

        # input clair
        self.txt_clair = StringVar()
        self.txt_clair.set("onattaquedemain")
        self.CLAIR = Entry(self, textvariable=self.txt_clair, width=100)
        self.CLAIR.grid(row=1, column=0, columnspan=4)

        # label output
        self.lblENCODE = Label(self, text="TEXTE CODÉ")
        self.lblENCODE.grid(row=5, column=0)

        # output code
        self.txt_code = StringVar()
        self.txt_code.set("Texte code")
        self.ENCODE = Entry(self, textvariable=self.txt_code, width=100)
        self.ENCODE.grid(row=6, column=0, columnspan=4)

        # label mot-cle
        self.lblMOTCLE = Label(self, text="mot clé de 4 lettres pour Vigenère : ")
        self.lblMOTCLE.grid(row=2, column=0)

        # input mot-cle
        self.MOTCLE = Entry(self, width=20)
        self.MOTCLE.grid(row=2, column=1)

        # label methode
        self.lblRADIO = Label(self, text="Méthode : ")
        self.lblRADIO.grid(row=3, column=0)

        # radio choix methode
        self.radioBtn = StringVar()
        self.RADIO1 = Radiobutton(self, text="César", variable=self.radioBtn, value=1)
        self.RADIO2 = Radiobutton(self, text="Vigenère", variable=self.radioBtn, value=2)
        self.RADIO1.grid(row=3, column=1)
        self.RADIO2.grid(row=3, column=2)
        self.radioBtn.set(1)
		
        # bouton formatage
        self.FORMAT = Button(self)
        self.FORMAT["text"] = "Formater"
        self.FORMAT["command"] = self.format
        self.FORMAT.grid(row=8, column=0)

        # bouton codage
        self.ENCODER = Button(self)
        self.ENCODER["text"] = "Coder avec la méthode choisie"
        self.ENCODER["command"] = self.encodage
        self.ENCODER.grid(row=8, column=1)

        # bouton quit
        self.QUIT = Button(self)
        self.QUIT["text"] = "Quitter"
        self.QUIT["command"] = root.destroy
        self.QUIT.grid(row=8, column=2)


    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.pack()
        self.createWidgets()

root = Tk()
root.title("TP1")
app = Application(master=root)
app.mainloop()

