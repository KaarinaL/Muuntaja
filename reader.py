import pandas as pd

# Lukee alkuperäisen 8x12 csv-tiedoston
def read_csv_file(filename):

    df = pd.read_csv(
        filename,
        header=None,
        dtype=str,
        keep_default_na=False
    )

    return df