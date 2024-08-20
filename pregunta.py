"""
Limpieza de datos usando Pandas
-----------------------------------------------------------------------------------------

Realice la limpieza del dataframe. Los tests evaluan si la limpieza fue realizada 
correctamente. Tenga en cuenta datos faltantes y duplicados.

"""

import pandas as pd

def procesar_datos():
    # Cargar datos desde archivo CSV
    datos = pd.read_csv("solicitudes_credito.csv", sep=";", index_col=0)

    # Reemplazar caracteres no deseados y estandarizar texto a minúsculas
    datos = datos.replace(["-", "_"], " ", regex=True)
    datos = datos.applymap(lambda x: x.lower() if isinstance(x, str) else x)

    # Transformar columna monto_del_credito a tipo numérico
    datos["monto_del_credito"] = (
        datos["monto_del_credito"]
        .str.strip()
        .str.replace(r"[,$]|(\.00$)", "", regex=True)
        .astype(float)
    )

    # Convertir columna fecha_de_beneficio a formato de fecha (dos intentos de formato)
    datos["fecha_de_beneficio"] = pd.to_datetime(
        datos["fecha_de_beneficio"], format="%d/%m/%Y", errors="coerce"
    )
    datos["fecha_de_beneficio"].fillna(
        pd.to_datetime(datos["fecha_de_beneficio"], format="%Y/%m/%d", errors="coerce"), inplace=True
    )

    # Convertir comuna_ciudadano a enteros, pero verificando que sean válidos
    datos = datos[datos["comuna_ciudadano"].notna()]  # Eliminar nulos antes de convertir
    datos["comuna_ciudadano"] = datos["comuna_ciudadano"].astype(int)

    # Eliminar duplicados y registros con valores nulos
    datos = datos.drop_duplicates().dropna()

    return datos

procesar_datos()
