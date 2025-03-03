import tkinter as tk
from tkinter import ttk, messagebox

class Player:
    def __init__(self, name, x, y, color, keys):
        self.name = name
        self.x = x
        self.y = y
        self.color = color
        self.keys = keys
        self.size = 40
        self.speed = 5
        self.direction = "right"
        self.health = 100
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
        self._create_start_dialog()

    def start_game(self):
        print("Zahajuji hru...")

    def _create_start_dialog(self):
        self.start_dialog = tk.Toplevel(self)
        self.start_dialog.title("Zadej jména hráčů")

        ttk.Label(self.start_dialog, text="Hráč 1 (WASD):").grid(row=0, padx=10, pady=5)
        self.p1_entry = ttk.Entry(self.start_dialog)
        self.p1_entry.grid(row=0, column=1, padx=10, pady=5)

        ttk.Label(self.start_dialog, text="Hráč 2 (šipky):").grid(row=1, padx=10, pady=5)
        self.p2_entry = ttk.Entry(self.start_dialog)
        self.p2_entry.grid(row=1, column=1, padx=10, pady=5)

        ttk.Button(self.start_dialog, text="Start hry", command=self.start_game).grid(row=2, columnspan=2, pady=10)
