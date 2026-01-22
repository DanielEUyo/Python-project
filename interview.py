from collections import Counter
import random
import psycopg2  # (only needed for DB part)


# Raw colour data extracted from the HTML
data = {
    "Monday": "GREEN YELLOW GREEN BROWN BLUE PINK BLUE YELLOW ORANGE CREAM ORANGE RED WHITE BLUE WHITE BLUE BLUE BLUE GREEN",
    "Tuesday": "ASH BROWN GREEN BROWN BLUE BLUE BLUE PINK PINK ORANGE ORANGE RED WHITE BLUE WHITE WHITE BLUE BLUE BLUE",
    "Wednesday": "GREEN YELLOW GREEN BROWN BLUE PINK RED YELLOW ORANGE RED ORANGE RED BLUE BLUE WHITE BLUE BLUE WHITE WHITE",
    "Thursday": "BLUE BLUE GREEN WHITE BLUE BROWN PINK YELLOW ORANGE CREAM ORANGE RED WHITE BLUE WHITE BLUE BLUE BLUE GREEN",
    "Friday": "GREEN WHITE GREEN BROWN BLUE BLUE BLACK WHITE ORANGE RED RED RED WHITE BLUE WHITE BLUE BLUE BLUE WHITE"
}

# Normalize and combine all colors
all_colors = []
for colors in data.values():
    all_colors.extend(colors.split())

# Fix spelling inconsistency
all_colors = ["BLUE" if c == "BLEW" else c for c in all_colors]

color_freq = Counter(all_colors)
total = len(all_colors)



# Answers to the Questions

# 1. Most Worn Color (Mode)
most_worn = color_freq.most_common(1)
print("Most worn color:", most_worn)


# 2. Mean Color
# Mean color = average frequency

mean_frequency = sum(color_freq.values()) / len(color_freq)
mean_color = [c for c, f in color_freq.items() if f == round(mean_frequency)]
print("Mean color(s):", mean_color)


# 3. Median Color
sorted_colors = sorted(color_freq.items(), key=lambda x: x[1])
mid = len(sorted_colors) // 2
median_color = sorted_colors[mid]
print("Median color:", median_color)

# 4. Variance of Colors (BONUS)
mean = sum(color_freq.values()) / len(color_freq)
variance = sum((f - mean) ** 2 for f in color_freq.values()) / len(color_freq)
print("Variance:", variance)

# 5. Probability of Picking RED (BONUS)
prob_red = color_freq["RED"] / total
print("Probability of RED:", prob_red)

# 6. Save to PostgreSQL Database
"""
CREATE TABLE colors (
    color VARCHAR(20),
    frequency INT
);
"""

conn = psycopg2.connect(
    dbname="bincom",
    user="postgres",
    password="password",
    host="localhost",
    port="5432"
)

cur = conn.cursor()
for color, freq in color_freq.items():
    cur.execute(
        "INSERT INTO colors (color, frequency) VALUES (%s, %s)",
        (color, freq)
    )

conn.commit()
cur.close()
conn.close()

# 7. Recursive Search Algorithm (BONUS)
def recursive_search(arr, target, index=0):
    if index == len(arr):
        return False
    if arr[index] == target:
        return True
    return recursive_search(arr, target, index + 1)

nums = [1, 3, 5, 7, 9]
print(recursive_search(nums, 7))

# 8. Generate Random Binary & Convert to Base 10
binary = ''.join(str(random.randint(0, 1)) for _ in range(4))
decimal = int(binary, 2)

print("Binary:", binary)
print("Decimal:", decimal)

# 9. Sum of First 50 Fibonacci Numbers
def fibonacci_sum(n):
    a, b = 0, 1
    total = 0
    for _ in range(n):
        total += a
        a, b = b, a + b
    return total

print("Sum of first 50 Fibonacci numbers:", fibonacci_sum(50))