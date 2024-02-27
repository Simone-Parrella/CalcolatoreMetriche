import os
import shutil
import unittest
from unittest.mock import patch, MagicMock
import requests
from model.LocalRepoModel import LocalRepoModel


class TestLocalRepoModel(unittest.TestCase):

    test_directory = None
    local_repo_model = None

    @classmethod
    @patch('model.DataAccessLayer.LocalDAO')
    @patch('model.LocalRepoModel.DAORepo')
    def setUpClass(self, mock_dao_repo, mock_local_dao):
        print("sto eseguendo local repo model testing white box")
        self.local_repo_model = LocalRepoModel()
        self.local_repo_model.CRUD = mock_dao_repo
        self.local_repo_model.LocalDAO = mock_local_dao
        # repo di prova
        self.repo_url = "https://github.com/Appendium/flatpack"
        self.test_directory = "repository"
        os.makedirs(self.test_directory, exist_ok=True)

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree("repository", ignore_errors=True)

    def test_getRepoData(self):
        # Testa il caso in cui repoData è None
        self.local_repo_model.repoData = None
        self.assertIsNone(self.local_repo_model.getRepoData())

        # Testa il caso in cui repoData non è None
        self.local_repo_model.repoData = "Test data"
        self.assertEqual(self.local_repo_model.getRepoData(), "Test data")

    def test_RepoDataUpdate(self):
        # Testa il caso in cui name e repoName sono None
        self.local_repo_model.LocalDAO.getRepoInfoFromGit.return_value = (None, None)
        self.local_repo_model.RepoDataUpdate()
        self.local_repo_model.CRUD.getRepoByNameeAuthor.assert_not_called()

        # Testa il caso in cui name e repoName non sono None, ma CRUD.getRepoByNameeAuthor ritorna None
        self.local_repo_model.LocalDAO.getRepoInfoFromGit.return_value = ("name", "repoName")
        self.local_repo_model.CRUD.getRepoByNameeAuthor.return_value = None
        self.local_repo_model.RepoDataUpdate()
        self.assertIsNone(self.local_repo_model.repoData)

        # Testa il caso in cui name e repoName non sono None, e CRUD.getRepoByNameeAuthor ritorna un valore
        mock_object = MagicMock()
        mock_object.name = "author:name repoName:repoName"
        mock_object.tag_releases = ["v1.0","v2.0","v3.0"]
        self.local_repo_model.CRUD.getRepoByNameeAuthor.return_value = mock_object
        self.local_repo_model.CRUD.get_all_release_tag_repo.return_value = mock_object.tag_releases
        self.local_repo_model.LocalDAO.getRepoInfoFromGit.return_value = ("name", "repoName")
        self.local_repo_model.RepoDataUpdate()
        self.assertEqual(self.local_repo_model.repoData, mock_object)
        self.assertEqual(self.local_repo_model.repoData.releases, mock_object.tag_releases)

    @patch('os.path.exists')
    @patch('os.makedirs')
    def test_CheckRepoDir_directory_exists(self, mock_makedirs, mock_exists):
        # Testa il caso in cui la directory esiste
        mock_exists.return_value = True
        self.local_repo_model._CheckRepoDir("existing_directory")
        mock_makedirs.assert_not_called()

    @patch('os.path.exists')
    @patch('os.makedirs')
    def test_CheckRepoDir_directory_does_not_exist(self, mock_makedirs, mock_exists):
        # Testa il caso in cui la directory non esiste
        mock_exists.return_value = False
        self.local_repo_model._CheckRepoDir("non_existing_directory")
        mock_makedirs.assert_called_once_with("non_existing_directory")

    def test_createLocalRepo(self):
        repoName = 'flatpack'
        url = f"https://api.github.com/search/repositories?q={repoName}+language:java"
        response = requests.get(url)
        risultati = response.json()["items"]
        self.repo_url = risultati[0]["html_url"]
        self.local_repo_model.createLocalRepo(url)
        self.local_repo_model.LocalDAO.cloneRepository.assert_called_once_with(url)

    def test_get_status_code(self):
        self.local_repo_model.CRUD.last_http_response = 200
        status_code = self.local_repo_model.get_status_code()
        self.assertEqual(status_code, 200)

    def test_getAllJavaClassProject(self):
        directory = "test_directory"
        self.local_repo_model.getAllJavaClassProject(directory)
        self.local_repo_model.LocalDAO.findJavaClass.assert_called_once_with(directory)

    def test_getCommitWithClassList(self):
        class_name = "TestClass"
        self.local_repo_model.getCommitWithClassList(class_name)
        self.local_repo_model.LocalDAO.get_commits_with_class.assert_called_once_with(class_name, "repository")

    def test_getYearList(self):
        self.local_repo_model.getYearList()
        self.local_repo_model.LocalDAO.extract_yearsList_with_branches.assert_called_once()

    def test_getClassListFromGivenCommit(self):
        commit = "test_commit"
        self.local_repo_model.getClassListFromGivenCommit(commit)
        self.local_repo_model.LocalDAO.getClassListFromGivenCommit.assert_called_once_with(commit)

    def test_getCommiListByYear(self):
        branch = "test_branch"
        year = 2023
        self.local_repo_model.getCommiListByYear(branch, year)
        self.local_repo_model.LocalDAO.dataCommitLinkYear.assert_called_once_with(branch, year)

    def test_getCommiListFromDate(self):
        date = "2023-01-01"
        yearToArrive = 2024
        self.local_repo_model.getCommiListFromDate(date, yearToArrive)
        self.local_repo_model.LocalDAO.getCommitsFromDate.assert_called_once_with(date, yearToArrive, "repository")

    def test_getCommitByHash(self):
        hash = "test_hash"
        self.local_repo_model.getCommitByHash(hash)
        self.local_repo_model.LocalDAO.getCommit.assert_called_once_with(hash)

    def test_getCommitInInterval(self):
        start_hash = "start_hash"
        end_hash = "end_hash"
        self.local_repo_model.getCommitInInterval(start_hash, end_hash)
        self.local_repo_model.LocalDAO.getCommitInInterval.assert_called_once_with(start_hash, end_hash)

    def test_switch_branch(self):
        branch = "test_branch"
        self.local_repo_model.switch_branch(branch)
        self.local_repo_model.LocalDAO.checkout_to.assert_called_once_with(branch)





if __name__ == '__main__':
    unittest.main()