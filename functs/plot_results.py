import matplotlib.pyplot as plt
import seaborn as sns
from collections import defaultdict

def format_key(key):
    if not key or all(not unit for unit in key):
        return 'None'
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

    sns.set(style="white")
    plt.figure(figsize=(12, 8))
    barplot = sns.barplot(x=values, y=[str(label) for label in labels], palette="viridis")
    barplot.set_xlabel('Count', fontsize=14)
    barplot.set_ylabel('Units', fontsize=14)
    barplot.set_title(title, fontsize=16)
    plt.xticks(fontsize=12)
    plt.yticks(fontsize=12)
    plt.tight_layout()
    plt.savefig(filename)
    plt.close()
