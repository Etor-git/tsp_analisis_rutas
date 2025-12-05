import math
import numpy as np
import matplotlib.pyplot as plt

# ---------------------------------------------------------------
# Proyecto TSP - archivo completo
# - Lee bayg29.tsp (líneas "id x y" y termina en EOF)
# - Calcula matriz de distancias (euclidiana redondeada)
# - Algoritmo "pétalos" visual (orden descendente por atan2 respecto al centro)
# - Grafica la ruta y etiqueta cada punto con su índice y ángulo (grados)
# - Guarda resultados básicos en archivos de texto
# ---------------------------------------------------------------

MAX_NODOS = 200

def leer_tsp(filename):
    """
    Lee coordenadas de un archivo .tsp con líneas 'id x y'.
    Ignora líneas que no sean tripletas y para al encontrar 'EOF'.
    Devuelve dos arrays numpy: x, y.
    """
    xcoord, ycoord = [], []
    with open(filename, "r") as f:
        for line in f:
            if line.strip().startswith("EOF"):
                break
            parts = line.strip().split()
            if len(parts) == 3 and parts[0].lstrip('-').isdigit():
                _, xs, ys = parts
                xcoord.append(float(xs))
                ycoord.append(float(ys))
    return np.array(xcoord), np.array(ycoord)

def calcular_matriz_distancias(x, y):
    """
    Calcula matriz de distancias euclidianas entre todos los pares.
    Las distancias se redondean al entero más cercano (como en tu código).
    """
    n = len(x)
    dist = np.zeros((n, n))
    for i in range(n):
        for j in range(n):
            dx = x[i] - x[j]
            dy = y[i] - y[j]
            dist[i, j] = round(math.sqrt(dx*dx + dy*dy))
    return dist

def costo_ruta(ruta, dist):
    """
    Calcula el costo total (suma de distancias redondeadas) de una ruta cerrada.
    'ruta' es una lista/array de índices 0-based.
    """
    costo = 0.0
    n = len(ruta)
    for i in range(n - 1):
        costo += dist[ruta[i], ruta[i+1]]
    costo += dist[ruta[-1], ruta[0]]  # regreso al inicio
    return costo

def graficar_ruta(x, y, ruta, costo_total, angulos=None, mostrar_angulos=True):
    """
    Grafica la ruta (con puntos y líneas). Si 'angulos' está dado y
    'mostrar_angulos' es True, muestra el ángulo en grados junto al índice.
    """
    plt.figure(figsize=(10, 8))
    plt.plot(x[ruta], y[ruta], 'bo-', label='Ruta (orden descendente por ángulo)')
    # Línea de regreso al inicio
    plt.plot([x[ruta[-1]], x[ruta[0]]], [y[ruta[-1]], y[ruta[0]]], 'r--', label='Regreso al inicio')
    # Marcar todos los puntos (en orden natural para etiquetas)
    for i, (xi, yi) in enumerate(zip(x, y)):
        if angulos is not None and mostrar_angulos:
            ang_text = f"{angulos[i]:.1f}°"
            plt.text(xi + 8, yi + 8, f"{i+1}\n{ang_text}", fontsize=8, ha='left')
        else:
            plt.text(xi + 8, yi + 8, f"{i+1}", fontsize=8, ha='left')
    plt.title(f"Recorrido ordenado por ángulo (descendente) — Costo: {costo_total:.2f}")
    plt.xlabel("Coordenada X")
    plt.ylabel("Coordenada Y")
    plt.legend()
    plt.grid(True)
    plt.axis('equal')  # mantener proporción real en ejes
    plt.show()

