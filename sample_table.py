import string
import pandas as pd

# Muuttaa 8x12 taulukon 96 näytteen listaksi. 
# Ensin luodaan NumPy-taulukko (.to_numpy()) 
# ja siitä tehdään yksiulotteinen (.T.flatten())

def create_sample_list(df):

    samples = df.to_numpy().T.flatten()

    return samples.tolist()

# Luo 96 näytepaikkaa (96-kuoppalevy). Käyttäjä valitsee ohjelmasta halutun
# analyysilaitteen pleitin (plate), esim. P4 ja ohjelma luo sen perusteella
# plate-paikat (esim. P4-A1, P4-A2 jne.).

def create_positions(plate):

    positions = []

    for column in range(1, 13):
        # käydään läpi numerot 1-12
        for row in string.ascii_uppercase[:8]:
            # käydään läpi aakkosten 8 ensimmäistä kirjainta
            positions.append(
                f"{plate}-{row}{column}"
            )

    return positions

# sama kuin yllä, mutta ilman plate-paikkaa
def create_well_plate_positions():
    well_plate_positions = []

    for column in range(1,13):
        for row in string.ascii_uppercase[:8]:
            well_plate_positions.append(
                f"{row}{column}"
            )

    return well_plate_positions

# Luo pipetointirobotin näytepaikat eli näytteiden alkuperäiset paikat.
# Pipetointirobotilla näytteet ovat 16 näytteen telineissä, joita on 
# 6 kpl. Robotti pipetoi 96-kuoppalevylle aina neljä näytettä kerrallaan
# ja koska näyteputket ovat suurempia kuin kuopat, näytteitä pipetoidaan 
# riveittäin joka toiseen kuoppaan.

def generate_original_positions(number_of_samples):
 
    positions = []

    row_pattern = [
        1, 5, 2, 6, 3, 7, 4, 8,
        9, 13, 10, 14, 11, 15, 12, 16
    ]

    for row in range(1, 7):   # 6 riviä eli 6 näytetelinettä

        for col in row_pattern:

            positions.append(f"{row}_{col}")

            if len(positions) >= number_of_samples:
                return positions

    return positions

# Muodostaa yhden DataFramen, jossa jokainen rivi vastaa
# yhtä 96-kuoppalevyn paikkaa. Sarakkeet: näytenumero, 
# plate-paikka, kuoppalevypaikka, alkuperäinen paikka.

def create_sample_table(df, plate):

    samples = create_sample_list(df)

    positions = create_positions(plate)

    well_plate_positions = create_well_plate_positions()

    original_positions = generate_original_positions(len(samples))

    sample_table = pd.DataFrame({
        "Sample Name": samples,
        "Sample Position": positions,
        "Well Plate Position": well_plate_positions,
        "Original Position": original_positions
    })

    return sample_table

