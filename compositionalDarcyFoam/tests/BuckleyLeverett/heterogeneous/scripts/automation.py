# -*- coding: utf-8 -*-
"""
File: automation.py
Author: Helio Ribeiro (Wikki Brasil)
Created: 02/07/2024
Python Version: 3.10.12

Description:
    This script compares the water saturation profile from analytical and numerical
    solutions at a specific simulation time. It reads data from CSV files, plots
    the results, and saves a PNG image.
"""

import numpy as np
import csv
import matplotlib.pyplot as plt
import os

# Time (in simulation units) at which the comparison is made
COMPARISON_TIME = 2000

# File paths
ANALYTICAL_FILE = 'analytical.csv'
NUMERICAL_FILE = f'../postProcessing/sets/{COMPARISON_TIME}/acrossFlow_S.water.xy'


def read_csv_data(filepath, delimiter=','):
    """
    Reads numerical data from a CSV file.

    Parameters:
        filepath (str): Path to the CSV file.
        delimiter (str): Delimiter used in the file.

    Returns:
        tuple: Two lists (x_values, y_values) with float values.
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
        print(f"File not found: {filepath}")
    except ValueError:
        print(f"Could not convert values in file: {filepath}")

    return x_values, y_values


def plot_results(x_analytical, y_analytical, x_numerical, y_numerical):
    """
    Plots the analytical and numerical data for comparison.

    Parameters:
        x_analytical (list): X values from analytical solution.
        y_analytical (list): Y values from analytical solution.
        x_numerical (list): X values from numerical solution.
        y_numerical (list): Y values from numerical solution.
    """
    plt.figure()

    plt.plot(x_analytical, y_analytical, 'k-', label="Analytical")
    plt.plot(x_numerical, y_numerical, 'r--', label="Numerical (porousMedia)")
    plt.legend(loc='upper right', ncol=1, fancybox=True, shadow=True)

    plt.xlim([0, 0.065])
    plt.xlabel(r'$y$ [m]')
    plt.ylabel(r'$S_w$ [-]')
    plt.title(f'Water Saturation Comparison at t = {COMPARISON_TIME}')
    plt.grid(True)

    output_file = 'comp.png'
    plt.savefig(output_file, dpi=600, bbox_inches='tight')
    print(f"Plot saved as '{output_file}'")


def main():
    """Main execution function."""
    print("Reading analytical data...")
    x_analytical, y_analytical = read_csv_data(ANALYTICAL_FILE, delimiter=',')

    print("Reading numerical data...")
    x_numerical, y_numerical = read_csv_data(NUMERICAL_FILE, delimiter=' ')

    if x_analytical and x_numerical:
        print("Plotting results...")
        plot_results(x_analytical, y_analytical, x_numerical, y_numerical)
    else:
        print("Plotting skipped due to missing or invalid data.")


if __name__ == '__main__':
    main()
