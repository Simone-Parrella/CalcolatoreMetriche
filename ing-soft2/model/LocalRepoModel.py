"""Questo modulo gestisce i dati locali delle repository"""
import os
from typing import List
from icecream import ic
from pydriller import Commit
from model.DataAccessLayer.DAORepo import DAORepo
from model.DataAccessLayer.LocalDAO import LocalDAO


class LocalRepoModel:
    """SINGLETON: modella le interazioni e il recupero dei dati locali
    (come il repo locale) necessari all app"""

    _instance = None
    repoData = None

    def __new__(cls):
        """Istanzia la classe"""
        if cls._instance is None:
            cls._instance = super(LocalRepoModel, cls).__new__(cls)
            cls._instance.CRUD = DAORepo()
            cls._instance.LocalDAO = LocalDAO()
        return cls._instance

    def getRepoData(self):
        """ritorna i metadati del repository installato localente"""
        return self.repoData

    def RepoDataUpdate(self):
        """Recupera i metadati aggiornati relativi al repository installato localmente."""
        self._CheckRepoDir()
        # Utilizzo del pattern DAO
        name, repoName = self.LocalDAO.getRepoInfoFromGit()

        if name is not None and repoName is not None:
            repodata = self.CRUD.getRepoByNameeAuthor(name, repoName)
            self.repoData = repodata
            if self.repoData is not None:
                self.repoData.releases = self.CRUD.get_all_release_tag_repo(
                    name, repoName
                )

    def createLocalRepo(self, url):
        """A partire dall'URL fornito, installa localmente in una
        directory 'repository' il repo cercato."""
        self.LocalDAO.cloneRepository(url)

    def _CheckRepoDir(self, directory_name="repository"):
        "controlla se la directory esiste localmente, altrimenti la crea"
        if not os.path.exists(directory_name):
            try:
                os.makedirs(directory_name)
            except OSError as e:
                print(f"Errore durante la creazione della cartella: {e}")
        else:
            return

    def get_status_code(self):
        """Accedi all'attributo last_http_code di CRUDRepo"""
        status_code = self.CRUD.last_http_response
        return status_code

    def getAllJavaClassProject(self, rootDirectory):
        """Ritorna Le classi java nel progetto"""
        return self.LocalDAO.findJavaClass(rootDirectory)

    def getCommitWithClassList(self, className):
        """dato il nome di una classe recupera tutti i commit in cui questa è presente"""
        return self.LocalDAO.get_commits_with_class(className, "repository")

    def getYearList(self) -> dict[int, set[str]]:
        """Recupera la lista degli anni"""
        return self.LocalDAO.extract_yearsList_with_branches()

    def getClassListFromGivenCommit(self, commit) -> List[str]:
        """Restituisce la lista delle classi presenti in un commit"""
        return self.LocalDAO.getClassListFromGivenCommit(commit)

    def getCommiListByYear(self, branch, year):
        """Recupera la lista dei commit per l'anno"""
        return self.LocalDAO.dataCommitLinkYear(branch, year)

    def getCommiListFromDate(self, date, yearToArrive):
        """Ritorna una lista di commit per data"""
        return self.LocalDAO.getCommitsFromDate(date, yearToArrive, "repository")

    def getCommitByHash(self, hash) -> Commit:
        """Ritorna il commit per hash"""
        return self.LocalDAO.getCommit(hash)

    def getCommitInInterval(self, start_hash, end_hash):
        """Recupera la lista di commit tra start_hash e end_hash."""
        return self.LocalDAO.getCommitInInterval(start_hash, end_hash)

    def switch_branch(self, branch):
        """checkouts the local repo to the given branch"""
        self.LocalDAO.checkout_to(branch)
