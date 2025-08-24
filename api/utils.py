from pathlib import Path
import pandas as pd

# Ruta al archivo CSV relativa a la raíz del proyecto
csv_path = Path(__file__).parent.parent / 'datos' / 'Copa_Libertadores_2023_Complete_Goal_Scorers.csv'

df = pd.read_csv(csv_path)

def jugadores_info(nombre):
    """
    Devuelve la información de los jugadores.
    """
    df_copy = df.copy()  # Hacer una copia del DataFrame para evitar modificar el original
    df_copy['Player'] = df_copy['Player'].str.lower()  # Normalizar nombres de jugadores a minúsculas
    nombre = nombre.lower()  # Normalizar el nombre del jugador a minúsculas
    nombre = nombre.replace("á", "a").replace("é", "e").replace("í", "i").replace("ó", "o").replace("ú", "u").replace("ñ", "n")  # Eliminar tildes
    nombre = nombre.replace(" ", "")  # Eliminar espacios en blanco
    nombre = re.sub(r'[^a-zA-Z]', '', nombre)  # Eliminar caracteres especiales
    df_copy['Player'] = df_copy['Player'].str.replace("á", "a").replace("é", "e").replace("í", "i").replace("ó", "o").replace("ú", "u").replace("ñ", "n")  # Eliminar tildes en el DataFrame
    df_copy['Player'] = df_copy['Player'].str.replace(" ", "")  # Eliminar espacios en blanco en el DataFrame
    df_copy['Player'] = df_copy['Player'].str.replace(r'[^a-zA-Z]', '', regex=True)  # Eliminar caracteres especiales en el DataFrame

    # Filtrar el DataFrame por el nombre del jugador
    df_player = df_copy[df_copy['Player'].str.contains(nombre, case=False, regex=True)]

    if df_player.empty:
        return {"error": "Player not found"}
    # Convertir el DataFrame filtrado a un diccionario
    df_player = df.loc[df_player.index]
    df_player['Player'] = df_player['Player'].str.title()  # Formate
    df_player['Team'] = df_player['Team'].str.title()  # Formatear nombres de equipos
    df_player['Country'] = df_player['Country'].str.title()  # Formatear nombres de países
    df_player['Team Nationality'] = df_player['Team Nationality'].str.title()  # Formatear nombres de países
    df_player['Goals'] = df_player['Goals'].astype(int)  # Asegurarse de que los goles son enteros
    df_player['Penalty Goals'] = df_player['Penalty Goals'].astype(int)  # Asegurarse de que los goles de penalti son enteros
    df_player = df_player[['Player', 'Team', 'Country', 'Team Nationality', 'Goals', 'Penalty Goals']]

    return df_player.to_dict(orient='records')


def pais_mas_goles():
    """
    Devuelve el pais con mas goles en la competición
    """
    # Agrupar por país y sumar goles
    goles_por_pais = df.groupby('Country')['Goals'].sum().reset_index()
    
    # Ordenar de mayor a menor por goles
    goles_por_pais = goles_por_pais.sort_values(by='Goals', ascending=False)
    
    # Tomar la primera fila (país con más goles)
    top_pais = goles_por_pais.head(1)
    
    # Devolver como lista de diccionarios (records)
    return top_pais.to_dict(orient='records')

def goles_por_pais():
    """
    Devuelve la cantidad de goles por país en la competición.
    """
    # Agrupar goles por país y sumar
    goles_totales = df.groupby('Country')['Goals'].sum().reset_index()
    
    # Opcional: ordenar de mayor a menor goles
    goles_totales = goles_totales.sort_values(by='Goals', ascending=False)
    
    # Devolver como lista de diccionarios
    return goles_totales.to_dict(orient='records')

def top_goleadores(top_n: int = 10):
    """
    Devuelve los jugadores con más goles en la competición, por defecto devolverá el top 10
    """
    # Filtrar fuera jugadores con 0 goles
    df_non_zero = df[df['Goals'] > 0]
    
    # Ordenar el DataFrame por goles (Goals) de forma descendente y tomar el top_n
    df_sorted = df_non_zero.sort_values(by='Goals', ascending=False).head(top_n)
    
    # Seleccionar columnas relevantes y formatear
    df_top = df_sorted[['Player', 'Team', 'Country', 'Team Nationality', 'Goals', 'Penalty Goals']].copy()
    df_top['Player'] = df_top['Player'].str.title()
    
    # Devolver como lista de diccionarios
    return df_top.to_dict(orient='records')

def goles_por_equipo():
    """
    Devuelve la cantidad de goles por equipo en la competición.
    """
    # Agrupar goles por equipo y sumar
    goles_totales = df.groupby('Team')['Goals'].sum().reset_index()
    
    # Ordenar de menor a mayor goles
    goles_totales = goles_totales.sort_values(by='Goals', ascending=False)
    
    # Devolver como lista de diccionarios
    return goles_totales.to_dict(orient='records')
