from config import (
    SAMPLE_TYPE
)
from pathlib import Path

# Luodaan laitteelle lähetettävä CSV-tiedosto
def create_device_file(
        sample_table,
        csv_file,
        method
):
    device_df = sample_table.copy()
    # kopioidaan luotu näytetaulukko

    sample_name = "Sample Name"
    device_df = device_df.dropna(
        subset=[sample_name]
    )
    # suodatetaan tyhjät rivit pois (ei näytteen nimeä)

    device_df = device_df[
        device_df[sample_name].astype(str).str.strip() != ""
    ]
    # muutetaan kaikki näytteen nimet string-muotoon 
    # ja poistetaan mahdolliset välilyönnit
   
    source_name = Path(csv_file).name
    # palautetaan polun viimeinen osa eli CSV-tiedoston nimi

    # luodaan data taulukkoon sarake kerrallaan
    device_df["Data File"] = (
        device_df[sample_name] + ".d"
        )

    device_df["Method"] = method

    device_df["Comment"] = ""

    device_df["Sample Type"] = SAMPLE_TYPE

    device_df["Level Name"] = ""

    device_df["Inj Vol (µl)"] = ""

    device_df[source_name] = ""

    # järjestetään sarakkeet oikeaan järjestykseen
    device_df = device_df[
        [
            "Data File",
            "Method",
            sample_name,
            "Comment",
            "Sample Position",
            "Sample Type",
            "Level Name",
            "Inj Vol (µl)",
            source_name
        ]
    ]
    
    return device_df