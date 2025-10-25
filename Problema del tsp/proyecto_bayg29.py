#Problema del Viajante (TSP): En matemáticas y ciencias de la computación, se refiere al problema del viajante, que busca la ruta más corta entre varias ciudades. 
"""
Librerias q se ocuparon:
* math
* numpy
* matplotlib

Para insalarlas es desde la terminal y usando este comando:
pip install (nombre de la libreria)
"""
import math
import numpy as np
import matplotlib.pyplot as plt

# Número máximo de nodos (ciudades) que puede manejar el programa
MAX_NODOS = 200

# ---------------------------------------------------------------
# Funciones para resolver el problema del viajante de comercio (TSP)
# usando un archivo con coordenadas de ciudades y cálculo de rutas.
# ---------------------------------------------------------------

def leer_tsp(filename):
    """
    Lee las coordenadas de las ciudades desde un archivo .tsp.
    El archivo contiene líneas con ID, coordenada X y coordenada Y.
    Se detiene al encontrar la línea 'EOF'.
    Devuelve dos arreglos numpy con las coordenadas X e Y.
    """
    xcoord, ycoord = [], []
    with open(filename, "r") as f:
        for line in f:
            # Si se encuentra la línea EOF, termina la lectura
            if line.strip().startswith("EOF"):
                break
            parts = line.strip().split()
            # Solo considera líneas con 3 partes y que la primera sea un número (ID)
            if len(parts) == 3 and parts[0].isdigit():
                _, x, y = parts
                # Agrega las coordenadas convertidas a float a las listas
                xcoord.append(float(x))
                ycoord.append(float(y))
    # Convierte las listas a arreglos numpy para facilitar cálculos posteriores
    return np.array(xcoord), np.array(ycoord)

def calcular_matriz_distancias(x, y):
    """
    Calcula la matriz de distancias euclidianas entre todas las ciudades.
    La distancia entre dos puntos se calcula con la fórmula sqrt((x2-x1)^2 + (y2-y1)^2).
    El resultado se redondea al entero más cercano.
    Devuelve una matriz cuadrada donde cada elemento [i,j] es la distancia entre ciudad i y j.
    """
    n = len(x)
    dist = np.zeros((n, n))  # Inicializa matriz de distancias con ceros
    for i in range(n):
        for j in range(n):
            dx, dy = x[i] - x[j], y[i] - y[j]
            dist[i, j] = round(math.sqrt(dx**2 + dy**2))
    return dist

def costo_ruta(ruta, dist):
    """
    Calcula el costo total (distancia) de una ruta cerrada.
    La ruta es una lista o arreglo con el orden de las ciudades visitadas.
    Suma las distancias entre ciudades consecutivas y la distancia de regreso al inicio.
    """
    costo = 0
    n = len(ruta)
    for i in range(n - 1):
        costo += dist[ruta[i], ruta[i + 1]]  # Distancia entre ciudad actual y siguiente
    costo += dist[ruta[-1], ruta[0]]  # Añade distancia de la última ciudad al inicio para cerrar la ruta
    return costo

def graficar_ruta(x, y, ruta, costo_total):
    """
    Muestra gráficamente el recorrido de la ruta.
    Dibuja líneas entre las ciudades en el orden de la ruta y marca la distancia total.
    También muestra etiquetas con números para identificar cada ciudad.
    """
    plt.figure(figsize=(8, 6))
    # Dibuja la ruta con puntos azules conectados por líneas
    plt.plot(x[ruta], y[ruta], 'bo-', label='Ruta')
    # Dibuja línea punteada roja para el regreso al punto inicial
    plt.plot([x[ruta[-1]], x[ruta[0]]], [y[ruta[-1]], y[ruta[0]]], 'r--', label='Regreso al inicio')
    # Añade número identificador cerca de cada ciudad
    for i, (xi, yi) in enumerate(zip(x, y), start=1):
        plt.text(xi + 2, yi + 2, str(i), fontsize=9)
    # Título con el costo total del recorrido
    plt.title(f"Recorrido de ciudades\nCosto total: {costo_total:.2f}")
    plt.xlabel("Coordenada X")
    plt.ylabel("Coordenada Y")
    plt.legend()
    plt.grid(True)
    plt.show()

def calcular_angulos(x, y):
    """
    Calcula el ángulo de cada ciudad respecto a la primera ciudad.
    Usa la función atan2 para obtener el ángulo en radianes y luego lo convierte a grados.
    Esto puede ayudar a ordenar las ciudades en sentido angular para ciertos algoritmos.
    Devuelve un arreglo con los ángulos correspondientes a cada ciudad.
    """
    x0, y0 = x[0], y[0]  # Ciudad de referencia (la primera)
    angulos = []
    for i in range(len(x)):
        dx, dy = x[i] - x0, y[i] - y0
        ang = math.degrees(math.atan2(dy, dx))  # Convertir a grados
        angulos.append(ang)
    return np.array(angulos)

