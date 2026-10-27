import math
import random
import tkinter as tk


GAME_WIDTH = 600
GAME_HEIGHT = 400
PADDLE_WIDTH = 110
PADDLE_HEIGHT = 14
BALL_SIZE = 18
FRAME_DELAY = 16
PLAYER_SPEED = 7


class Paddle:
    def __init__(self, canvas):
        self.canvas = canvas
        self.width = PADDLE_WIDTH
        self.height = PADDLE_HEIGHT
        self.x = (GAME_WIDTH - self.width) / 2
        self.y = GAME_HEIGHT - self.height - 18
        self.shadow = canvas.create_rectangle(
            self.x + 4,
            self.y + 4,
            self.x + self.width + 4,
            self.y + self.height + 4,
            fill="#0f172a",
            outline="",
            tags="paddle",
        )
        self.item = canvas.create_rectangle(
            self.x,
            self.y,
            self.x + self.width,
            self.y + self.height,
            fill="#f97316",
            outline="#fdba74",
            width=3,
            tags="paddle",
        )
        self.highlight = canvas.create_rectangle(
            self.x + 8,
            self.y + 3,
            self.x + self.width - 8,
            self.y + self.height / 2,
            fill="#fed7aa",
            outline="",
            tags="paddle",
        )

    def move_to(self, x):
        self.x = max(0, min(x, GAME_WIDTH - self.width))
        self.canvas.coords(
            self.shadow,
            self.x + 4,
            self.y + 4,
            self.x + self.width + 4,
            self.y + self.height + 4,
        )
        self.canvas.coords(
            self.item,
            self.x,
            self.y,
            self.x + self.width,
            self.y + self.height,
        )
        self.canvas.coords(
            self.highlight,
            self.x + 8,
            self.y + 3,
            self.x + self.width - 8,
            self.y + self.height / 2,
        )

    def move(self, direction):
        self.move_to(self.x + direction * PLAYER_SPEED)

    def reset(self):
        self.move_to((GAME_WIDTH - self.width) / 2)


class Ball:
    def __init__(self, canvas, score):
        self.canvas = canvas
        self.size = BALL_SIZE
        self.x = random.uniform(0, GAME_WIDTH - self.size)
        self.y = 20
        speed = 3.5 + random.random() * 1.5 + score * 0.05
        angle = (random.random() * 1.8 - 0.9) * 1.4
        self.vx = speed * math.sin(angle)
        self.vy = speed * math.cos(angle) + 2
        self.shadow = canvas.create_oval(
            self.x + 3,
            self.y + 3,
            self.x + self.size + 3,
            self.y + self.size + 3,
            fill="#111827",
            outline="",
            tags="ball",
        )
        self.item = canvas.create_oval(
            self.x,
            self.y,
            self.x + self.size,
            self.y + self.size,
            fill="#fbbf24",
            outline="#fff7ed",
            width=2,
            tags="ball",
        )
        self.inner = canvas.create_oval(
            self.x + 5,
            self.y + 5,
            self.x + self.size - 5,
            self.y + self.size - 5,
            fill="#fde68a",
            outline="",
            tags="ball",
        )

    def move(self):
        self.x += self.vx
        self.y += self.vy

    def draw(self):
        self.canvas.coords(
            self.shadow,
            self.x + 3,
            self.y + 3,
            self.x + self.size + 3,
            self.y + self.size + 3,
        )
        self.canvas.coords(
            self.item,
            self.x,
            self.y,
            self.x + self.size,
            self.y + self.size,
        )
        self.canvas.coords(
            self.inner,
            self.x + 5,
            self.y + 5,
            self.x + self.size - 5,
            self.y + self.size - 5,
        )

    def destroy(self):
        self.canvas.delete(self.shadow)
        self.canvas.delete(self.item)
        self.canvas.delete(self.inner)


class PingPongGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Ping Pong test")
        self.root.resizable(False, False)
        self.root.configure(bg="#020817")
        self.root.geometry("680x560")

        self.title_label = tk.Label(
            root,
            text="PING PONG",
            font=("Arial", 22, "bold"),
            fg="#e2e8f0",
            bg="#020817",
            pady=14,
        )
        self.title_label.pack()

        self.score_label = tk.Label(
            root,
            text="",
            font=("Arial", 14, "bold"),
            fg="#f8fafc",
            bg="#0f172a",
            padx=18,
            pady=8,
            relief="flat",
            bd=0,
        )
        self.score_label.pack(pady=(0, 12))

        self.canvas = tk.Canvas(
            root,
            width=GAME_WIDTH,
            height=GAME_HEIGHT,
            bg="#081b2b",
            highlightthickness=0,
        )
        self.canvas.pack(padx=12, pady=(0, 8))

        self.restart_button = tk.Button(
            root,
            text="Jogar novamente",
            command=self.reset_game,
            bg="#f59e0b",
            fg="#111827",
            font=("Arial", 12, "bold"),
            padx=18,
            pady=8,
            relief="flat",
            activebackground="#fbbf24",
            cursor="hand2",
        )
        self.restart_window = self.canvas.create_window(
            GAME_WIDTH / 2,
            GAME_HEIGHT / 2 + 65,
            window=self.restart_button,
            state="hidden",
        )

        self.left_pressed = False
        self.right_pressed = False
        self.after_id = None

        self.root.bind("<KeyPress>", self.on_key_press)
        self.root.bind("<KeyRelease>", self.on_key_release)

        self.reset_game()

    def draw_background(self):
        self.canvas.create_rectangle(
            0,
            0,
            GAME_WIDTH,
            GAME_HEIGHT,
            fill="#081b2b",
            outline="",
            tags="background",
        )
        self.canvas.create_line(
            GAME_WIDTH / 2,
            0,
            GAME_WIDTH / 2,
            GAME_HEIGHT,
            fill="#38bdf8",
            dash=(10, 8),
            width=2,
            tags="background",
        )
        for x, y in [
            (40, 45),
            (130, 90),
            (500, 55),
            (540, 150),
            (70, 300),
            (530, 280),
        ]:
            self.canvas.create_oval(
                x,
                y,
                x + 6,
                y + 6,
                fill="#67e8f9",
                outline="",
                tags="background",
            )

    def reset_game(self):
        if self.after_id is not None:
            self.root.after_cancel(self.after_id)
            self.after_id = None

        self.canvas.delete("game_over")
        self.canvas.itemconfigure(self.restart_window, state="hidden")
        self.score = 0
        self.lives = 2
        self.running = True
        self.left_pressed = False
        self.right_pressed = False

        self.canvas.delete("all")
        self.draw_background()
        self.paddle = Paddle(self.canvas)
        self.ball = Ball(self.canvas, self.score)

        self.restart_window = self.canvas.create_window(
            GAME_WIDTH / 2,
            GAME_HEIGHT / 2 + 65,
            window=self.restart_button,
            state="hidden",
        )
        self.update_score()
        self.game_loop()

    def update_score(self):
        self.score_label.config(
            text=f"Pontuação: {self.score}   •   Vidas: {self.lives}",
            bg="#0f172a",
            fg="#f8fafc",
        )

    def spawn_ball(self):
        self.ball = Ball(self.canvas, self.score)

    def lose_life(self):
        self.lives -= 1
        self.update_score()

        if self.lives <= 0:
            self.end_game()
        else:
            self.spawn_ball()

    def end_game(self):
        self.running = False
        self.canvas.create_rectangle(
            70,
            110,
            GAME_WIDTH - 70,
            GAME_HEIGHT - 90,
            fill="#0f172a",
            outline="#38bdf8",
            width=3,
            tags="game_over",
        )
        self.canvas.create_text(
            GAME_WIDTH / 2,
            GAME_HEIGHT / 2 - 32,
            text="Fim de jogo",
            fill="#f8fafc",
            font=("Arial", 30, "bold"),
            tags="game_over",
        )
        self.canvas.create_text(
            GAME_WIDTH / 2,
            GAME_HEIGHT / 2 + 8,
            text=f"Pontuação final: {self.score}",
            fill="#cbd5e1",
            font=("Arial", 20),
            tags="game_over",
        )
        self.canvas.itemconfigure(self.restart_window, state="normal")

    def handle_paddle_collision(self):
        ball_bottom = self.ball.y + self.ball.size
        ball_right = self.ball.x + self.ball.size
        paddle_right = self.paddle.x + self.paddle.width

        touching_paddle = (
            ball_bottom >= self.paddle.y
            and self.ball.y <= self.paddle.y + self.paddle.height
            and ball_right >= self.paddle.x
            and self.ball.x <= paddle_right
        )
        if not touching_paddle or self.ball.vy <= 0:
            return

        hit_position = (
            self.ball.x
            + self.ball.size / 2
            - (self.paddle.x + self.paddle.width / 2)
        ) / (self.paddle.width / 2)
        self.ball.vy = -abs(self.ball.vy) - 0.4
        self.ball.vx = hit_position * 6 + self.ball.vx * 0.25
        self.ball.y = self.paddle.y - self.ball.size - 1
        self.score += 1
        self.update_score()

    def game_loop(self):
        if not self.running:
            return

        if self.left_pressed:
            self.paddle.move(-1)
        if self.right_pressed:
            self.paddle.move(1)

        self.ball.move()

        if self.ball.x <= 0 or self.ball.x + self.ball.size >= GAME_WIDTH:
            self.ball.x = max(0, min(self.ball.x, GAME_WIDTH - self.ball.size))
            self.ball.vx *= -1

        if self.ball.y <= 0:
            if self.ball.vy < 0:
                self.ball.destroy()
                self.score += 1
                self.update_score()
                self.spawn_ball()
            else:
                self.ball.y = 0
                self.ball.vy = abs(self.ball.vy)

        self.handle_paddle_collision()

        if self.ball.y + self.ball.size >= GAME_HEIGHT:
            self.ball.destroy()
            self.lose_life()
            if not self.running:
                return

        self.ball.draw()
        self.after_id = self.root.after(FRAME_DELAY, self.game_loop)

    def on_key_press(self, event):
        key = event.keysym.lower()
        if key in ("left", "a"):
            self.left_pressed = True
        elif key in ("right", "d"):
            self.right_pressed = True

    def on_key_release(self, event):
        key = event.keysym.lower()
        if key in ("left", "a"):
            self.left_pressed = False
        elif key in ("right", "d"):
            self.right_pressed = False


if __name__ == "__main__":
    root = tk.Tk()
    PingPongGame(root)
    root.mainloop()
