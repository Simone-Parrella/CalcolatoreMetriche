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
from model.ComputingEndpointModel import ComputingEndpointModel
import subprocess as sub
from git import Repo, Commit
from multiprocessing.connection import Connection
from model.Domain import HttpResponse
import psutil
import subprocess


class ComputingEndpointModelIT(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        # funge anche da metodo di test per activateLocal
        self.model = ComputingEndpointModel()
        # call site sotto test
        self.p = self.model.activateLocal()

    def test_otherProcess_cls1(self):
        # verifica che la chiamata nel metodo di setup funzioni
        pid = self.p.pid
        self.assertTrue(psutil.pid_exists(pid))

    def test_otherProcess_cls2(self):
        time.sleep(3)
        # call site sotto test
        r = self.model.isActiveLocal()
        self.assertEqual(r, True)

    def test_otherProcess_cls3(self):
        # call site sotto test
        p = self.model.sendMessageToEndpoint({"fun": "ping", "num1": 1, "num2": 2})
        # testa anche questo call site
        value = self.model.receiveMessageFromEndpoint()
        self.assertEqual(value, 3)

    def test_otherProcess_cls3(self):
        pid = self.p.pid
        # call site sotto test
        self.model.destroy()
        time.sleep(3)
        self.assertFalse(psutil.pid_exists(pid))


if __name__ == "__main__":
    unittest.main()
