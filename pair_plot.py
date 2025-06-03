from utils.data_utils import load_data
import matplotlib.pyplot as plt
import sys

def pair_plot(src='data/dataset_train.csv'):
    df = load_data(src)
    numeric_cols = df.columns[5:]
    if "Hogwarts House" not in df.columns:
        print("Error: 'Hogwarts House' column not found in the dataset.")
        return

    houses = df["Hogwarts House"].dropna().unique()
    colors = {house: color for house, color in zip(houses, ['red', 'green', 'blue', 'orange'])}
    for i in range(len(numeric_cols)):
        feature1 = numeric_cols[i]
        plt.figure(figsize=(15, 15))
        plt.suptitle(f"Scatter Plots for {feature1}", fontsize=16)
        plot_index = 1
        for j in range(len(numeric_cols)):
            if i == j:
                continue
            feature2 = numeric_cols[j]
            plt.subplot(5, 5, plot_index)
            for house in houses:
                house_data = df[df["Hogwarts House"] == house]
                plt.scatter(house_data[feature1], house_data[feature2], alpha=0.5, label=house, color=colors[house])
            plt.xlabel(feature1, fontsize=8)
            plt.ylabel(feature2, fontsize=8)
            plt.title(f"{feature1} vs {feature2}", fontsize=10)
            plt.grid(True)
            plot_index += 1

        plt.legend(houses, loc="upper right", fontsize=8)
        plt.tight_layout(rect=[0, 0, 1, 0.95])
        plt.show()

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Error: only dataset_train.csv required")
        sys.exit(1)

    pair_plot(sys.argv[1])