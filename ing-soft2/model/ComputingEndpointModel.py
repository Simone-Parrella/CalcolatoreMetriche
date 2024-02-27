"""ComputingEndpointModel per la gestione dei processi"""

import multiprocessing
from backend.start_endpoint import startEndpoint  # Importa il target del processo


class ComputingEndpointModel:
    """Istanze statiche della classe"""

    _instance = None

    def __new__(cls):
        """Crea nuova classe"""
        if cls._instance is None:
            cls._instance = super(ComputingEndpointModel, cls).__new__(cls)
            cls.parent_conn = None
            cls.process_pid = None
        return cls._instance

    def activateLocal(self):
        """Richiede l'attivazione del servizio locale."""
        try:
            self.parent_conn, self.child_conn = multiprocessing.Pipe()
            self.p = multiprocessing.Process(
                target=startEndpoint, args=(self.child_conn,)
            )
            self.p.start()
            self.process_pid = self.p.pid
            # Assegna il PID del processo a una variabile di istanza
            print(f"Processo avviato con PID: {self.process_pid}")
            return self.p
        except Exception as e:
            print(f"Errore durante l'attivazione del processo: {e}")
            raise

    def isActiveLocal(self):
        """Verifica se il processo creato è attivo."""
        try:
            self.parent_conn.send({"fun": "ping", "num1": 1, "num2": 2})
            result = self.parent_conn.recv()
            return result == 3
            # Restituisce True se la risposta è quella attesa
        except Exception as e:
            print(f"Errore durante il controllo dell'attività del processo locale: {e}")
            return False  # Restituisce False in caso di errore

    def sendMessageToEndpoint(self, message):
        """Invia un messaggio al processo."""
        try:
            self.parent_conn.send(message)
        except Exception as e:
            print(f"Errore durante l'invio del messaggio al processo: {e}")

    def receiveMessageFromEndpoint(self):
        """Ricevi un messaggio dal processo."""
        try:
            message = self.parent_conn.recv()
            return message
        except Exception as e:
            print(f"Errore durante la ricezione del messaggio dal processo: {e}")

    def destroy(self) -> bool:
        """Distrugge il thread"""
        self.parent_conn.send({"fun": "destroy"})

        message = self.parent_conn.recv()
        self.p.join()
        print(message)
        if message == "destroy request ok":
            self.child_conn.close()
            self.parent_conn.close()
            print("recieved")
            return True
        else:
            return False
