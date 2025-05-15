# -*- coding: utf-8 -*-
"""
File: automation.py
Author: Helio Ribeiro (Wikki Brasil)
Created: 02/07/2024
Python Version: 3.10.12

Description:
    This script compares water saturation profiles from analytical and numerical
    solutions at a specific simulation time. It reads data from CSV files, plots
    the comparison, and saves the figure as a PNG image.
"""

import csv
import matplotlib.pyplot as plt

# Time (from numerical simulation) at which the comparison is made
comparison_time = 1800

# File paths
analytical_file = 'analytical.csv'
numerical_file = f'../postProcessing/sets/{comparison_time}/acrossFlow_S.water.xy'
output_plot = 'comp.png'


def read_csv_data(filepath, delimiter=','):
    """
    Reads x and y float values from a CSV file.

    Parameters:
        filepath (str): Path to the CSV file.
        delimiter (str): Character used to separate values in the file.

    Returns:
        tuple: Two lists of floats (x_values, y_values).
    """
    x_values, y_values = [], []

    try:
        with open(filepath, newline='') as csvfile:
            reader = csv.reader(csvfile, skipinitialspace=True, delimiter=delimiter)
            for row in reader:
                if len(row) >= 2:
                    x_values.append(float(row[0]))
                    y_values.append(float(row[1]))
    except FileNotFoundError:
        print(f"[Erro] Arquivo não encontrado: {filepath}")
    except ValueError:
        print(f"[Erro] Conversão de dados falhou no arquivo: {filepath}")

    return x_values, y_values


def plot_comparison(x_analytical, y_analytical, x_numerical, y_numerical):
    """
    Plots and saves a comparison between analytical and numerical water saturation.

    Parameters:
        x_analytical (list): Y positions from analytical data.
        y_analytical (list): Saturation values from analytical data.
        x_numerical (list): Y positions from numerical data.
        y_numerical (list): Saturation values from numerical data.
    """
    plt.figure()

    plt.plot(x_analytical, y_analytical, 'k-', label="Analytical")
    plt.plot(x_numerical, y_numerical, 'r--', label="Numerical (porousMedia)")

    plt.legend(loc='upper right', fancybox=True, shadow=True)
    plt.xlim([0, 0.065])
    plt.xlabel(r'$y$ [m]')
    plt.ylabel(r'$S_w$ [-]')
    plt.title(f'Water Saturation Comparison at t = {comparison_time}')
    plt.grid(True)

    plt.savefig(output_plot, dpi=600, bbox_inches='tight')
    print(f"[Info] Gráfico salvo como '{output_plot}'")


def main():
    """Main function: loads data and generates the comparison plot."""
    print("[Info] Lendo dados analíticos...")
    x_analytical, y_analytical = read_csv_data(analytical_file, delimiter=',')

    print("[Info] Lendo dados numéricos...")
    x_numerical, y_numerical = read_csv_data(numerical_file, delimiter=' ')

    if x_analytical and x_numerical:
        print("[Info] Gerando gráfico...")
        plot_comparison(x_analytical, y_analytical, x_numerical, y_numerical)
    else:
        print("[Aviso] Dados incompletos — gráfico não gerado.")


if __name__ == '__main__':
    main()
