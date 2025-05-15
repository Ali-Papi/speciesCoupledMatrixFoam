# -*- coding: utf-8 -*-
"""
Script: timeStep.py
Author: Helio Ribeiro (Wikki Brasil)
Date: 23/03/2025

Description:
    Extracts time step values (deltaT) and simulation time from an OpenFOAM log file.
    Computes the average time step and generates a plot of deltaT vs time.
"""

import re
import matplotlib.pyplot as plt
import numpy as np
from typing import List, Optional


def get_value_from_tag(text: str, tag: str, value_pattern: Optional[str] = r'(\S+);') -> List[str] | bool:
    """
    Extracts values related to a tag from the input text using regex.

    Parameters:
        text (str): Full text to search within.
        tag (str): Tag or keyword to search.
        value_pattern (str, optional): Regex pattern to capture the value.

    Returns:
        list: List of matched string values, or False if not found.
    """
    expression = rf'\s*{tag}\s+{value_pattern}'
    matches = re.findall(expression, text)
    return matches if all(matches) else False


def plot_time_step(
    x, y, xlabel: str, ylabel: str, title: str, filename: str,
    color: str = 'k', line_style: str = '-'
) -> None:
    """
    Plots and saves a time series of time step values.

    Parameters:
        x (array-like): x-axis values (e.g., time)
        y (array-like): y-axis values (e.g., deltaT)
        xlabel (str): x-axis label
        ylabel (str): y-axis label
        title (str): plot title
        filename (str): output filename (e.g., 'deltaT.png')
        color (str): line color
        line_style (str): line style

    Returns:
        None
    """
    plt.figure(figsize=(8, 6))
    plt.plot(x, y, line_style, color=color)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(filename)
    print(f"[Info] Plot saved as '{filename}'")


def main():
    """Main execution: read log, extract values, compute and plot."""
    log_file_path = '../log.coupledMatrixFoam'

    # Try to read the log file
    try:
        with open(log_file_path, 'r') as file:
            content = file.read()
    except FileNotFoundError:
        print(f"[Erro] Arquivo não encontrado: {log_file_path}")
        return

    # Extract deltaT values
    delta_ts = get_value_from_tag(content, 'deltaT =', r'(.*?)\n')
    if not delta_ts:
        print("[Erro] Nenhum valor de deltaT encontrado.")
        return
    delta_ts = np.array([float(i) for i in delta_ts])

    # Extract time values
    times = get_value_from_tag(content, r'\nTime =', r'(.*?)\s+\n')
    if not times:
        print("[Erro] Nenhum valor de tempo encontrado.")
        return
    times = np.array([float(i) for i in times])

    # Verificar consistência
    n = min(len(times), len(delta_ts))
    times = times[:n]
    delta_ts = delta_ts[:n]

    # Calcular média
    average_dt = np.mean(delta_ts)
    print(f"\n[Info] Média de deltaT em {n} passos: {average_dt:.6f} segundos\n")

    # Plotar gráfico
    plot_time_step(
        x=times,
        y=delta_ts,
        xlabel='Time [s]',
        ylabel='Time step [s]',
        title='Time step over time',
        filename='deltaT.png'
    )


if __name__ == "__main__":
    main()
