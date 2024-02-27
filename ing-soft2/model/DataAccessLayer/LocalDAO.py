"""Questo modulo gestisce i dati locali delle repository"""

from datetime import datetime
import os
import subprocess
import shutil
import stat
from icecream import ic
import git
from pydriller import Repository, Commit
from model.repo_utils import get_commits, repo_to_use
from git.repo.base import Repo
import subprocess


class LocalDAO:
    """Local DAO class"""

    def findJavaClass(self, directory):
        """Metodo che trova tutte le classi di un progetto java"""
        """ Questo metodo cerca tutti i file java in una cartella e ne
          restituisce una lista di nomi di file """
        risultati = []
        cartella = os.path.abspath(directory)
        for root, dirs, files in os.walk(cartella):
            for file in files:
                if file.endswith(".java"):
                    risultati.append(file)
        return risultati

    def getRepoInfoFromGit(self):
        """Ottieni le informazioni del repository dal sistema Git."""
        os.chdir("repository")

        result = subprocess.check_output(["git", "remote", "show", "origin"]).decode(
            "utf-8"
        )
        firstLine = result.split("\n")[1]
        name = firstLine.split("/")[-2]
        repoName = firstLine.split("/")[-1]
        os.chdir("..")
        return name, repoName

    def cloneRepository(self, url):
        """Clona il repository usando il comando 'git clone'."""

        def on_rm_error(func, path, exc_info):
            os.chmod(path, stat.S_IWRITE)
            os.unlink(path)

        shutil.rmtree("repository", onerror=on_rm_error)
        try:
            # clona il repo
            p = subprocess.call(["git", "clone", url, "repository"])
        except Exception as e:
            # Gestisci eccezioni in caso di fallimento del clone
            print(f"Errore durante il clone del repository: {e}")

    def _class_exists_in_commit(self, commit, class_name):
        """Verifica se la classe è presente in un commit"""
        try:
            tree = commit.tree
            file_blob = tree[class_name]
            return True
        except KeyError:
            return False

    def get_commits_with_class(self, class_name, repo_path):
        """recupera nel repo specificato una lista dei commit in cui era
        presente la calsse dal nome passato come parametro"""
        repo = git.Repo(repo_path)
        commit_list = []
        for commit in repo.iter_commits():
            if self._class_exists_in_commit(commit, class_name):
                commit_list.append(commit)
        return commit_list

    def extract_yearsList_with_branches(self, folder="repository"):
        """Estrae la lista di anni con i branch"""
        repo = Repository(folder)
        years = {}
        for commit in repo.traverse_commits():
            commit_date = commit.committer_date
            year = commit_date.year
            if year not in years.keys():
                years[year] = set(commit.branches)
            else:
                branches = years[year]
                branches.update(
                    commit.branches
                )  # Utilizza il metodo 'update' per unire i set
        # Converti il set in una lista e restituiscila
        return years

    def getClassListFromGivenCommit(self, commit_hash, repo_path="repository"):
        """Da una lista di classi da un commit dato"""
        repo = git.Repo(repo_path)
        commit = repo.commit(commit_hash)
        dict_file = set()

        albero_commit = commit.tree
        for blob in albero_commit.traverse():
            if isinstance(blob, git.Blob) and ".java" in blob.path:
                dict_file.add(blob.path.split("/")[-1])
        return dict_file

    def dataCommitLinkYear(self, branch, year, rep="repository"):
        """Metodo che prende tutti i commit con relativa data in base all'anno e
        li inserisce in un dataframe che ritorna"""
        year = int(year)
        return list(
            Repository(
                rep,
                only_in_branch=branch,
                since=datetime(year, 1, 1),
                to=datetime(year, 12, 31),
            ).traverse_commits()
        )

    def getCommit(self, hash: str, rep: str = "repository") -> Commit:
        """Ritorna i commit"""
        repo = Repository(rep, single=hash)
        commits = repo.traverse_commits()
        # Cerca il commit con l'hash desiderato
        for commit in commits:
            if commit.hash == hash:
                return commit
        # Se non viene trovato alcun commit con l'hash desiderato, solleva un'eccezione
        raise ValueError(f"Commit with hash {hash} not found in repository {rep}")

    def getCommitsFromDate(self, date: datetime, yearToArrive, repo):
        """Ritorna i commit per data"""
        commits = list(
            Repository(
                repo, since=date, to=datetime(int(yearToArrive), 12, 31)
            ).traverse_commits()
        )
        if not commits:
            print("errore")
        return commits

    def getCommitInInterval(self, start_commit, end_commit, repo_path="repository"):
        # oggetto Repository
        repo = Repository(repo_path)
        # Dizionario per salvare i commit nell'intervallo
        commits_in_range = {}
        # Flag per verificare se l'hash di inizio è valido
        start_commit_valid = not start_commit
        # Itera attraverso tutti i commit nel repository nell'intervallo specificato
        for commit in repo.traverse_commits():
            if start_commit and commit.hash == start_commit:
                start_commit_valid = True
            if start_commit_valid:
                commits_in_range[commit.hash] = {
                    "hash": commit.hash,
                    "date": commit.committer_date,
                }
            if end_commit and commit.hash == end_commit:
                break
        return commits_in_range

    def checkout_to(self, branch):
        """Fa il checkout a un commit"""
        try:
            # Esegui il checkout del branch
            subprocess.check_call(["git", "checkout", branch], cwd="repository")
            print(f"Checked out to branch: {branch}")
        except subprocess.CalledProcessError as e:
            # Se il branch non esiste, solleva un'eccezione manualmente
            if "did not match any file(s) known to git" in str(e):
                print(f"Branch '{branch}' does not exist.")
                raise
            else:
                # Se si verifica un altro errore, rilancia l'eccezione
                print(f"Error during checkout: {e}")
                raise
