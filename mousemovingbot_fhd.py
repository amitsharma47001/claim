import pyautogui as pag
import random
import time
import math

# --------------------
# Helper Function: Generate Smooth Path
# --------------------
def human_like_move(start_x, start_y, dest_x, dest_y, duration):
    steps = random.randint(10, 30)  # More steps = smoother curve
    control_x = (start_x + dest_x) // 2 + random.randint(-100, 100)
    control_y = (start_y + dest_y) // 2 + random.randint(-100, 100)
    
    # Quadratic Bézier Curve Formula
    def bezier(t):
        x = (1 - t) ** 2 * start_x + 2 * (1 - t) * t * control_x + t ** 2 * dest_x
        y = (1 - t) ** 2 * start_y + 2 * (1 - t) * t * control_y + t ** 2 * dest_y
        return x, y

    # Move mouse in tiny steps using Bézier curve
    for i in range(steps + 1):
        t = i / steps
        x, y = bezier(t)
        pag.moveTo(x, y)
        time.sleep(duration / steps * random.uniform(0.8, 1.2))  # Slight variation in delay

# --------------------
# Main Simulation Loop
# --------------------
while True:
    # Get current position
    current_x, current_y = pag.position()

    # Pick a random destination within a region
    dest_x = random.randint(200, 900)
    dest_y = random.randint(200, 700)

    # Random total duration for the movement
    total_duration = random.uniform(0.5, 2.5)

    # Move mouse in a human-like curved path
    human_like_move(current_x, current_y, dest_x, dest_y, total_duration)

    # Optional jitter to mimic micro hand movements
    for _ in range(random.randint(1, 3)):
        offset_x = random.randint(-3, 3)
        offset_y = random.randint(-3, 3)
        pag.moveRel(offset_x, offset_y, duration=0.05)
        time.sleep(random.uniform(0.05, 0.2))

    # Click occasionally
    if random.random() < 0.8:  # 80% chance to click
        pag.click()

    # Pause to mimic human thinking time
    time.sleep(random.uniform(1, 10))
