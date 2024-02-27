"""Modulo per il controller della pagina principale"""
from typing import Callable, List
import threading
import os
from git import Repo
from customtkinter import CTkProgressBar
from model.LocalRepoModel import LocalRepoModel
from model.RepoModel import RepoModel
from icecream import ic


class MainPageController:
    """Classe MainPageController"""

    def __init__(self):
        """Inizializzatore della classe"""
        super().__init__()
        self.process = None
        self.globalModel = LocalRepoModel()
        self.repoModel = RepoModel()
        self.update_in_progress = False
        self.is_request_for_repos_running = False

    def getStatusCodeFromLocalModel(self):
        """Ritorna il codice di stato da localModel"""
        return self.globalModel.get_status_code()

    def getAllJavaClassByLocalRepoModel(self, rootDirectory):
        """Ritorna tutte le classi java dal LocalRepoModel"""
        return self.globalModel.getAllJavaClassProject(rootDirectory=rootDirectory)

    def requestRepoUpdate(
        self,
        callbackBefore: Callable[[], None] = None,
        callbackAfter: Callable[[], None] = None,
    ) -> threading.Thread:
        """Metodo che esegue l'aggiornamento del repository scaricato in locale"""

        def toRun():
            """Imposta la variabile a True quando l'aggiornamento è in corso"""
            self.update_in_progress = True
            if callbackBefore is not None:
                callbackBefore()
            self.globalModel.RepoDataUpdate()
            if callbackAfter is not None:
                callbackAfter()
            # variabile che tiene conto dell'aggiornamento del repository
            self.update_in_progress = False

        # Crea un thread e avvialo
        thread = threading.Thread(target=toRun)
        thread.start()
        return thread

    def getRepoData(self):
        """Callback a getRepoData"""
        return self.globalModel.getRepoData()

    def request_for_repos(self, query, callback: Callable[[List], any]):
        """Recupera una nuova lista di repository in maniera asincrona"""

        def toRun():
            """Imposta la variabile globale a True per indicare che è in esecuzione"""
            self.is_request_for_repos_running = True
            author_query = None
            repo_name_query = None
            # Parsing della query per estrarre gli attributi author e repoName
            query_parts = query.split()
            for part in query_parts:
                if part.startswith("author:"):
                    author_query = part.split(":")[1]
                elif part.startswith("repoName:"):
                    repo_name_query = part.split(":")[1]
            # Chiama i metodi del modello in base agli attributi estratti dalla query
            if author_query and repo_name_query:
                repoList = self.repoModel.getRepoListByAuthorAndRepoName(
                    author_query, repo_name_query
                )
            elif author_query:
                repoList = self.repoModel.getRepoListByAuthor(author_query)
            elif repo_name_query:
                repoList = self.repoModel.getRepoListByName(repo_name_query)
            else:
                repoList = self.repoModel.getRepoListByName(query)
            callback(repoList)
            # Imposta la variabile globale a False per indicare che l'esecuzione è terminata
            self.is_request_for_repos_running = False

        # Crea un thread e avvialo
        t = threading.Thread(target=toRun)
        t.start()
        return t

    def is_request_for_repos_executing(self):
        """Restituisce lo stato corrente dell'esecuzione di request_for_repos"""
        return self.is_request_for_repos_running

    def get_selected_repo(self, url):
        """Ritorna la repository selezionata"""
        self.globalModel.createLocalRepo(url)
        return True

    def update_branches(self, loadBar: CTkProgressBar, repo=None):
        """downloads branches for the local repository updating given progress bar in real-time"""
        # se ci sono branch aggiuntivi li scarica tutti
        if repo is None:
            repo = Repo("repository")
        branches = [
            ref.name
            for ref in repo.references
            if "origin" in ref.name and "HEAD" not in ref.name
        ]
        ic(repo.references)
        print(branches)
        # Verifica se l'elenco dei branch è vuoto prima di calcolare la lunghezza
        if branches:
            steplen = 1 / len(branches)
            # non so perché nell'implementazione di questa roba la velocità di
            # spostamento della barra viene divisa per 50
            # quindi per farla avanzare di quanto vogliamo noi, moltiplico per 50
            loadBar.configure(determinate_speed=steplen * 50)
            loadBar.update()
            for branch in branches:
                self.globalModel.switch_branch(branch.split("/")[-1])
                loadBar.step()
            if "origin/main" in branches:
                self.globalModel.switch_branch("main")
            else:
                self.globalModel.switch_branch("master")
        else:
            # quando non ci sono branch
            print("Nessun branch disponibile")

    def checkRepo(self):
        """Controlla la repo"""
        percorso_git = os.path.join("repository", ".git")
        if os.path.exists(percorso_git) and os.path.isdir(percorso_git):
            return True
        else:
            return False
