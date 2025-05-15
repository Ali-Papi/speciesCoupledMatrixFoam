# -*- coding: utf-8 -*-
"""
File: automation.py
Author: Helio Ribeiro (Wikki Brasil)
Date created: 02/07/2024
Python Version: 3.10.12

Description:
    This script compares water saturation profiles from a numerical simulation
    against a reference solution (e.g., analytical or benchmark data). It reads
    both datasets from CSV files and generates a comparison plot.
"""

import csv
import matplotlib.pyplot as plt

# Time (simulation step) to extract numerical data from
comparison_time = 1800

# File paths
reference_file = 'reference.csv'
numerical_file = f'../postProcessing/sets/{comparison_time}/acrossFlow_S.water.xy'
output_image = 'comp.png'


def read_csv_data(filepath, delimiter=','):
    """
    Reads x and y float values from a CSV file.

    Parameters:
        filepath (str): Path to the CSV file.
        delimiter (str): Delimiter used in the file.

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
        print(f"[Erro] Erro de conversão de dados no arquivo: {filepath}")

    return x_values, y_values


def plot_comparison(x_ref, y_ref, x_num, y_num):
    """
    Plots and saves a comparison between reference and numerical data.

    Parameters:
        x_ref (list): Y positions from the reference dataset.
        y_ref (list): Water saturation values from the reference dataset.
        x_num (list): Y positions from the numerical simulation.
        y_num (list): Water saturation values from the simulation.
    """
    plt.figure()

    plt.plot(x_ref, y_ref, 'k-', label="Reference")
    plt.plot(x_num, y_num, 'r--', label="porousMedia")

    plt.legend(loc='upper right', fancybox=True, shadow=True)
    plt.xlim([0, 0.065])
    plt.xlabel(r'$y$ [m]')
    plt.ylabel(r'$S_w$ [-]')
    plt.title(f'Water Saturation Profile at t = {comparison_time}')
    plt.grid(True)

    plt.savefig(output_image, dpi=600, bbox_inches='tight')
    print(f"[Info] Gráfico salvo como '{output_image}'")


def main():
    """Main execution: load data and generate the comparison plot."""
    print("[Info] Lendo dados de referência...")
    y_ref, sw_ref = read_csv_data(reference_file, delimiter=',')

    print("[Info] Lendo dados numéricos...")
    y_num, sw_num = read_csv_data(numerical_file, delimiter=' ')

    if y_ref and y_num:
        print("[Info] Gerando gráfico de comparação...")
        plot_comparison(y_ref, sw_ref, y_num, sw_num)
    else:
        print("[Aviso] Dados insuficientes para plotagem.")


if __name__ == '__main__':
    main()
