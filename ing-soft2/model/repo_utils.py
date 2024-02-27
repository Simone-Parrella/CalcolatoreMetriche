"""
Questo è un modulo di utilità per la gestione dei repository.
Contiene funzioni utili per la manipolazione delle repository.
"""

import os
import json
import subprocess
from datetime import datetime
import pandas as pd
from pydriller import Repository
from git import Repo, InvalidGitRepositoryError


setting = open("settings.json")
settings = json.load(setting)
remote_repo = settings['repo']


def check_repo(folder="repository"):
    """Metodo che controlla se il progetto da analizzare è presente"""
    if os.path.exists(folder):
        content = os.listdir(folder)
        if content is not None:
            return 0
    else:
        clone_repo(folder)


def check_folder(folder="output"):
    """Metodo che controlla se la cartella di output è presente"""
    if not os.path.exists(folder):
        path = os.path.join(folder)
        os.mkdir(path)


def clone_repo(folder="repository"):
    """Metodo che effettua il clone di un repository target"""
    subprocess.call(['git', 'clone', remote_repo, folder])


def print_current_branch(repository):
    """Metodo che mostra il nome del branch attivo"""
    print(repository.active_branch)


def repo_to_use(folder="repository"):
    """Metodo che restituisce un oggetto Repository o None se la cartella non esiste."""
    if not os.path.exists(folder):
        return None
    repo_path = os.path.abspath(folder)
    try:
        repo = Repo(repo_path)
        return repo
    except InvalidGitRepositoryError:
        return None


def get_commits(repository):
    """Metodo che restituisce tutti i commit di una Repository"""
    return repository.traverse_commits()


def dataCommit(folder="repository"):
    """Metodo che prende tutti i commit con relativa data e li 
    inserisce in un dataframe che ritorna"""
    commit_data = []
    repo = repo_to_use(folder)
    if repo == -1:
        return -1
    for commit in get_commits(repo):
        commit_hash = commit.hash
        commit_date = commit.committer_date
        commit_data.append({'Titolo del Commit': commit_hash, 'Data del Commit': commit_date})
    return pd.DataFrame(commit_data)


def dataCommitLink(rep):
    """Metodo che prende tutti i commit con relativa 
    data e li inserisce in un dataframe che ritorna"""
    commit_data = []
    if not isinstance(rep, Repository):
        return -1
    for commit in get_commits(rep):
        commit_hash = commit.hash
        commit_date = commit.committer_date
        commit_data.append({'Commit Hash': commit_hash, 'Data del Commit': commit_date})
    return pd.DataFrame(commit_data)


def dataCommitLinkYear(rep, year):
    """Metodo che prende tutti i commit con relativa data in
      base all'anno e li inserisce in un dataframe che ritorna"""
    if not isinstance(rep, Repository):
        return -1
    if not isinstance(year, int):
        return -1
    current_year = datetime.now().year
    if year > current_year:
        return -1
    commit_data = []
    for commit in get_commits(rep):
        commit_hash = commit.hash
        commit_date = commit.committer_date
        if commit_date.year == year:
            commit_data.append({'Commit Hash': commit_hash, 'Data del Commit': commit_date})
    return pd.DataFrame(commit_data)


def delete_garbage(keep, output=None, folder="output"):
    """Elimina i file non utilizzabili creati con le metriche della classe"""
    if output is None:
        output_dir = os.path.abspath(folder)
    else:
        output_dir = os.path.join(os.path.abspath("output"), str(output))
    for filename in os.listdir(output_dir):
        if not keep in filename:
            file_to_remove = os.path.join(output_dir, filename)
            os.remove(file_to_remove)


def trova_file_classe(classe_filename, folder="repository"):
    """ Questo metodo trova una classe in una repository
      e ne ritorna il path assoluto """
    repository_path = os.path.abspath(folder)
    if not os.path.exists(repository_path):
        return -1
    for root, dirs, files in os.walk(repository_path):
        if classe_filename in files:
            return os.path.join(root, classe_filename)
    return None


def cerca_file_java(cartella_name):
    """ Questo metodo cerca tutti i file java in una cartella e ne
      restituisce una lista di nomi di file """
    risultati = []
    cartella = os.path.abspath(cartella_name)
    if not os.path.exists(cartella_name):
        return -1
    for root, dirs, files in os.walk(cartella):
        for file in files:
            if file.endswith(".java"):
                risultati.append(file)
    return risultati


def get_commit_date(commit_hash, folder="repository"):
    """Questo metodo restituisce la data del commit richiesto"""
    try:
        cartella = os.path.abspath(folder)
        if not os.path.exists(cartella):
            return None
        result = subprocess.run(['git', 'show', '--format=%aI', '-s', commit_hash],
                                cwd=os.path.abspath(folder),
                                capture_output=True, text=True, check=True)
        commit_date = result.stdout.strip()
        return commit_date
    except subprocess.CalledProcessError as e:
        print(f"Errore nell'ottenere la data del commit {commit_hash}: {e.stderr}")
        return None


def checkout_commit(commit_hash, folder="repository"):
    """Questo metodo effettua il checkout a un commit specifico"""
    try:
        subprocess.run(['git', 'checkout', commit_hash], cwd=os.path.abspath(folder), check=True)
    except subprocess.CalledProcessError as e:
        print(f"Errore durante il checkout al commit {commit_hash}: {e.stderr}")


def extract_years_from_commits(folder="repository"):
    """Questo metodo estrae gli anni disponibili dai commit delle repo """
    cartella = os.path.abspath(folder)
    if not os.path.exists(cartella):
        return -1
    repo = repo_to_use(folder)
    years = set()
    for commit in get_commits(repo):
        commit_date = commit.committer_date
        year = commit_date.year
        years.add(year)
    ordered_list = list(years)
    ordered_list.sort()
    return ordered_list
