"""
Questo modulo si occupa di combinare le fasi di estrazioni di metriche per 
l'utilizzo delle metriche estratte su interfaccia grafica
"""
import subprocess
import os
import shutil
import pandas as pd
import model.process_metrics as pm
import model.repo_utils as ru
import model.git_ck as ck


def generate_process_metrics(nome_classe, commits_dict, folder = "repository"):
    """Genera le metriche di processo, è possibile specificare il
    commit da analizzare e il folder dove è conservata la repository
    Questo metodo dovrà essere utilizzato per fare tutte le analisi 
    disponibili con le metriche di processo"""
    cartella = os.path.abspath(folder)
    print("\n\n\n\n")
    print(type(commits_dict))
    if not os.path.exists(cartella):
        return -1
    latest_commit_hash = subprocess.check_output(["git", "rev-parse", "HEAD"],
                                                  cwd=os.path.abspath(folder),
                                                 text=True).strip()
    if ru.trova_file_classe(nome_classe, folder) is None:
        return -1
    if  isinstance(commits_dict, str ) or isinstance(commits_dict, int ):
        return -1
    if  isinstance(commits_dict, dict ):
        df_filtrato = pd.DataFrame(list(commits_dict.items()),
                                   columns=['Commit Hash', 'Data del Commit'])
        df_filtrato['Data del Commit'] = df_filtrato['Data del Commit'].apply(lambda x: x['date'])
        flag = False
        df_finale= pd.DataFrame(columns=['Commit hash', 'Data del Commit',
                                          'Numero di Revisioni', 'Linee di Codice', 'Linee vuote', 
                                          'Commenti', 'Autori Distinti', 'Settimane file', 
                                          'Bugfix commit', 'Code churn'])
    else:
        df_filtrato = pd.DataFrame(commits_dict, columns=['Commit Hash', 'Data del Commit'])
        df_filtrato['Data del Commit'] = pd.to_datetime(df_filtrato['Data del Commit'], utc=True)
        flag = False
        df_finale= pd.DataFrame(columns=['Commit hash', 'Data del Commit',
                                          'Numero di Revisioni', 'Linee di Codice', 'Linee vuote',
                                          'Commenti', 'Autori Distinti', 'Settimane file',
                                          'Bugfix commit', 'Code churn'])
    for index, element in enumerate(df_filtrato["Commit Hash"]):
        ru.checkout_commit(element)
        if flag is not True:
            ru.check_folder(folder="Giulio")
            folderG = os.path.join(os.path.abspath("Giulio"), "giulio.txt")
            shutil.copy2(ru.trova_file_classe(nome_classe, folder), folderG )
            cc = 0
            flag = True
        else:
            cc = pm.calcola_code_churn(ru.trova_file_classe(nome_classe), folderG)
        nr = pm.controlla_numero_revisioni_per_classe(nome_classe, folder)
        rig, rigv, com = pm.calcola_loc(nome_classe, folder)
        ad = pm.calcola_autori_distinti_per_file(nome_classe, folder)
        sf = pm.calcola_settimane_file(nome_classe, folder)
        bf = pm.calcola_numero_bug_fix(folder)
        temp_df = pd.DataFrame({'Commit hash': element,
                                'Data del Commit': df_filtrato.loc[index, 'Data del Commit'],  
                                'Numero di Revisioni': nr,
                                'Linee di Codice': rig,
                                'Linee vuote': rigv,
                                'Commenti': com,
                                'Autori Distinti': [ad],
                                'Settimane file': sf,
                                'Bugfix commit': bf,
                                'Code churn': cc}, index=[0])
        df_finale = pd.concat([df_finale, temp_df], ignore_index=True)
    ru.checkout_commit(latest_commit_hash)
    file_path = os.path.join("Giulio", "giulio.txt")
    if os.path.exists(file_path):
        os.remove(file_path)
    if os.path.exists("Giulio"):
        os.rmdir("Giulio")
    return df_finale





def generate_metrics_ck(commits_dict, folder = "repository",
                         measures =["cbo", "wmc", "dit", "noc", "rfc", "lcom"], output = None):
    """Genera le metriche ad oggetti , questo metodo prende la release da 
    cui si vuole partire(opzionale), trova i commit e li inserisce in un dataframe
    Poi li filtra dal commit dopo la release precedente, alla release scelta e 
    ritorna il primo dataframe filtrato, Una volta richiamato il metodo, se gli si passa
    il dataframe e i due hash per cui si vuole avere l'intervallo di analisi,
    filtra di nuovo il df e analizza"""
    cartella = os.path.abspath(folder)
    if not os.path.exists(cartella):
        return -1
    latest_commit_hash = subprocess.check_output(["git", "rev-parse", "HEAD"],
                                                 cwd=os.path.abspath(folder), text=True).strip()
    if isinstance(commits_dict, str ) or isinstance(commits_dict, int):
        return -1
    if isinstance(commits_dict, dict ):
        df_filtrato = pd.DataFrame(list(commits_dict.items()),
                                   columns=['Commit Hash', 'Data del Commit'])
        df_filtrato['Data del Commit'] = df_filtrato['Data del Commit'].apply(lambda x: x['date'])
    else:
        df_filtrato = pd.DataFrame(commits_dict, columns=['Commit Hash', 'Data del Commit'])
        df_filtrato['Data del Commit'] = pd.to_datetime(df_filtrato['Data del Commit'], utc=True)
    commit=ck.commit_measure_interval(measures, df_filtrato, folder, output= output)
    if commit.empty:
        print("Non ci sono commit disponibili")
        ru.checkout_commit(latest_commit_hash)
        return 0
    ru.checkout_commit(latest_commit_hash)
    return commit
