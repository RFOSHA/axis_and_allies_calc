#Function to plot the results of the battle simulations
import matplotlib.pyplot as plt
import os
from collections import defaultdict

def format_key(key):
    return ', '.join([f"{unit} {num}" for unit, num in key])

def plot_results(units_count, title, filename):
    units_dict = defaultdict(int)
    for units, count in units_count.items():
        units_dict[units] += count

    labels = []
    values = []

    for units, count in units_dict.items():
        labels.append(format_key(units))
        values.append(count)

    plt.figure(figsize=(10, 6))
    plt.barh(range(len(labels)), values, tick_label=[str(label) for label in labels])
    plt.xlabel('Count')
    plt.title(title)
    plt.tight_layout()
    plt.savefig(filename)
    plt.close()
