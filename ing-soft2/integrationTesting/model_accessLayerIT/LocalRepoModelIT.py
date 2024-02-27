from datetime import datetime
import shutil
import threading
import time
import unittest
import sys
import os
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
from model.LocalRepoModel import LocalRepoModel
from model.ComputingEndpointModel import ComputingEndpointModel
import subprocess as sub
from git import Repo, Commit
from multiprocessing.connection import Connection
from model.Domain import HttpResponse
import subprocess


class LocalRepoModelIT(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        def get_local_repo_url():
            try:
                # Esegui il comando git per ottenere l'URL remoto del repository
                result = subprocess.run(
                    ["git", "config", "--get", "remote.origin.url"],
                    capture_output=True,
                    text=True,
                    check=True,
                    cwd="repository",
                )
                url = (
                    result.stdout.strip()
                )  # Ottieni l'URL dalla risposta e rimuovi eventuali spazi bianchi
                return url
            except subprocess.CalledProcessError as e:
                print(f"Errore durante il recupero dell'URL del repository: {e}")
                return None

        self.repoUrl = get_local_repo_url()

    # test integrazione con LocalDAO
    def test_LocalDAO_cls1(self):
        # funzione sotto test
        repo = LocalRepoModel()
        self.assertIsNotNone(repo.CRUD)

    @patch("shutil.rmtree")
    @patch("subprocess.call")
    def test_LocalDAO_cls2(self, rmtree: Mock, subP: Mock):
        repo = LocalRepoModel()
        # funzione sotto test
        repo.createLocalRepo("myRepo")
        rmtree.assert_called_once()
        subP.assert_called_once()

    @patch("os.path.abspath")
    @patch("os.walk")
    def test_LocalDAO_cls3(self, walk: Mock, path: Mock):
        path.return_value = "path"
        walk.return_value = [("root", "dirs", ["files.java"])]
        local = LocalRepoModel()
        # funzione sotto test
        value = local.getAllJavaClassProject("repository")
        self.assertIsNotNone(value)

    @patch("git.repo.base.Repo.iter_commits")
    @patch("git.Repo")
    def test_LocalDAO_cls4(self, repo: Mock, iterCommit: Mock):
        class treeDriver:
            def __getitem__(self, index):
                return "commitHash"

        class CommitDriver:
            tree = treeDriver()

        repo.return_value = Repo()
        iterCommit.return_value = [CommitDriver()]

        local = LocalRepoModel()
        # call sotto test
        value = local.getCommitWithClassList("commitHash")
        self.assertEqual(value, iterCommit.return_value)

    @patch("pydriller.Repository.traverse_commits")
    def test_LocalDAO_cls5(self, traverse: Mock):
        class CommitDriver:
            committer_date = datetime(year=2023, month=12, day=23)
            branches = ["branch1", "branch2"]

        traverse.return_value = [CommitDriver()]
        local = LocalRepoModel()
        # call sotto test
        year = local.getYearList()
        self.assertEqual(year, {2023: {"branch1", "branch2"}})

    @patch("git.Tree.traverse")
    @patch("git.Tree")
    @patch("git.objects.commit.Commit.tree")
    @patch("git.objects.commit.Commit")
    @patch("git.repo.base.Repo.commit")
    def test_LocalDAO_cls6(
        self,
        commitfun: Mock,
        repoCommit: Mock,
        commitTree: Mock,
        tree: Mock,
        traverse: Mock,
    ):
        class mYTree:
            def traverse(self):
                return [
                    git.Blob(
                        "local",
                        "12345678901234567890".encode("utf-8"),
                        path="myfile.java",
                    )
                ]

        class myCommitDriver:
            tree = mYTree()

            def be():
                return

        commitfun.return_value = myCommitDriver()
        commitTree.return_value = mYTree()

        local = LocalRepoModel()
        # call site sotto test
        value = local.getClassListFromGivenCommit("commit1")
        self.assertEqual(value, {"myfile.java"})

    @patch("pydriller.repository.Repository.traverse_commits")
    def test_LocalDAO_cls7(self, traverseFun: Mock):
        traverseFun.return_value = ["commit1", "commit2"]
        local = LocalRepoModel()
        # call site sotto test
        myList = local.getCommiListByYear(branch="b1", year=1999)
        self.assertEqual(myList, traverseFun.return_value)

    @patch("pydriller.repository.Repository.traverse_commits")
    def test_LocalDAO_cls8(self, traverseFun: Mock):
        traverseFun.return_value = ["commit1", "commit2"]
        local = LocalRepoModel()
        # call site sotto test
        myList = local.getCommiListFromDate(
            datetime(year=2020, month=12, day=25), yearToArrive=2022
        )
        self.assertEqual(myList, traverseFun.return_value)

    @patch("pydriller.repository.Repository.traverse_commits")
    def test_LocalDAO_cls8(self, traverseFun: Mock):
        traverseFun.return_value = ["commit1", "commit2"]
        local = LocalRepoModel()
        # call site sotto test
        myList = local.getCommiListFromDate(
            datetime(year=2020, month=12, day=25), yearToArrive=2022
        )
        self.assertEqual(myList, traverseFun.return_value)

    @patch("pydriller.repository.Repository")
    @patch("pydriller.repository.Repository.traverse_commits")
    def test_LocalDAO_cls9(self, traverseFun: Mock, repo: Mock):
        class myCommitDriver:
            hash = "12345678901234567890"

        traverseFun.return_value = [myCommitDriver()]
        local = LocalRepoModel()
        # call site sotto test
        myCom = local.getCommitByHash(hash="12345678901234567890")
        self.assertEqual(myCom, traverseFun.return_value[0])

    @patch("pydriller.repository.Repository")
    @patch("pydriller.repository.Repository.traverse_commits")
    def test_LocalDAO_cls10(self, traverseFun: Mock, repo: Mock):
        class myCommitDriver:
            def __init__(self, hash="12345678901234567890"):
                self.hash = hash
                self.committer_date = 1

        traverseFun.return_value = [
            myCommitDriver(),
            myCommitDriver("12345678901234567891"),
        ]
        local = LocalRepoModel()
        # call site sotto test
        myCom = local.getCommitInInterval(
            start_hash="12345678901234567890", end_hash="12345678901234567891"
        )
        ic(myCom)
        self.assertEqual(
            myCom,
            {
                "12345678901234567890": {"date": 1, "hash": "12345678901234567890"},
                "12345678901234567891": {"date": 1, "hash": "12345678901234567891"},
            },
        )

    @patch("subprocess.check_call")
    def test_LocalDAO_cls11(self, check_call: Mock):
        local = LocalRepoModel()
        # call site sotto test
        local.switch_branch("b1")
        check_call.assert_called_once_with(["git", "checkout", "b1"], cwd="repository")

    # da qui test di integrazione con DAORepo
    @patch("model.Domain.HttpResponse")
    @patch("requests.get")
    def test_DAORepo_cls1(self, get: Mock, Httpresp: Mock):
        class ResponseDriver:
            status_code = 200

            def json(self):
                return JsonDeriver()

        class ResponseDriver1:
            status_code = 200

            def json(self):
                return [{"tag_name": "rel"}]

        class JsonDeriver:
            items = {}

            def keys(self):
                return ["key1"]

            def __setitem__(self, key, item):
                self.items[key] = item

            def __getitem__(self, value):
                return "value"

        class HttpReponseDriver:
            def __init__(self, code, json):
                self.status_code = code
                self.json = JsonDeriver()

        Httpresp.return_value = HttpReponseDriver(200, {"releases": "tag"})

        get.side_effect = [ResponseDriver(), ResponseDriver1()]
        print("ciao")
        local = LocalRepoModel()
        local.repoData = None
        local.createLocalRepo("https://github.com/CostaMart/Prova-per-ing-soft.git")
        # call site sotto test
        val = local.RepoDataUpdate()
        get.assert_called()
        self.assertIsNotNone(local.repoData)
        self.assertIsNotNone(local.repoData.releases)

    @classmethod
    def tearDownClass(self):
        local = LocalRepoModel()
        local.createLocalRepo(self.repoUrl)


if __name__ == "__main__":
    unittest.main()
