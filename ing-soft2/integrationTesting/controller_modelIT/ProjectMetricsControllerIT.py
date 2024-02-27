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


from controller.ProjectMetricsContoller import ProjectMetricsController
from unittest.mock import patch, Mock
import tkinter as tk
from model.LocalRepoModel import LocalRepoModel
from model.ComputingEndpointModel import ComputingEndpointModel
import subprocess as sub
from git import Repo
from multiprocessing.connection import Connection


class ProjectControllerIntegrationTest(unittest.TestCase):
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

        # init computationModel

        class myConnectionDriver:
            """imita il comportamento di Connection, non di interesse in questo test"""

            def send(self, msg):
                return

            def recv(self):
                return "msg"

        self.comp = ComputingEndpointModel()
        self.comp.child_conn = myConnectionDriver()
        self.comp.parent_conn = myConnectionDriver()

    # da qui test interazioni con LocalDAO
    def test_localRepo_cls1(self):
        class ReleasesMock:
            releases = "rel"

            def __init__(self):
                return

        # sostiuisce le componenti di più alto livello
        mock = Mock(return_value=["one", "two"])
        mockTwo = Mock(return_value=ReleasesMock())
        mockThree = Mock(return_value="correct value")
        with patch(
            "model.DataAccessLayer.LocalDAO.LocalDAO.getRepoInfoFromGit", mock
        ), patch(
            "model.DataAccessLayer.DAORepo.DAORepo.getRepoByNameeAuthor", mockTwo
        ), patch(
            "model.DataAccessLayer.DAORepo.DAORepo.get_all_release_tag_repo",
            mockThree,
        ):
            self.globalModel.RepoDataUpdate()
            controller = ProjectMetricsController()
            controller.localModel = self.globalModel

            # il seguente è il call point sotto test
            data = controller.getLocalRepoData()
            self.assertIsNotNone(data)

    def test_localRepo_cls2(self):
        controller = ProjectMetricsController()
        theList = controller.getClassesList("7832e47e2ffbd512ec86956eea718fa5aae60e44")
        self.assertIsNotNone(theList)

    def test_localRepo_cls3(self):
        mock = Mock(return_value=["class 0"])
        with patch(
            "model.DataAccessLayer.LocalDAO.LocalDAO.get_commits_with_class", mock
        ):
            # call point sotto test
            controller = ProjectMetricsController()
            theList = controller.getCommitWithClassList("prova")
            self.assertEqual(theList[0], "class 0")

    def test_localRepo_cls4(self):
        mock = Mock(return_value=["class 0"])
        with patch("model.DataAccessLayer.LocalDAO.LocalDAO.dataCommitLinkYear", mock):
            controller = ProjectMetricsController()
            mylist = []

            def toRun(lista):
                nonlocal mylist
                mylist = lista

            # call point sotto test
            t = controller.updateCommitsListByYear(1, "branch", callback=toRun)
            t.join()
            self.assertIsNotNone(mylist[0])

    def test_localRepo_cls5(self):
        mock = Mock(return_value=["year"])
        with patch(
            "model.DataAccessLayer.LocalDAO.LocalDAO.extract_yearsList_with_branches",
            mock,
        ):
            controller = ProjectMetricsController()
            # call point sotto test
            theList = controller.getYearList()
            self.assertIsNotNone(theList)

    def test_localRepo_cls5(self):
        mock = Mock(return_value="the commit")
        with patch(
            "model.DataAccessLayer.LocalDAO.LocalDAO.getCommit",
            mock,
        ):
            controller = ProjectMetricsController()
            # call point sotto test
            commit = controller.getCommitByhash("hash")
            self.assertIsNotNone(commit)

    def test_localRepo_cls6(self):
        mock = Mock(return_value="the commit")
        with patch(
            "model.DataAccessLayer.LocalDAO.LocalDAO.getCommitsFromDate",
            mock,
        ):
            theList = None
            controller = ProjectMetricsController()

            def toRun(list):
                nonlocal theList
                theList = list

            # call point sotto test
            t = controller.getCommiListFromDate("date", "yearToarrive", toRun)
            t.join()
            self.assertIsNotNone(theList)

    def test_localRepo_cls7(self):
        mock = Mock(return_value=["myCommit"])
        with patch(
            "model.DataAccessLayer.LocalDAO.LocalDAO.getCommitInInterval",
            mock,
        ):
            theList = None
            controller = ProjectMetricsController()

            # call point sotto test
            theList = controller.getCommitsBetweenHashes("hash1", "hash2")
            self.assertIsNotNone(theList)

    # computing endPoint call sites
    def test_computingEndpoint_cls1(self):
        mock = Mock(return_value="res")
        mock2 = Mock(return_value="result")

        result = None

        def toRun(message):
            nonlocal result
            result = message

        controller = ProjectMetricsController()
        controller.computingEndPointModel = self.comp
        t = controller.request_service("the message", toRun)
        t.join()

        self.assertIsNotNone(result)


if __name__ == "__main__":
    unittest.main()
