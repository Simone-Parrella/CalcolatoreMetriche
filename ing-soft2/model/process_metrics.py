"""Questo modulo si propone di calcolare le metriche di processo di una repo
github, quindi implementa i metodi necessari"""
import subprocess
import datetime
import difflib
import os
import chardet
import git
import model.repo_utils as ru




def controlla_numero_revisioni_per_classe(classe_filename, folder="repository"):
    """Metodo che dato il nome di una classe ne calcola il numero di revisioni"""
    repository_path = os.path.abspath(folder)
    classe_file_path = ru.trova_file_classe(classe_filename, folder)
    # print(classe_file_path)
    if classe_file_path is None:
        return -1
    if not os.path.exists(repository_path):
        return -1
    repo = git.Repo(repository_path)
    numero_revisioni = 0

    for commit in repo.iter_commits(paths=classe_file_path):
        numero_revisioni += 1
    repo.close()
    return numero_revisioni


def calcola_numero_bug_fix(folder="repository"):
    """Metodo che calcola i bug fix di un progetto se documentati"""
    repository_path = os.path.abspath(folder)
    if not os.path.exists(repository_path):
        return -1
    repo = git.Repo(repository_path)
    numero_bug_fix = 0

    for commit in repo.iter_commits():
        if "fix" in commit.message.lower():
            numero_bug_fix += 1
    repo.close()
    return numero_bug_fix


def calcola_code_churn(file1, file2):
    """Calcola il numero di modifiche tra due file e restituisce il risultato"""
    if file1 is None or file2 is None:
        return -1
    with open(file1, "r", encoding="utf-8") as f1, open(
        file2, "r", encoding="utf-8"
    ) as f2:
        lines1 = f1.readlines()
        lines2 = f2.readlines()

    # Calcola il diff tra le linee dei due file
    differ = difflib.Differ()
    diff = list(differ.compare(lines1, lines2))

    # Conta il numero di linee modificate (inizia con '+' o '-')
    numero_modifiche = sum(
        1 for line in diff if line.startswith("+") or line.startswith("-")
    )

    return numero_modifiche


def calcola_loc(classe_filename, folder="repository"):
    """Questo metodo calcola le misure LOC di un codice restituendo il
    numero di linee di codice il numero di linee vuote e il numero di commenti"""
    classe_file_path = ru.trova_file_classe(classe_filename, folder)
    if classe_file_path is None or classe_file_path == -1:
        return -1
    with open(classe_file_path, "rb") as raw_file:
        raw_data = raw_file.read()
        encoding_info = chardet.detect(raw_data)
        file_encoding = encoding_info["encoding"]

    # Verifica la codifica rilevata
    if file_encoding is None:
        file_encoding = (
            "utf-8"  # Imposta una codifica predefinita se non può essere rilevata
        )
    # print(file_encoding)
    with open(classe_file_path, "r", encoding=file_encoding) as file:
        linee_di_codice = 0
        linee_vuote = 0
        commenti = 0

        for linea in file:
            linea = linea.strip()
            if not linea:
                linee_vuote += 1
            elif (
                linea.startswith("#")
                or linea.startswith("//")
                or linea.startswith("*")
                or linea.startswith("*/")
                or linea.startswith("/*")
                or linea.startswith('"""')
                or linea.endswith('"""')
            ):
                commenti += 1
            else:
                linee_di_codice += 1

        return linee_di_codice, linee_vuote, commenti


def calcola_autori_distinti_per_file(file_name, folder="repository"):
    """Questo metodo calcola il numero di autori distinti per file e ne
    restituisce una lista di nomi"""
    file_path = ru.trova_file_classe(file_name, folder)
    repository_path = os.path.abspath(folder)
    if file_path is None or file_path == -1 or not os.path.exists(repository_path):
        return -1

    # Esegui il comando Git per ottenere gli autori
    git_command = ["git", "log", '--format="%an"', "--follow", file_path]
    output = subprocess.check_output(git_command, cwd=repository_path)

    # Rileva la codifica dell'output
    encoding_info = chardet.detect(output)
    output_encoding = encoding_info["encoding"]
    # print(encoding_info)
    # Verifica la codifica rilevata
    if output_encoding is None:
        output_encoding = (
            "utf-8"  # Imposta una codifica predefinita se non può essere rilevata
        )

    # Decodifica l'output con la codifica corretta
    decoded_output = output.decode(output_encoding)

    autori_distinti = set()
    lines = decoded_output.split("\n")
    for line in lines:
        autore = line.strip('"\n')  # Rimuovi i caratteri di citazione e newline
        autori_distinti.add(autore)
    return autori_distinti


def calcola_settimane_file(class_name, folder="repository"):
    """Questo metodo calcola l'età del file richiesto in settimane"""
    repository_path = os.path.abspath(folder)
    if not os.path.exists(repository_path):
        return -1
    file_path = ru.trova_file_classe(class_name, folder)
    if file_path is None or file_path == -1:
        return -1
    git_command = f'git log --diff-filter=A --format=%ct -- "{file_path}"'
    result = (
        subprocess.check_output(git_command, cwd=repository_path, shell=True)
        .decode()
        .strip()
    )

    if not result:
        return None
    timestamps = result.split("\n")

    # Prendi solo la prima parte del timestamp (ignorando il timestamp doppio se presente)
    first_timestamp = timestamps[0]

    # Converti il timestamp in un intero
    file_creation_timestamp = int(first_timestamp)
    file_creation_date = datetime.datetime.utcfromtimestamp(file_creation_timestamp)

    current_time = datetime.datetime.now()
    time_difference = current_time - file_creation_date

    # Calcola il numero di giorni
    return time_difference.days
