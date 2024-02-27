import shutil
import threading
import time
import unittest
import sys
import os
import git
from icecream import ic

directory_corrente = os.path.abspath(os.path.dirname(__file__))

divided = directory_corrente.split(os.sep)
final = []

for division in divided:
    if division == "ing-soft2":
        break
    final.append(division)
final.append("ing-soft2")
final_dir = os.sep.join(final)

sys.path.append(final_dir)


from controller.mainPageContoller import MainPageController
from unittest.mock import patch, Mock
import tkinter as tk
from model.LocalRepoModel import LocalRepoModel
import subprocess as sub
from git import Repo


class MainPageControllerIntegrationTest(unittest.TestCase):
    """integration testing basato su call sites"""

    # test integrazione con model per repo locali
    @classmethod
    def setUpClass(self) -> None:
        """setup repoModel"""
        self.globalModel = LocalRepoModel()
        directory_path = "repository"

        if not os.path.exists(directory_path) or not os.path.isdir(directory_path):
            os.mkdir(directory_path)

        self.globalModel.createLocalRepo(
            "https://github.com/CostaMart/Prova-per-ing-soft.git"
        )
        self.globalModel.RepoDataUpdate()

    def test_MPcontroller_LocalRepoModel_cls1(self):
        """testa tutti i call site di LocalRepo in MPcontoller"""
        # callsite 1
        controller = MainPageController()
        controller.globalModel = self.globalModel
        code = controller.getStatusCodeFromLocalModel()

        self.assertIsNotNone(code)

    @patch("requests.get")
    def test_MPcontroller_LocalRepoModel_cls2(self, get: Mock):
        get.return_value = 200
        controller = MainPageController()

        t = controller.requestRepoUpdate(callbackAfter=None, callbackBefore=None)
        t: threading.Thread
        t.join()
        # //// questo è da sistemare
        get.assert_called()

    # test con classe per repo esterni

    def test_MPcontroller_RepoModel_cls1(self):
        repoList = None
        controller = MainPageController()

        def toRun(ls):
            nonlocal repoList
            repoList = ls

        t = controller.request_for_repos("per-ing-soft", toRun)
        t.join()
        self.assertIsNotNone(repoList)

    def test_MPcontroller_RepoModel_cls2(self):
        repoList = None
        controller = MainPageController()

        def toRun(ls):
            nonlocal repoList
            repoList = ls

        t = controller.request_for_repos("repoName:per-ing-soft", toRun)
        t.join()
        self.assertIsNotNone(repoList)

    def test_MPcontroller_RepoModel_cls3(self):
        repoList = None
        controller = MainPageController()

        def toRun(ls):
            nonlocal repoList
            repoList = ls

        t = controller.request_for_repos("author:per-ing-soft", toRun)
        t.join()
        self.assertIsNotNone(repoList)

    def test_MPcontroller_RepoModel_cls4(self):
        directory_path = f"repository"
        if os.path.exists(directory_path) and os.path.isdir(directory_path):
            try:
                # Rimuove la directory e tutto il suo contenuto
                shutil.rmtree(directory_path)
                print(
                    f"La directory '{directory_path}' è stata eliminata con successo."
                )
            except OSError as e:
                print(
                    f"Errore durante l'eliminazione della directory '{directory_path}': {e}"
                )
            else:
                print(
                    f"La directory '{directory_path}' non esiste o non è una directory valida."
                )
        os.mkdir("repository")
        controller = MainPageController()
        controller.get_selected_repo(
            "https://github.com/CostaMart/Prova-per-ing-soft.git"
        )

        rep = None
        try:
            rep = Repo("repository")
        except git.exc.InvalidGitRepositoryError:
            print("no valid repo")

        self.assertIsNotNone(rep)


if __name__ == "__main__":
    unittest.main()
