from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import api.sodoku_solver as motor_sudoku 
import numpy as np
import random 
from api.genetic_logic import evolucionar

app = FastAPI()

#configuramos servidor para aceptar peticiones del frontend
# Definimos quién tiene permiso para hablar con este servidor.
sitios_permitidos = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=sitios_permitidos,
    allow_credentials=True,
    allow_methods=["*"], # Permitir todo tipo de peticiones (GET, POST, etc.)
    allow_headers=["*"],
)

class Entidad(BaseModel):
    id: int # El frontend envía IDs numéricos (timestamp)
    x: float
    y: float
    radio: Optional[float] = 0

class SolicitudSudoku(BaseModel):
    board: List[List[int]]

class SimulationInput(BaseModel):
    precio_actual: float
    volatilidad: float  # En porcentaje anual (ej. 0.20 para 20%)
    dias: int
    num_simulaciones: int

class Punto(BaseModel):
    id: int
    x: float
    y: float
    radio: Optional[float] = 0

class Peticion(BaseModel):
    ciudades: List[Entidad]
    obstaculos: List[Entidad]
    poblacion: List[List[Entidad]] = [] # Lista de listas de Entidades
    tamano_poblacion: int = 40


@app.post("/api/evolve")
def endpoint_evolucionar(data: Peticion):
    # Validar que haya ciudades antes de procesar
    if len(data.ciudades) < 2:
        return {"error": "Se necesitan al menos 2 ciudades"}

    poblacion = data.poblacion
    
    if not poblacion:
        for _ in range(data.tamano_poblacion):
            ruta = data.ciudades[:] 
            random.shuffle(ruta)
            poblacion.append(ruta)
            
    # Evolucionar
    mejor_distancia = 0
    try:
        # Intentamos evolucionar 10 veces
        for _ in range(10):
            poblacion, mejor_distancia = evolucionar(poblacion, data.obstaculos)
    except Exception as e:
        print(f"Error interno en lógica genética: {e}")
        # Si falla la lógica, devolvemos lo que tenemos para no romper el frontend
        return {
             "poblacion": poblacion,
             "mejor_ruta": poblacion[0] if poblacion else [],
             "mejor_distancia": 999999
        }
        
    mejor_ruta = poblacion[0]
    
    return {
        "poblacion": poblacion,
        "mejor_ruta": mejor_ruta,
        "mejor_distancia": mejor_distancia
    }