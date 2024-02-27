import unittest
from unittest.mock import patch
from model.DataAccessLayer.DAORepo import DAORepo
import unittest
from unittest.mock import MagicMock, patch


class TestDAORepo(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        print("Sto eseguendo testDAORepo")

    def setUp(self):
        # Creare un'istanza di DAORepo
        self.dao_repo = DAORepo()


    @patch('model.DataAccessLayer.DAORepo')
    def test_get_java_repo_list_for_author_and_repo_Negative(self, mock_get):
        # Test Case: Invalid author and repo_name
        dao_repo = DAORepo()
        mock_get.return_value.status_code = 200  # Assuming a successful response
        mock_get.return_value.json.return_value = {'not_items_key': 'some_value'}  # Modify the response structure
        result = dao_repo.getJavaRepoListForAuthorAndRepo("nonexistent_author", "nonexistent_repo")
        self.assertEqual(result, None)
    @patch('requests.get')
    def test_get_repo_list_by_author_Negative(self, mock_requests_get):
        # Configurare il mock per restituire un oggetto di risposta con stato diverso da 200
        mock_response = MagicMock()
        mock_response.status_code = 404
        mock_requests_get.return_value = mock_response

        # Eseguire il metodo sotto test
        result = self.dao_repo.getRepoListByAuthor("nonexistent_author")

        # Assert sul risultato
        self.assertEqual(len(result), 0)  # Nessun risultato dovrebbe essere restituito per un'autore inesistente
        self.assertEqual(self.dao_repo.last_http_response.status_code, 404)

    @patch('requests.get')
    def test_get_all_release_tag_repo_EmptyResponse(self, mock_requests_get):
        # Configurare il mock per restituire un oggetto di risposta con stato 200 ma senza dati
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = []
        mock_requests_get.return_value = mock_response

        # Eseguire il metodo sotto test
        result = self.dao_repo.get_all_release_tag_repo("empty_owner", "empty_repo")

        # Assert sul risultato
        self.assertEqual(result, [])

    @patch('requests.get')
    def test_get_repo_by_name_and_author_Negative(self, mock_requests_get):
        # Configurare il mock per restituire un oggetto di risposta con stato diverso da 200
        mock_response = MagicMock()
        mock_response.status_code = 404
        mock_requests_get.return_value = mock_response

        # Eseguire il metodo sotto test
        result = self.dao_repo.getRepoByNameeAuthor("nonexistent_owner", "nonexistent_repo")

        # Assert sul risultato
        self.assertIsNone(result)
        self.assertEqual(self.dao_repo.last_http_response.status_code, 404)




    @patch('requests.get')
    def test_get_repo_list_Positive(self, mock_requests_get):
        # Configurare il mock per restituire un oggetto di risposta con stato 200 e alcuni risultati
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"items": [{"name": "repo1", "html_url": "url1", "description": "desc1"},
                                                     {"name": "repo2", "html_url": "url2", "description": "desc2"}]}
        mock_requests_get.return_value = mock_response

        # Eseguire il metodo sotto test
        result = self.dao_repo.getRepoList("test_repo")

        # Assert sul risultato
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0].name, "repo1")
        self.assertEqual(result[0].description, "desc1")
        self.assertEqual(result[1].name, "repo2")
        self.assertEqual(result[1].description, "desc2")

    @patch('requests.get')
    def test_get_java_repo_list_Positive(self, mock_requests_get):
        # Configurare il mock per restituire un oggetto di risposta con stato 200 e alcuni risultati
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "items": [{"name": "java_repo1", "html_url": "url1", "description": "desc1"},
                      {"name": "java_repo2", "html_url": "url2", "description": "desc2"}]}
        mock_requests_get.return_value = mock_response

        # Eseguire il metodo sotto test
        result = self.dao_repo.getJavaRepoList("java_test_repo")

        # Assert sul risultato
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0].name, "java_repo1")
        self.assertEqual(result[0].description, "desc1")
        self.assertEqual(result[1].name, "java_repo2")
        self.assertEqual(result[1].description, "desc2")

    @patch('requests.get')
    def test_get_all_release_tag_repo_Positive(self, mock_requests_get):
        # Configurare il mock per restituire un oggetto di risposta con stato 200 e alcuni risultati
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = [{"tag_name": "v1.0"}, {"tag_name": "v2.0"}]
        mock_requests_get.return_value = mock_response

        # Eseguire il metodo sotto test
        result = self.dao_repo.get_all_release_tag_repo("test_owner", "test_repo")

        # Assert sul risultato
        self.assertEqual(result, ["v1.0", "v2.0"])

    @patch('requests.get')
    def test_get_all_release_tag_repo_Negative(self, mock_requests_get):
        # Configurare il mock per restituire un oggetto di risposta con stato diverso da 200
        mock_response = MagicMock()
        mock_response.status_code = 404
        mock_requests_get.return_value = mock_response

        # Eseguire il metodo sotto test
        result = self.dao_repo.get_all_release_tag_repo("nonexistent_owner", "nonexistent_repo")

        # Assert sul risultato
        self.assertIsNone(result)
        # Verifica che il messaggio di errore venga stampato

    @patch('requests.get')
    def test_get_java_repo_list_for_author_and_repo_Positive(self, mock_requests_get):
        # Configurare il mock per restituire un oggetto di risposta con stato 200 e alcuni risultati
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "items": [{"name": "java_repo1", "html_url": "url1", "description": "desc1"},
                      {"name": "java_repo2", "html_url": "url2", "description": "desc2"}]}
        mock_requests_get.return_value = mock_response

        # Eseguire il metodo sotto test
        result = self.dao_repo.getJavaRepoListForAuthorAndRepo("test_author", "java_test_repo")

        # Assert sul risultato
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0].name, "java_repo1")
        self.assertEqual(result[0].description, "desc1")
        self.assertEqual(result[1].name, "java_repo2")
        self.assertEqual(result[1].description, "desc2")

    @patch('requests.get')
    def test_get_repo_list_by_author_Positive(self, mock_requests_get):
        # Configurare il mock per restituire un oggetto di risposta con stato 200 e alcuni risultati
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "items": [{"name": "author_repo1", "html_url": "url1", "description": "desc1"},
                      {"name": "author_repo2", "html_url": "url2", "description": "desc2"}]}
        mock_requests_get.return_value = mock_response

        # Eseguire il metodo sotto test
        result = self.dao_repo.getRepoListByAuthor("test_author")

        # Assert sul risultato
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0].name, "author_repo1")
        self.assertEqual(result[0].description, "desc1")
        self.assertEqual(result[1].name, "author_repo2")
        self.assertEqual(result[1].description, "desc2")
