import tkinter as tk
from tkinter import ttk, messagebox
from math import sqrt

class Player:
    def __init__(self, name, x, y, color, keys):
        self.name = name
        self.start_x = x
        self.start_y = y
        self.x = x
        self.y = y
        self.color = color
        self.keys = keys
        self.size = 40
        self.speed = 5
        self.direction = "right"
        self.health = 100
        self.lives = 3
        self.can_shoot = True

class Projectile:
    def __init__(self, x, y, color, direction):
        self.x = x
        self.y = y
        self.color = color
        self.direction = direction
        self.speed = 10
        self.size = 5

class GameApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Dvouhráčová střílečka")
        self.geometry("800x600")
        self.players = []
        self.projectiles = []
        self.game_active = False
        self.pressed_keys = set()
        self.canvas = tk.Canvas(self, bg="lightgray")
        self.canvas.pack(fill=tk.BOTH, expand=True)
        self._create_start_dialog()

    def _draw_players(self):
        self.canvas.delete("all")
        for index, p in enumerate(self.players):
            self.canvas.create_rectangle(
                p.x - p.size//2, p.y - p.size//2,
                p.x + p.size//2, p.y + p.size//2,
                fill=p.color
            )
            self.canvas.create_rectangle(
                p.x - p.size//2, p.y - p.size//2 - 20,
                p.x + p.size//2, p.y - p.size//2 - 15,
                fill="gray"
            )
            self.canvas.create_rectangle(
                p.x - p.size//2, p.y - p.size//2 - 20,
                p.x - p.size//2 + (p.health // 2), p.y - p.size//2 - 15,
                fill="green"
            )
            self.canvas.create_text(
                p.x, p.y - p.size//2 - 30,
                text=f"Životy: {p.lives}",
                font=("Arial", 12),
                fill="black"
            )
        for proj in self.projectiles:
            self.canvas.create_oval(
                proj.x - proj.size, proj.y - proj.size,
                proj.x + proj.size, proj.y + proj.size,
                fill=proj.color
            )
        self.canvas.create_text(400, 50, text="Hra spuštěna", font=("Arial", 24), fill="black")

    def _bind_controls(self):
        self.bind("<KeyPress>", self.key_down)
        self.bind("<KeyRelease>", self.key_up)

    def start_game(self):
        p1_name = self.p1_entry.get() or "Hráč 1"
        p2_name = self.p2_entry.get() or "Hráč 2"
        self.start_dialog.destroy()
        self.players.append(Player(
            p1_name, 100, 300, "blue",
            {'left': 'a', 'right': 'd', 'up': 'w', 'down': 's', 'shoot': 'space'}
        ))
        self.players.append(Player(
            p2_name, 700, 300, "red",
            {'left': 'Left', 'right': 'Right', 'up': 'Up', 'down': 'Down', 'shoot': 'Return'}
        ))
        self._draw_players()
        self._bind_controls()
        self.game_active = True
        self.game_loop()

    def _create_start_dialog(self):
        self.start_dialog = tk.Toplevel(self)
        self.start_dialog.title("Zadej jména hráčů")
        self.start_dialog.geometry("300x150")
        self.start_dialog.transient(self)
        self.start_dialog.grab_set()
        ttk.Label(self.start_dialog, text="Hráč 1 (WASD):").grid(row=0, padx=10, pady=5)
        self.p1_entry = ttk.Entry(self.start_dialog)
        self.p1_entry.grid(row=0, column=1, padx=10, pady=5)
        ttk.Label(self.start_dialog, text="Hráč 2 (šipky):").grid(row=1, padx=10, pady=5)
        self.p2_entry = ttk.Entry(self.start_dialog)
        self.p2_entry.grid(row=1, column=1, padx=10, pady=5)
        ttk.Button(self.start_dialog, text="Start hry", command=self.start_game).grid(row=2, columnspan=2, pady=10)

    def key_down(self, event):
        self.pressed_keys.add(event.keysym)

    def key_up(self, event):
        if event.keysym in self.pressed_keys:
            self.pressed_keys.remove(event.keysym)
        for p in self.players:
            if event.keysym == p.keys['shoot']:
                p.can_shoot = True

    def shoot(self, shooter):
        directions = {
            "left": (-1, 0),
            "right": (1, 0),
            "up": (0, -1),
            "down": (0, 1)
        }
        dx, dy = directions[shooter.direction]
        proj = Projectile(
            shooter.x + dx * (shooter.size // 2),
            shooter.y + dy * (shooter.size // 2),
            shooter.color,
            shooter.direction
        )
        self.projectiles.append(proj)

    def check_collision(self, projectile):
        for p in self.players:
            if p.color != projectile.color:
                distance = sqrt((p.x - projectile.x) ** 2 + (p.y - projectile.y) ** 2)
                if distance < p.size // 2 + projectile.size:
                    return p
        return None

    def game_loop(self):
        if not self.game_active:
            return
        for p in self.players:
            if p.keys['left'] in self.pressed_keys:
                p.x -= p.speed
                p.direction = "left"
            if p.keys['right'] in self.pressed_keys:
                p.x += p.speed
                p.direction = "right"
            if p.keys['up'] in self.pressed_keys:
                p.y -= p.speed
                p.direction = "up"
            if p.keys['down'] in self.pressed_keys:
                p.y += p.speed
                p.direction = "down"
            if p.keys['shoot'] in self.pressed_keys:
                if p.can_shoot:
                    self.shoot(p)
                    p.can_shoot = False
            else:
                p.can_shoot = True
            p.x = max(p.size // 2, min(p.x, 800 - p.size // 2))
            p.y = max(p.size // 2, min(p.y, 600 - p.size // 2))
        for proj in self.projectiles[:]:
            directions = {
                "left": (-1, 0),
                "right": (1, 0),
                "up": (0, -1),
                "down": (0, 1)
            }
            dx, dy = directions[proj.direction]
            proj.x += dx * proj.speed
            proj.y += dy * proj.speed
            hit_player = self.check_collision(proj)
            if hit_player:
                hit_player.health -= 10
                self.projectiles.remove(proj)
                if hit_player.health <= 0:
                    hit_player.lives -= 1
                    if hit_player.lives <= 0:
                        self.game_over(hit_player)
                        return
                    else:
                        hit_player.health = 100
                        hit_player.x = hit_player.start_x
                        hit_player.y = hit_player.start_y
            if proj.x < 0 or proj.x > 800 or proj.y < 0 or proj.y > 600:
                if proj in self.projectiles:
                    self.projectiles.remove(proj)
        self._draw_players()
        self.after(30, self.game_loop)

    def game_over(self, loser):
        self.game_active = False
        winner = next(p for p in self.players if p != loser)
        messagebox.showinfo("Konec hry", f"{winner.name} vyhrává!")
        self.destroy()

