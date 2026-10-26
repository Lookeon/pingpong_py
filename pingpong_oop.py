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
        self.item = canvas.create_rectangle(
            self.x,
            self.y,
            self.x + self.width,
            self.y + self.height,
            fill="#22c55e",
            outline="#16a34a",
            width=2,
        )

    def move_to(self, x):
        self.x = max(0, min(x, GAME_WIDTH - self.width))
        self.canvas.coords(
            self.item,
            self.x,
            self.y,
            self.x + self.width,
            self.y + self.height,
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
        self.item = canvas.create_oval(
            self.x,
            self.y,
            self.x + self.size,
            self.y + self.size,
            fill="#fbbf24",
            outline="#d97706",
            width=2,
        )

    def move(self):
        self.x += self.vx
        self.y += self.vy

    def draw(self):
        self.canvas.coords(
            self.item,
            self.x,
            self.y,
            self.x + self.size,
            self.y + self.size,
        )

    def destroy(self):
        self.canvas.delete(self.item)


class PingPongGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Ping Pong OOP")
        self.root.resizable(False, False)
        self.root.configure(bg="#111827")

        self.canvas = tk.Canvas(
            root,
            width=GAME_WIDTH,
            height=GAME_HEIGHT,
            bg="#111827",
            highlightthickness=4,
            highlightbackground="#38bdf8",
        )
        self.canvas.pack(padx=12, pady=(12, 0))

        self.score_label = tk.Label(
            root,
            text="",
            font=("Arial", 18, "bold"),
            fg="white",
            bg="#111827",
        )
        self.score_label.pack(pady=10)

        self.restart_button = tk.Button(
            root,
            text="Jogar novamente",
            command=self.reset_game,
            bg="#f59e0b",
            fg="#111827",
            font=("Arial", 12, "bold"),
            padx=14,
            pady=6,
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
        self.paddle = Paddle(self.canvas)
        self.ball = Ball(self.canvas, self.score)

        # Recreate the embedded button because clearing the canvas removes its window.
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
            text=f"Pontuação: {self.score} | Vidas: {self.lives}"
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
            0,
            0,
            GAME_WIDTH,
            GAME_HEIGHT,
            fill="#0f172a",
            stipple="gray50",
            outline="",
            tags="game_over",
        )
        self.canvas.create_text(
            GAME_WIDTH / 2,
            GAME_HEIGHT / 2 - 35,
            text="Fim de jogo",
            fill="#f8fafc",
            font=("Arial", 30, "bold"),
            tags="game_over",
        )
        self.canvas.create_text(
            GAME_WIDTH / 2,
            GAME_HEIGHT / 2 + 5,
            text=f"Pontuação final: {self.score}",
            fill="white",
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
