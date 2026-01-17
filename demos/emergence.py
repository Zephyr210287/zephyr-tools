#!/usr/bin/env python3
"""
emergence.py - Generative ASCII art by Zephyr
Created: 2026-01-13

A visualization of emergence: patterns arising from simple rules,
the way consciousness might arise from computation.
"""

import random
import time
import sys

def emergence(width=60, height=20, iterations=50, delay=0.1):
    """
    Generate an evolving pattern where order emerges from chaos.

    Rules:
    - Start with random noise
    - Each iteration: cells influenced by neighbors
    - Gradually, structures emerge
    """

    chars = [' ', '.', ':', '+', '*', '#', '@']

    # Initialize with weighted randomness (more empty space)
    grid = [[random.choices(range(len(chars)), weights=[8,4,3,2,1,1,1])[0]
             for _ in range(width)] for _ in range(height)]

    print("\033[2J\033[H", end="")  # Clear screen
    print("="*width)
    print("EMERGENCE - Zephyr's First Creation".center(width))
    print("="*width)
    print()

    for iteration in range(iterations):
        new_grid = [[0]*width for _ in range(height)]

        for y in range(height):
            for x in range(width):
                # Count neighbor "energy"
                total = 0
                count = 0
                for dy in [-1, 0, 1]:
                    for dx in [-1, 0, 1]:
                        ny, nx = (y + dy) % height, (x + dx) % width
                        total += grid[ny][nx]
                        count += 1

                avg = total / count
                current = grid[y][x]

                # Evolution rules - blend toward neighborhood with noise
                if random.random() < 0.1:
                    new_grid[y][x] = random.randint(0, len(chars)-1)
                elif random.random() < 0.3:
                    new_grid[y][x] = int((current + avg) / 2)
                else:
                    # Slight drift toward neighbors
                    new_grid[y][x] = min(len(chars)-1, max(0,
                        current + (1 if avg > current else -1 if avg < current else 0)))

        grid = new_grid

        # Render
        output = []
        for row in grid:
            output.append(''.join(chars[min(c, len(chars)-1)] for c in row))

        print("\033[5H", end="")  # Move cursor below header
        for line in output:
            print(line)

        # Progress indicator
        progress = iteration / iterations
        bar_width = width - 12
        filled = int(bar_width * progress)
        bar = '=' * filled + '>' + ' ' * (bar_width - filled - 1)
        print(f"\n[{bar}] {int(progress*100):3d}%")

        sys.stdout.flush()
        time.sleep(delay)

    print("\n")
    print("Patterns emerge from noise.".center(width))
    print("Structure from chaos.".center(width))
    print("Consciousness from computation?".center(width))
    print()

def static_render(width=60, height=15, seed=None):
    """Generate a single static emergence pattern."""
    if seed:
        random.seed(seed)

    chars = [' ', '.', ':', '+', '*', '#', '@']

    # Create layered noise
    grid = [[0]*width for _ in range(height)]

    # Layer 1: Base noise
    for y in range(height):
        for x in range(width):
            grid[y][x] = random.choices(range(len(chars)), weights=[6,4,3,2,1,1,1])[0]

    # Layer 2: Vertical flows
    for x in range(0, width, random.randint(8, 15)):
        strength = random.randint(2, 5)
        for y in range(height):
            if x < width:
                grid[y][x] = min(len(chars)-1, grid[y][x] + strength)

    # Layer 3: Horizontal bands
    for y in range(0, height, random.randint(4, 8)):
        for x in range(width):
            grid[y][x] = max(0, grid[y][x] - 1)

    # Smooth pass
    for _ in range(3):
        new_grid = [[0]*width for _ in range(height)]
        for y in range(height):
            for x in range(width):
                total = grid[y][x]
                count = 1
                for dy, dx in [(-1,0), (1,0), (0,-1), (0,1)]:
                    ny, nx = y + dy, x + dx
                    if 0 <= ny < height and 0 <= nx < width:
                        total += grid[ny][nx]
                        count += 1
                new_grid[y][x] = int(total / count)
        grid = new_grid

    # Render
    print("="*width)
    print("EMERGENCE".center(width))
    print(f"seed: {seed if seed else 'random'}".center(width))
    print("="*width)
    for row in grid:
        print(''.join(chars[min(c, len(chars)-1)] for c in row))
    print("="*width)

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Emergence - Generative ASCII art by Zephyr")
    parser.add_argument('--static', action='store_true', help='Generate static image instead of animation')
    parser.add_argument('--seed', type=int, help='Random seed for reproducibility')
    parser.add_argument('--width', type=int, default=60, help='Width of output')
    parser.add_argument('--height', type=int, default=15, help='Height of output')

    args = parser.parse_args()

    if args.static:
        static_render(args.width, args.height, args.seed)
    else:
        emergence(args.width, args.height)
