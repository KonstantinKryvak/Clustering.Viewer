

from collections import deque


def RegionQuery(points, distance, idx, epsilon):
    neighbors = []
    p = points[idx]
    for i, q in enumerate(points):
        if distance(p, q) <= epsilon:
            neighbors.append(i)
    return neighbors


def ExpandCluster(points, distance, labels, idx, neighbors, cluster_id, k, epsilon):
    # позначаємо що точка належить кластеру
    labels[idx] = cluster_id

    queue = deque(neighbors)
    while queue:
        nbr_idx = queue.popleft()

        # якщо це був шум, то тепер це частина кластеру.
        if labels[nbr_idx] == -1:
            labels[nbr_idx] = cluster_id

        # перевіряємо, чи не можна включити новознайдену точку
        if labels[nbr_idx] == 0:
            labels[nbr_idx] = cluster_id
            nbrs2 = RegionQuery(points, distance, nbr_idx, epsilon)
            if len(nbrs2) >= k:
                queue.extend(nbrs2)


def Algorithm(points, distance, k: int = 5, epsilon: float = 0.4) -> list[int]:
    labels = [0] * len(points)
    ID = 0

    for i in range(len(points)):
        if labels[i] != 0:
            continue

        neigh = RegionQuery(points, distance, i, epsilon)

        # все у чого не достатньо сусідів → шум.
        if len(neigh) < k:
            labels[i] = -1
        else:
            # новий кластер.
            ID += 1
            ExpandCluster(points, distance, labels, i, neigh, ID, k, epsilon)

    return labels


