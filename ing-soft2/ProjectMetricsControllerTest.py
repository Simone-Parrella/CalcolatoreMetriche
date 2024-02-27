import unittest
from unittest import mock
from unittest.mock import MagicMock, patch
from pydriller import Commit
from controller.ProjectMetricsContoller import ProjectMetricsController
from model import Domain
from model.ComputingEndpointModel import ComputingEndpointModel

from model.LocalRepoModel import LocalRepoModel


class TestProjectMetricsController(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        print("sto eseguendo project metrics controller test")

    def setUp(self):
        # Create a mock for LocalRepoModel
        self.local_model_mock = MagicMock(spec=LocalRepoModel)

        # Create a mock for ComputingEndpointModel
        self.computing_endpoint_model_mock = MagicMock(spec=ComputingEndpointModel)

        # Create an instance of ProjectMetricsController with the mocks
        self.controller = ProjectMetricsController()
        self.controller.localModel = self.local_model_mock
        self.controller.computingEndPointModel = self.computing_endpoint_model_mock

    def test_getLocalRepoData(self):
        # Mock the behavior of getRepoData
        mock_repo_data = Domain.Repository(name='MockRepo', html_url='http://mockrepo.com',
                                           description='Mock description')
        self.local_model_mock.getRepoData.return_value = mock_repo_data

        # Call the method to be tested
        result = self.controller.getLocalRepoData()

        # Assert the result
        self.assertEqual(result.name, 'MockRepo')
        self.assertEqual(result.url, 'http://mockrepo.com')
        self.assertEqual(result.description, 'Mock description')

    def test_getClassesList(self):
        # Mock the behavior of getClassListFromGivenCommit
        self.local_model_mock.getClassListFromGivenCommit.return_value = {'ClassA.py', 'ClassB.py'}

        # Call the method to be tested
        result = self.controller.getClassesList(commitHash='mock_commit_hash')

        # Assert the result
        self.assertEqual(result, {'ClassA.py', 'ClassB.py'})

    def test_updateRepoYearList(self):
        # Mock the behavior of the callback function
        callback_mock = MagicMock()

        # Call the method to be tested
        self.controller.updateRepoYearList(callback=callback_mock)

        # Assert that the callback was called
        callback_mock.assert_called_once()

    def test_updateCommitsListByYear(self):
        # Simulare il comportamento del localModel.getCommiListByYear
        with patch.object(self.controller.localModel, 'getCommiListByYear', return_value=['commit1', 'commit2']):
            # Verificare che il metodo chiami la callback con la lista di commit
            callback_mock = MagicMock()
            self.controller.updateCommitsListByYear(2023, 'main', callback_mock)
            callback_mock.assert_called_once_with(['commit1', 'commit2'])

    def test_getYearList(self):
        # Simula il comportamento del localModel.getYearList
        with patch.object(self.controller.localModel, 'getYearList', return_value={2021: {'ClassA', 'ClassB'}}):
            year_list = self.controller.getYearList()
        self.assertIsInstance(year_list, dict)
        self.assertIn(2021, year_list)
        self.assertIsInstance(year_list[2021], set)

    def test_get_commit_by_hash(self):
        # Crea un mock di un oggetto Commit
        commit_mock = mock.MagicMock(spec=Commit)
        self.controller.localModel.getCommitByHash = MagicMock(return_value=commit_mock)
        hash_to_test = 'hash1'

        # Chiama il metodo getCommitByHash
        result = self.controller.getCommitByhash(hash_to_test)

        # Verifica che il metodo sia stato chiamato con l'hash specificato
        self.controller.localModel.getCommitByHash.assert_called_once_with(hash_to_test)
        # Verifica che il risultato sia il mock di Commit
        self.assertEqual(result, commit_mock)

    def test_getCommiListFromDate(self):
        # Simulare il comportamento del localModel.getCommiListFromDate
        with patch.object(self.controller.localModel, 'getCommiListFromDate', return_value=['commit1', 'commit2']):
            # Verificare che il metodo chiami la callback con la lista di commit
            callback_mock = MagicMock()
            self.controller.getCommiListFromDate('2023-01-01', 2023, callback_mock)
            callback_mock.assert_called_once_with(['commit1', 'commit2'])

    def test_getCommitsBetweenHashes(self):
        # Simulare il comportamento del localModel.getCommitInInterval
        with patch.object(self.controller.localModel, 'getCommitInInterval', return_value=['commit3', 'commit4']):
            commits_list = self.controller.getCommitsBetweenHashes('hash_start', 'hash_end')
        self.assertIsInstance(commits_list, list)
        self.assertEqual(commits_list, ['commit3', 'commit4'])

    def test_request_service(self):
        # Simulare il comportamento del computingEndPointModel
        with patch.object(self.controller.computingEndPointModel, 'sendMessageToEndpoint'), \
                patch.object(self.controller.computingEndPointModel, 'receiveMessageFromEndpoint',
                             return_value='result'):
            # Verificare che il metodo chiami la callback con il risultato
            callback_mock = MagicMock()
            self.controller.request_service('some_message', callback_mock)
            callback_mock.assert_called_once_with('result')
