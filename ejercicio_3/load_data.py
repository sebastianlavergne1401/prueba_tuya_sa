import pandas as pd
import sqlite3
import os

def prepare_database():
    # 1. Configurar conexión
    conn = sqlite3.connect('ejercicio_3/solution_database.db')
    cursor = conn.cursor()

    # 2. Leer el Schema
    with open('ejercicio_3/schema.sql', 'r', encoding='utf-8') as f:
        cursor.executescript(f.read())

    # 3. Cargar datos
    path_excel = 'ejercicio_3/Prueba Tecnica.xlsx'
    df_historia = pd.read_excel(path_excel, sheet_name='historia')
    df_retiros = pd.read_excel(path_excel, sheet_name='retiros')

    # Eliminar duplicados exactos y asegurar formatos de fecha
    df_historia = df_historia.drop_duplicates()
    df_historia['corte_mes'] = pd.to_datetime(df_historia['corte_mes']).dt.strftime('%Y-%m-%d')
    df_retiros['fecha_retiro'] = pd.to_datetime(df_retiros['fecha_retiro']).dt.strftime('%Y-%m-%d')

    # 4. Cargar a SQLite
    df_historia.to_sql('historia', conn, if_exists='append', index=False)
    df_retiros.to_sql('retiros', conn, if_exists='append', index=False)

    print("Base de datos construida y datos cargados con éxito.")
    conn.close()

if __name__ == "__main__":
    prepare_database()