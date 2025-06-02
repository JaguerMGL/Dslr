from stats_utils import my_max, my_min

def calculate_variance_between_houses(df, course, houses):
    """
    Calculate the difference between the maximum and minimum variance of a course across houses.
    """
    variances = []
    for house in houses:
        scores = df[df["Hogwarts House"] == house][course].dropna()
        if len(scores) > 0:
            mean = sum(scores) / len(scores)
            variance = sum((x - mean) ** 2 for x in scores) / len(scores)
            variances.append(variance)
    return my_max(variances) - my_min(variances) if len(variances) == len(houses) else float('inf')