"""Questo modulo gestisce l'app grafica """
import time
import threading
import customtkinter as ctk
from controller.StartAppContoller import StartAppController
from view.MainPage import MainPage


class IngSoftApp(ctk.CTk):
    """rappresenta l'intera applicazione, gestisce la navigazione tra
    le pagine e l'accesso ai dati globali dell'applicazione"""

    def __init__(self, gitv, endpointStatus, run=True):
        """Inizializza l'interfaccia grafica"""

        super().__init__()
        self.edpointStatus = endpointStatus
        self.contoller = StartAppController()
        self.testRepoList = []
        self.pageStack = []
        self.stop = False
        ctk.set_appearance_mode("dark")
        self.title("Ing_soft")
        height = self.winfo_screenheight()
        width = self.winfo_screenwidth()
        height = self.winfo_screenheight()
        width = self.winfo_screenwidth()
        self.geometry(f"{width}x{height}")
        self.minsize(800, 600)
        self.maxsize(1920, 1080)
        self.contoller.getLocalRepoData()
        # Avvia il ciclo principale dell'applicazione
        newPage = MainPage(self, gitv=gitv)
        self.pageStack.append(newPage)
        newPage.place(relwidth=1, relheight=1, rely=0, relx=0)

        def _on_closing():
            """inizia il processo di chiusura in un thread apposito"""
            self.after(100, self._suicide)

            def closeThread():
                """attendi che tutti i thread abbiano concluso il proprio lavoro, dopodichè
                richiedi la chiusura del mainthread settando stop a true
                ps. solo il main thread può gestire se stesso"""
                self.contoller.closeSubProcess()
                for thread in threading.enumerate():
                    if (
                        thread is not threading.main_thread()
                        and thread is not threading.current_thread()
                    ):
                        thread.join()
                self.stop = True

            threading.Thread(target=closeThread).start()

        self.protocol("WM_DELETE_WINDOW", _on_closing)
        if run:
            self.mainloop()

    # ----------------------------- METODI PER LA GESTINE DELLA PAGINA E DEI DATI -----------

    def _suicide(self):
        """Si chiude da solo"""
        if self.stop == True:
            self.quit()
            self.destroy()
        else:
            self.after(100, self._suicide)

    def previousPage(self):
        """ "ritorna alla pagina precedente contenuta nel page stack, utilizza
        un'animazione di sliding"""
        page = self.pageStack[-2]
        page.place(relwidth=1, relheight=1, rely=0, relx=1)
        self._previousPageAnimation(self.pageStack[-1], page, 0)
        old = self.pageStack.pop()
        old.destroy()

    def newPage(self, newPage):
        """passa la schermata ad una nuova pagina, ossia quella passata come parametro
        (è necessario passare il costruttore della pagina come funzione,
        ossia senza parentesi tonde)"""
        page = newPage(self)
        page.place(relwidth=1, relheight=1, rely=0, relx=1)
        self._newPageAnimation(self.pageStack[-1], page, 0)
        self.pageStack[-1].place_forget()
        self.pageStack.append(page)

        # ----------------------------- METODI PER LA GESTIONE DELLA GRAFICA ----------

    def _newPageAnimation(self, leftPage, rigPage, l):
        """utilty function, avvia un'animazione di sliding
        pensta unicamente per essere utilzzata da newpage"""
        while l < 1:
            leftPage.place(relwidth=1, relheight=1, relx=-l)
            rigPage.place(relwidth=1, relheight=1, relx=1 - l)
            l = l + 0.1
            time.sleep(0.01)
            self.update()
        l = 1
        leftPage.place(relwidth=1, relheight=1, rely=0, relx=-l)
        rigPage.place(relwidth=1, relheight=1, rely=0, relx=1 - l)

    def _previousPageAnimation(self, leftPage, rigPage, l):
        """utilty function, avvia un'animazione di sliding
        pensta unicamente per essere utilzzata da previousPage"""
        while l < 1:
            leftPage.place(relwidth=1, relheight=1, relx=l)
            rigPage.place(relwidth=1, relheight=1, relx=-1 + l)
            l = l + 0.1
            time.sleep(0.01)
            self.update()
        l = 1
        leftPage.place(relwidth=1, relheight=1, rely=0, relx=-l)
        rigPage.place(relwidth=1, relheight=1, rely=0, relx=1 - l)

    def toggle_fullscreen(self, event=None):
        """Va in fullscreen"""
        self.attributes("-fullscreen", not self.attributes("-fullscreen"))

    def exit_fullscreen(self, event=None):
        """Esci dalla modalità fullscreen"""
        self.attributes("-fullscreen", False)
