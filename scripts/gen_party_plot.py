import matplotlib.pyplot as plt
import numpy as np

# 1. Define party names, seat counts, and respective colors
parties = ['PAP', 'WP', 'No party affiliation']
seats = [86,12,9]  # Must sum to total seats
colors = ["#B81111", "#1d93f9", "#4D4D4D"]

# 2. Build the ordered seat color pool
# Reversing the color assignments maps the first group to the left side (180 degrees)
seat_colors = []
for color, count in zip(colors, seats):
    seat_colors.extend([color] * count)

total_seats = len(seat_colors)

# 3. Define multi-row concentric semicircles
num_rows = 5
radii = np.linspace(1.0, 2.0, num_rows)

# Distribute seats across rows proportionally based on radius length
row_lengths = radii / np.sum(radii)
row_counts = np.round(row_lengths * total_seats).astype(int)

# Fix rounding errors to match total_seats exactly
diff = total_seats - np.sum(row_counts)
row_counts[-1] += diff

# 4. Generate positions from left (pi) to right (0) for correct ordering
x_coords = []
y_coords = []

for r, r_count in zip(radii, row_counts):
    if r_count <= 0:
        continue
    # np.pi to 0 creates a clean left-to-right sweep across the arc
    angles = np.linspace(np.pi, 0, r_count)
    for theta in angles:
        x_coords.append(r * np.cos(theta))
        y_coords.append(r * np.sin(theta))

# 5. Sort seats by angle to group the same ethnicities together across rows
# Calculating the arc tangent clusters the colors sequentially from left to right
angles_calc = np.arctan2(y_coords, x_coords)
sorted_indices = np.argsort(angles_calc)[::-1]  # Sort descending (left to right)

# Reorder positions based on the angular sort
x_sorted = [x_coords[i] for i in sorted_indices]
y_sorted = [y_coords[i] for i in sorted_indices]

# 6. Plot the layout
fig, ax = plt.subplots(figsize=(8, 5))
ax.scatter(x_sorted, y_sorted, c=seat_colors, s=120, edgecolors='w', lw=1)

# Add a clean legend
for eth, col in zip(parties, colors):
    ax.scatter([], [], c=col, label=eth, edgecolors='w', s=120)
ax.legend(loc='lower center', bbox_to_anchor=(0.5, -0.1), ncol=3, frameon=False)

ax.set_aspect('equal')
ax.axis('off')
plt.title('Distribution By Party Affiliation', fontsize=14, fontweight='bold', pad=20)
plt.show()