import pandas as pd
import json
import math


# Load CSV
df = pd.read_csv('df_balanced.csv')

# Set the desired time filter
target_month = 7          # July
target_dayofweek = 5      # Friday

# Filter based on month and day of week
filtered = df[
    (df["MONTH"] == target_month) & 
    (df["DAYOFWEEK"] == target_dayofweek)
]

# Get top 50 high-crime block codes
block_counts = filtered.groupby("BLOCK CODE").size().sort_values(ascending=False)
top_blocks = block_counts.head(50)

# Define thresholds for risk levels
high_threshold = top_blocks.quantile(0.90)
medium_threshold = top_blocks.quantile(0.75)

# Get average coordinates for each block
coordinates = filtered.groupby("BLOCK CODE")[["LATITUDE", "LONGITUDE"]].mean()

# Create hotspot list with risk levels and costs
results = []
for block in top_blocks.index:
    count = top_blocks[block]
    if count >= high_threshold:
        level = "high"
        cost = 1
    elif count >= medium_threshold:
        level = "medium"
        cost = 3
    else:
        level = "low"
        cost = 5

    lat = coordinates.loc[block]["LATITUDE"]
    lng = coordinates.loc[block]["LONGITUDE"]

    results.append({
        "block_code": int(block),
        "lat": lat,
        "lng": lng,
        "level": level,
        "cost": cost
    })

# Save initial JSON (raw points)
with open('crime_hotspots.json', 'w') as f:
    json.dump({
        "points": results,
        "path": results  # Placeholder
    }, f, indent=2)

# Load data back
with open('crime_hotspots.json', 'r') as f:
    data = json.load(f)

points = data["points"]

# Distance between two points
def distance(a, b):
    R = 6371  # Earth radius in km
    lat1 = math.radians(a["lat"])
    lon1 = math.radians(a["lng"])
    lat2 = math.radians(b["lat"])
    lon2 = math.radians(b["lng"])

    dlat = lat2 - lat1
    dlon = lon2 - lon1

    hav = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
    c = 2 * math.atan2(math.sqrt(hav), math.sqrt(1 - hav))

    return R * c

# Build a graph of all node connections with distances
def build_graph(points):
    graph = {}
    for i, node in enumerate(points):
        graph[i] = []
        for j, other in enumerate(points):
            if i != j:
                dist = distance(node, other)
                graph[i].append((j, dist))
    return graph

# A* algorithm using cost (crime risk) + distance
def a_star_path(points, graph):
    visited = set()
    path = []
    current = 0
    visited.add(current)
    path.append(points[current])

    while len(visited) < len(points):
        next_node = None
        min_f = float("inf")

        for neighbor, dist in graph[current]:
            if neighbor in visited:
                continue
            g = points[neighbor]["cost"]  # crime cost
            h = dist                      # distance
            f = g + h                     # total cost
            if f < min_f:
                min_f = f
                next_node = neighbor

        if next_node is None:
            break  # Dead end

        current = next_node
        visited.add(current)
        path.append(points[current])

    return path

# Build graph and run A*
graph = build_graph(points)
optimal_path = a_star_path(points, graph)

# Save final result with computed optimal path
with open('crime_hotspots.json', 'w') as f:
    json.dump({
        "points": points,
        "path": optimal_path
    }, f, indent=2)
print(optimal_path)