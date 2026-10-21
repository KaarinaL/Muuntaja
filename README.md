# Muuntaja

## Tietoa sovelluksesta

Muuntaja on Pythonilla toteutettu Windows-työpöytäsovellus, joka automatisoi pipetointirobotin tuottaman CSV-tiedoston muuntamisen analyysilaitteelle sopivaan muotoon. Sovellus muodostaa lisäksi näytteiden viivakoodit ja pipetointitiedot sisältävän PDF-raportin.

Sovelluksen tavoitteena on vähentää manuaalisen tiedostonkäsittelyn tarvetta ja helpottaa näytteiden käsittelyä laboratoriotyössä.

## Ominaisuudet

* CSV-tiedoston valinta graafisella käyttöliittymällä
* Pleitin valinta (P1–P6)
* Analyysimetodin valinta
* Laitteelle vietävän CSV-tiedoston muodostaminen
* Pipetointilistan (PDF) muodostaminen
* Tyhjien näytepaikkojen automaattinen käsittely

## Käyttö

1. Käynnistä sovellus.
2. Valitse käsiteltävä CSV-tiedosto.
3. Valitse käytettävä pleitti ja analyysimenetelmä.
4. Käynnistä käsittely.
5. Sovellus tallentaa muodostetut tiedostot alkuperäisen CSV-tiedoston kansioon.

## Teknologiat

* Python 3.14
* pandas
* tkinter
* python-barcode
* Pillow
* ReportLab
* PyInstaller

## Projektin rakenne

* `main.py` – ohjelman pääohjelma
* `gui.py` – graafinen käyttöliittymä
* `reader.py` – CSV-tiedoston luku
* `sample_table.py` – näytetaulukon muodostaminen
* `csv_exporter.py` – laitteelle vietävän CSV:n luonti
* `barcode_generator.py` – viivakoodien muodostaminen
* `pdf_exporter.py` – pipetointilistan PDF:n luonti
* `config.py` – ohjelman asetukset

## Käynnistäminen

Asenna tarvittavat kirjastot:

```bash
pip install -r requirements.txt
```

Käynnistä ohjelma:

```bash
python main.py
```

## Kehitystyö

Tämä projekti on toteutettu osana opinnäytetyöprojektia. Kehitystyössä on käytetty apuna OpenAI:n ChatGPT-tekoälyä.