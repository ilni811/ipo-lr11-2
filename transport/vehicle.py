from transport.client import Client
import random

class Vehicle:
    def __init__(self, capacity):
        self.vehicle_id = str(random.randint(1000, 100000))
        self.capacity = capacity
        self.current_load = 0
        self.clients_list = []

    def load_cargo(self, client):
        if not isinstance(client.cargo_weight, (int, float)) or client.cargo_weight <= 0:
            raise ValueError("Вес груза клиента должен быть положительным числом!")
        if self.current_load + client.cargo_weight > self.capacity:
            raise ValueError("Загрузка этого груза превысит грузоподъемность транспорта")
        self.current_load += client.cargo_weight
        self.clients_list.append(client)

    def __str__(self):
        return (f"ID транспорта: {self.vehicle_id}, Грузоподъёмность: {self.capacity} "
                f"Текущая загрузка: {self.current_load}")

class Ship(Vehicle):
    def __init__(self, capacity, name):
        super().__init__(capacity)
        self.name = name

    def __str__(self):
        return (f"Ship Name: {self.name}, ID: {self.vehicle_id}, "
                f"Capacity: {self.capacity} tons, Current Load: {self.current_load} tons")

class Truck(Vehicle):
    def __init__(self, capacity, color):
        super().__init__(capacity)
        self.color = color

    def __str__(self):
        return (f"Truck Color: {self.color}, ID: {self.vehicle_id}, "
                f"Capacity: {self.capacity} tons, Current Load: {self.current_load} tons")
