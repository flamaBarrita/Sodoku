"use client";
import { useState } from 'react';

// Constante: Tablero de ejemplo 
const TABLERO_EJEMPLO = [
  [5, 3, 0, 0, 7, 0, 0, 0, 0],
  [6, 0, 0, 1, 9, 5, 0, 0, 0],
  [0, 9, 8, 0, 0, 0, 0, 6, 0],
  [8, 0, 0, 0, 6, 0, 0, 0, 3],
  [4, 0, 0, 8, 0, 3, 0, 0, 1],
  [7, 0, 0, 0, 2, 0, 0, 0, 6],
  [0, 6, 0, 0, 0, 0, 2, 8, 0],
  [0, 0, 0, 4, 1, 9, 0, 0, 5],
  [0, 0, 0, 0, 8, 0, 0, 7, 9]
];

// Constante: Genera un tablero vacío de 9x9 con ceros
const TABLERO_VACIO = Array(9).fill().map(() => Array(9).fill(0));

export default function VisualizadorSudoku() {
  // --- ESTADOS (Variables que cambian) ---
  const [tablero, setTablero] = useState(TABLERO_EJEMPLO);
  const [estaResolviendo, setEstaResolviendo] = useState(false);
  const [mensajeEstado, setMensajeEstado] = useState("Listo para jugar");


  // Actualiza una celda específica cuando el usuario escribe un número
  const actualizarCelda = (fila, columna, valorInput) => {
    const valorNumerico = parseInt(valorInput) || 0;
    
    // Solo permitimos números del 0 al 9
    if (valorNumerico >= 0 && valorNumerico <= 9) {
      // Creamos una copia del tablero actual para no modificar el estado directamente
      const nuevoTablero = tablero.map(fila => [...fila]);
      nuevoTablero[fila][columna] = valorNumerico;
      setTablero(nuevoTablero);
    }
  };


  const URL_API = process.env.NODE_ENV === 'production' 
  ? 'https://sodoku-api.vercel.app/'
  : 'http://localhost:8000';

  // Función principal conectado con el backend
  const resolverSudoku = async () => {
    if (estaResolviendo) return; // Evitar doble clic
    
    setEstaResolviendo(true);
    setMensajeEstado("Calculando solución...");

    try {
      //Enviamos el tablero actual al Backend
      const respuesta = await fetch(`${URL_API}/api/solve-sudoku`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ board: tablero }) 
      });

      const datos = await respuesta.json();

      if (!datos.solvable) {
        setMensajeEstado(" Este tablero no tiene solución posible.");
        setEstaResolviendo(false);
        return;
      }

      // 2. Si hay solución, iniciamos la animación
      setMensajeEstado(`¡Solución encontrada! Reproduciendo ${datos.history.length} pasos...`);
      animarSolucion(datos.history);

    } catch (error) {
      console.error(error);
      setMensajeEstado(" Error: No se pudo conectar con el servidor");
      setEstaResolviendo(false);
    }
  };

  // Reproduce el historial de cambios paso a paso
  const animarSolucion = (historialPasos) => {
    let pasoActual = 0;
    
    const intervaloAnimacion = setInterval(() => {
      // Condición de parada: Si llegamos al final del historial
      if (pasoActual >= historialPasos.length) {
        clearInterval(intervaloAnimacion);
        setEstaResolviendo(false);
        setMensajeEstado("¡Sudoku Resuelto!");
        return;
      }

      // Actualizamos el tablero visual con la "foto" del paso actual
      setTablero(historialPasos[pasoActual]);
      pasoActual++;
    }, 30); // Velocidad de visualizacion
  };

  // render que se muestra en pantalla
  return (
    <main className="flex flex-col items-center justify-center min-h-screen bg-gray-50 p-5 font-sans">
      <h1 className="text-3xl font-bold mb-2 text-gray-800">Visualizador de Sudoku</h1>
      <p className="text-gray-600 mb-6 font-medium">{mensajeEstado}</p>

      {/* Contenedor del Grid (Borde grueso exterior) */}
      <div className="bg-black border-4 border-black p-1 shadow-lg">
        {/* Grid CSS de 9x9 */}
        <div className="grid grid-cols-9 gap-px bg-black">
          {tablero.map((fila, indiceFila) => (
            fila.map((valorCelda, indiceColumna) => {
              
              // Lógica visual: Añadir margen extra cada 3 celdas para separar los cuadrantes
              const bordeDerecho = (indiceColumna + 1) % 3 === 0 && indiceColumna !== 8 ? 'mr-1' : '';
              const bordeInferior = (indiceFila + 1) % 3 === 0 && indiceFila !== 8 ? 'mb-1' : '';

              return (
                <input
                  key={`${indiceFila}-${indiceColumna}`}
                  type="text"
                  maxLength="1"
                  value={valorCelda === 0 ? '' : valorCelda}
                  onChange={(e) => actualizarCelda(indiceFila, indiceColumna, e.target.value)}
                  disabled={estaResolviendo}
                  className={`
                    w-8 h-8 sm:w-10 sm:h-10 text-center text-xl font-medium outline-none
                    ${bordeDerecho} ${bordeInferior}
                    ${valorCelda !== 0 ? 'bg-white text-gray-900' : 'bg-blue-50 text-blue-800'}
                    focus:bg-blue-200 transition-colors cursor-pointer
                  `}
                />
              );
            })
          ))}
        </div>
      </div>

      {/* Botonera */}
      <div className="flex gap-4 mt-8">
        <button
          onClick={() => setTablero(TABLERO_EJEMPLO)}
          disabled={estaResolviendo}
          className="px-4 py-2 bg-gray-200 text-gray-700 rounded hover:bg-gray-300 transition disabled:opacity-50 font-medium"
        >
          Cargar Ejemplo
        </button>
        
        <button
          onClick={() => setTablero(TABLERO_VACIO)}
          disabled={estaResolviendo}
          className="px-4 py-2 bg-red-100 text-red-600 rounded hover:bg-red-200 transition disabled:opacity-50 font-medium"
        >
          Limpiar
        </button>

        <button
          onClick={resolverSudoku}
          disabled={estaResolviendo}
          className="px-6 py-2 bg-blue-600 text-white font-bold rounded shadow hover:bg-blue-700 transition disabled:opacity-50 transform hover:scale-105 active:scale-95"
        >
          {estaResolviendo ? 'Resolviendo...' : 'Resolver'}
        </button>
      </div>
    </main>
  );
}