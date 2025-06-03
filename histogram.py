from utils.data_utils import load_data
from utils.hogwarts_utils import calculate_variance_between_houses
import matplotlib.pyplot as plt
import sys

def find_homogeneous_course(df):
    houses = df["Hogwarts House"].dropna().unique()
    courses = df.columns[6:]
    homogeneous_course = None
    min_variance_diff = float('inf')

    for course in courses:
        variance_diff = calculate_variance_between_houses(df, course, houses)
        if variance_diff < min_variance_diff:
            min_variance_diff = variance_diff
            homogeneous_course = course

    return homogeneous_course

def plot_histogram_for_course(df, course):
    houses = df["Hogwarts House"].dropna().unique()
    plt.figure(figsize=(10, 6))
    for house in houses:
        scores = df[df["Hogwarts House"] == house][course].dropna()
        plt.hist(scores, bins=20, alpha=0.5, label=house)

    plt.title(f"Score distribution for {course}")
    plt.xlabel("Scores")
    plt.ylabel("Frequency")
    plt.legend()
    plt.grid(True)
    plt.show()

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Error: only .py and dataset_train.csv required")
        sys.exit(1)

    df = load_data(sys.argv[1])
    homogeneous_course = find_homogeneous_course(df)
    if homogeneous_course:
        plot_histogram_for_course(df, homogeneous_course)
    else:
        print("Error: function find_homogeneous_course returned None")
        sys.exit(1)