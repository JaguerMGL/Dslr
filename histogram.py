import pandas as pd
import matplotlib.pyplot as plt
import sys

def load_dataset(filepath):
    try:
        return pd.read_csv(filepath)
    except Exception as e:
        print(f"Error loading file {filepath}: {e}")
        exit(1)

def my_max(data):
    maximum = data[0]
    for x in data:
        if x > maximum:
            maximum = x
    return maximum

def my_min(data):
    minimum = data[0]
    for x in data:
        if x < minimum:
            minimum = x
    return minimum

def calculate_variance_between_houses(df, course, houses):
    variances = []
    for house in houses:
        scores = df[df["Hogwarts House"] == house][course].dropna()
        if len(scores) > 0:
            mean = sum(scores) / len(scores)
            variance = sum((x - mean) ** 2 for x in scores) / len(scores)
            variances.append(variance)
    return my_max(variances) - my_min(variances) if len(variances) == len(houses) else float('inf')

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
        print("Error: dataset_train.csv is required")
        sys.exit(1)

    df = load_dataset(sys.argv[1])
    homogeneous_course = find_homogeneous_course(df)
    if homogeneous_course:
        plot_histogram_for_course(df, homogeneous_course)
    else:
        print("Error: function find_homogeneous_course returned None")
        sys.exit(1)