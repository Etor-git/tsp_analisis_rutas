#TSP Análisis de Rutas

Este proyecto implementa un programa en C y en Python que calcula y compara rutas entre un conjunto de ciudades (Traveling Salesman Problem - TSP).

#¿Qué hace este programa?

- Lee coordenadas desde un archivo `.tsp`.
- Calcula la **matriz de distancias** entre cada par de puntos.
- Genera una **ruta secuencial** (1 → 2 → 3 → … → 1).
- Crea **rutas aleatorias** y calcula su **costo total** (distancia recorrida).
- Compara los costos y muestra **la mejor ruta encontrada**.
- Guarda la información en archivos:
  - `matriz.txt` → matriz de distancias.
  - `vector_clientes.txt` → lista de ciudades.
  - `ruta_y_costo.txt` → mejor ruta y su costo.

#Objetivo

Simular y analizar rutas usando un enfoque de **optimización combinatoria y análisis probabilístico**, con aplicaciones en:
- Logística y transporte
- Optimización de rutas
- Análisis de datos espaciales

#Extensiones posibles

- Exportar resultados a CSV para análisis con Python o Excel.
- Añadir heurísticas como “Vecino más Cercano” o “2-opt”.
- Visualizar las rutas gráficamente.


**Autor:** Héctor Jesús Valadez Pardo

**Lenguaje:** C y Python
**Tema:** Optimización, Análisis de datos, Probabilidad aplicada
**Materia** Matemáticas Aplicadas a la Computación/ UAEM/ 4 Semestre
