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
from model.RepoModel import RepoModel
from model.ComputingEndpointModel import ComputingEndpointModel
import subprocess as sub
from git import Repo, Commit
from multiprocessing.connection import Connection
from model.Domain import HttpResponse
import subprocess


class RepoModelIT(unittest.TestCase):
    @patch("requests.get")
    def test_DAORepo_cls1(self, get: Mock):
        class ResponseDriver:
            status_code = 200

            def json(self):
                return {
                    "items": [
                        {"name": "name", "html_url": "url", "description": "desc"}
                    ]
                }

        get.return_value = ResponseDriver()
        model = RepoModel()
        # call site sotto test
        result = model.getRepoListByName("repo")
        result = result[0]
        self.assertEqual(result.name, "name")
        self.assertEqual(result.url, "url")
        self.assertEqual(result.description, "desc")

    @patch("requests.get")
    def test_DAORepo_cls2(self, get: Mock):
        class ResponseDriver:
            status_code = 200

            def json(self):
                return {
                    "items": [
                        {"name": "name", "html_url": "url", "description": "desc"}
                    ]
                }

        get.return_value = ResponseDriver()
        model = RepoModel()
        # call site sotto test
        result = model.getRepoListByAuthorAndRepoName("author", "repo")
        result = result[0]
        self.assertEqual(result.name, "name")
        self.assertEqual(result.url, "url")
        self.assertEqual(result.description, "desc")

    @patch("requests.get")
    def test_DAORepo_cls3(self, get: Mock):
        class ResponseDriver:
            status_code = 200

            def json(self):
                return {
                    "items": [
                        {"name": "name", "html_url": "url", "description": "desc"}
                    ]
                }

        get.return_value = ResponseDriver()
        model = RepoModel()
        # call site sotto test
        result = model.getRepoListByAuthor("author")
        result = result[0]
        self.assertEqual(result.name, "name")
        self.assertEqual(result.url, "url")
        self.assertEqual(result.description, "desc")


if __name__ == "__main__":
    unittest.main()
