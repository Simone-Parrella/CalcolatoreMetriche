import unittest
import os
import model.process_metrics as pm
import model.repo_utils as ru
from pydriller import Repository
from pandas import DataFrame
import model.spMetrics as sp
import model.git_ck as ck
from git import Repo
import pandas as pd
import subprocess
class TestMetriche(unittest.TestCase):

    repository = os.path.join("TestingMetriche","Prova-per-ing-soft")
    repo_fuori = "TestingMetriche"
    classe = "azz.java"
    invalidClasse = "104.java"
    invalidFolder = "104"
    file1 = "papa.txt"
    file2 = "angelone.txt"
    commit = "b4e3ae581bb983d394e38606a08bb9f172d9f59b"
    diction = [('615c5403d94b89eb6380b1832f31afd5caab995a', '2023-11-06 16:18:49+01:00'),
 ('cbdd35d610093c131a1f7a03d1b6b4c5ff020bdc', '2023-11-06 16:25:13+01:00'),
 ('b4e3ae581bb983d394e38606a08bb9f172d9f59b', '2023-11-06 16:26:42+01:00')]
    invalidCommit = "sonoInvalido"
    
    repositoryCK = os.path.join("TestingMetriche", "ck", "Prova-per-ing-soft")
    measure = "cbo"
    measures =["cbo", "wmc", "dit", "noc", "rfc", "lcom"]


    @classmethod
    def setUpClass(cls):
        ru.check_folder("repository")
        ru.check_folder()
        controllaSeStaTutto()

    ######   INIZIO TESTING git_ck            ######
    def test_v__ckmetrics_for_single_commit(self):
        ck.ck_metrics_for_single_commit(self.commit, folder=self.repositoryCK)
        file_name = self.commit + "class.csv"
        output_dir = os.path.abspath("output")
        file_path = os.path.join(output_dir, file_name)
        if os.path.exists(file_path):
            assert True
        result = ck.ck_metrics_for_single_commit(self.invalidCommit,folder = self.repositoryCK)
        self.assertLess(result, 0)
        result = ck.ck_metrics_for_single_commit(self.invalidCommit, folder = self.invalidFolder)
        self.assertLess(result, 0)
        result = ck.ck_metrics_for_single_commit(self.commit,folder = self.repositoryCK)
        self.assertLess(result, 0)



    def test_w_commit_measure_avg(self):
        current_directory = os.getcwd()
        parent_directory = os.path.dirname(current_directory)
        parent1 = os.path.dirname(parent_directory)
        parent2 = os.path.dirname(parent1)
        os.chdir(parent2)
        result = ck.commit_measure_avg(self.measure, self.commit+"class.csv")
        if(result == "nan"):
            assert True
        result = ck.commit_measure_avg("tizio", "caio")
        self.assertLess(result, 0)
        result = ck.commit_measure_avg(self.measure, "caio")
        self.assertLess(result, 0)
        result = ck.commit_measure_avg("tizio", self.commit+"class.csv")
        self.assertIsNone(result)

    def test_x_analyze_commits_for_interval(self):
        df_filtrato = pd.DataFrame(self.diction, columns=['Commit Hash', 'Data del Commit'])
        df_filtrato['Data del Commit'] = pd.to_datetime(df_filtrato['Data del Commit'], utc=True)
        result = ck.analyze_commits_for_interval(df_filtrato, self.repositoryCK, output="TESTCODECK")
        self.assertIsInstance(result, DataFrame)
        result = ck.analyze_commits_for_interval(df_filtrato, self.invalidFolder, output="TESTCODECK")
        self.assertIsNone(result)
        result = ck.analyze_commits_for_interval("qualcosaDiInvalido" ,self.invalidFolder, output="TESTCODECK")
        self.assertIsNone(result)
        result = ck.analyze_commits_for_interval("qualcosaDiInvalido" ,self.repositoryCK, output="TESTCODECK")
        self.assertIsNone(result)

    def test_y_commits_measure_interval(self):
        df_filtrato = pd.DataFrame(self.diction, columns=['Commit Hash', 'Data del Commit'])
        df_filtrato['Data del Commit'] = pd.to_datetime(df_filtrato['Data del Commit'], utc=True)
        result = ck.commit_measure_interval(self.measures,df_filtrato, self.repositoryCK, output="TESTCODECK")
        self.assertIsInstance(result, DataFrame)
        current_directory = os.getcwd()
        parent_directory = os.path.dirname(current_directory)
        parent1 = os.path.dirname(parent_directory)
        parent2 = os.path.dirname(parent1)
        os.chdir(parent2)
        result = ck.commit_measure_interval(self.measures,df_filtrato, self.invalidFolder, output="TESTCODECK")
        self.assertIsNone(result)
        result = ck.commit_measure_interval(self.measures,"qualcosaDiInvalido" ,self.invalidFolder, output="TESTCODECK")
        self.assertIsNone(result)
        result = ck.commit_measure_interval(self.measures,"qualcosaDiInvalido" ,self.repositoryCK, output="TESTCODECK")
        self.assertIsNone(result)
        result = ck.commit_measure_interval("tipo",df_filtrato, self.repositoryCK, output="TESTCODECK")
        self.assertIsNone(result)
        result = ck.commit_measure_interval("tipo",df_filtrato, self.invalidFolder, output="TESTCODECK")
        self.assertIsNone(result)
        result = ck.commit_measure_interval("tipo","qualcosaDiInvalido" ,self.invalidFolder, output="TESTCODECK")
        self.assertIsNone(result)
        result = ck.commit_measure_interval("tipo","qualcosaDiInvalido" ,self.repositoryCK, output="TESTCODECK")
        self.assertIsNone(result)
    
    ######   INIZIO TESTING PROCESS METRICS   ######
    def test_controlla_numero_revisioni_per_classe(self):
        # Test with valid class name
        result = pm.controlla_numero_revisioni_per_classe(self.classe, folder =self.repository)
        self.assertGreaterEqual(result, 0)
        # Test with invalid class name 
        result = pm.controlla_numero_revisioni_per_classe(self.invalidClasse, folder =self.repository)
        self.assertLessEqual(result, 0)  
        # Test with invalid folder
        result = pm.controlla_numero_revisioni_per_classe(self.classe, folder =self.invalidFolder)
        self.assertLessEqual(result, 0)
        result = pm.controlla_numero_revisioni_per_classe(self.invalidClasse, folder =self.invalidFolder)
        self.assertLessEqual(result, 0)

    def test_calcola_numero_bug_fix(self):
        result = pm.calcola_numero_bug_fix(folder =self.repository)
        self.assertGreaterEqual(result, 0)
        result = pm.calcola_numero_bug_fix(folder =self.invalidFolder)
        self.assertLess(result, 0)

    def test_calcola_code_churn(self):
        # caso file buoni
        result = pm.calcola_code_churn(ru.trova_file_classe(self.file1, folder=self.repo_fuori), ru.trova_file_classe(self.file2, folder = self.repo_fuori))
        self.assertGreaterEqual(result, 0)
        # caso primo file cattivo
        result = pm.calcola_code_churn(ru.trova_file_classe("nient.txt", folder=self.repo_fuori), ru.trova_file_classe(self.file2, folder =self.repo_fuori))
        self.assertLessEqual(result, 0)
        # caso secondo file cattivo
        result = pm.calcola_code_churn(ru.trova_file_classe(self.file1, folder=self.repo_fuori), ru.trova_file_classe("nient.txt", folder=self.repo_fuori))
        self.assertLessEqual(result, 0)
        # caso entrambi file cattivi
        result = pm.calcola_code_churn(ru.trova_file_classe("nient.txt", folder=self.repo_fuori), ru.trova_file_classe("nient.txt", folder=self.repo_fuori))
        self.assertLessEqual(result, 0)

    def test_calcola_loc(self):
        # tutto buono
        result = pm.calcola_loc(self.classe, folder =self.repository)
        self.assertGreaterEqual(result[0], 0)
        # caso classe cattiva
        result = pm.calcola_loc(self.invalidClasse, folder =self.repository)
        self.assertLessEqual(result, 0)
        # caso cartella cattiva
        result = pm.calcola_loc(self.classe, folder =self.invalidFolder)
        self.assertLessEqual(result, 0)
        result = pm.calcola_loc(self.invalidClasse, folder =self.invalidFolder)
        self.assertLessEqual(result, 0)

    def test_calcola_autori_distinti_per_file(self):
        # tutto buono
        result = pm.calcola_autori_distinti_per_file(self.classe, folder =self.repository)
        self.assertGreater(len(result), 0)
        # caso classe cattiva
        result = pm.calcola_autori_distinti_per_file(self.invalidClasse, folder =self.repository)
        self.assertLessEqual(result, 0)
        # caso cartella cattiva
        result = pm.calcola_autori_distinti_per_file(self.classe, folder =self.invalidFolder)
        self.assertLessEqual(result, 0)
        result = pm.calcola_autori_distinti_per_file(self.invalidClasse, folder =self.invalidFolder)
        self.assertLessEqual(result, 0)

    def test_calcola_settimane_file(self):
        # tutto buono
        result = pm.calcola_settimane_file(self.classe, folder =self.repository)
        self.assertGreater(result, 0)
        # caso classe cattiva
        result = pm.calcola_settimane_file(self.invalidClasse, folder =self.repository)
        self.assertLessEqual(result, 0)
        # caso cartella cattiva
        result = pm.calcola_settimane_file(self.classe, folder =self.invalidFolder)
        self.assertLessEqual(result, 0)
        result = pm.calcola_settimane_file(self.invalidClasse, folder =self.invalidFolder)
        self.assertLessEqual(result, 0)
    
    ##### FINE TESTING PROCESS METRICS #####
    ##### INIZIO TESTING REPO UTILS ########

    def test_repo_to_use(self):
        result = ru.repo_to_use(self.repository)
        self.assertIsInstance(result, Repo)
        result = ru.repo_to_use(self.invalidFolder)
        self.assertIsNone(result)


    def test_data_commit_link(self):
        result = ru.dataCommitLink(Repository(self.repository))
        self.assertIsInstance(result, DataFrame)
        result = ru.dataCommitLink("nonrepo")
        self.assertLess(result, 0)

    def test_data_commit_link_year(self):
        result = ru.dataCommitLinkYear(Repository(self.repository), 2023)
        self.assertIsInstance(result, DataFrame)
        result = ru.dataCommitLinkYear("nonrepo", 2023)
        self.assertLess(result, 0)
        result = ru.dataCommitLinkYear(Repository(self.repository), "2025")
        self.assertLess(result, 0)
        result = ru.dataCommitLinkYear("nonrepo", "2025")
        self.assertLess(result, 0)
        result = ru.dataCommitLinkYear(Repository(self.repository), 3001)
        self.assertLess(result, 0)

    def test_trova_file_classe(self):
        result = ru.trova_file_classe(self.classe, self.repository)
        self.assertIsInstance(result, str)
        result = ru.trova_file_classe(self.classe, self.invalidFolder)
        self.assertLess(result, 0)
        result = ru.trova_file_classe(self.invalidClasse, self.repository)
        self.assertIsNone(result)
        result = ru.trova_file_classe(self.invalidClasse, self.invalidFolder)
        self.assertLess(result, 0)

    def test_cerca_file_java(self):
        result = ru.cerca_file_java(self.repository)
        self.assertIsInstance(result, list)
        result = ru.cerca_file_java(self.invalidFolder)
        self.assertLess(result, 0)

    def test_get_commit_date(self):
        result = ru.get_commit_date(self.commit, self.repository)
        self.assertIsInstance(result, str)
        result = ru.get_commit_date(self.commit, self.invalidFolder)
        self.assertIsNone(result)
        result = ru.get_commit_date("nessuno", self.repository)
        self.assertIsNone(result)
        result = ru.get_commit_date("nessuno", self.invalidFolder)
        self.assertIsNone(result)

    ###### FINE TESTING REPO UTILS  ########
    ###### INIZIO TESTING SP-METRICS #######
    
    def test_sp_process_metrics(self):
        result = sp.generate_process_metrics(self.classe, self.diction, self.repository)
        self.assertIsInstance(result, DataFrame)
        result = sp.generate_process_metrics(self.invalidClasse, self.diction, self.repository)
        self.assertLess(result, 0)
        result = sp.generate_process_metrics(self.classe, "qualcosanonBuono", self.repository)
        self.assertLess(result, 0)
        result = sp.generate_process_metrics(self.classe, self.diction, self.invalidFolder)
        self.assertLess(result, 0)
        result = sp.generate_process_metrics(self.invalidClasse, 11, self.invalidFolder)
        self.assertLess(result, 0)
        result = sp.generate_process_metrics(self.invalidClasse, "qualcosanonBuono", self.repository)
        self.assertLess(result, 0)
        result = sp.generate_process_metrics(self.classe, "qualcosanonBuono", self.invalidFolder)
        self.assertLess(result, 0)
        result = sp.generate_process_metrics(self.invalidClasse, self.diction, self.invalidFolder)
        self.assertLess(result, 0)

    def test_sp_generate_metrics_ck(self):
        result = sp.generate_metrics_ck(self.diction, self.repositoryCK, self.measures)
        self.assertIsInstance(result, DataFrame)
        result = sp.generate_metrics_ck("qualcosanonBuono", self.repositoryCK, self.measures)
        self.assertLess(result, 0)
        result = sp.generate_metrics_ck(self.diction, self.invalidFolder, self.measures)
        self.assertLess(result, 0)
        result = sp.generate_metrics_ck(11, self.invalidFolder, "niente")
        self.assertLess(result, 0)
        result = sp.generate_metrics_ck("qualcosanonBuono", self.repositoryCK, "niente")
        self.assertLess(result, 0)
        result = sp.generate_metrics_ck("qualcosanonBuono", self.invalidFolder, "niente")
        self.assertLess(result, 0)
        result = sp.generate_metrics_ck(self.diction, self.invalidFolder, "niente")
        self.assertLess(result, 0)
        result = sp.generate_metrics_ck(self.diction, self.repositoryCK, "niente")
        self.assertIsInstance(result, DataFrame)



