
import subprocess

def run_tests(path):
    # Esegui il test corrente
    cmd = ["pytest", "-s", path, "--verbose", "--color=yes"]
    result = subprocess.run(cmd, capture_output=True, text=True)

    # Stampa l'output dei test
    print(result.stdout)

    # stampa l'output di errore su standard err
    if result.returncode != 0:
        print(result.stderr)
        return False  # Restituisci False se un test fallisce
    else:
        return True  # Restituisci True se il test ha successo

if __name__ == "__main__":
    # Lista dei percorsi dei test da eseguire
    test_paths_list = [
        "pmTest.py",
        "MainPageControllerTest.py",
        "ooTest.py",
        "LocalRepoModelTestingWhiteBox.py",
        "RepoModelTest.py",
        "LocalDAOTesting.py",
        "DAORepoTesting.py",
        "ComputingEndpointModelTest.py",
        "ProjectMetricsControllerTest.py"
    ]

    # Esegui i test uno alla volta per ciascuna lista di test
    success = True
    for test_path in test_paths_list:
        if not run_tests(test_path):
            success = False  # Imposta success a False se un test fallisce

    # Restituisci un codice di uscita appropriato
    if success:
        print("Tutti i test sono stati eseguiti con successo.")
        exit(0)
    else:
        print("Almeno un test ha fallito.")
        exit(1)
