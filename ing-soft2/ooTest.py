import unittest
import model.ComputingEndpointModel  as ce
import backend.functionFactory as FunctionFactory
import inspect
import model.DataAccessLayer.DAORepo as dao
import model.DataAccessLayer.LocalDAO as lao
from unittest.mock import patch, MagicMock
import datetime
import model.Domain as dd
from model import LocalRepoModel as lrm
import model.RepoModel as rm
class TestOO(unittest.TestCase):
    ##### ComputingEndpointModel ######
    @patch("multiprocessing.Pipe")
    @patch("multiprocessing.Process")
    def test_activate_local_success(self, mock_process, mock_pipe):
        mock_parent_conn = MagicMock()
        mock_child_conn = MagicMock()
        mock_pipe.return_value = (mock_parent_conn, mock_child_conn)
        model_instance = ce.ComputingEndpointModel()
        model_instance.activateLocal()
        mock_pipe.assert_called_once()
        mock_process.assert_called_once_with(target=ce.startEndpoint, args=(mock_child_conn,))
        mock_process.return_value.start.assert_called_once()
        self.assertEqual(model_instance.parent_conn, mock_parent_conn)

    def test_new_method_creates_instance(self):
        instance = ce.ComputingEndpointModel.__new__(ce.ComputingEndpointModel)
        self.assertIsNotNone(instance)
        self.assertIsInstance(instance, ce.ComputingEndpointModel)

    def test_new_method_returns_same_instance(self):
        instance1 = ce.ComputingEndpointModel.__new__(ce.ComputingEndpointModel)
        instance2 = ce.ComputingEndpointModel.__new__(ce.ComputingEndpointModel)
        self.assertIs(instance1, instance2)

    def test_destroy_success(self):
        mock_parent_conn = MagicMock()
        mock_parent_conn.recv.return_value = "destroy request ok"
        computing_model = ce.ComputingEndpointModel()
        computing_model.parent_conn = mock_parent_conn
        result = computing_model.destroy()
        mock_parent_conn.send.assert_called_once_with({"fun": "destroy"})
        mock_parent_conn.recv.assert_called_once()
        self.assertTrue(result)

    def test_destroy_failure(self):
        mock_parent_conn = MagicMock()
        mock_parent_conn.recv.return_value = "unexpected message"
        computing_model = ce.ComputingEndpointModel()
        computing_model.parent_conn = mock_parent_conn
        result = computing_model.destroy()
        mock_parent_conn.send.assert_called_once_with({"fun": "destroy"})
        mock_parent_conn.recv.assert_called_once()
        self.assertFalse(result)

    ##### fine ComputingEndpointModel ######
    ###### RepoModel  ########
    @patch('model.DataAccessLayer.DAORepo')
    def test_get_repo_list_by_name(self, mock_dao_repo):
        self.repo_model = rm.RepoModel()
        self.mock_crud_repo = MagicMock()
        mock_dao_repo.return_value = self.mock_crud_repo
        expected_repo_list = ['repo1', 'repo2']
        self.mock_crud_repo.getRepoList.return_value = expected_repo_list
        repo_list = self.repo_model.getRepoListByName('name')
        self.assertGreater(len(repo_list), 0)

    @patch('model.DataAccessLayer.DAORepo')
    def test_get_repo_list_by_author_and_repo_name(self, mock_dao_repo):
        self.repo_model = rm.RepoModel()
        self.mock_crud_repo = MagicMock()
        mock_dao_repo.return_value = self.mock_crud_repo
        expected_repo_list = ['repo1', 'repo2']
        self.mock_crud_repo.getJavaRepoListForAuthorAndRepo.return_value = expected_repo_list
        repo_list = self.repo_model.getRepoListByAuthorAndRepoName('author', 'repo_name')
        self.assertGreaterEqual(len(repo_list), 0)

    @patch('model.DataAccessLayer.DAORepo')
    def test_get_repo_list_by_author(self, mock_dao_repo):
        self.repo_model = rm.RepoModel()
        self.mock_crud_repo = MagicMock()
        mock_dao_repo.return_value = self.mock_crud_repo
        expected_repo_list = ['repo1', 'repo2']
        self.mock_crud_repo.getRepoListByAuthor.return_value = expected_repo_list
        repo_list = self.repo_model.getRepoListByAuthor('author')
        self.assertGreaterEqual(len(repo_list), 0)

    ##### Fine RepoModel   ###
    ##### Local Repo Model ###

    @patch('os.makedirs')
    @patch('builtins.print')   
    def test__CheckRepoDir_directory_does_not_exist(self, mock_print, mock_makedirs):
        local_repo_model = lrm.LocalRepoModel()
        with patch('os.path.exists', return_value=False):
            local_repo_model._CheckRepoDir()
        mock_makedirs.assert_called_once_with('repository')
        mock_print.assert_not_called()

    @patch('os.makedirs', side_effect=OSError("Mocked OSError"))
    @patch('builtins.print')  
    def test__CheckRepoDir_directory_creation_error(self, mock_print, mock_makedirs):
        local_repo_model = lrm.LocalRepoModel()
        with patch('os.path.exists', return_value=False):
            local_repo_model._CheckRepoDir()
        mock_makedirs.assert_called_once_with('repository')
        mock_print.assert_called_once_with("Errore durante la creazione della cartella: Mocked OSError")

    @patch('os.path.exists', return_value=True)
    @patch('os.makedirs')
    @patch('builtins.print')  # If using Python 3
    def test__CheckRepoDir_directory_exists(self, mock_print, mock_makedirs, mock_exists):
        local_repo_model = lrm.LocalRepoModel()
        local_repo_model._CheckRepoDir()
        mock_makedirs.assert_not_called()
        mock_print.assert_not_called()

    @patch('model.DataAccessLayer.DAORepo')
    @patch('model.DataAccessLayer.LocalDAO')
    def test_getRepoData_returns_correct_value(self, mock_local_dao, mock_dao_repo):
        self.instance = lrm.LocalRepoModel()
        expected_repo_data = MagicMock()
        self.instance.repoData = expected_repo_data
        result = self.instance.getRepoData()
        self.assertEqual(result, expected_repo_data)

    @patch('model.DataAccessLayer.DAORepo')
    @patch('model.DataAccessLayer.LocalDAO')
    def test_singleton_instance_creation(self, mock_local_dao, mock_dao_repo):
        instance1 = lrm.LocalRepoModel()
        self.assertIsInstance(instance1.CRUD, dao.DAORepo)
        self.assertIsInstance(instance1.LocalDAO, lao.LocalDAO)
        instance2 = lrm.LocalRepoModel()
        self.assertIs(instance1, instance2)
        self.assertIsInstance(instance2.CRUD, dao.DAORepo)
        self.assertIsInstance(instance2.LocalDAO, lao.LocalDAO)

    @patch('model.DataAccessLayer.DAORepo')
    @patch('model.DataAccessLayer.LocalDAO')
    def test_RepoDataUpdate(self, mock_local_dao, mock_dao_repo):
        local_repo_model = lrm.LocalRepoModel()
        mock_local_dao.getRepoInfoFromGit.return_value = ('author_name', 'repo_name')
        mock_dao_repo.getRepoByNameeAuthor.return_value = MagicMock()
        mock_dao_repo.get_all_release_tag_repo.return_value = MagicMock()
        result = local_repo_model.RepoDataUpdate()
        self.assertIsNone(result)

    ##### Fine LocalRepoModel #####
    ##### Domain   ################
    def test_repository(self):
        repository_data = {
            'name': 'repo_name',
            'html_url': 'http://example.com/repo',
            'description': 'Repo description',
            'releases': ['release1', 'release2']
        }
        repository = dd.Repository(**repository_data)
        self.assertEqual(repository.name, 'repo_name')
        self.assertEqual(repository.url, 'http://example.com/repo')
        self.assertEqual(repository.description, 'Repo description')
        self.assertEqual(repository.releases, ['release1', 'release2'])

    def test_commit_initialization(self):
        sample_data = {
            'sha': 'abc123',
            'node_id': 'xyz456',
            'author_name': 'John Doe',
            'author_email': 'john.doe@example.com',
            'author_date': '2022-01-01T12:00:00Z',
            'committer_name': 'Jane Smith',
            'committer_email': 'jane.smith@example.com',
            'committer_date': '2022-01-02T12:00:00Z',
            'message': 'Initial commit',
            'tree_sha': 'def789',
            'tree_url': 'https://github.com/user/sample_repo/tree/main',
            'commit_url': 'https://github.com/user/sample_repo/commit/abc123',
            'html_url': 'https://github.com/user/sample_repo/commit/abc123',
            'comments_url': 'https://github.com/user/sample_repo/commit/abc123/comments',
            'author_login': 'johndoe',
            'author_id': 123,
            'author_avatar_url': 'https://example.com/avatar_johndoe.png',
        }

        commit_instance = dd.Commit(**sample_data)
        self.assertEqual(commit_instance.sha, 'abc123')
        self.assertEqual(commit_instance.node_id, 'xyz456')
        self.assertEqual(commit_instance.author['name'], 'John Doe')

    def test_metadata_repository_initialization(self):
        sample_data = {
            'id': 123,
            'node_id': 'abc123',
            'name': 'sample_repo',
            'full_name': 'user/sample_repo',
            'private': False,
            'owner': {
                'login': 'user',
                'id': 456,
                'avatar_url': 'https://example.com/avatar.png',
            },
            'html_url': 'https://github.com/user/sample_repo',
            'description': 'A sample repository',
            'fork': False,
            'url': 'https://api.github.com/repos/user/sample_repo',
            'created_at': '2022-01-01T12:00:00Z',
            'updated_at': '2022-02-01T12:00:00Z',
            'pushed_at': '2022-03-01T12:00:00Z',
            'git_url': 'git://github.com/user/sample_repo.git',
            'ssh_url': 'git@github.com:user/sample_repo.git',
            'clone_url': 'https://github.com/user/sample_repo.git',
            'svn_url': 'https://svn.example.com/user/sample_repo',
            'homepage': 'https://example.com/sample_repo',
            'size': 1024,
            'stargazers_count': 42,
            'watchers_count': 25,
            'language': 'Python',
            'has_issues': True,
            'has_projects': False,
            'has_downloads': True,
            'has_wiki': False,
            'has_pages': True,
            'has_discussions': True,
            'forks_count': 5,
            'archived': False,
            'disabled': False,
            'open_issues_count': 2,
            'license': {'key': 'mit', 'name': 'MIT License', 'url': 'https://opensource.org/licenses/MIT'},
            'allow_forking': True,
            'is_template': False,
            'web_commit_signoff_required': True,
            'topics': ['sample', 'repository', 'GitHub'],
            'visibility': 'public',
            'forks': 3,
            'open_issues': 1,
            'watchers': 10,
            'default_branch': 'main',
            'temp_clone_token': 'abc123',
            'organization': 'sample_org', 
            'network_count': 15,
            'subscribers_count': 8,
          
        }

        metadata_repository = dd.MetadataRepository(sample_data)
        self.assertEqual(metadata_repository.id, 123)
        self.assertEqual(metadata_repository.node_id, 'abc123')
        self.assertEqual(metadata_repository.name, 'sample_repo')
        self.assertEqual(metadata_repository.full_name, 'user/sample_repo')

    def test_http_response(self):
        http_response = dd.HttpResponse(status_code=200, body='OK')
        self.assertEqual(http_response.status_code, 200)
        self.assertEqual(http_response.body, 'OK')
    ##### fine Domain  #######


    ##### LocalDAO ############
    @patch('os.walk')
    def test_findJavaClass_success(self, mock_os_walk):
        mock_os_walk.return_value = [
            ("/path/to/directory", [], ["File1.java", "File2.java"])
        ]
        local_dao = lao.LocalDAO()
        result = local_dao.findJavaClass("/path/to/directory")
        self.assertEqual(result, ["File1.java", "File2.java"])

    @patch('os.walk')
    def test_findJavaClass_no_java_files(self, mock_os_walk):
   
        mock_os_walk.return_value = [
            ("/path/to/directory", [], ["File1.py", "File2.py"])
        ]
        local_dao = lao.LocalDAO()
        result = local_dao.findJavaClass("/path/to/directory")
        self.assertEqual(result, [])

    @patch('model.DataAccessLayer.LocalDAO.Commit')
    def test_class_exists_in_commit_success(self, mock_commit):
       
        mock_tree = MagicMock()
        mock_commit.tree = mock_tree
        mock_tree.__getitem__.return_value = MagicMock()
        class_name = 'MyClass'
        your_instance = lao.LocalDAO()
        result = your_instance._class_exists_in_commit(mock_commit, class_name)
        self.assertTrue(result)

    @patch('model.DataAccessLayer.LocalDAO.Commit')
    def test_class_exists_in_commit_failure(self, mock_commit):
     
        mock_tree = MagicMock()
        mock_commit.tree = mock_tree
        mock_tree.__getitem__.side_effect = KeyError
        class_name = 'NonExistentClass'
        your_instance = lao.LocalDAO()
        result = your_instance._class_exists_in_commit(mock_commit, class_name)
        self.assertFalse(result)
    
    @patch('model.DataAccessLayer.LocalDAO.Commit')
    @patch('model.DataAccessLayer.LocalDAO.git.Repo')
    def test_get_commits_with_class_success(self, mock_repo, mock_commit):
  
        mock_repo_instance = MagicMock()
        mock_repo.return_value = mock_repo_instance
        mock_commit_instance = MagicMock()
        mock_repo_instance.iter_commits.return_value = [mock_commit_instance]
        mock_class_exists = MagicMock(return_value=True)
        with patch('model.DataAccessLayer.LocalDAO.LocalDAO._class_exists_in_commit', mock_class_exists):
            your_instance = lao.LocalDAO()
            result = your_instance.get_commits_with_class('MyClass', '/path/to/repo')
            self.assertIn(mock_commit_instance, result)

    @patch('model.DataAccessLayer.LocalDAO.Commit')
    @patch('model.DataAccessLayer.LocalDAO.git.Repo')
    def test_get_commits_with_class_no_commits(self, mock_repo, mock_commit):
        
        mock_repo_instance = MagicMock()
        mock_repo.return_value = mock_repo_instance
        mock_repo_instance.iter_commits.return_value = []
        mock_class_exists = MagicMock(return_value=True)
        with patch('model.DataAccessLayer.LocalDAO.LocalDAO._class_exists_in_commit', mock_class_exists):
            your_instance = lao.LocalDAO()
            result = your_instance.get_commits_with_class('MyClass', '/path/to/repo')
            self.assertEqual(result, [])

    # @mock.patch('model.repo_utils.repo_to_use')
    # @mock.patch('model.DataAccessLayer.LocalDAO.get_commits')
    # def test_extract_yearsList_with_branches(self, mock_get_commits, mock_repo_to_use):
    #     mock_repo_instance = mock.MagicMock()
    #     mock_repo_to_use.return_value = mock_repo_instance
    #     mock_commit_1 = mock.MagicMock()
    #     mock_commit_1.committer_date.year = 2022
    #     mock_commit_1.branches = ['master']
    #     mock_commit_2 = mock.MagicMock()
    #     mock_commit_2.committer_date.year = 2022
    #     mock_commit_2.branches = ['feature']
    #     mock_get_commits.return_value = [mock_commit_1, mock_commit_2]
    #     your_instance = lao.LocalDAO()
    #     result = your_instance.extract_yearsList_with_branches()
    #     expected_result = {2022: {'master', 'feature'}}
    #     self.assertEqual(result, expected_result)

    # @patch('pydriller.Repository')
    # def test_dataCommitLinkYear(self, mock_repository):
    #     mock_repo = MagicMock()
    #     mock_commit1 = MagicMock()
    #     mock_commit2 = MagicMock()
    #     mock_commit1.committer_date = datetime.datetime(2022, 1, 15)
    #     mock_commit2.committer_date = datetime.datetime(2022, 2, 20)
    #     mock_repo.traverse_commits.return_value = [mock_commit1, mock_commit2]
    #     mock_repository.return_value = mock_repo
    #     your_instance = lao.LocalDAO()
    #     result = your_instance.dataCommitLinkYear(branch='Master', year='2022')
    #     self.assertGreater(len(result), 0)

    #####  functionFactory  ######
    def setUp(self):
            self.factory = FunctionFactory.FunctionFactory()
        
    def test_getExistingFunction(self):
        # Verifica che la funzione esista nel modulo 'compute'
        funct_name = "generate_metrics"
        function = self.factory.getFunct(funct_name)
        self.assertIsNotNone(function)
        self.assertTrue(inspect.isfunction(function))

    def test_getNonExistingFunction(self):
        # Verifica che la funzione non esista nel modulo 'compute'
        funct_name = "funzione_inesistente"
        function = self.factory.getFunct(funct_name)
        self.assertIsNone(function)
    
    #### Fine functionFactory #####
    #### DAORepo  #################



    
    @patch('requests.get')
    def test_getRepoByNameeAuthor_failure(self, mock_requests_get):
        # Configura il mock della risposta HTTP con uno stato diverso da 200
        mock_response = MagicMock()
        mock_response.status_code = 404
        mock_requests_get.return_value = mock_response
        your_instance = dao.DAORepo()
        result = your_instance.getRepoByNameeAuthor('repo_owner', 'repo_name')
        self.assertIsNone(result)

    @patch('requests.get')
    def test_getRepoList_success(self, mock_requests_get):
        # Configura il mock della risposta HTTP
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "items": [
                {
                    "name": "repo1",
                    "html_url": "https://github.com/repo1",
                    "description": "Description 1",
                },
                {
                    "name": "repo2",
                    "html_url": "https://github.com/repo2",
                    "description": "Description 2",
                },
            ]
        }
        mock_requests_get.return_value = mock_response
        dao_repo = dao.DAORepo()
        result = dao_repo.getRepoList("java")
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0].name, "repo1")
        self.assertEqual(result[1].url, "https://github.com/repo2")
        mock_requests_get.assert_called_once_with("https://api.github.com/search/repositories?q=java+language:java")

    @patch('requests.get')
    def test_getRepoList_empty_name(self, mock_requests_get):
        dao_repo = dao.DAORepo()
        result = dao_repo.getRepoList("")
        self.assertEqual(result, [])
        mock_requests_get.assert_not_called()

    @patch('requests.get')
    def test_getJavaRepoList_success(self, mock_requests_get):
        # Configura il mock della risposta HTTP
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "items": [
                {
                    "name": "repo1",
                    "html_url": "https://github.com/repo1",
                    "description": "Description 1",
                },
                {
                    "name": "repo2",
                    "html_url": "https://github.com/repo2",
                    "description": "Description 2",
                },
            ]
        }
        mock_requests_get.return_value = mock_response
        your_instance = dao.DAORepo()
        # Chiamare il metodo getJavaRepoList
        result = your_instance.getJavaRepoList("java")
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0].name, "repo1")
        self.assertEqual(result[1].url, "https://github.com/repo2")
        mock_requests_get.assert_called_once_with("https://api.github.com/search/repositories?q=java+language:java")

    @patch('requests.get')
    def test_getJavaRepoList_empty_result(self, mock_requests_get):
        # Configura il mock della risposta HTTP con risultato vuoto
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"items": []}
        mock_requests_get.return_value = mock_response
        your_instance = dao.DAORepo()
        result = your_instance.getJavaRepoList("java")
        self.assertEqual(result, [])
        mock_requests_get.assert_called_once_with("https://api.github.com/search/repositories?q=java+language:java")

    @patch('requests.get')
    def test_get_all_release_tag_repo_success(self, mock_requests_get):
        # Configura il mock della risposta HTTP
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = [
            {"tag_name": "v1.0.0"},
            {"tag_name": "v1.1.0"},
            {"tag_name": "v1.2.0"},
        ]
        mock_requests_get.return_value = mock_response
        your_instance = dao.DAORepo()
        result = your_instance.get_all_release_tag_repo("owner_name", "repo_name")
        self.assertEqual(result, ["v1.0.0", "v1.1.0", "v1.2.0"])
        mock_requests_get.assert_called_once_with("https://api.github.com/repos/owner_name/repo_name/releases")

    @patch('requests.get')
    def test_get_all_release_tag_repo_failure(self, mock_requests_get):
        # Configura il mock della risposta HTTP con errore
        mock_response = MagicMock()
        mock_response.status_code = 404
        mock_requests_get.return_value = mock_response
        your_instance = dao.DAORepo()
        result = your_instance.get_all_release_tag_repo("owner_name", "repo_name")
        self.assertIsNone(result)
        mock_requests_get.assert_called_once_with("https://api.github.com/repos/owner_name/repo_name/releases")

    @patch('requests.get')
    def test_getJavaRepoListForAuthorAndRepo_success(self, mock_requests_get):
        # Configura il mock della risposta HTTP
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "items": [
                {
                    "name": "repo1",
                    "html_url": "https://github.com/repo1",
                    "description": "Description 1",
                },
                {
                    "name": "repo2",
                    "html_url": "https://github.com/repo2",
                    "description": "Description 2",
                },
            ]
        }
        mock_requests_get.return_value = mock_response
        your_instance = dao.DAORepo()
        result = your_instance.getJavaRepoListForAuthorAndRepo("author_name", "repo_name")
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0].name, "repo1")
        self.assertEqual(result[1].url, "https://github.com/repo2")
        mock_requests_get.assert_called_once_with("https://api.github.com/search/repositories?q=user:author_name+repo:repo_name+language:java")

    @patch('requests.get')
    def test_getJavaRepoListForAuthorAndRepo_failure(self, mock_requests_get):
        mock_response = MagicMock()
        mock_response.status_code = 404
        mock_requests_get.return_value = mock_response
        your_instance = dao.DAORepo()
        result = your_instance.getJavaRepoListForAuthorAndRepo("author_name", "repo_name")
        self.assertEqual(result, [])
        mock_requests_get.assert_called_once_with("https://api.github.com/search/repositories?q=user:author_name+repo:repo_name+language:java")

    @patch('requests.get')
    def test_getRepoListByAuthor_success(self, mock_requests_get):
        # Configura il mock della risposta HTTP
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "items": [
                {
                    "name": "repo1",
                    "html_url": "https://github.com/repo1",
                    "description": "Description 1",
                },
                {
                    "name": "repo2",
                    "html_url": "https://github.com/repo2",
                    "description": "Description 2",
                },
            ]
        }
        mock_requests_get.return_value = mock_response
        your_instance = dao.DAORepo()
        result = your_instance.getRepoListByAuthor("author_name")
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0].name, "repo1")
        self.assertEqual(result[1].url, "https://github.com/repo2")
        mock_requests_get.assert_called_once_with("https://api.github.com/search/repositories?q=user:author_name+language:java")

    @patch('requests.get')
    def test_getRepoListByAuthor_failure(self, mock_requests_get):
        # Configura il mock della risposta HTTP con errore
        mock_response = MagicMock()
        mock_response.status_code = 404
        mock_requests_get.return_value = mock_response
        your_instance =dao.DAORepo()
        result = your_instance.getRepoListByAuthor("author_name")
        self.assertEqual(result, [])
        mock_requests_get.assert_called_once_with("https://api.github.com/search/repositories?q=user:author_name+language:java")



    ##### fine DAO repo #######


if __name__ == '__main__':
    unittest.main()


if __name__ == '__main__':
    unittest.main()