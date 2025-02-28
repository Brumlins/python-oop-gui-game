

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
