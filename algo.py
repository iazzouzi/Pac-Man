"""Pathfinding helpers for ghost movement.

Provides a breadth-first search over the maze grid to find the next
step a ghost should take toward a destination cell.
"""

from queue import Queue
from typing import Optional


def nmap(bin: str) -> set[str]:
    """Determine which sides of a maze cell are open.

    Args:
        bin: The cell's wall bitmask, as a 4-character binary string.

    Returns:
        A set of open sides among ``{'w', 's', 'e', 'n'}``.
    """
    ports = set()
    if bin[0] == '0':
        ports.add('w')
    if bin[1] == '0':
        ports.add('s')
    if bin[2] == '0':
        ports.add('e')
    if bin[3] == '0':
        ports.add('n')
    return ports


def reconstruct_path(
    map: dict[tuple[int, int], Optional[tuple[int, int]]],
    dest: tuple[int, int],
) -> list[tuple[int, int]]:
    """Rebuild the path from the BFS root to ``dest``.

    Args:
        map: Mapping of each visited cell to the cell it was reached
            from (the root maps to ``None``).
        dest: The destination cell to trace the path back from.

    Returns:
        The list of cells from the root to ``dest``, inclusive.
    """
    path = []
    curr: Optional[tuple[int, int]] = dest
    while curr is not None:
        path.append(curr)
        curr = map[curr]
    return path[::-1]


def next(
    maze: list[list[int]],
    root: tuple[int, int],
    dest: tuple[int, int],
) -> Optional[tuple[int, int]]:
    """Find the next cell to move to from ``root`` toward ``dest``.

    Runs a breadth-first search over the maze's open corridors and
    returns the first step of the shortest path found.

    Args:
        maze: The maze grid, where each cell encodes its open walls.
        root: The starting cell.
        dest: The destination cell.

    Returns:
        The next cell on the shortest path toward ``dest``, or ``None``
        if ``root`` and ``dest`` are the same cell or no path exists.
    """
    queue: Queue[tuple[int, int]] = Queue()
    queue.put(root)
    visited = set()
    visited.add(root)
    map: dict[tuple[int, int], Optional[tuple[int, int]]] = {root: None}
    while not queue.empty():
        curr = queue.get()
        if curr == dest:
            path = reconstruct_path(map, dest)
            return path[1] if len(path) > 1 else None
        x = curr[0]
        y = curr[1]
        for port in nmap(f'{maze[y][x]:04b}'):
            if port == 'w':
                nxt = (x - 1, y)
                if nxt not in visited:
                    queue.put(nxt)
                    visited.add(nxt)
                    map[nxt] = curr
            elif port == 's':
                nxt = (x, y + 1)
                if nxt not in visited:
                    queue.put(nxt)
                    visited.add(nxt)
                    map[nxt] = curr
            elif port == 'e':
                nxt = (x + 1, y)
                if nxt not in visited:
                    queue.put(nxt)
                    visited.add(nxt)
                    map[nxt] = curr
            elif port == 'n':
                nxt = (x, y - 1)
                if nxt not in visited:
                    queue.put(nxt)
                    visited.add(nxt)
                    map[nxt] = curr
    return None
