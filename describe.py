import pandas as pd
import sys
import math

def load_dataset(filepath):
    try:
        db = pd.read_csv(filepath)
        return db
    except Exception as e:
        print(f"Error: file {filepath}: {e}")
        sys.exit(1)

def is_numeric(column):
    try:
        for x in column.dropna():
            x = float(x) 
        return True
    except ValueError:
        return False

def my_mean(data):
    total = 0
    for x in data:
        total += x
    return total / len(data)

def my_std(data, mean):
    variance = 0
    for x in data:
        variance += (x - mean) ** 2
    return math.sqrt(variance / len(data))

def my_min(data):
    minimum = data[0]
    for x in data:
        if x < minimum:
            minimum = x
    return minimum

def my_max(data):
    maximum = data[0]
    for x in data:
        if x > maximum:
            maximum = x
    return maximum

def my_sort(data):
    sorted_data = data[:]
    for i in range(len(sorted_data)):
        for j in range(i + 1, len(sorted_data)):
            if sorted_data[j] < sorted_data[i]:
                sorted_data[i], sorted_data[j] = sorted_data[j], sorted_data[i]
    return sorted_data

def get_percentile(p, data_sorted, n):
    k = (n - 1) * p
    f = int(k)
    c = f + 1 if f + 1 < n else f
    return data_sorted[f] + (data_sorted[c] - data_sorted[f]) * (k - f)

def my_quartiles(data):
    data_sorted = my_sort(data)
    n = len(data_sorted)
    q1 = get_percentile(0.25, data_sorted, n)
    q2 = get_percentile(0.5, data_sorted, n)
    q3 = get_percentile(0.75, data_sorted, n)
    return q1, q2, q3

def describe(df):
    numeric_cols = [col for col in df.columns if is_numeric(df[col])]
    stats = {
        "Count": [],
        "Mean": [],
        "Std": [],
        "Min": [],
        "25%": [],
        "50%": [],
        "75%": [],
        "Max": []
    }

    for col in numeric_cols:
        clean_data = [float(x) for x in df[col] if x == x]
        if not clean_data:
            for key in stats:
                stats[key].append(float('nan'))
            continue
        m = my_mean(clean_data)
        s = my_std(clean_data, m)
        q1, q2, q3 = my_quartiles(clean_data)
        stats["Count"].append(len(clean_data))
        stats["Mean"].append(m)
        stats["Std"].append(s)
        stats["Min"].append(my_min(clean_data))
        stats["25%"].append(q1)
        stats["50%"].append(q2)
        stats["75%"].append(q3)
        stats["Max"].append(my_max(clean_data))

    return numeric_cols, stats

def truncate_feature_name(name):
    if len(name) > 9:
        return name[:9] + "."
    return name

def print_describe(numeric_cols, stats):
    col_width = 15
    print("Statistic".ljust(col_width), end="")
    for col in numeric_cols:
        print(truncate_feature_name(col).ljust(col_width), end="")
    print()
    for stat in stats:
        print(stat.ljust(col_width), end="")
        for value in stats[stat]:
            formatted = f"{value:.4f}" if value == value else "NaN"
            print(formatted.ljust(col_width), end="")
        print()

# def write_describe(numeric_cols, stats, output_file="describe_output.txt"):
#     col_width = 30
#     with open(output_file, "w") as f:
#         f.write("Statistic".ljust(col_width))
#         for col in numeric_cols:
#             f.write(col.ljust(col_width))
#         f.write("\n")
#         for stat in stats:
#             f.write(stat.ljust(col_width))
#             for value in stats[stat]:
#                 formatted = f"{value:.4f}" if value == value else "NaN"
#                 f.write(formatted.ljust(col_width))
#             f.write("\n")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Error: dataset_train.csv required")
        sys.exit(1)

    db = load_dataset(sys.argv[1])
    numeric_cols, stats = describe(db)
    print_describe(numeric_cols, stats)
    # write_describe(numeric_cols, stats)