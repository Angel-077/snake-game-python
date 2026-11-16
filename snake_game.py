import random
import tkinter as tk

WIDTH = 420
HEIGHT = 420
GRID_SIZE = 20
SPEED = 120


class SnakeGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Snake Game")
        self.root.resizable(False, False)

        self.canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT, bg="#0f172a", highlightthickness=0)
        self.canvas.pack(padx=12, pady=12)

        self.score_var = tk.StringVar(value="0")
        self.best_var = tk.StringVar(value="0")

        self.info = tk.Frame(root, bg="#111827")
        self.info.pack(fill="x", padx=12, pady=(0, 12))

        tk.Label(self.info, text="Score", bg="#111827", fg="#cbd5e1", font=("Arial", 10, "bold")).pack(side="left", padx=(16, 0))
        tk.Label(self.info, textvariable=self.score_var, bg="#111827", fg="#e2e8f0", font=("Arial", 12, "bold")).pack(side="left", padx=(6, 20))

        tk.Label(self.info, text="Best", bg="#111827", fg="#cbd5e1", font=("Arial", 10, "bold")).pack(side="left")
        tk.Label(self.info, textvariable=self.best_var, bg="#111827", fg="#e2e8f0", font=("Arial", 12, "bold")).pack(side="left", padx=(6, 16))

        self.button = tk.Button(root, text="Start", command=self.start_game, bg="#34d399", fg="#062b20", font=("Arial", 11, "bold"), relief="flat")
        self.button.pack(pady=(0, 12))

        self.root.bind("<KeyPress>", self.on_key)
        self.root.focus_set()

        self.game_over = False
        self.running = False
        self.snake = []
        self.direction = (1, 0)
        self.next_direction = (1, 0)
        self.food = None
        self.score = 0
        self.best_score = int(self.root.tk.call("::tk::msgcat::mcset", "", "", "")) if False else 0

        self.best_score = int(open("snake_best_score.txt", "r", encoding="utf-8").read().strip() or "0") if __import__("os").path.exists("snake_best_score.txt") else 0
        self.best_var.set(str(self.best_score))
        self.reset_board()

    def save_best_score(self):
        with open("snake_best_score.txt", "w", encoding="utf-8") as f:
            f.write(str(self.best_score))

    def reset_board(self):
        self.canvas.delete("all")
        self.snake = [(10, 10), (9, 10), (8, 10)]
        self.direction = (1, 0)
        self.next_direction = (1, 0)
        self.score = 0
        self.score_var.set("0")
        self.food = self.spawn_food()
        self.game_over = False
        self.running = False
        self.draw_board()

    def spawn_food(self):
        while True:
            food = (random.randint(0, GRID_SIZE - 1), random.randint(0, GRID_SIZE - 1))
            if food not in self.snake:
                return food

    def start_game(self):
        self.reset_board()
        self.running = True
        self.button.config(text="Restart")
        self.root.focus_set()
        self.game_loop()

    def game_loop(self):
        if not self.running:
            return

        self.direction = self.next_direction
        head_x, head_y = self.snake[0]
        new_head = (head_x + self.direction[0], head_y + self.direction[1])

        if (
            new_head[0] < 0
            or new_head[0] >= GRID_SIZE
            or new_head[1] < 0
            or new_head[1] >= GRID_SIZE
            or new_head in self.snake
        ):
            self.running = False
            self.game_over = True
            self.canvas.create_text(WIDTH / 2, HEIGHT / 2, text="Game Over", fill="#f8fafc", font=("Arial", 24, "bold"))
            self.canvas.create_text(WIDTH / 2, HEIGHT / 2 + 28, text="Press Start to play again", fill="#94a3b8", font=("Arial", 12))
            return

        self.snake.insert(0, new_head)

        if new_head == self.food:
            self.score += 10
            self.score_var.set(str(self.score))
            if self.score > self.best_score:
                self.best_score = self.score
                self.best_var.set(str(self.best_score))
                self.save_best_score()
            self.food = self.spawn_food()
        else:
            self.snake.pop()

        self.draw_board()
        self.root.after(SPEED, self.game_loop)

    def draw_board(self):
        self.canvas.delete("all")
        cell = WIDTH / GRID_SIZE

        for x in range(GRID_SIZE):
            for y in range(GRID_SIZE):
                self.canvas.create_rectangle(x * cell, y * cell, (x + 1) * cell, (y + 1) * cell, fill="#0f172a", outline="#1e293b")

        for x, y in self.snake:
            self.canvas.create_rectangle(x * cell + 1, y * cell + 1, (x + 1) * cell - 1, (y + 1) * cell - 1, fill="#34d399", outline="#10b981")

        food_x, food_y = self.food
        self.canvas.create_oval(food_x * cell + 4, food_y * cell + 4, (food_x + 1) * cell - 4, (food_y + 1) * cell - 4, fill="#fbbf24")

    def on_key(self, event):
        key = event.keysym.lower()
        mapping = {
            "up": (0, -1),
            "w": (0, -1),
            "down": (0, 1),
            "s": (0, 1),
            "left": (-1, 0),
            "a": (-1, 0),
            "right": (1, 0),
            "d": (1, 0),
        }

        if key not in mapping:
            return

        new_direction = mapping[key]
        current = self.direction
        if new_direction[0] == -current[0] and new_direction[1] == -current[1]:
            return

        self.next_direction = new_direction


if __name__ == "__main__":
    root = tk.Tk()
    root.configure(bg="#020817")
    SnakeGame(root)
    root.mainloop()
