"""E' solo un modo per risparmiare tempo con i loc del df"""
import pandas as pd


######### INIZIO METODI PER METRICHE DI PROCESSO QUINDI DA USARE IL DATFRAME
#  RESTITUITO DA generate_process_metrics in spMetrics ###########


def revision_number(df):
    """Genera e restituisce un grafico a barre con il numero totale di autori
    per data del commit"""
    return df["Numero di Revisioni"].tolist(), df["Data del Commit"].tolist()


def loc_number(df):
    """Genera e restituisce un grafico a linee LOC con l'indice basato sulla
      data del commit"""
    return (
        df["Linee di Codice"].tolist(),
        df["Linee vuote"].tolist(),
        df["Commenti"].tolist(),
        df["Data del Commit"].tolist(),
    )


def authors(df):
    """Genera e restituisce un grafico a barre con il numero totale di
      autori per ogni data del commit"""
    authors_count = pd.DataFrame(columns=["Data del Commit", "Numero di Autori"])
    for date, group in df.groupby("Data del Commit"):
        authors_count = pd.concat(
            [
                authors_count,
                pd.DataFrame(
                    {
                        "Data del Commit": [date],
                        "Numero di Autori": [
                            len(set(group["Autori Distinti"].sum())) - 1
                        ],
                    }
                ),
            ]
        )
    return (
        authors_count["Numero di Autori"].tolist(),
        authors_count["Data del Commit"].tolist(),
    )


def perAuthorContribution(df: pd.DataFrame) -> dict[str, int]:
    """Genera il contributo per autore"""
    contributors = {}
    for index, row in df.iterrows():
        authors = row["Autori Distinti"]
        authors: set
        for author in authors:
            if author == "":
                continue
            if author not in contributors:
                # se il contributo non è in lista aggiungilo
                contributors[author] = 1
            else:
                # se il contributor è già in lista aumenta le sue presenze di 1
                contributors[author] = contributors[author] + 1
    return contributors


def weeks(df):
    """Genera e restituisce un grafico a barre con il numero di settimane 
    del file per data del commit"""
    return df["Settimane file"].tolist(), df["Data del Commit"].tolist()


def codeC(df):
    """Genera e restituisce un grafico a barre con il numero di codechurn
      per  data del commit"""

    return df["Code churn"].tolist(), df["Data del Commit"].tolist()


def bugfix(df):
    """Genera e restituisce un grafico a barre con il numero di bugfix 
    per data del commit"""
    return df["Bugfix commit"].tolist(), df["Data del Commit"].tolist()


######### FINE METODI PER METRICHE DI PROCESSO QUINDI DA USARE IL DATFRAME
#  RESTITUITO DA generate_process_metrics #####################


######### INIZIO METODI PER METRICHE DI PROGETTO QUINDI DA USARE IL DATFRAME
#  RESTITUITO DA generate_metrics_ck in spMetrics ###########


def wmc(df):
    """Genera e restituisce un grafico a linee con il valore di wmc per data del commit"""
    return df["wmc"].tolist(), df["Data del Commit"].tolist()


def cbo(df):
    """Genera e restituisce un grafico a linee con il valore di cbo per data del commit"""
    return df["cbo"].tolist(), df["Data del Commit"].tolist()


def dit(df):
    """Genera e restituisce un grafico a linee con il valore di dit per data del commit"""
    return df["dit"].tolist(), df["Data del Commit"].tolist()


def noc(df):
    """Genera e restituisce un grafico a linee con il valore di noc per data del commit"""
    return df["noc"].tolist(), df["Data del Commit"].tolist()


def rfc(df):
    """Genera e restituisce un grafico a linee con il valore di rfc per data del commit"""
    return df["rfc"].tolist(), df["Data del Commit"].tolist()


def lcom(df):
    """Genera e restituisce un grafico a linee con il valore di lcom per data del commit"""
    return df["lcom"].tolist(), df["Data del Commit"].tolist()


######### FINE METODI PER METRICHE DI PROGETTO QUINDI DA USARE IL
# DATFRAME RESTITUITO DA generate_metrics_ck #################
