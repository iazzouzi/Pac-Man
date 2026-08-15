import pygame
from pygame import surface
import webcolors
from mazegen import MazeGen

CELL_SIZE = 100
WALL_COLOR = webcolors.name_to_rgb('white')

def maze_to_directions(maze: list[list[int]]) -> list[list[dict[str, bool]]]:
    cells_directions = []
    for row in maze:
        row_maze = []
        for col in row:
            row_maze.append(
                {
                    "N": bool(col & 1),
                    "E": bool(col & 2), 
                    "S": bool(col & 4),
                    "W": bool(col & 8) 
                }
                )
        cells_directions.append(row_maze)
    return cells_directions

pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Pacman")
running =  True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    pygame.display.flip()
pygame.quit()
