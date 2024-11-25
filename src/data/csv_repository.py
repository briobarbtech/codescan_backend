import csv
from datetime import datetime
import pandas as pd
    
def read_csv(file_name):
    data = []
    with open(f'data/{file_name}.csv', mode='r',encoding='utf-8',newline='') as csv_file:
        csv_file_read = csv.reader(csv_file)
        
        for row in csv_file_read:
            data.append(row)
    return data
    

def write_csv(file_name,data):
    assistance = read_csv(file_name)
    with open(f'data/{file_name}.csv', mode='w',encoding='utf-8',newline='') as csv_file:
        csv_file_writer = csv.writer(csv_file)
        fecha_actual = datetime.now().strftime("%d/%m/%Y")
        assistance.append([data,fecha_actual])
        print(assistance)
        csv_file_writer.writerows(assistance) 
    
        
def convertir_a_excel(dttm):
    # Leer el archivo de entradas y de nombres
    entrada_csv = "data/assistance.csv"
    estudiantes_csv = "data/students.csv"

    df_entradas = pd.read_csv(entrada_csv)
    df_estudiantes = pd.read_csv(estudiantes_csv)

    # Eliminar duplicados en asistencias
    df_entradas = df_entradas.drop_duplicates()

    # Generar una tabla pivote para asistencias
    pivot_asistencias = df_entradas.pivot_table(
        index="id_estudiante", columns="fecha", aggfunc="size", fill_value=0
    ).reset_index()

    # Convertir valores de asistencia a "Presente"
    pivot_asistencias = pivot_asistencias.replace({1: "Presente", 0: "Asusente"})
    pivot_asistencias = pivot_asistencias.replace({0: "Ausente"})
    # Combinar con los datos de estudiantes
    resultado = pd.merge(df_estudiantes, pivot_asistencias, on="id_estudiante", how="left")

    # Exportar a Excel
    resultado.to_excel(f"excel/asistencia_estudiantes_{dttm}.xlsx", index=False)

    print(f"Archivo Excel generado: asistencia_estudiantes_{dttm}.xlsx")

    