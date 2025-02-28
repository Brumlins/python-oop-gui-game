import tkinter as tk

class GameApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Dvouhráčová střílečka")
        self.geometry("800x600")

if __name__ == "__main__":
    app = GameApp()
    app.mainloop()