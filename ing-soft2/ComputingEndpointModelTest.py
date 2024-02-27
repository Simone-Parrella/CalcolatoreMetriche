import multiprocessing
import time
import unittest
from time import sleep
from unittest.mock import patch, MagicMock

import psutil

from backend.start_endpoint import ComputationEndpoint
from model.ComputingEndpointModel import ComputingEndpointModel


class TestComputingEndpointModel(unittest.TestCase):
    model = None
    process_pid = None

    @classmethod
    def setUpClass(cls):
        print("Sto eseguendo ComputingEndpointmodel test")
        # Create the ComputingEndpointModel object at the beginning of each test
        cls.model = ComputingEndpointModel()
        cls.model.activateLocal()
        sleep(3)
        cls.process_pid = cls.model.process_pid

    def stop_process_by_pid(pid):
        try:
            process = psutil.Process(pid)
            children = process.children(recursive=True)
            for child in children:
                child.terminate()
            process.terminate()
        except psutil.NoSuchProcess:
            print(f"Processo con PID {pid} non trovato.")
        except Exception as e:
            print(f"Errore durante la terminazione del processo: {e}")
    @classmethod
    def tearDownClass(cls):
        sleep(2)
        # Destroy the ComputingEndpointModel object at the end of each test
        cls.stop_process_by_pid(cls.process_pid)


    def setUp(self):
        self.patcher = None

    def tearDown(self):
        if self.patcher:
            self.patcher.stop()

    def test_A_is_active_local(self):
        # Act
        verifier = self.model.isActiveLocal()

        # Assert
        self.assertEqual(verifier, True)

    def test_is_active_local_raises_exception(self):
        # Arrange - Manually replace the parent_conn attribute with a MagicMock
        original_parent_conn = self.model.parent_conn
        self.model.parent_conn = MagicMock()
        self.model.parent_conn.recv.side_effect = Exception("Errore di connessione")

        # Act
        is_active = self.model.isActiveLocal()

        # Assert
        self.assertEqual(is_active, False)  # The method should return False if an exception is raised

        # Revert the change
        self.model.parent_conn = original_parent_conn

    def test_A_send_message_to_endpoint_valid_message(self):
        # Act
        self.model.sendMessageToEndpoint({"fun": "ping", "num1": 1, "num2": 2})
        time.sleep(1)  # Give the process time to handle the message

        message = self.model.receiveMessageFromEndpoint()
        self.assertEqual(message, 3)

    def test_B_send_message_to_endpoint_invalid_message(self):
        self.model.sendMessageToEndpoint("a")
        message = self.model.receiveMessageFromEndpoint()
        self.assertEqual(
            "Errore: il messaggio deve essere un dizionario che contiene il parametro 'fun' per specificare la funzione.",
            message)

    def test_activate_local_exception(self):
        # Arrange - Forzare un'eccezione durante l'attivazione
        self.patcher = patch('multiprocessing.Pipe', side_effect=Exception("Errore di attivazione"))
        self.patcher.start()

        with self.assertRaises(Exception):
            # Act
            self.model.activateLocal()

        # Stop the patch
        self.patcher.stop()

    def test_is_active_local_exception(self):
        # Arrange - Forzare un'eccezione durante la verifica di attività solo per questo test
        self.patcher = patch.object(self.model.parent_conn, 'send', side_effect=Exception("Errore di connessione"))
        self.patcher.start()

        # Act
        is_active = self.model.isActiveLocal()

        # Assert
        self.assertFalse(is_active)

    def test_activate_local_exception_during_send(self):
        # Arrange - Forzare un'eccezione durante l'invio
        self.patcher = patch('multiprocessing.Pipe')
        mock_pipe = self.patcher.start()
        mock_pipe.return_value = (MagicMock(), MagicMock())

        mock_process_patcher = patch('multiprocessing.Process')
        mock_process = mock_process_patcher.start()
        mock_process.return_value = MagicMock()

        self.model.activateLocal()  # Per evitare l'eccezione durante la creazione

        # Simula un'eccezione durante l'invio
        self.patcher = patch.object(self.model.parent_conn, 'send', side_effect=Exception("Errore durante l'invio"))
        self.patcher.start()

        # Act
        self.model.activateLocal()

        # Stop the patches
        mock_process_patcher.stop()

    def test_is_active_local_exception_during_send(self):
        # Arrange - Forzare un'eccezione durante l'invio in isActiveLocal
        self.model.parent_conn = MagicMock()

        self.patcher = patch.object(self.model.parent_conn, 'send', side_effect=Exception("Errore durante l'invio"))
        self.patcher.start()

        # Act
        is_active = self.model.isActiveLocal()

        # Assert
        self.assertFalse(is_active)

    def test_send_message_to_endpoint_exception(self):
        # Arrange - Forzare un'eccezione durante l'invio di un messaggio
        self.model.parent_conn = MagicMock()

        self.patcher = patch.object(self.model.parent_conn, 'send', side_effect=Exception("Errore durante l'invio"))
        self.patcher.start()

        # Act
        self.model.sendMessageToEndpoint({"fun": "ping"})

    def test_receive_message_from_endpoint_exception(self):
        # Arrange - Forzare un'eccezione durante la ricezione di un messaggio
        self.model.parent_conn = MagicMock()

        self.patcher = patch.object(self.model.parent_conn, 'recv',
                                    side_effect=Exception("Errore durante la ricezione"))
        self.patcher.start()

        # Act
        message = self.model.receiveMessageFromEndpoint()

    def test_destroy_exception(self):
        model = ComputingEndpointModel()
        # Arrange - Forzare un'eccezione durante la distruzione
        model.parent_conn = MagicMock()

        self.patcher = patch.object(model.parent_conn, 'send', side_effect=Exception("Errore durante la distruzione"))
        self.patcher.start()

        # Act & Assert
        with self.assertRaises(Exception):
            model.destroy()

        # Stop the patch
        self.patcher.stop()

    def test_destroy_success(self):
        # Arrange
        mock_parent_conn = MagicMock()
        mock_parent_conn.recv.return_value = "destroy request ok"
        self.model.parent_conn = mock_parent_conn

        # Act
        result = self.model.destroy()

        # Assert
        self.assertTrue(result)

    def test_destroy_failure(self):
        # Arrange
        mock_parent_conn = MagicMock()
        mock_parent_conn.recv.return_value = "destroy request failed"
        self.model.parent_conn = mock_parent_conn

        # Act
        result = self.model.destroy()

        # Assert
        self.assertFalse(result)

    def test_destroy_exception(self):
        # Arrange
        mock_parent_conn = MagicMock()
        mock_parent_conn.recv.side_effect = Exception("Errore durante la ricezione")
        self.model.parent_conn = mock_parent_conn

        # Act & Assert
        with self.assertRaises(Exception):
            self.model.destroy()

if __name__ == '__main__':
    unittest.main()