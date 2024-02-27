from datetime import datetime
import shutil
import threading
import time
import unittest
import sys
import os
from urllib.parse import urlparse
import git
from icecream import ic
from numpy import True_

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


from controller.ProjectMetricsContoller import ProjectMetricsController
from unittest.mock import patch, Mock
import tkinter as tk
from view.MainPage import MainPage
from model.LocalRepoModel import LocalRepoModel
import subprocess as sub
from git import Repo, Commit
from multiprocessing.connection import Connection
from model.Domain import HttpResponse
import psutil
import subprocess
import tkinter


class MainPageIT(unittest.TestCase):
    @patch("model.LocalRepoModel.LocalRepoModel.getRepoData")
    @patch("threading.Thread.start")
    def test_MainPageContIT_cls1(self, start: Mock, get: Mock):
        master = tkinter.Frame()
        # call site sotto test
        view = MainPage(master, "false")
        get.return_value = "updated"
        start.assert_called()
        get.assert_called_once()

    @patch("threading.Thread.start")
    def test_MainPageContIT_cls2(self, start: Mock):
        master = tkinter.Frame()
        view = MainPage(master, "false")
        # call site sotto test
        view._start_request()
        start.assert_called()

    @patch("threading.Thread.start")
    def test_MainPageContIT_cls3(self, start: Mock):
        master = tkinter.Frame()
        view = MainPage(master, "false")
        # call site sotto test
        view._recoverRepoData()
        start.assert_called()

    @patch("threading.Thread.start")
    def test_MainPageContIT_cls4(self, start: Mock):
        master = tkinter.Frame()
        view = MainPage(master, "false")
        # call site sotto test
        view._initRepoData()
        start.assert_called()

    @patch("model.LocalRepoModel.LocalRepoModel.switch_branch")
    @patch("model.LocalRepoModel.LocalRepoModel.createLocalRepo")
    @patch("threading.Thread.start")
    def test_MainPageContIT_cls5(self, start: Mock, create: Mock, switch: Mock):
        def get_local_repo_url():
            try:
                repo = Repo("repository")
                remote_urls = [remote.url for remote in repo.remotes]

                return remote_urls[0] if remote_urls else None
            except Exception as e:
                print(f"Errore: {e}")
                return None

        url = get_local_repo_url()
        controller = LocalRepoModel()
        controller.createLocalRepo(
            "https://github.com/CostaMart/Prova-per-ing-soft.git"
        )

        master = tkinter.Frame()
        view = MainPage(master, "false")
        view.loading = False
        # call site sotto test
        view._downloadRepo(value="val", intero=1)
        controller
        start.assert_called()

        if url == None:
            controller.createLocalRepo(url)


if __name__ == "__main__":
    unittest.main()
