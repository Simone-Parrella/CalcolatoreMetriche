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
from view.ProjectMetricsPage import ProjectMetricsPage
from model.LocalRepoModel import LocalRepoModel
import subprocess as sub
from git import Repo, Commit
from multiprocessing.connection import Connection
from model.Domain import HttpResponse
import psutil
import subprocess
import tkinter


class ProjectMetricsPageIT(unittest.TestCase):
    # integrazione con ProjectMetricsController
    @patch("controller.ProjectMetricsContoller.ProjectMetricsController.getYearList")
    @patch(
        "controller.ProjectMetricsContoller.ProjectMetricsController.getLocalRepoData"
    )
    @patch("threading.Thread.start")
    @patch("model.LocalRepoModel.LocalRepoModel.getCommitInInterval")
    def test_PRJMC_cls1(self, interval: Mock, start: Mock, cont: Mock, years: Mock):
        class repodataDriver:
            name = "name"
            git_url = "url"
            license = {"name": "name"}
            owner = {"login": "login", "owner": "owner", "url": "url"}

        years.return_value = {2000: ["branch1"]}
        cont.return_value = repodataDriver()
        interval.return_value = ["com1", "com2"]
        frame = tkinter.Button()
        page = ProjectMetricsPage(master=frame)
        # questa chiamata testa due call site verso il controller
        page.start_dataRequest()
        interval.assert_called()
        start.assert_called()

    @patch("controller.ProjectMetricsContoller.ProjectMetricsController.getYearList")
    @patch(
        "controller.ProjectMetricsContoller.ProjectMetricsController.getLocalRepoData"
    )
    @patch("threading.Thread.start")
    @patch("model.LocalRepoModel.LocalRepoModel.getCommitInInterval")
    def test_PRJMC_cls2(self, interval: Mock, start: Mock, cont: Mock, years: Mock):
        class repodataDriver:
            name = "name"
            git_url = "url"
            license = {"name": "name"}
            owner = {"login": "login", "owner": "owner", "url": "url"}

        years.return_value = {2000: ["branch1"]}
        cont.return_value = repodataDriver()
        interval.return_value = ["com1", "com2"]
        frame = tkinter.Button()
        page = ProjectMetricsPage(master=frame)
        # questa è la chiamata del call site
        page.start_CKdataRequest()
        interval.assert_called()
        start.assert_called()

    @patch("controller.ProjectMetricsContoller.ProjectMetricsController.getYearList")
    @patch(
        "controller.ProjectMetricsContoller.ProjectMetricsController.getLocalRepoData"
    )
    @patch("threading.Thread.start")
    def test_PRJMC_cls3(self, start: Mock, cont: Mock, years: Mock):
        class repodataDriver:
            name = "name"
            git_url = "url"
            license = {"name": "name"}
            owner = {"login": "login", "owner": "owner", "url": "url"}

        years.return_value = {2000: ["branch1"]}
        cont.return_value = repodataDriver()
        frame = tkinter.Button()
        page = ProjectMetricsPage(master=frame)
        # questa è la chiamata del call site
        page.update_branchList("2000")
        start.assert_called()

    @patch("model.LocalRepoModel.LocalRepoModel.getClassListFromGivenCommit")
    @patch("controller.ProjectMetricsContoller.ProjectMetricsController.getYearList")
    @patch(
        "controller.ProjectMetricsContoller.ProjectMetricsController.getLocalRepoData"
    )
    @patch("threading.Thread.start")
    def test_PRJMC_cls4(self, start: Mock, cont: Mock, years: Mock, repo: Mock):
        class repodataDriver:
            name = "name"
            git_url = "url"
            license = {"name": "name"}
            owner = {"login": "login", "owner": "owner", "url": "url"}

        repo.return_value = ["commit2"]
        years.return_value = {2000: ["branch1"]}
        cont.return_value = repodataDriver()
        frame = tkinter.Button()
        page = ProjectMetricsPage(master=frame)
        # questa chiamata testa due call site verso il controller
        page.updateClassList("12345678901234567890")
        start.assert_called()

    @patch("model.LocalRepoModel.LocalRepoModel.getCommitByHash")
    @patch("controller.ProjectMetricsContoller.ProjectMetricsController.getYearList")
    @patch(
        "controller.ProjectMetricsContoller.ProjectMetricsController.getLocalRepoData"
    )
    @patch("threading.Thread.start")
    def test_PRJMC_cls5(self, start: Mock, cont: Mock, years: Mock, commit: Mock):
        class commitDriver:
            committer_date = datetime(year=2000, month=12, day=1)

        class repodataDriver:
            name = "name"
            git_url = "url"
            license = {"name": "name"}
            owner = {"login": "login", "owner": "owner", "url": "url"}

        commit.return_value = commitDriver()
        years.return_value = {2000: ["branch1"]}
        cont.return_value = repodataDriver()
        frame = tkinter.Button()
        page = ProjectMetricsPage(master=frame)
        # questa chiamata testa due call site verso il controller
        page.start_updateArriveCommitList("calss")
        start.assert_called()


if __name__ == "__main__":
    unittest.main()
