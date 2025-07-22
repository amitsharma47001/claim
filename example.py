import pyautogui
import time
import random
import numpy as np

# 1280x720 display zone
SCREEN_WIDTH = 900
SCREEN_HEIGHT = 720

def human_like_mouse_move(start_x, start_y, end_x, end_y, duration=1.5):
    steps = random.randint(10, 25)
    x_points = np.linspace(start_x, end_x, steps)
    y_points = np.linspace(start_y, end_y, steps)

    # Add curved jitter to Y-axis (simulate hand movement)
    jitter_strength = random.uniform(1.5, 4.0)
    y_points += np.random.normal(0, jitter_strength, steps)

    for x, y in zip(x_points, y_points):
        pyautogui.moveTo(x, y, duration=random.uniform(0.01, 0.05))
        if random.random() < 0.1:  # occasional pause
            time.sleep(random.uniform(0.05, 0.2))

def random_move_within_area(x_range, y_range):
    # Clamp values to 1280x720
    x_min, x_max = max(0, x_range[0]), min(SCREEN_WIDTH, x_range[1])
    y_min, y_max = max(0, y_range[0]), min(SCREEN_HEIGHT, y_range[1])

    current_x, current_y = pyautogui.position()

    target_x = random.randint(x_min, x_max)
    target_y = random.randint(y_min, y_max)
    duration = random.uniform(0.8, 2.5)

    human_like_mouse_move(current_x, current_y, target_x, target_y, duration)

    time.sleep(random.uniform(1, 3))  # Pause before next move

# Safe center area (avoids screen edges)
x_range = (int(SCREEN_WIDTH * 0.2), int(SCREEN_WIDTH * 0.8))   # ~256 to 1024
y_range = (int(SCREEN_HEIGHT * 0.2), int(SCREEN_HEIGHT * 0.8)) # ~144 to 576

# 🔁 Run forever
while True:
    random_move_within_area(x_range, y_range)