def algoritmo_petalos(x, y, dist):
    """
    Implementación simplificada del algoritmo de pétalos para resolver TSP.
    Ordena las ciudades según el ángulo respecto a la primera ciudad.
    Devuelve la ruta ordenada, el costo total y los ángulos calculados.
    """
    n = len(x)
    angulos = calcular_angulos(x, y)
    orden = np.argsort(angulos)  # Ordena por ángulo creciente
    ruta = orden.tolist()
    costo_total = costo_ruta(ruta, dist)
    return ruta, costo_total, angulos

def main():
    # Nombre del archivo con las coordenadas de las ciudades
    filename = "bayg29.tsp"

    # --- Lectura del archivo ---
    # Lee las coordenadas X e Y desde el archivo .tsp
    x, y = leer_tsp(filename)
    n = len(x)  # Número de ciudades leídas

    # --- Cambio del punto inicial ---
    # Queremos que la ciudad 13 sea el punto de partida (índice 12)
    punto_inicial = 13 - 1  # índice base 0 para ciudad 13
    # Intercambiamos las coordenadas de la ciudad 1 y la ciudad 13 para que la ciudad 13 sea la primera
    x[[0, punto_inicial]] = x[[punto_inicial, 0]]
    y[[0, punto_inicial]] = y[[punto_inicial, 0]]
    print(f"La ciudad 13 ahora es el punto inicial (nueva ciudad 1)\n")

    print(f"Se leyeron {n} nodos del archivo {filename}\n")

    # --- Mostrar coordenadas ---
    # Imprime una tabla con los IDs y las coordenadas de cada ciudad
    print("ID\tX\t\tY")
    print("-----------------------------------")
    for i in range(n):
        print(f"{i+1:2d}\t{x[i]:.2f}\t{y[i]:.2f}")
    print("-----------------------------------\n")

    # --- Cálculo de matriz de distancias ---
    # Genera la matriz con las distancias entre todas las ciudades
    dist = calcular_matriz_distancias(x, y)

    # --- Vector de clientes ---
    # Crea un vector con los IDs de las ciudades (1..n)
    vector_clientes = np.arange(1, n+1)
    print("Vector de clientes:", vector_clientes, "\n")

    # --- Ruta secuencial directa ---
    # Define la ruta que visita las ciudades en orden secuencial 1 → 2 → 3 → ... → n
    ruta = np.arange(n)
    # Calcula el costo total de esta ruta
    costo_total = costo_ruta(ruta, dist)
    print("Ruta secuencial directa (1 → 2 → 3 → ... → n → 1):", [r+1 for r in ruta])

    # --- Detalle del recorrido paso a paso ---
    # Imprime las distancias entre cada par de ciudades consecutivas en la ruta
    print("Recorrido paso a paso:")
    for i in range(n - 1):
        d = dist[ruta[i], ruta[i + 1]]
        print(f"De ciudad {ruta[i]+1:2d} a ciudad {ruta[i+1]+1:2d} → Distancia: {d:.2f}")
    # Imprime la distancia de regreso de la última ciudad a la primera para cerrar el ciclo
    print(f"De ciudad {ruta[-1]+1:2d} a ciudad {ruta[0]+1:2d} → Distancia: {dist[ruta[-1], ruta[0]]:.2f} (regreso al inicio)")

    # Muestra el costo total de la ruta completa
    print(f"\nCosto total del recorrido: {costo_total:.2f}")

    # --- Guardar resultados en archivos ---
    # Guarda el vector de clientes en un archivo de texto
    np.savetxt("vector_clientes.txt", vector_clientes, fmt="%d")
    # Guarda la matriz de distancias en un archivo de texto
    np.savetxt("matriz.txt", dist, fmt="%.0f")
    # Guarda la ruta y el costo total en un archivo de texto
    with open("ruta_y_costo.txt", "w") as f:
        f.write("Ruta generada por el algoritmo de pétalos:\n")
        f.write(" ".join(str(i+1) for i in ruta) + "\n")
        f.write(f"Costo total: {costo_total:.2f}\n")

    print("\nArchivos generados: vector_clientes.txt, matriz.txt, ruta_y_costo.txt")
    print("Programa finalizado correctamente.\n")

    # --- Mostrar visualización de la ruta ---
    # Dibuja y muestra la ruta calculada en un gráfico
    graficar_ruta(x, y, ruta, costo_total)


if __name__ == "__main__":
    main()

    # Ejemplo de cálculo de ángulo arcotangente
    # Calcula el ángulo entre el punto (0,0) y (20,20) usando atan2
    dx, dy = 20, 20
    angulo_radianes = math.atan2(dy, dx)
    angulo_grados = math.degrees(angulo_radianes)
    print(f"\nEjemplo de ángulo entre (0,0) y (20,20): {angulo_grados:.2f}°")
