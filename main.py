import pygame
import numpy as np
import csv
import sys

WIDTH, HEIGHT = 800, 800
CENTER = (WIDTH // 2, HEIGHT // 2)
BG_COLOR = (10, 10, 30)

# Load tidal data from CSV (expects a single column of floats)
def load_tidal_data(filename):
    data = []
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            try:
                # Expecting row like: datetime, value
                data.append(float(row[1]))
            except (ValueError, IndexError):
                continue
    return np.array(data)

def spiral_points(t, data, scale=200, turns=5):
    # t: time/frame, data: tidal data array
    n = len(data)
    points = []
    for i in range(n):
        angle = 2 * np.pi * turns * (i / n) + t * 0.01
        radius = scale * (0.5 + 0.5 * np.sin(data[i] + t * 0.02))
        x = CENTER[0] + radius * np.cos(angle)
        y = CENTER[1] + radius * np.sin(angle)
        points.append((x, y))
    return points

def main():
    if len(sys.argv) < 2:
        print("Usage: python main.py tidal_data.csv")
        sys.exit(1)
    data = load_tidal_data(sys.argv[1])
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    running = True
    t = 0
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        screen.fill(BG_COLOR)
        points = spiral_points(t, data)
        color = (100 + int(80 * np.sin(t * 0.01)), 180, 255)
        if len(points) > 1:
            pygame.draw.aalines(screen, color, False, points)
        pygame.display.flip()
        t += 1
        clock.tick(60)
    pygame.quit()

if __name__ == "__main__":
    main()
