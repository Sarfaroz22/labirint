import tkinter as tk
from tkinter import messagebox
import queue

# Размеры
WIDTH, HEIGHT = 20, 20
CELL_SIZE = 25

class MazeApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Лабиринт с жучком")
        self.labyrinth = [[0 for _ in range(WIDTH)] for _ in range(HEIGHT)]
        self.start = (1, 1)
        self.exit = (18, 18)
        self.moth = (1, 1)  # Жучок, начальная позиция

        self.canvas = tk.Canvas(root, width=WIDTH*CELL_SIZE, height=HEIGHT*CELL_SIZE, bg='white')
        self.canvas.pack()

        self.canvas.bind("<Button-1>", self.on_canvas_click)

        btn_frame = tk.Frame(root)
        btn_frame.pack(pady=5)

        self.btn_path = tk.Button(btn_frame, text="Найти путь для жучка", command=self.find_path_for_moth)
        self.btn_path.pack(side=tk.LEFT, padx=5)

        self.btn_clear = tk.Button(btn_frame, text="Очистить", command=self.clear_labyrinth)
        self.btn_clear.pack(side=tk.LEFT, padx=5)

        self.create_maze()
        self.draw_grid()

    def create_maze(self):
        # Пример готового лабиринта
        maze_pattern = [
            "11111111111111111111",
            "10000000000000000001",
            "10111111111111111101",
            "10100000000000000101",
            "10101111111111110101",
            "10101000000000110101",
            "10101011111110110101",
            "10101010000010110101",
            "10101010111110110101",
            "10101010100010110101",
            "10101010101110110101",
            "10101010101010110101",
            "10101010101110110101",
            "10101010100010110101",
            "10101011111110110101",
            "10100000000000000101",
            "10111111111111111101",
            "10000000000000000001",
            "11111111111111111111",
        ]
        for y, row in enumerate(maze_pattern):
            for x, ch in enumerate(row):
                if ch == '1':
                    self.labyrinth[y][x] = 1
        # Начальная позиция жучка
        self.moth = self.start = (1, 1)
        self.exit = (18, 17)  # Выход

    def draw_grid(self):
        self.rects = []
        for y in range(HEIGHT):
            row = []
            for x in range(WIDTH):
                color = 'white'
                if (x, y) == self.start:
                    color = 'green'
                elif (x, y) == self.exit:
                    color = 'red'
                elif (x, y) == self.moth:
                    color = 'blue'  # Жучок
                elif self.labyrinth[y][x] == 1:
                    color = 'black'
                rect = self.canvas.create_rectangle(
                    x*CELL_SIZE, y*CELL_SIZE, (x+1)*CELL_SIZE, (y+1)*CELL_SIZE,
                    fill=color, outline='gray'
                )
                row.append(rect)
            self.rects.append(row)

    def update_cell(self, x, y):
        """Обновляет цвет клетки"""
        color = 'white'
        if (x, y) == self.start:
            color = 'green'
        elif (x, y) == self.exit:
            color = 'red'
        elif (x, y) == self.moth:
            color = 'blue'
        elif self.labyrinth[y][x] == 1:
            color = 'black'
        self.canvas.itemconfig(self.rects[y][x], fill=color)

    def on_canvas_click(self, event):
        x = event.x // CELL_SIZE
        y = event.y // CELL_SIZE
        if (x, y) == self.start or (x, y) == self.exit or (x, y) == self.moth:
            return  # Не изменять старт, выход, жучка
        if self.labyrinth[y][x] == 0:
            self.labyrinth[y][x] = 1
        else:
            self.labyrinth[y][x] = 0
        self.update_cell(x, y)

    def clear_labyrinth(self):
        for y in range(HEIGHT):
            for x in range(WIDTH):
                self.labyrinth[y][x] = 0
                if (x, y) == self.start:
                    self.update_cell(x, y)
                elif (x, y) == self.exit:
                    self.update_cell(x, y)
                elif (x, y) == self.moth:
                    self.update_cell(x, y)
        self.draw_grid()

    def find_path_for_moth(self):
        """Находит путь для жучка от его текущей позиции к выходу"""
        path = self.bfs(self.moth, self.exit)
        if path:
            # Отобразим путь зелёным
            for (x, y) in path:
                if (x, y) != self.start and (x, y) != self.exit and (x, y) != self.moth:
                    self.canvas.itemconfig(self.rects[y][x], fill='yellow')
            messagebox.showinfo("Путь найден", f"Длина пути: {len(path)}")
        else:
            messagebox.showinfo("Без пути", "Путь не найден!")

    def bfs(self, start, goal):
        """Поиск кратчайшего пути BFS"""
        visited = [[False]*WIDTH for _ in range(HEIGHT)]
        prev = [[None]*WIDTH for _ in range(HEIGHT)]
        q = queue.Queue()
        q.put(start)
        visited[start[1]][start[0]] = True

        while not q.empty():
            x, y = q.get()
            if (x, y) == goal:
                break
            for dx, dy in [(-1,0),(1,0),(0,-1),(0,1)]:
                nx, ny = x + dx, y + dy
                if 0 <= nx < WIDTH and 0 <= ny < HEIGHT:
                    if not visited[ny][nx] and self.labyrinth[ny][nx] == 0:
                        visited[ny][nx] = True
                        prev[ny][nx] = (x, y)
                        q.put((nx, ny))
        # Восстановление пути
        path = []
        at = goal
        while at:
            path.append(at)
            at = prev[at[1]][at[0]]
        path.reverse()
        if path and path[0] == start:
            return path
        else:
            return []

if __name__ == "__main__":
    root = tk.Tk()
    app = MazeApp(root)
    root.mainloop()
