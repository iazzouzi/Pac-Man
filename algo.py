from queue import Queue

def nmap(bin: str) -> set[str]:
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

def reconstruct_path(map: dict[tuple[int, int], tuple[int, int]], dest: tuple[int, int]) -> list[tuple[int, int]]:
    path = []
    curr = dest
    while curr is not None:
        path.append(curr)
        curr = map[curr]
    return path[::-1]

def next(maze: list[list[int]], root: tuple[int, int], dest: tuple[int, int]) -> tuple[int, int]:
    queue = Queue()
    queue.put(root)
    visited = set()
    visited.add(root)
    map = {root: None}
    while not queue.empty():
        curr = queue.get()
        if curr == dest:
            return reconstruct_path(map, dest)[1] if len(reconstruct_path(map, dest)) > 1 else None
        x = curr[0]
        y = curr[1]
        for port in nmap(f'{maze[y][x]:04b}'):
            if port == 'w':
                nxt = (x - 1, y)
                if not nxt in visited:
                    queue.put(nxt)
                    visited.add(nxt)
                    map[nxt] = curr
            elif port == 's':
                nxt = (x, y + 1)
                if not nxt in visited:
                    queue.put(nxt)
                    visited.add(nxt)
                    map[nxt] = curr
            elif port == 'e':
                nxt = (x + 1, y)
                if not nxt in visited:
                    queue.put(nxt)
                    visited.add(nxt)
                    map[nxt] = curr
            elif port == 'n':
                nxt = (x, y - 1)
                if not nxt in visited:
                    queue.put(nxt)
                    visited.add(nxt)
                    map[nxt] = curr
    return None