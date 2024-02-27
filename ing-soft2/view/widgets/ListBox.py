"""Widget per le liste"""
import customtkinter as ctk

class ListBox(ctk.CTkScrollableFrame):
    """ classe che rappresenta una lista scrollabile di elementi che possono
    essere aggiunti dinamicamente"""
    def __init__(self, master):
        """Inizializza la classe ListBox"""
        super().__init__(master= master)
        self.childList = []

    def addBox(self, text: str, author:str ,command = None):
        """  aggiunge un elemento alla lista """
        newbox = self._ListItem(self, text, author, command = command)
        self.childList.append(newbox)
        newbox.pack(fill = ctk.X, expand = True, pady = 1)

    def cleanList(self):
        """ rimuove tutti gli elementi dalla lista """
        for child in self.childList:
            child.destroy()
        self.childList= []

    class _ListItem(ctk.CTkFrame):
        """ classe che rappresenta la lista """
        def __init__(self, master: any, title: str, author, command = None):
            """Inizializza la classe ListItem"""
            super().__init__(master = master, height= 40)
            self.configure(fg_color="#1d1e1e")
            my_font = ctk.CTkFont( weight= "bold", size=16)
            label = ctk.CTkLabel(self, text= title, font= my_font)
            label.grid(row= 0, column= 0, padx = 10, sticky = "w")
            my_font2 = ctk.CTkFont(size=13)
            self.label2 = ctk.CTkLabel(self, text= author , font= my_font2)
            self.label2.configure(fg_color= "#1d1e1e", bg_color= "#1d1e1e" )
            self.label2.grid(row= 0, column= 1, padx= 10, pady= 2)
            self.bind(sequence= "<Enter>", command= self.on_enter)
            self.bind(sequence= "<Leave>", command= self.on_leave)
            self.bind(sequence= "<Button-1>", command = command)
            self.label2.bind(sequence= "<Enter>", command= self.on_enter)
            self.label2.bind(sequence= "<Leave>", command= self.on_leave)
            self.label2.bind(sequence= "<Button-1>", command = command)

        def on_enter(self, event):
            """All'entrata"""
            self.label2.configure(fg_color="#847F7C")
            self.configure(fg_color="#847F7C")
            event.widget.configure(cursor="hand2")

        def on_leave(self, event):
            """All'uscita"""
            self.label2.configure(fg_color="#1d1e1e")
            self.configure(fg_color="#1d1e1e")
            event.widget.configure(cursor="arrow")
