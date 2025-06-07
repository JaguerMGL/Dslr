from utils.data_utils import load_data
from utils.stats_utils import my_mean, my_std, sigmoid
import numpy as np
import sys

#transforme une valeur en une probabilité entre 0 et 1


#evalue la qualite des predictions
def compute_cost(X, y, theta):
    m = len(y)
    h = sigmoid(X @ theta)
    cost = (-1 / m) * (y.T @ np.log(h) + (1 - y).T @ np.log(1 - h))
    return cost

#optimise les poids du modèle en utilisant la descente de gradient
def gradient_descent(X, y, theta, alpha, num_iters):
    m = len(y)
    for i in range(num_iters):
        h = sigmoid(X @ theta)
        gradient = (1 / m) * (X.T @ (h - y))
        theta -= alpha * gradient

        if i % 100 == 0:
            cost = compute_cost(X, y, theta)
            print(f"Iteration {i}: Cost = {cost:.4f}")
    return theta

#entraine des modèles de régression logistique pour chaque classe en utilisant la méthode one vs all
def train_one_vs_all(X, y, num_classes, alpha=0.01, num_iters=1000):
    m, n = X.shape
    all_theta = np.zeros((num_classes, n))
    for c in range(num_classes):
        y_c = (y == c).astype(int)
        theta = np.zeros(n)
        all_theta[c] = gradient_descent(X, y_c, theta, alpha, num_iters)
    return all_theta

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Error: only .py and dataset_train.csv required")
        sys.exit(1)

    # Load dataset
    dataset = load_data(sys.argv[1])
    if "Hogwarts House" not in dataset.columns:
        print("Error: 'Hogwarts House' column not found in the dataset.")
        sys.exit(1)

    # Prepare data
    X = dataset.iloc[:, 5:].values  # Features
    y = dataset["Hogwarts House"].map({"Gryffindor": 0, "Hufflepuff": 1, "Ravenclaw": 2, "Slytherin": 3}).values

    # Normalize features using mean and std from stats_utils
    X_norm = (X - my_mean(X)) / my_std(X, my_mean(X))
    X = np.c_[np.ones(X_norm.shape[0]), X_norm]  # Add intercept term

    # Train models
    num_classes = len(np.unique(y))
    all_theta = train_one_vs_all(X, y, num_classes)

    # Save weights to file
    np.savetxt("weights.csv", all_theta, delimiter=",")
    print("Weights saved to weights.csv")