from vehicle import Vehicle

class Truck(Vehicle):
    def __init__(self, capacity, color):
        super().__init__(capacity)
        if isinstance(color, str):
            self.color = color
        else:
            raise TypeError("Цвет должен быть строкой")

