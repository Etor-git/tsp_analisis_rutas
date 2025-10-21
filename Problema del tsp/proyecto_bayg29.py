import math
import numpy as np
import matplotlib.pyplot as plt

MAX_NODOS = 200

def leer_tsp(filename):
    """Lee coordenadas de un archivo .tsp"""
    xcoord, ycoord = [], []
    with open(filename, "r") as f:
        for line in f:
            if line.strip().startswith("EOF"):
                break
            parts = line.strip().split()
            if len(parts) == 3 and parts[0].isdigit():
                _, x, y = parts
                xcoord.append(float(x))
                ycoord.append(float(y))
    return np.array(xcoord), np.array(ycoord)

def calcular_matriz_distancias(x, y):
    """Calcula matriz de distancias euclidianas redondeadas"""
    n = len(x)
    dist = np.zeros((n, n))
    for i in range(n):
        for j in range(n):
            dx, dy = x[i] - x[j], y[i] - y[j]
            dist[i, j] = round(math.sqrt(dx**2 + dy**2))
    return dist

def costo_ruta(ruta, dist):
    """Calcula el costo total de una ruta cerrada"""
    costo = 0
    n = len(ruta)
    for i in range(n - 1):
        costo += dist[ruta[i], ruta[i + 1]]
    costo += dist[ruta[-1], ruta[0]]  # regreso al inicio
    return costo

def graficar_ruta(x, y, ruta, costo_total):
    """Muestra visualmente el recorrido"""
    plt.figure(figsize=(8, 6))
    plt.plot(x[ruta], y[ruta], 'bo-', label='Ruta')
    plt.plot([x[ruta[-1]], x[ruta[0]]], [y[ruta[-1]], y[ruta[0]]], 'r--', label='Regreso al inicio')
    for i, (xi, yi) in enumerate(zip(x, y), start=1):
        plt.text(xi + 2, yi + 2, str(i), fontsize=9)
    plt.title(f"Recorrido de ciudades\nCosto total: {costo_total:.2f}")
    plt.xlabel("Coordenada X")
    plt.ylabel("Coordenada Y")
    plt.legend()
    plt.grid(True)
    plt.show()

def main():
    filename = "bayg29.tsp"
    x, y = leer_tsp(filename)
    n = len(x)
    print(f"Se leyeron {n} nodos del archivo {filename}\n")

    # Mostrar coordenadas
    print("ID\tX\t\tY")
    print("-----------------------------------")
    for i in range(n):
        print(f"{i+1:2d}\t{x[i]:.2f}\t{y[i]:.2f}")
    print("-----------------------------------\n")

    # Matriz de distancias
    dist = calcular_matriz_distancias(x, y)

    # Vector de clientes (1..n)
    vector_clientes = np.arange(1, n+1)
    print("Vector de clientes:", vector_clientes, "\n")

    # Ruta ejemplo (secuencial)
    ruta = np.arange(n)
    costo_total = costo_ruta(ruta, dist)

    print("Recorrido paso a paso:")
    for i in range(n - 1):
        d = dist[ruta[i], ruta[i + 1]]
        print(f"De ciudad {ruta[i]+1:2d} a ciudad {ruta[i+1]+1:2d} → Distancia: {d:.2f}")
    print(f"De ciudad {ruta[-1]+1:2d} a ciudad {ruta[0]+1:2d} → Distancia: {dist[ruta[-1], ruta[0]]:.2f} (regreso al inicio)")

    print(f"\nCosto total del recorrido: {costo_total:.2f}")

    # Guardar resultados
    np.savetxt("vector_clientes.txt", vector_clientes, fmt="%d")
    np.savetxt("matriz.txt", dist, fmt="%.0f")
    with open("ruta_y_costo.txt", "w") as f:
        f.write("Ruta secuencial:\n")
        f.write(" ".join(str(i+1) for i in ruta) + "\n")
        f.write(f"Costo total: {costo_total:.2f}\n")

    print("\nArchivos generados: vector_clientes.txt, matriz.txt, ruta_y_costo.txt")
    print("Programa finalizado correctamente.\n")

    # --- Mostrar visualización ---
    graficar_ruta(x, y, ruta, costo_total)

if __name__ == "__main__":
    main()