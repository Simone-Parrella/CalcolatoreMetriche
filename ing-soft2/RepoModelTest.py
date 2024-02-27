import unittest
from unittest.mock import MagicMock, patch

from model.DataAccessLayer import DAORepo
from model.RepoModel import RepoModel
import requests


class RepoModelTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        print("sto eseguendo repo model test")

    def setUp(self):
        self.repo_model = RepoModel()

    def test_get_repo_list_by_name_empty_name(self):
        """Test getting repository list with an empty name"""
        repo_list = self.repo_model.getRepoListByName('')
        self.assertEqual(repo_list, [])

    def test_A_get_repo_list_by_name_valid_name(self):
        """Test getting repository list with a valid name"""
        repo_list = self.repo_model.getRepoListByName("java")
        self.assertTrue(len(repo_list) > 0)

    def test_C_get_repo_list_by_author_and_repo_name_empty_author(self):
        """Test getting repository list with an empty author and valid repo name"""
        repo_list = self.repo_model.getRepoListByAuthorAndRepoName('', 'spring-boot')
        self.assertEqual(repo_list, None)

    def test_B_get_repo_list_by_author_and_repo_name_valid_author_empty_repo_name(self):
        """Test getting repository list with a valid author and empty repo name"""
        repo_list = self.repo_model.getRepoListByAuthorAndRepoName('octokit', '')
        self.assertEqual(repo_list, [])

    @patch('requests.get')
    def test_D_get_repo_list_by_author_and_repo_name_valid_author_valid_repo_name(self, mock_get):
        """Test getting repository list with a valid author and valid repo name"""

        mock_get.return_value.json.return_value = {"items": [{"owner": "test_owner", "name": "test_repo"
                                                              ,"html_url": "this_url"
                                                              ,"description": "this_description"}]}

        # Esegui la funzione che vuoi testare
        repo_list = self.repo_model.getRepoListByAuthorAndRepoName("test_owner", "test_repo")

        # Verifica che il risultato sia corretto
        self.assertTrue(len(repo_list) > 0)

    def test_get_repo_list_by_author_empty_author(self):
        """Test getting repository list by author with an empty author"""
        repo_list = self.repo_model.getRepoListByAuthor('')
        self.assertEqual(repo_list, [])

    @patch('requests.get')
    def test_get_repo_list_by_author_valid_author(self, mock_requests_get):
        """Test getting repository list by author with a valid author"""
        # Configura il comportamento desiderato per il mock requests.get
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value =  {"items": [{"owner": "test_owner", "name": "test_repo"
                                                              ,"html_url": "this_url"
                                                              ,"description": "this_description"}]}
        mock_requests_get.return_value = mock_response

        # Esegui la funzione che vuoi testare
        repo_list = self.repo_model.getRepoListByAuthor('octokit')

        # Verifica che il risultato sia corretto
        self.assertTrue(len(repo_list) > 0)

    def test_get_repo_list_by_name_empty_name_with_spaces(self):
        """Test getting repository list with an empty name with spaces"""
        repo_list = self.repo_model.getRepoListByName(' ')
        self.assertEqual(repo_list, [])

    def test_get_repo_list_by_author_valid_author_with_spaces(self):
        """Test getting repository list by author with an author with spaces"""
        repo_list = self.repo_model.getRepoListByAuthor('octokit ')
        self.assertEqual(repo_list, [])


