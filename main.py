import pandas as pd
from reader import read_csv_file
from pathlib import Path
from csv_exporter import create_device_file
from barcode_generator import create_barcode
from pdf_exporter import create_bc_pdf
import shutil
from sample_table import create_sample_table
from gui import get_user_input
import traceback


# Tyhjennetään barcodes-kansio
def clean_barcode_folder(folder="barcodes"):

    folder_path = Path(folder)

    if folder_path.exists():

        for file in folder_path.iterdir():

            if file.is_file():
                file.unlink()

            elif file.is_dir():
                shutil.rmtree(file)


def process_files(settings):

    try:

        csv_file = settings["csv_file"]
        plate = settings["plate"]
        method = settings["method"]

        csv_path = Path(csv_file)

        output_folder = csv_path.parent

        base_name = csv_path.stem

        device_output = (
            output_folder /
            f"{base_name}_laitteelle.csv"
        )

        bc_pdf_output = (
            output_folder /
            f"{base_name}_pipetointilista.pdf"
        )

        # Luetaan alkuperäinen CSV ja luodaan taulukko
        df = read_csv_file(csv_file)

        # Tarkistetaan, että CSV sisältää vähintään yhden näytteen
        has_samples = df.astype(str).apply(
            lambda x: x.str.strip() != ""
        ).any().any()

        if not has_samples:
            return False, "Tyhjä näytelista", "CSV-tiedostossa ei ole yhtään näytettä."
        
        sample_table = create_sample_table(
            df,
            plate
        )

        # Tehdään taulukosta CSV-tiedosto
        output = create_device_file(
            sample_table,
            csv_file,
            method
        )

        output.to_csv(
            str(device_output),
            index=False,
            encoding="utf-8-sig"
        )

        # Luodaan pipetointilista (PDF)
        # yllä luodun taulukon pohjalta
        bc_rows = []

        barcode_folder = output_folder / "barcodes"

        for _, row in sample_table.iterrows():

            sample = row["Sample Name"]

            # Suodatetaan tyhjät näytepaikat pois
            if pd.isna(sample) or str(sample).strip() == "":
                continue

            barcode_image = create_barcode(
                sample,
                barcode_folder
            )

            bc_rows.append({
                # Lisätään tiedot taulukkoon
                "Sample Name": sample,
                "Barcode": barcode_image,
                "Well Plate Position": row["Well Plate Position"],
                "Original Position": row["Original Position"]
            })

        bc_data = pd.DataFrame(bc_rows)

        create_bc_pdf(
            bc_data,
            str(bc_pdf_output)
        )

        # Poistetaan väliaikaiset viivakoodit
        clean_barcode_folder(barcode_folder)

        return (
            True,
            device_output,
            bc_pdf_output
        )

    except Exception as e:

        traceback.print_exc()

        return (
            False,
            type(e).__name__,
            str(e)
        )


if __name__ == "__main__":
    get_user_input(process_files)