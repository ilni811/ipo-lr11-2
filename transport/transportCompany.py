from transport.client import Client
from transport.vehicle import Ship, Truck

class TransportCompany:
    def __init__(self, name):
        self.name = name
        self.vehicles = []
        self.clients = []

    def add_vehicle(self, vehicle):
        self.vehicles.append(vehicle)

    def add_client(self, client):
        self.clients.append(client)

    def list_vehicles(self):
        return [str(vehicle) for vehicle in self.vehicles]

    def list_clients(self):
        vip_clients = [client for client in self.clients if client.is_vip]
        prostclients = [client for client in self.clients if not client.is_vip]
        return vip_clients, prostclients

    def optimize_cargo_distribution(self):
        # Сортируем клиентов: VIP клиенты в первую очередь
        sorted_clients = sorted(self.clients, key=lambda c: not c.is_vip)

        # Распределяем грузы по транспортным средствам
        for client in sorted_clients:
            for vehicle in self.vehicles:
                try:
                    vehicle.load_cargo(client)
                    break
                except ValueError:
                    continue

    def __str__(self):
        return f"Transport Company: {self.name}, Vehicles: {len(self.vehicles)}, Clients: {len(self.clients)}"
