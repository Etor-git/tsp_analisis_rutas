#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>
#include <math.h>

#define MAX_NODOS 200  // límite máximo de nodos

// ---------- Prototipo ----------
double costoRuta(int ruta[], double dist[][MAX_NODOS + 1], int n);

int main(int argc, char *argv[]) {
    const char *filename = "bayg29.tsp";
    if (argc >= 2) filename = argv[1];

    FILE *f = fopen(filename, "r");
    if (!f) {
        perror(filename);
        return 1;
    }

    char line[512];
    int n = 0, id;
    double xcoord, ycoord;
    static double vector_x[MAX_NODOS + 1];
    static double vector_y[MAX_NODOS + 1];

    // ---------- Leer coordenadas del archivo .tsp ----------
    while (fgets(line, sizeof(line), f)) {
        if (strncmp(line, "EOF", 3) == 0) break;
        char *p = line;
        while (isspace((unsigned char)*p)) p++;
        if (!isdigit((unsigned char)*p)) continue;
        if (sscanf(p, "%d %lf %lf", &id, &xcoord, &ycoord) == 3) {
            if (n + 1 > MAX_NODOS) {
                fprintf(stderr, "Demasiados nodos. Aumenta MAX_NODOS.\n");
                fclose(f);
                return 1;
            }
            n++;
            vector_x[n] = xcoord;
            vector_y[n] = ycoord;
        }
    }
    fclose(f);

    if (n == 0) {
        printf("No se encontraron nodos válidos en %s\n", filename);
        return 1;
    }

    printf("Se leyeron %d nodos del archivo %s\n\n", n, filename);

    // ---------- Mostrar coordenadas ----------
    printf("Coordenadas leídas:\n");
    printf("ID\tX\t\tY\n");
    printf("-----------------------------------\n");
    for (int i = 1; i <= n; i++) {
        printf("%2d\t%.2f\t%.2f\n", i, vector_x[i], vector_y[i]);
    }
    printf("-----------------------------------\n\n");

    // ---------- Calcular matriz de distancias ----------
    static double dist[MAX_NODOS + 1][MAX_NODOS + 1];
    for (int i = 1; i <= n; i++) {
        for (int j = 1; j <= n; j++) {
            double dx = vector_x[i] - vector_x[j];
            double dy = vector_y[i] - vector_y[j];
            dist[i][j] = round(sqrt(dx * dx + dy * dy));
        }
    }

    // ---------- Vector de clientes ----------
    int vector_clientes[MAX_NODOS + 1];
    for (int i = 1; i <= n; i++) {
        vector_clientes[i] = i;
    }

    // Mostrar vector de clientes
    printf("Vector de clientes:\n[ ");
    for (int i = 1; i <= n; i++) printf("%d ", vector_clientes[i]);
    printf("]\n\n");

    // ---------- Ruta de ejemplo (puede cambiarse) ----------
    int ruta_ejemplo[MAX_NODOS + 1];
    for (int i = 1; i <= n; i++) ruta_ejemplo[i] = i; // secuencial

    // ---------- Mostrar paso a paso y calcular costo ----------
    double costoTotal = 0;
    printf("Recorrido paso a paso:\n");
    for (int i = 1; i < n; i++) {
        int origen = ruta_ejemplo[i];
        int destino = ruta_ejemplo[i + 1];
        double d = dist[origen][destino];
        costoTotal += d;
        printf("De ciudad %2d a ciudad %2d → Distancia: %.2f\n", origen, destino, d);
    }
    // regreso al inicio
    costoTotal += dist[ruta_ejemplo[n]][ruta_ejemplo[1]];
    printf("De ciudad %2d a ciudad %2d → Distancia: %.2f (regreso al inicio)\n",
           ruta_ejemplo[n], ruta_ejemplo[1], dist[ruta_ejemplo[n]][ruta_ejemplo[1]]);

    printf("\nCosto total del recorrido: %.2f\n", costoTotal);

    // ---------- Guardar resultados ----------
    FILE *fvec = fopen("vector_clientes.txt", "w");
    fprintf(fvec, "Vector de clientes (índices de las ciudades):\n");
    for (int i = 1; i <= n; i++) fprintf(fvec, "%d ", vector_clientes[i]);
    fclose(fvec);

    FILE *fmat = fopen("matriz.txt", "w");
    fprintf(fmat, "Matriz de distancias redondeada (1..%d):\n", n);
    for (int i = 1; i <= n; i++) {
        for (int j = 1; j <= n; j++) fprintf(fmat, "%6.0f ", dist[i][j]);
        fprintf(fmat, "\n");
    }
    fclose(fmat);

    FILE *rout = fopen("ruta_y_costo.txt", "w");
    fprintf(rout, "Ruta secuencial:\n");
    for (int i = 1; i <= n; i++) fprintf(rout, "%d ", ruta_ejemplo[i]);
    fprintf(rout, "\nCosto total: %.2f\n", costoTotal);
    fclose(rout);

    printf("\nArchivos generados: vector_clientes.txt, matriz.txt, ruta_y_costo.txt\n");
    printf("Programa finalizado correctamente.\n");

    return 0;
}

// ---------- Función costoRuta ----------
double costoRuta(int ruta[], double dist[][MAX_NODOS + 1], int n) {
    double costo = 0;
    for (int i = 1; i < n; i++) {
        costo += dist[ruta[i]][ruta[i + 1]];
    }
    costo += dist[ruta[n]][ruta[1]]; // Regreso al inicio
    return costo;
}