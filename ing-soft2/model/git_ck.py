""" Questo modulo si propone di calcolare metriche di progetto tramite 
il jar ck
"""

import subprocess
import os
import pandas as pd
from pandas import DataFrame
import model.repo_utils as ru



def ck_metrics_for_single_commit(commit_hash, output = None, folder = "repository"):
    """Questo metodo estrae le metriche del commit scelto
    Utilizzato per fare analisi su commit singoli
    Utilizzato per fare analisi su commit in maniera iterativa
    per le richieste di metriche per intervallo"""
    partenza = os.getcwd()
    repo_to_analyze = os.path.abspath(folder)
    if not os.path.exists(repo_to_analyze):
        return -1
    ck_tool = os.path.abspath('ck.jar')
    if (output is not None and output != "TESTCODECK"):
        output_dir = os.path.join( os.path.abspath("output"),output)
        os.makedirs(output_dir, exist_ok=True)
    else:
        output_dir = os.path.abspath("output")
    file_name = commit_hash + "class.csv"
    file_path = os.path.join(output_dir, file_name)
    if not os.path.exists(file_path):
        os.chdir(repo_to_analyze)
        try:
            subprocess.check_call(['git', 'checkout', '-f', commit_hash])
        except subprocess.CalledProcessError:
            return -1

        os.chdir(os.path.dirname(ck_tool))
        subprocess.call(['java', '-jar', 'ck.jar', repo_to_analyze, 'true', '0',
                        'false', f"{output_dir}/{commit_hash}"])
        if(output is not None and output != "TESTCODECK"):
            ru.delete_garbage("class", output)
            os.chdir(partenza)
    # Non ritorna nulla ma crea il file csv con metriche per il commit richiesto



def commit_measure_avg(measure, commit_hash, output =None):
    """Questo metodo estrae la media della metrica desiderata dal commit"""
    current_directory = os.getcwd()
    if output is None or output == "TESTCODECK":
        dir = os.path.join(os.path.abspath("output"),commit_hash)
        if not os.path.exists(dir):
            return -1
    else:
        dir = os.path.join(os.path.join(os.path.abspath("output"),output),commit_hash)
    df = pd.read_csv(dir)
    if measure not in df.columns:
        print(f"Metrica '{measure}' non trovata nel file CSV.")
        return None
    # Calcola la media della metrica specificata
    mean_value = df[measure].mean()
    return mean_value



def analyze_commits_for_interval(df, folder = "repository", output = None):
    """Questo metodo estrae i commit corrispondenti all'intervallo scelto e li analizza"""
    commits = df
    if not isinstance(commits, DataFrame):
        return None
    if commits.empty:
        return pd.DataFrame()
    if not os.path.exists(os.path.abspath(folder)):
        return None
    if not commits.empty:  # Controlla se il DataFrame non è vuoto
        commit_messages = commits.iloc[:, 0]
        for commit_message in commit_messages:
            ck_metrics_for_single_commit(commit_message, folder = folder, output= output)
        if output != "TESTCODECK":
            ru.delete_garbage("class")
        return commits
    else:
        print("Nessun commit disponibile per il tag di rilascio specificato.")



def commit_measure_interval(measures, df, folder = "repository", output = None):
    """ Questo metodo calcola le metriche per l'intervallo e fa la 
    media delle metriche richieste per ogni commit"""
    commit = analyze_commits_for_interval(df, folder, output)
    if commit is None:
        return None
    if commit.empty:
        return pd.DataFrame
    commit['Commit Hash'] = commit['Commit Hash'] + 'class.csv'
    result_data = []
    path = os.path.abspath("output")
    element_names = os.listdir(path)
    for name in element_names:
        metric_averages = {}
        for measure in measures:
            metric_averages[measure] = commit_measure_avg(measure, name, output)
        result_data.append({"Commit Hash": name, **metric_averages})
    result_df = pd.DataFrame(result_data)
    result = commit.merge(result_df, on ="Commit Hash")
    return result
