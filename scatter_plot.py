from utils.data_utils import load_data
from utils.stats_utils import pearson_correlation
import matplotlib.pyplot as plt
import sys

def find_most_correlated_features(data):
    numeric_data = data.select_dtypes(include=['float64', 'int64'])
    columns = numeric_data.columns
    max_corr = 0
    feature_pair = (None, None)
    for i in range(len(columns)):
        for j in range(i + 1, len(columns)):
            col1 = numeric_data[columns[i]]
            col2 = numeric_data[columns[j]]
            valid_indices = col1.notna() & col2.notna()  
            col1 = col1[valid_indices].tolist()
            col2 = col2[valid_indices].tolist()
            corr = abs(pearson_correlation(col1, col2))
            if corr > max_corr:
                max_corr = corr
                feature_pair = (columns[i], columns[j])

    return feature_pair

def plot_scatter(data, feature1, feature2):
    if "Hogwarts House" in data.columns:
        categories = data["Hogwarts House"].dropna().unique()
        colors = {category: color for category, color in zip(categories, ['red', 'green', 'blue', 'orange'])}
        point_colors = data["Hogwarts House"].map(colors)
        plt.scatter(data[feature1], data[feature2], alpha=0.5, c=point_colors)
        legend_handles = [plt.Line2D([0], [0], marker='o', color='w', markerfacecolor=color, markersize=10, label=category) 
                          for category, color in colors.items()]
        plt.legend(handles=legend_handles, title="Hogwarts House")
    else:
        point_colors = ['red' if x % 2 == 0 else 'blue' for x in range(len(data))]
        plt.scatter(data[feature1], data[feature2], alpha=0.5, c=point_colors)
        plt.legend(["Red: even index", "Blue: odd index"], loc="upper right")
    plt.title(f"Scatter Plot: {feature1} vs {feature2}")
    plt.xlabel(feature1)
    plt.ylabel(feature2)
    plt.grid(True)
    plt.show()

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Error: only data.csv is required")
        sys.exit(1)
    data = load_data(sys.argv[1])
    feature1, feature2 = find_most_correlated_features(data)
    if feature1 and feature2:
        plot_scatter(data, feature1, feature2)
    else:
        print("Error: No correlated features found.")