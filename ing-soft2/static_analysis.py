import re
import subprocess

def run_pylint(file_name, output_file):
    command = ["pylint", "--disable=C0103", file_name]

    try:
        result = subprocess.run(command, check=False, capture_output=True, text=True)
    except subprocess.CalledProcessError as e:
        print(f"Error running pylint on {file_name}:")
        print(e.stderr)
    else:
        # Aggiungi l'output di Pylint a un file globale
        with open(output_file, "a") as report_file:
            report_file.write(f"Pylint output for {file_name}:\n{result.stdout}\n\n")

        # Estrai il punteggio di Pylint dall'output
        match = re.search(r"Your code has been rated at ([\d\.]+)/10", result.stdout)
        if match:
            return float(match.group(1))

    return 0.0  # Restituisci 0 se non è stato possibile eseguire Pylint o estrarre il punteggio

def main():
    # Specifica il nome del file globale per tutti i report
    global_output_file = "pylint_report.txt"

    # Leggi i nomi dei file dal file static_analysis.txt
    with open("static_analysis.txt", "r") as file:
        # Leggi e rimuovi eventuali spazi bianchi e a capo
        file_names = [line.strip() for line in file]

        # Analizza ciascun file con Pylint e aggiungi l'output al file globale
        scores = []
        for file_name in file_names:
            # Unisci il percorso del progetto e il nome del file
            full_path = f"{file_name}.py"

            # Esegui Pylint e aggiungi l'output al file globale
            score = run_pylint(full_path, global_output_file)
            scores.append(score)

        # Calcola e restituisci il punteggio medio
        average_score = sum(scores) / len(scores) if scores else 0.0
        print(average_score)

if __name__ == "__main__":
    main()
