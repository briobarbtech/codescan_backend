import csv
from datetime import datetime
import pandas as pd
    
def read_csv(file_name):
    data = []
    with open(f'src/data/{file_name}.csv', mode='r',encoding='utf-8',newline='') as csv_file:
        csv_file_read = csv.reader(csv_file)
        
        for row in csv_file_read:
            data.append(row)
    return data
    

def write_csv(file_name,data):
    assistance = read_csv(file_name)
    with open(f'src/data/{file_name}.csv', mode='w',encoding='utf-8',newline='') as csv_file:
        csv_file_writer = csv.writer(csv_file)
        fecha_actual = datetime.now().strftime("%d/%m/%Y")
        assistance.append([data,fecha_actual])
        print(assistance)
        csv_file_writer.writerows(assistance) 
    
        
def convertir_a_excel(dttm):
    # Leer el archivo de entradas y de nombres
    entrada_csv = "src/data/assistance.csv"
    estudiantes_csv = "src/data/students.csv"

    df_entradas = pd.read_csv(entrada_csv)
    df_estudiantes = pd.read_csv(estudiantes_csv)

    # Asegurar que las fechas sean de tipo datetime
    df_entradas['fecha'] = pd.to_datetime(df_entradas['fecha'])

    
    # Unir las entradas con los nombres de los estudiantes
    df_combinado = pd.merge(df_entradas, df_estudiantes, on='id_estudiante')
    if 'fecha_de_nacimiento' in df_combinado.columns:
        df_combinado = df_combinado.drop(columns=['fecha_de_nacimiento'])
    # Crear la tabla pivote
    pivot_df = df_combinado.pivot_table(
        index=['id_estudiante', 'nombre','apellido'],  # Incluir nombre como parte del índice
        columns='fecha',
        aggfunc=lambda x: 'Presente',
        fill_value='Ausente'
    )

    # Aplanar las columnas de MultiIndex a un simple Index
    pivot_df.columns = pivot_df.columns.get_level_values(0)

    # Formatear las columnas de fechas
    pivot_df.columns = [col.strftime('%Y-%m-%d') if isinstance(col, pd.Timestamp) else col for col in pivot_df.columns]

    # Resetear el índice para que `id_estudiante` y `nombre` sean columnas normales
    pivot_df = pivot_df.reset_index()

    # Guardar como archivo Excel
    excel_file = f"excel/asistencia_estudiantes_{dttm}.xlsx"
    pivot_df.to_excel(excel_file, index=False)

    print(f"Archivo Excel generado: {excel_file}")