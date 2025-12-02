import random
import math

# --- MATEMÁTICAS: DETECCIÓN DE CHOQUES ---

def distancia_punto_segmento(px, py, x1, y1, x2, y2):
    """Calcula la distancia mínima entre un punto (p) y un segmento de línea (x1,y1)-(x2,y2)."""
    # Longitud del segmento al cuadrado
    l2 = (x1 - x2)**2 + (y1 - y2)**2
    if l2 == 0: return math.sqrt((px - x1)**2 + (py - y1)**2) # Los puntos son iguales

    # Proyectar el punto sobre la línea (valor t entre 0 y 1)
    t = ((px - x1) * (x2 - x1) + (py - y1) * (y2 - y1)) / l2
    t = max(0, min(1, t)) # Limitamos al segmento

    # Encontrar el punto de proyección
    proy_x = x1 + t * (x2 - x1)
    proy_y = y1 + t * (y2 - y1)

    # Distancia euclidiana
    return math.sqrt((px - proy_x)**2 + (py - proy_y)**2)

def choca_con_obstaculo(c1, c2, obstaculo):
    """Verifica si la línea entre ciudad 1 y ciudad 2 toca el círculo del obstáculo."""
    dist = distancia_punto_segmento(obstaculo.x, obstaculo.y, c1.x, c1.y, c2.x, c2.y)
    # Si la distancia es menor al radio, hay choque. 
    # Agregamos +5 de margen para que no pase "rozando".
    return dist < (obstaculo.radio + 5)

# --- ALGORITMO GENÉTICO ---

def calcular_fitness(ruta, obstaculos):
    distancia_total = 0
    penalizacion = 0
    
    for i in range(len(ruta)):
        a = ruta[i]
        b = ruta[(i + 1) % len(ruta)] # Conectar último con primero
        
        # 1. Distancia normal
        d = math.sqrt((a.x - b.x)**2 + (a.y - b.y)**2)
        distancia_total += d
        
        # 2. Verificar obstáculos
        for obs in obstaculos:
            if choca_con_obstaculo(a, b, obs):
                # ¡CASTIGO! Sumamos 5000 puntos de distancia falsa.
                # El algoritmo evitará esto a toda costa.
                penalizacion += 5000 
                break # Con chocar uno basta

    # Retornamos la distancia penalizada (mientras menor sea, mejor)
    return distancia_total + penalizacion

def crear_hijo(padre1, padre2):
    """
    Cruce 'Ordered Crossover'.
    Toma una sección del Padre 1 y rellena con el Padre 2 sin repetir ciudades.
    """
    size = len(padre1)
    # Elegir dos puntos de corte al azar
    start, end = sorted(random.sample(range(size), 2))
    
    hijo = [None] * size
    # Copiar el ADN del padre 1
    hijo[start:end] = padre1[start:end]
    
    # Rellenar huecos con el padre 2 (en orden)
    pos = end
    for gen in padre2:
        # Si la ciudad no está ya en el hijo (comparando IDs)
        if gen.id not in [g.id for g in hijo if g is not None]:
            if pos >= size: pos = 0 # Dar la vuelta
            while hijo[pos] is not None:
                pos += 1
                if pos >= size: pos = 0
            hijo[pos] = gen
            
    return hijo

def mutar(ruta):
    """Intercambia dos ciudades al azar."""
    if random.random() < 0.3: # 30% de probabilidad
        i, j = random.sample(range(len(ruta)), 2)
        ruta[i], ruta[j] = ruta[j], ruta[i]
    return ruta

def evolucionar(poblacion, obstaculos):
    # 1. Evaluar a todos
    # Guardamos (ruta, puntaje)
    evaluados = []
    for ruta in poblacion:
        score = calcular_fitness(ruta, obstaculos)
        evaluados.append((ruta, score))
    
    # 2. Ordenar: El menor puntaje (distancia) va primero
    evaluados.sort(key=lambda x: x[1])
    
    # Elitismo: El mejor pasa directo a la siguiente generación
    nueva_gen = [evaluados[0][0]]
    
    # 3. Reproducción (Torneo simple)
    top_50_porciento = [x[0] for x in evaluados[:len(evaluados)//2]]
    
    while len(nueva_gen) < len(poblacion):
        # Elegir padres del top 50%
        p1 = random.choice(top_50_porciento)
        p2 = random.choice(top_50_porciento)
        
        hijo = crear_hijo(p1, p2)
        hijo = mutar(hijo)
        nueva_gen.append(hijo)
        
    return nueva_gen, evaluados[0][1] # Devolvemos pob nueva y mejor distancia