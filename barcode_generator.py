import barcode
from barcode.writer import ImageWriter
from pathlib import Path


def create_barcode(sample_name, output_folder):
    # Luodaan viivakoodit kuvina kansioon. 
    # Jokaisen kuvan nimi on sama kuin näytteen nimi.

    output_folder = Path(output_folder)
    output_folder.mkdir(exist_ok=True)

    barcode_file = output_folder / sample_name

    code128 = barcode.get(
        "code128",
        sample_name,
        writer=ImageWriter()
    )

    filename = code128.save(
        str(barcode_file),
        options={
            "write_text": False,
            "module_width": 0.5,
            "module_height": 20,
            "quiet_zone": 5
        }
    )

    return filename