def algoritmo_petalos(x, y, dist, mostrar_grafica=True, mostrar_angulos=True):
    """
    Algoritmo de pétalos (versión requerida por ti):
      - Calcula atan2(dy, dx) respecto al centro geométrico (mean x, mean y).
      - Ordena ciudades de mayor a menor ángulo (descendente).
      - Devuelve ruta (lista de índices), costo_total y array de angulos (grados).
      - Si mostrar_grafica=True, dibuja la figura y etiqueta con ángulos.
    Notas:
      - La ordenación es puramente angular; no garantiza la mejor ruta TSP.
      - Puedes cambiar mostrar_angulos para ocultar los grados en la gráfica.
    """
    n = len(x)
    if n == 0:
        return [], 0.0, np.array([])

    # Centro geométrico (promedio)
    x_centro = np.mean(x)
    y_centro = np.mean(y)

    # Calcular ángulos (en grados) respecto al centro
    angulos = []
    for i in range(n):
        dx = x[i] - x_centro
        dy = y[i] - y_centro
        rad = math.atan2(dy, dx)      # atan2(dy, dx) -> radianes en (-pi, pi]
        deg = math.degrees(rad)       # convertir a grados
        angulos.append(deg)
    angulos = np.array(angulos)

    # Ordenar de mayor a menor ángulo (descendente)
    orden = np.argsort(angulos)[::-1]
    ruta = orden.tolist()

    # Calcular coste con la ruta resultante (índices 0-based)
    costo_total = costo_ruta(ruta, dist)

    # Graficar si se pide
    if mostrar_grafica:
        plt.figure(figsize=(10, 8))
        # Dibujar ruta en orden angular descendente
        plt.plot(x[ruta], y[ruta], 'bo-', label='Ruta ordenada (mayor→menor ángulo)')
        plt.plot([x[ruta[-1]], x[ruta[0]]], [y[ruta[-1]], y[ruta[0]]], 'r--', label='Regreso al inicio')
        # Marcar centro geométrico
        plt.plot(x_centro, y_centro, 'go', label='Centro geométrico')

        # Etiquetas (índice y ángulo)
        for i, (xi, yi) in enumerate(zip(x, y)):
            ang_text = f"{angulos[i]:.1f}°" if mostrar_angulos else ""
            txt = f"{i+1}\n{ang_text}" if mostrar_angulos else f"{i+1}"
            plt.text(xi + 8, yi + 8, txt, fontsize=8, ha='left')

        plt.title(f"Recorrido (orden descendente por ángulo)\nCosto total: {costo_total:.2f}")
        plt.xlabel("Coordenada X")
        plt.ylabel("Coordenada Y")
        plt.legend()
        plt.grid(True)
        plt.axis('equal')
        plt.show()

    return ruta, costo_total, angulos

def main():
    # Nombre del archivo TSP (ajusta ruta si es necesario)
    filename = "bayg29.tsp"

    # --- Leer coordenadas ---
    x, y = leer_tsp(filename)
    n = len(x)
    if n == 0:
        print("No se leyeron ciudades. Revisa el archivo.")
        return

    # (Opcional) Intercambiar para que la ciudad 13 sea la primera,
    # según lo tenías en versiones previas. Si no quieres esto, comentarlo.
    if n >= 13:
        punto_inicial = 13 - 1
        x[[0, punto_inicial]] = x[[punto_inicial, 0]]
        y[[0, punto_inicial]] = y[[punto_inicial, 0]]
        print("Se intercambiaron las coordenadas para que la ciudad 13 sea la ciudad 1 (opcional).")

    print(f"Se leyeron {n} nodos desde '{filename}'\n")

    # Mostrar coordenadas (índice 1-based)
    print("ID\tX\t\tY")
    print("-----------------------------------")
    for i in range(n):
        print(f"{i+1:2d}\t{x[i]:.2f}\t{y[i]:.2f}")
    print("-----------------------------------\n")

    # --- Matriz de distancias ---
    dist = calcular_matriz_distancias(x, y)

    # --- Ejecutar algoritmo de pétalos (descendente) y graficar ---
    ruta, costo_total, angulos = algoritmo_petalos(x, y, dist, mostrar_grafica=True, mostrar_angulos=True)

    # Imprimir ruta resultante (1-based para lectura)
    ruta_1based = [i+1 for i in ruta]
    print("Ruta (orden descendente por ángulo, 1-based):", ruta_1based)

    # Mostrar recorrido paso a paso con distancias utilizadas (redondeadas)
    print("\nRecorrido paso a paso:")
    for i in range(len(ruta) - 1):
        a, b = ruta[i], ruta[i+1]
        print(f"De ciudad {a+1:2d} a ciudad {b+1:2d} → Distancia: {dist[a,b]:.0f}")
    # regreso al inicio
    a, b = ruta[-1], ruta[0]
    print(f"De ciudad {a+1:2d} a ciudad {b+1:2d} → Distancia: {dist[a,b]:.0f} (regreso al inicio)")

    print(f"\nCosto total (ruta angular descendente): {costo_total:.2f}")

    # --- Guardar resultados básicos
    np.savetxt("vector_clientes.txt", np.arange(1, n+1), fmt="%d")
    np.savetxt("matriz.txt", dist, fmt="%.0f")
    with open("ruta_y_costo.txt", "w") as f:
        f.write("Ruta (orden descendente por ángulo, 1-based):\n")
        f.write(" ".join(str(i) for i in ruta_1based) + "\n")
        f.write(f"Costo total: {costo_total:.2f}\n")

    print("\nArchivos generados: vector_clientes.txt, matriz.txt, ruta_y_costo.txt")
    print("Programa finalizado correctamente.\n")

    # Ejemplo pequeño de atan2
    dx_ex, dy_ex = 20, 20
    rad_ex = math.atan2(dy_ex, dx_ex)
    deg_ex = math.degrees(rad_ex)
    print(f"Ejemplo atan2: dx={dx_ex}, dy={dy_ex} -> {deg_ex:.2f}°")

if __name__ == "__main__":
    main()
