"""Modulo per i dati dinamici"""
import requests
from icecream import ic
from model.Domain import HttpResponse, Repository, MetadataRepository


class DAORepo:
    """Dichiarazione classe"""

    def __init__(self):
        """Inizializzazione"""
        self.last_http_response = None

    def getRepoByNameeAuthor(self, repoOwner, repoName):
        """Ritorna Repo dall'autore"""
        response = requests.get(f"https://api.github.com/repos/{repoOwner}/{repoName}")
        self.last_http_response = HttpResponse(response.status_code, response.json())
        if response.status_code == 200:
            repository_data = response.json()
            repository = MetadataRepository(repository_data)

            return repository
        else:
            return None

    def getRepoList(self, repoName):
        """Ritorna la lista di repo"""
        if repoName == "" or repoName == " ":
            return []
        # Solo i repository java
        url = f"https://api.github.com/search/repositories?q={repoName}+language:java"
        response = requests.get(url)
        self.last_http_response = HttpResponse(response.status_code, response.json())
        risultati = response.json()["items"]
        # Crea una lista di oggetti di tipo Repository
        repositories = []
        for risultato in risultati:
            name = risultato["name"]
            html_url = risultato["html_url"]
            description = risultato["description"]
            repository = Repository(name, html_url, description)
            repositories.append(repository)

        return repositories

    def getJavaRepoList(self, repoName):
        """Ritorna le repo in java"""
        url = f"https://api.github.com/search/repositories?q={repoName}+language:java"
        response = requests.get(url)
        self.last_http_response = HttpResponse(response.status_code, response.json())
        risultati = response.json()["items"]
        # Crea una lista di oggetti di tipo Repository
        repositories = []
        for risultato in risultati:
            name = risultato["name"]
            html_url = risultato["html_url"]
            description = risultato["description"]
            repository = Repository(name, html_url, description)
            repositories.append(repository)
        return repositories

    def get_all_release_tag_repo(self, owner, repo_name):
        """Metodo che ritorna tutte le  releases di uno specifico progetto"""
        url = f"https://api.github.com/repos/{owner}/{repo_name}/releases"
        response = requests.get(url)
        if response.status_code == 200:
            releases = response.json()
            # Estrai solo i tag delle release dalla lista di release
            release_tags = [release["tag_name"] for release in releases]
            return release_tags
        else:
            print(
                f"Errore {response.status_code}: Impossibile ottenere le release del progetto."
            )
            return None

    def getJavaRepoListForAuthorAndRepo(self, author, repo_name):
        """Se l'autore è specificato, cerca per il nome del repository all'interno
        dell'account dell'autore"""
        url = f"https://api.github.com/search/repositories?q=user:{author}+repo:{repo_name}+language:java"
        response = requests.get(url)
        self.last_http_response = HttpResponse(response.status_code, response.json())
        # Verifica se la risposta contiene dati JSON
        try:
            json_data = response.json()
        except ValueError:
            return None
        # Verifica se la chiave "items" è presente nel dizionario JSON
        risultati = json_data.get("items")
        if risultati is None:
            return None
        # Crea una lista di oggetti di tipo Repository
        repositories = []
        for risultato in risultati:
            name = risultato["name"]
            html_url = risultato["html_url"]
            description = risultato["description"]
            repository = Repository(name, html_url, description)
            repositories.append(repository)
        return repositories

    def getRepoListByAuthor(self, author):
        """Ritorna la lista di repo da autore"""
        url = (
            f"https://api.github.com/search/repositories?q=user:{author}+language:java"
        )
        response = requests.get(url)
        print("response: ")
        print(response)
        self.last_http_response = HttpResponse(response.status_code, response.json())
        repositories = []
        if response.status_code == 200:
            risultati = response.json()["items"]
            for risultato in risultati:
                name = risultato["name"]
                html_url = risultato["html_url"]
                description = risultato["description"]
                repository = Repository(name, html_url, description)
                repositories.append(repository)
        return repositories
