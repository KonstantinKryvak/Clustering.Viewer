


def Algorithm(points, distance, N: int = 3) -> list[int]:
    # стандартний старт. кожна точка - це окремий кластер.
    clusters = [{i} for i in range(len(points))]

    def cluster_dist(c1, c2):
        return max(distance(points[i], points[j]) for i in c1 for j in c2)

    # об'єднуєио, поки кількість кластерів не дорівнює бажаній, або об'єднувати вже нічого.
    while len(clusters) > N:
        min_d = float('inf')
        to_merge = (None, None)
        for idx1 in range(len(clusters)):
            for idx2 in range(idx1 + 1, len(clusters)):
                d = cluster_dist(clusters[idx1], clusters[idx2])
                if d < min_d:
                    min_d = d
                    to_merge = (idx1, idx2)

        i, j = to_merge
        # j об'єднуємо з i (перевірка на i < j для коректності)
        if i > j:
            i, j = j, i
        clusters[i] = clusters[i].union(clusters[j])
        clusters.pop(j)

    # даємо кожномі кластеру ідентифікатор, починаючи з 0.
    labels = [None] * len(points)
    for cluster_id, cluster in enumerate(clusters):
        for idx in cluster:
            labels[idx] = cluster_id

    return labels