def controllaSeStaTutto():
    nome_directory = 'TestingMetriche'
    cartella_prova_ing_soft = 'Prova-per-ing-soft'
    percorso_directory = os.path.join(os.getcwd(), nome_directory)
    if not os.path.exists(percorso_directory):
        os.makedirs(percorso_directory)
        print(f"La directory '{nome_directory}' è stata creata con successo.")
    else:
        print(f"La directory '{nome_directory}' esiste già.")
    nome_directory2 = os.path.join('TestingMetriche','ck')
    percorso_directory2 = os.path.join(os.getcwd(), nome_directory2)
    if not os.path.exists(percorso_directory2):
        os.makedirs(percorso_directory2)
        print(f"La directory '{nome_directory2}' è stata creata con successo.")
    else:
        print(f"La directory '{nome_directory2}' esiste già.")
    file_papa = 'papa.txt'
    path_papa = os.path.join(percorso_directory, file_papa)
    file_angelone = 'angelone.txt'
    path_angelone = os.path.join(percorso_directory, file_angelone)
    contenuto_papa = 'angelone'
    contenuto_angelone = "angelone\nil mio pap"
    if not os.path.exists(path_papa) and not os.path.exists(path_angelone):
        with open(path_papa, 'w') as file:
            file.write(contenuto_papa)
            print(f"Contenuto scritto in '{file_papa}': '{contenuto_papa}'")
        with open(path_angelone, 'w') as file:
            file.write(contenuto_angelone)
            print(f"Contenuto scritto in '{file_angelone}': '{contenuto_angelone}'")
    else:
        print(f"I file '{file_papa}' e '{file_angelone}' esistono già.")
    percorso_cartella_prova_ing_soft = os.path.join(percorso_directory, cartella_prova_ing_soft)
    percorso_cartella_prova_ck = os.path.join(percorso_directory2, cartella_prova_ing_soft)
    if not os.path.exists(percorso_cartella_prova_ck):
        ru.clone_repo(folder = percorso_cartella_prova_ck)

    if not os.path.exists(percorso_cartella_prova_ing_soft):
        ru.clone_repo(percorso_cartella_prova_ing_soft)




if __name__ == '__main__':
    ru.check_folder("repository")
    ru.check_folder()
    controllaSeStaTutto()
    unittest.main()
