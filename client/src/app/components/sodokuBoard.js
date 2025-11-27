import { useState } from 'react';

// Tablero inicial vacío (9x9 de ceros)
const emptyBoard = Array(9).fill().map(() => Array(9).fill(0));

export default function SudokuBoard() {
  const [board, setBoard] = useState(emptyBoard);
  const [isSolving, setIsSolving] = useState(false);

  // Manejar cambio en inputs
  const handleChange = (row, col, value) => {
    const newVal = parseInt(value) || 0;
    if (newVal >= 0 && newVal <= 9) {
      const newBoard = board.map(r => [...r]); // Copia profunda simple
      newBoard[row][col] = newVal;
      setBoard(newBoard);
    }
  };

  const handleSolve = async () => {
    setIsSolving(true);
    const res = await fetch('/api/solve-sudoku', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ board: board })
    });
    const data = await res.json();
    
    if (data.history) {
      animateSolution(data.history);
    } else {
        alert("No tiene solución o hubo un error");
        setIsSolving(false);
    }
  };

  const animateSolution = (history) => {
    let i = 0;
    const interval = setInterval(() => {
        if (i >= history.length) {
            clearInterval(interval);
            setIsSolving(false);
            return;
        }
        setBoard(history[i]);
        i++;
    }, 50); // Velocidad muy rápida (50ms) porque Sudoku tiene muchos pasos
  };

  return (
    <div className="flex flex-col items-center gap-6">
      {/* Grid CSS específico para Sudoku: bordes gruesos cada 3 celdas */}
      <div className="grid grid-cols-9 border-4 border-black bg-black gap-px">
        {board.map((row, rIndex) => (
          row.map((cell, cIndex) => {
            // Lógica para bordes gruesos internos
            const borderRight = (cIndex + 1) % 3 === 0 && cIndex !== 8 ? 'border-r-2 border-r-black' : '';
            const borderBottom = (rIndex + 1) % 3 === 0 && rIndex !== 8 ? 'border-b-2 border-b-black' : '';

            return (
              <input
                key={`${rIndex}-${cIndex}`}
                type="text"
                value={cell === 0 ? '' : cell}
                onChange={(e) => handleChange(rIndex, cIndex, e.target.value)}
                disabled={isSolving}
                className={`w-10 h-10 text-center text-xl focus:bg-blue-100 outline-none
                  ${borderRight} ${borderBottom} bg-white`}
              />
            );
          })
        ))}
      </div>

      <div className="flex gap-4">
        <button 
            onClick={handleSolve} 
            className="bg-green-600 text-white px-6 py-2 rounded font-bold hover:bg-green-700 disabled:opacity-50">
            {isSolving ? 'Resolviendo...' : 'Resolver Sudoku'}
        </button>
        <button 
            onClick={() => setBoard(emptyBoard)}
            className="bg-red-500 text-white px-4 py-2 rounded hover:bg-red-600">
            Limpiar
        </button>
      </div>
    </div>
  );
}