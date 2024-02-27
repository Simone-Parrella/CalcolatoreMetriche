"""Modulo per la ricerca"""
from model.DataAccessLayer.DAORepo import DAORepo


class RepoModel:
    """Classe che recupera i repository utilizzando il layer
    di accesso ai dati"""

    def __init__(self):
        """Inizializzazione"""
        self.CRUD = DAORepo()

    def getRepoListByName(self, name):
        """Trova i nomi delle repo"""
        return self.CRUD.getRepoList(name)

    def getRepoListByAuthorAndRepoName(self, author, repo_name):
        """Trova i repo per autore"""
        return self.CRUD.getJavaRepoListForAuthorAndRepo(author, repo_name)

    def getRepoListByAuthor(self, author):
        """Restituisce la lista di repo per autore"""
        return self.CRUD.getRepoListByAuthor(author)
