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
from view.App import IngSoftApp
from model.LocalRepoModel import LocalRepoModel
import subprocess as sub
from git import Repo, Commit
from multiprocessing.connection import Connection
from model.Domain import HttpResponse
import psutil
import subprocess
import tkinter


class IngSoftAppIT(unittest.TestCase):
    @patch("model.LocalRepoModel.LocalRepoModel.RepoDataUpdate")
    def test_startAppCont_cls1(self, model: Mock):
        model.return_value = "datas"
        app = IngSoftApp(gitv="g", endpointStatus=False)
        model.assert_called_once()


if __name__ == "__main__":
    unittest.main()
