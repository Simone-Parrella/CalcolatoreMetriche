"""Modulo per la gestione della pagina principale"""

import os
import tkinter as tk
from tkinter import font
from typing import List
import time
import threading
import customtkinter as ctk
from model.Domain import Repository
from controller.mainPageContoller import MainPageController
from view.widgets.LoadingIcon import RotatingIcon
from view.ProjectMetricsPage import ProjectMetricsPage
from view.widgets.SideButton import SideButton
from .widgets.ListBox import ListBox


class MainPage(ctk.CTkFrame):
    """ main page dell'app """

    def __init__(self, master, gitv):
        """Inizializza MainPage"""
        self.loading = False
        self.controller = MainPageController()
        self.text = tk.StringVar()
        self.master = master
        self.testRepoList = []
        self.pageStack = []
        super().__init__(master=master)
        ctk.set_appearance_mode("dark")
        self._initSearchBlock()
        # inizializza la lista a centro pagina
        self.centralbox = ctk.CTkFrame(self)
        self.centralbox.pack(fill=ctk.BOTH, expand=True)
        self.listBox = ListBox(self.centralbox)
        self.listBox.pack(padx=10, pady= 40, fill=ctk.BOTH, expand=True)
        # inizializza il frame di status di git (barra in basso)
        self.gitStatusFrame = tk.Frame(self, height=15)
        self.gitStatusFrame.config(bg="#1d1e1e")
        self.gitStatusFrame.pack(fill="x")
        f = font.Font(size=7)
        self.gitStatusLabel = tk.Label(self.gitStatusFrame, text=gitv,
                                        background="#1d1e1e", foreground="white", font=f)
        self.gitStatusLabel.place(x=5, y=0)
        self.testRepoList = []
        self._initRepoData()
        if self.controller.getRepoData() is None:
            self.sideB.place_forget()
        else:
            self.sideB.place(y=10, relx=0.9)

    # -----------------------------GUI management -----------------------------
    def _initSearchBlock(self):
        """ inizializza la sezione con il form di ricerca """
        # inizializza il modulo a centro pagina
        my_font = ctk.CTkFont(family="Arial black", size=25)
        label = ctk.CTkLabel(self, text="Search for a repo ", width=10, font=my_font)
        label.pack(side=ctk.TOP, pady=10)
        self.entry = ctk.CTkEntry(self, width=400)
        self.entry.pack()
        # inizializza il bottone laterale
        searchBut = ctk.CTkButton(self, text="Search", command=self._start_request)
        searchBut.pack(pady=10)
        self.sideB = SideButton(self.master, self.onSideButtonPress, ProjectMetricsPage)
        # finalizza inizializzazione del modulo di centro pagina
        font = ("Arial black", 12)
        self.messageBox = tk.Frame(self)
        self.messageBox.configure(bg="#1d1e1e")
        self.messageBox.pack(fill="x")
        self.message = tk.Label(self.messageBox, textvariable=self.text,
                                background="#1d1e1e", foreground="#FFFFFF")
        self.message.config(font=font)
        self.message.pack()
        """Sistemazione dell'icona del s.o."""
        icon_filename = "rotationLoading.png"
        resources_directory = "resources"
        icon_path = os.path.join(resources_directory, icon_filename)
        self.icon = RotatingIcon(self.messageBox, iconPath=icon_path,
                                 backgroundColor="#1d1e1e")

    def showMessage(self, msg):
        """ modifica il messaggio visualizzato """
        self.text.set(msg)

    def _start_request(self):
        """Avvia richiesta"""
        self.listBox.cleanList()
        self.controller.request_for_repos(self.entry.get(), self._updateRepoList)

    def _recoverRepoData(self):
        """Rimuovi repo data"""
        self.controller.requestRepoUpdate(self.beforeRepoDataUpdate,
                                          self.afterRepoDataUpdate)

    def _initRepoData(self):
        """Inizializza repo data"""
        self.showMessage("we are initializing repo data")
        self.loading = True
        self._recoverRepoData()

    # ----------------------------- callbacks -----------------------------
    def onSideButtonPress(self, param):
        """Click bottone"""
        self.listBox.cleanList()
        self.master.newPage(param)

    def _updateRepoList(self, repolist: List[Repository]):
        """ medoto che esegue l'update della list, passato come callback alla funzione
          asincrona del controller,tramite generateCommand assegna ad ogni elemento 
          della lista una callback per il download del repo assegnato"""
        if repolist != None:
            self.testRepoList = repolist
        for repo in self.testRepoList:
            command = self._generateCommand(repo.url)
            self.listBox.addBox(repo.name, repo.description, command=command)

    def _generateCommand(self, value):
        """ restituisce una clousre che avvia il donwload asincrono del repo.
          la funzione di download (che gestisce anche
        l'aggiornamento dell'interfaccia durante il caricamento) è downloadRepo """
        def asyncFun(event):
            thread = threading.Thread(target=self._downloadRepo, args=[value, 0])
            thread.start()
        return asyncFun

    def _downloadRepo(self, value, intero):
        """ avvia il download del repo selezionato mostrando un messaggio sullo stato del download,
        viene utilzzata da generateCommand per generare una closure """
        if self.loading == False:
            self.loading = True
            self.sideB.place_forget()
            self.icon.pack()
            self.icon.beginRotation()
            self.showMessage(f"now downloading: {str(value)}")
            self.controller.get_selected_repo(value)
            # setta la loadingBar
            self.loadbar = ctk.CTkProgressBar(self.messageBox, orientation= "horizontal")
            self.loadbar.set(0)
            self.loadbar.update()
            self.loadbar.pack(pady= 10)
            self.controller.update_branches(self.loadbar)
            self.showMessage("download complete")
            time.sleep(2)
            self.icon.stop()
            self.icon.pack_forget()
            self.showMessage(" ")
            self._recoverRepoData()

    def beforeRepoDataUpdate(self):
        """Stato prima di update"""
        self.icon.pack()
        self.icon.beginRotation()
        self.showMessage("we are now analyzing this repo")

    def afterRepoDataUpdate(self):
        """Stato dopo update"""
        response = self.controller.getStatusCodeFromLocalModel()
        # Accedi allo status_code e al body dell'oggetto HttpResponse
        status_code = response.status_code
        body = response.body
        if self.controller.getRepoData() is not None:
            self.sideB.place(y=10, relx=0.9)
            self.showMessage("done!")
            self.icon.stop()
            self.icon.pack_forget()
            time.sleep(4)
            self.showMessage("")
            if "loadbar" in self.__dict__:
                self.loadbar.destroy()
            self.loading = False
        else:
            if "API rate limit exceeded" in str(body):
                body = "GIT API rate limit exceeded"
            elif "Not found" in str(body):
                body = "Repo not found"
            else:
                body = "your repo dir is empty "
            self.showMessage(f"{str(status_code)}: {str(body)}")
            self.icon.stop()
            self.icon.pack_forget()
            time.sleep(4)
            self.showMessage("")
            if "loadbar" in self.__dict__:
                self.loadbar.destroy()
            self.loading = False
