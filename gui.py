import tkinter as tk
from tkinter import ttk, filedialog
from tkinter import messagebox
from PIL import Image, ImageTk
from pathlib import Path
import sys
import os
from config import METHODS, PLATES, VERSION

""" 
Ohjelman graafinen käyttöliittymä (GUI), jossa valitaan
pipetointirobotilta saatu csv-tiedosto ja haluttu plate 
sekä ajometodi analyysilaitteella.
"""


def get_user_input(process_function):
    # Näyttää käyttöliittymän ja käynnistää tiedostojen käsittelyn
    # käyttäjän tekemien valintojen perusteella.

    # ---------- Ikkuna ----------

    root = tk.Tk()
    root.title("Muuntaja")
    root.geometry("620x390")
    root.resizable(False, False)
    root.title(f"Muuntaja v{VERSION}")

    main_frame = ttk.Frame(root, padding=20)
    main_frame.pack(fill="both", expand=True)
    main_frame.columnconfigure(1, weight=1)

    ttk.Label(
        main_frame,
        text=(
            "Valitse pipetointirobotilta saatu CSV-tiedosto "
            "sekä analyysilaitteella käytettävä plate ja ajometodi.\n"
            "\n"
            "Ohjelma luo kaksi tiedostoa:\n"
            "1. analyysilaitteelle siirrettävän CSV-tiedoston\n"
            "2. viivakoodit sisältävän pipetointilistan PDF-muodossa\n"
            "\n"
            "Tiedostot tallennetaan samaan kansioon kuin mistä alkuperäinen CSV-tiedosto haettiin."
        ),
        justify="left"
    ).grid(
        row=0,
        column=0,
        columnspan=3,
        sticky="w",
        pady=(0, 15)
    )

    ttk.Separator(
        main_frame,
        orient="horizontal"
    ).grid(
        row=1,
        column=0,
        columnspan=3,
        sticky="ew",
        pady=15
    )

    # ---------- Kuva ----------

    # resurssitiedoston polun palauttaminen
    def resource_path(relative_path):

        # pakatussa sovelluksessa
        if hasattr(sys, "_MEIPASS"):
            return Path(sys._MEIPASS) / relative_path

        return Path(__file__).parent / relative_path
    
    image = Image.open(
        resource_path("images/image.png")
    )

    resized_image = image.resize((50, 50))

    photo_image = ImageTk.PhotoImage(resized_image)

    label = ttk.Label(
        main_frame,
        image=photo_image
    )

    label.image = photo_image

    label.grid(
        row=5,
        column=2,
        padx=15,
        pady=15,
    )

    # ---------- Muuttujat ----------

    csv_var = tk.StringVar()
    plate_var = tk.StringVar(
        value=PLATES[0]
    )
    method_var = tk.StringVar(
        value=METHODS[0]
    )

    # ---------- Callback-funktiot ----------

    def browse_csv():

        filename = filedialog.askopenfilename(
            title="Valitse CSV-tiedosto",
            filetypes=[
                ("CSV-tiedostot", "*.csv")
            ]
        )

        if filename:
            csv_var.set(filename)

    def run():

        if not csv_var.get():

            messagebox.showerror(
                "Virhe",
                "Valitse ensin CSV-tiedosto."
            )

            return

        settings = {
            "csv_file": csv_var.get(),
            "plate": plate_var.get(),
            "method": method_var.get()
        }

        success, csv_path, pdf_path = process_function(settings)

        if success:

            messagebox.showinfo(
                "Valmis",
                f"Tiedostot luotiin onnistuneesti.\n\n"
                f"CSV:\n{csv_path.name}\n\n"
                f"PDF:\n{pdf_path.name}"
            )

            csv_var.set("")

            os.startfile(pdf_path) # avataan PDF-tiedosto
            os.startfile(csv_path.parent) # avataan tiedostokansio

        else:

            messagebox.showerror(
                "Virhe",
                f"{csv_path}\n\n{pdf_path}"
            )

    def cancel():

        root.destroy()

    # ---------- CSV ----------

    ttk.Label(
        main_frame,
        text="CSV-tiedosto"
    ).grid(
        row=2,
        column=0,
        sticky="w",
        pady=8
    )

    csv_entry = ttk.Entry(
        main_frame,
        textvariable=csv_var
    )

    csv_entry.grid(
        row=2,
        column=1,
        sticky="ew",
        padx=(10, 10)
    )

    ttk.Button(
        main_frame,
        text="Selaa...",
        command=browse_csv
    ).grid(
        row=2,
        column=2
    )

    # ---------- Plate ----------

    ttk.Label(
        main_frame,
        text="Plate"
    ).grid(
        row=3,
        column=0,
        sticky="w",
        pady=15
    )

    ttk.Combobox(
        main_frame,
        textvariable=plate_var,
        values=PLATES,
        state="readonly",
        width=8
    ).grid(
        row=3,
        column=1,
        sticky="w",
        padx=(10, 0)
    )

    # ---------- Ajometodi ----------

    ttk.Label(
        main_frame,
        text="Ajometodi"
    ).grid(
        row=4,
        column=0,
        sticky="w",
        pady=15
    )

    ttk.Combobox(
        main_frame,
        textvariable=method_var,
        values=METHODS,
        state="readonly",
        width=20
    ).grid(
        row=4,
        column=1,
        sticky="w",
        padx=(10, 0)
    )

    # ---------- Painikkeet ----------

    button_frame = ttk.Frame(main_frame)

    button_frame.grid(
        row=5,
        column=0,
        columnspan=3,
        pady=25
    )

    create_button = ttk.Button(
        button_frame,
        text="Luo tiedostot",
        width=18,
        command=run
    )

    create_button.pack(
        side="left",
        padx=5
    )

    create_button.focus_set()

    ttk.Button(
        button_frame,
        text="Peruuta",
        width=12,
        command=cancel
    ).pack(
        side="left",
        padx=5
    )

    # ---------- Tapahtumat ------------

    root.bind(
        "<Return>",
        lambda event: run()
    )

    root.bind(
        "<Escape>",
        lambda event: cancel()
    )

    root.protocol(
        "WM_DELETE_WINDOW",
        cancel
    )

    root.mainloop()