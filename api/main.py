from fastapi import FastAPI
from pydantic import BaseModel
from api.utils import jugadores_info, pais_mas_goles ,goles_por_pais, top_goleadores , goles_por_equipo , df

app = FastAPI()

class Player(BaseModel):
    name: str
    team: str
    country: str
    team_nationality: str
    goals: int
    penalty_goals: int

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/players/")
def read_players():
    return df.to_dict(orient='records')

@app.get("/players/{player_name}")
def read_player(player_name: str):
    player_data = jugadores_info(player_name)
    if player_data:
        return player_data
    return {"error": "Player not found"}

@app.get("/country/max-goals")
def obtener_pais_mas_goles():
    resultado = pais_mas_goles()
    return resultado

@app.get("/countries/goals")
def obtener_goles_por_pais():
    return goles_por_pais()

@app.get("/top-scorers")
def obtener_top_goleadores(top: int = 10):
    resultados = top_goleadores(top)
    return resultados

@app.get("/teams/goals")
def obtener_goles_por_equipo():
    return goles_por_equipo()