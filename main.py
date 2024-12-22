from transport.client import Client
from transport.vehicle import Ship, Truck
from transport.transportCompany import TransportCompany

def menu():
    company = TransportCompany("Компания")

    while True:
        print("\nВыберете пункт действия:")
        print("1. Добавить клиента")
        print("2. Добавить транспортное средство")
        print("3. Показать все транспортные средства")
        print("4. Показать всех клиентов")
        print("5. Распределить грузы")
        print("6. Показать результат распределения")
        print("7. Выйти из программы")

        res = input("\nВыберите пункт из предложенного списка: ")

        if res == "1":
            name = input("Введите имя клиента:")
            weight = input("Введите вес груза:")
            try:
                weight = float(weight)
            except ValueError:
                print("Ошибка! Вес вводится числом")
            else:
                while True:
                 is_vip_input = input("Клиент VIP? (Да/Нет):").strip().lower()
                 if is_vip_input == 'да':
                     is_vip = True
                     break
                 elif is_vip_input == 'нет':
                      is_vip = False
                      break
                 else:
                     print("Ошибка! Введите 'Да' или 'Нет'")
                
                company.add_client(Client(name, weight, is_vip))
                print("Клиент добавлен")

        elif res == "2":
            type_vehicle = input("Выберите вид транспорта (1-корабль, 2-грузовик):")
            capacity = input("Введите грузоподъёмность:")
            try:
                capacity = float(capacity)
            except ValueError:
                print("Ошибка! Грузоподъемность вводится числом")
            else:
                if type_vehicle == "1":
                    name = input("Введите название судна:")
                    company.add_vehicle(Ship(capacity, name))
                    print("Судно добавлено")

                elif type_vehicle == "2":
                    color = input("Введите цвет грузовика:")
                    company.add_vehicle(Truck(capacity, color))
                    print("Грузовик добавлен")
                else:
                    print("Введен неправильный тип транспорта")

        elif res == "3":
            print("\nТранспортные средства:")
            for transport in company.list_vehicles():
                print(transport)

        elif res == "4":
            vip_clients, prostclients = company.list_clients()
            print("VIP клиенты:")
            for client in vip_clients:
                print(f" Клиент: {client.name}, Вес груза: {client.cargo_weight}")
            print("Обычные клиенты:")
            for client in prostclients:
                print(f" Клиент: {client.name}, Вес груза: {client.cargo_weight}")

        elif res == "5":
            company.optimize_cargo_distribution()
            print("Грузы успешно распределены!")

        elif res == "6":
            print("\nРезультат распределения груза:")
            for vehicle in company.vehicles:
                print(vehicle)
                for client in vehicle.clients_list:
                    print(f"  Клиент: {client.name}, Вес груза: {client.cargo_weight}, VIP: {client.is_vip}")

        elif res == "7":
            print("Завершение программы")
            break

        else:
            print("Неправильный выбор, попробуйте снова")


print(menu())
