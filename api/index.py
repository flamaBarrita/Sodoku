from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
import api.sodoku_solver as motor_sudoku 

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


class SolicitudSudoku(BaseModel):
    board: List[List[int]]

@app.post("/api/solve-sudoku")
def endpoint_resolver_sudoku(datos: SolicitudSudoku):
   # recibimos el tablero desde el frontend y preparamos todo para resolverlo

    # Borramos las fotos de la jugada anterior
    motor_sudoku.historial_visual.clear()
    
    # Creamos una copia de trabajo del tablero recibido
    # (Usamos comprensión de listas para copiar fila por fila y evitar errores de referencia)
    tablero_para_resolver = [fila[:] for fila in datos.board]
    
    # Ejecutamos el algoritmo 
    se_encontro_solucion = motor_sudoku.resolver_sudoku(tablero_para_resolver)
    
    # Empaquetamos todo para enviarlo de vuelta al navegador
    return {
        "solvable": se_encontro_solucion,         # Booleano: ¿Se pudo resolver? T - F
        "solution": tablero_para_resolver,        # El tablero final ya resuelto
        "history": motor_sudoku.historial_visual  # La lista de "fotos" para la animación
    }