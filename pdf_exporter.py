from reportlab.lib.pagesizes import A4
from reportlab.platypus import (
    SimpleDocTemplate,
    Table,
    TableStyle,
    Paragraph,
    Spacer,
    Image
)
from reportlab.lib.styles import getSampleStyleSheet


def create_bc_pdf(
        bc_data,
        pdf_output_file,
        title="Pipetointilista"
):

    pdf = SimpleDocTemplate(
        pdf_output_file,
        pagesize=A4,
        topMargin=25,
        bottomMargin=25,
        leftMargin=25,
        rightMargin=25
    )

    styles = getSampleStyleSheet()

    styles["Heading2"].fontSize = 14
    styles["Heading2"].leading = 16

    elements = []

    elements.append(
        Paragraph(title, styles["Heading2"])
    )

    elements.append(
        Spacer(1, 12)
    )

    table_data = [
    [
        "Nro",
        "Näytenumero",
        "Viivakoodi",
        "Paikka 96-kuoppalevyllä",
        "Alkuperäinen paikka"
    ]
    ]

    for i, (_, row) in enumerate(
        bc_data.iterrows(),
        start=1
    ):

        table_data.append([
            i,
            row["Sample Name"],
            Image(
                row["Barcode"],
                width=120,
                height=35
            ),
            row["Well Plate Position"],
            row["Original Position"]
        ])

    table = Table(
        table_data,
        repeatRows=1
    )


    table.setStyle(
        TableStyle([
            ("GRID", (0, 0), (-1, -1), 0.5, None),
            ("FONT", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("ALIGN", (0, 0), (0, -1), "CENTER"), # Nro
            ("ALIGN", (2, 0), (2, 0), "CENTER"), # Viivakoodi
            ("ALIGN", (3, 1), (4, -1), "CENTER"), # Paikka ja alkup. paikka
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ("FONTSIZE", (0, 0), (-1, -1), 9),
            ("TOPPADDING", (0, 0), (-1, -1), 5),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ])
    )

    elements.append(table)

    pdf.build(elements)
     