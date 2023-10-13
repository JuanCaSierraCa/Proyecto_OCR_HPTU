import pandas as pd
import tabula.io as tabula
import os
from tkinter import filedialog
from tkinter import Tk

def extract_data_from_pdf(pdf_path):
    area = [85.12, 56.65, 299.88, 292.83]
    df = tabula.read_pdf(pdf_path, pages=3, area=area, stream=True, multiple_tables=False)[0]

    df['Antibiotic'] = df['Antibiotic MIC value mcg/ml'].str.extract(r'([a-zA-Z\s/]+)')
    df['MIC value mcg/ml (mg/L)'] = df['Antibiotic MIC value mcg/ml'].str.extract(r'(\>\d+|\d+)')
    df.drop(columns=['Antibiotic MIC value mcg/ml', 'Unnamed: 1'], inplace=True)

    df = df[['Antibiotic', 'MIC value mcg/ml (mg/L)', 'Interpretation']]

    # Elimina cualquier fila con NaN en la columna 'Antibiotic'
    df = df.dropna(subset=['Antibiotic'])

    df = df.drop([0, 20])
    df.reset_index(drop=True, inplace=True)

    return(df)

def main():
    # Permite al usuario seleccionar varios archivos PDF
    root = Tk()
    root.withdraw()
    file_paths = filedialog.askopenfilenames(title="Selecciona los archivos PDF", filetypes=(("PDF files", "*.pdf"), ("all files", "*.*")))

    for file_path in file_paths:
        df = extract_data_from_pdf(file_path)
        if df is None:
            print(f"El archivo {file_path} no devolvió un DataFrame válido.")
            continue
        output_csv = os.path.splitext(file_path)[0] + ".csv"
        df.to_csv(output_csv, index=False)
        print(f"Archivo {output_csv} generado correctamente.")


main()

