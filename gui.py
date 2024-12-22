import tkinter as tk # Импортируем библиотеку tkinter как tk для удобства
import json # Импортируем модуль json для работы с JSON-данными
import csv # Импортируем модуль csv для работы с CSV-файлами
from tkinter import messagebox, ttk # Импортируем messagebox для отображения сообщений и ttk для использования виджетов с темами
from transport.client import Client # Импортируем класс Client из модуля transport.Client
from transport.truck import Truck # Импортируем класс Truck из модуля transport.Truck
from transport.ship import Ship # Импортируем класс Ship из модуля transport.Ship
from transport.transportCompany import TransportCompany # Импортируем класс TransportCompany из модуля transport.TransportCompany

class TransportCompanyApp: # Класс TransportCompanyApp, который представляет приложение транспортной компании
    def __init__(self, root): # Метод инициализации класса, принимающий главное окно
        self.root = root # Сохраняем ссылку на него
        self.root.title("Транспортная Компания Экспресс") # Устанавливаем заголовок
        self.root.geometry("820x595") # Устанавливаем размеры окна
        self.root.resizable(width=False, height=False) # Запрещаем изменение размеров окна
        self.root.configure(bg="white") # Устанавливаем белый цвет фона окна

        self.company = TransportCompany("Транспортная Компания") # Экземпляр класса TransportCompany с заданным именем
        self.clients_data = self.load_data_from_json_clients() # Загружаем данные клиентов из JSON-файла
        self.vehicles_data = self.load_data_from_json_vehicles() # Загружаем данные о транспортных средствах из JSON-файла
        self.load_clients() # Загружаем клиентов в приложение
        self.load_vehicles() # Загружаем транспортные средства в приложение

    def load_data_from_json_clients(self): # Метод для загрузки данных клиентов из JSON-файла
        try:
            with open("dump_clients.json", "r", encoding="utf-8") as file:
                return json.load(file)
        except FileNotFoundError:
            return []

    def load_data_from_json_vehicles(self): # Метод для загрузки данных о транспортных средствах из JSON-файла
        try:
            with open("dump_vehicles.json", "r", encoding="utf-8") as file:
                vehicles_data = json.load(file)
                for vehicle_data in vehicles_data:
                    if vehicle_data['type'] == 'Грузовик':
                        vehicle = Truck(capacity=vehicle_data['capacity'], color=vehicle_data['color'])
                    elif vehicle_data['type'] == 'Судно':
                        vehicle = Ship(capacity=vehicle_data['capacity'], name_shap=vehicle_data['number_of_cars'])
                    else:
                        continue
                    self.company.add_vehicle(vehicle)
        except FileNotFoundError:
            return []

    def save_data_to_json_clients(self, data): # Метод для сохранения данных клиентов в JSON-файл
        data_to_save = [client.to_dict() for client in data] # Преобразуем каждый объект клиента в словарь с помощью метода to_dict() и сохраняем в список
        with open("dump_clients.json", "w", encoding="utf-8") as file:
            json.dump(data_to_save, file, indent=4)

    def save_data_to_json_vehicles(self, vehicles_data): # Метод для сохранения данных о транспортных средствах в JSON-файл
        vehicles_data_to_save = [] 
        for vehicle in vehicles_data:
            if isinstance(vehicle, Truck):
                vehicles_data_to_save.append({
                    'type': 'Грузовик',
                    'capacity': vehicle.capacity,
                    'color': vehicle.color
                })
            elif isinstance(vehicle, Ship):
                vehicles_data_to_save.append({
                    'type': 'Судно',
                    'capacity': vehicle.capacity,
                    'name_ship': vehicle.name_ship
                })
        with open("dump_vehicles.json", "w", encoding="utf-8") as file:
            json.dump(vehicles_data_to_save, file, indent=4)

    def load_clients(self): # Метод для загрузки клиентов
        if isinstance(self.clients_data, list): # Проверяем, что загруженные данные клиентов являются списком
            for client_dict in self.clients_data: # Перебираем каждый словарь с данными клиента
                try:
                    client = Client(client_dict['name'], client_dict['cargo_weight'], client_dict['is_vip']) # Создаем объект клиента с данными из словаря и добавляем его в компанию
                    self.company.add_client(client)  # Добавляем клиента в компанию
                except ValueError as e:
                    print(f"Ошибка при загрузке клиента: {e}")

    def load_vehicles(self): # Метод для загрузки транспортных средств
        if isinstance(self.vehicles_data, list):
            for vehicle_dict in self.vehicles_data:
                try:
                    if vehicle_dict['type'] == 'Грузовик': # проверяем, является ли тип транспортного средства "Грузовик"
                        vehicle = Truck(vehicle_dict['capacity'], vehicle_dict['color'])
                    elif vehicle_dict['type'] == 'Судно': # проверяем, является ли тип транспортного средства "Судно"
                        vehicle = Ship(vehicle_dict['capacity'], vehicle_dict['name_ship'])
                    self.company.add_vehicle(vehicle) # Добавляем созданное транспортное средство в компанию
                except ValueError as e:
                    print(f"Ошибка при загрузке транспортного средства: {e}")

        self.setup_ui() # Вызываем метод для настройки пользовательского интерфейса

    def setup_ui(self):
        frame1 = tk.Frame(self.root, bg='gray15')
        frame1.place(relx=0.25, rely=0.26, relwidth=0.5, relheight=0.5)

        frame2 = tk.Frame(self.root, bg='gray15')
        frame2.place(relx=0.08, rely=0.029, relwidth=0.85, relheight=0.2)

        info_text1 = """
        Добро пожаловать на страничку транспортной
        компании 82TP!"""
        main_label = tk.Label(self.root, text=info_text1, font=("Arial", 17, 'bold'), fg="white", bg="gray15")
        main_label.place(relx=0.5, rely=0.1, anchor=tk.CENTER)

        info_text2 = """
        Вы можете как просматривать списки уже 
        существующих клиентов, транспортных 
        средств, так и регистрировать их со всеми 
        параметрами. Также наша компания 
        предоставляет возможность распределять 
        груз по транспортным средствам. 

        Чтобы груз клиента распределялся в 
        первоочередном порядке, клиенту нужен 
        VIP-статус."""
        info_label = tk.Label(self.root, text=info_text2, font=("Arial", 12), fg="white", bg="gray15")
        info_label.place(relx=0.487, rely=0.5, anchor=tk.CENTER)

        btn_open_clients = tk.Button(self.root, text="Добавить клиента", width=35, height=5, bg="black", fg="white", command=self.open_new_clientsworkwindow)
        btn_open_clients.place(x=130, y=470)

        btn_open_vehicles = tk.Button(self.root, text="Добавить транспорт", width=35, height=5, bg="black", fg="white", command=self.open_new_vehidesworkwindow)
        btn_open_vehicles.place(x=450, y=470)

        btn_open_cargo = tk.Button(self.root, text="Распределить грузы", width=23, height=5, bg="black", fg="white", command=self.open_new_cargo_distribution)
        btn_open_cargo.pack(side=tk.LEFT, padx=10, pady=10)

        btn_exit = tk.Button(self.root, text="Выйти из программы", width=23, height=5, bg="black", fg="white", command=self.root.quit)
        btn_exit.pack(side=tk.RIGHT, padx=10, pady=10)

        self.status = tk.Label(self.root, text='', bg='white', fg='black')
        self.status.place(relx=0.5, rely=0.985, anchor=tk.CENTER)

        self.setup_menu() # Вызываем метод для настройки меню приложения

    def setup_menu(self): # Метод для создания меню приложения
        menubar = tk.Menu(self.root) # Создаем объект меню, привязанный к главному окну
        export_menu = tk.Menu(menubar, tearoff=0) # Создаем подменю для экспорта, отключая возможность "отрыва" меню
        export_menu.add_command(label="Экспорт результата", command=self.export_results) # Добавляем команду для экспорта результатов
        export_menu.add_separator() # Добавляем разделитель в меню
        export_menu.add_command(label="О программе", command=self.show_about) # Добавляем команду для отображения информации о программе
        menubar.add_cascade(label="Меню", menu=export_menu) # Добавляем подменю в главное меню
        self.root.config(menu=menubar) # Настраиваем главный экран для использования созданного меню

    def export_results(self): # Метод для экспорта результатов распределения грузов в CSV файл
        filename = "cargo_distribution_results.csv" # Устанавливаем имя файла для сохранения результатов
        
        try:
            with open(filename, mode='w', newline='', encoding='utf-8') as file: # Открываем файл для записи, создавая его, если он не существует
                writer = csv.writer(file) # Создаем объект writer для записи в CSV файл
                writer.writerow(["Тип транспорта", "Грузоподъемность", "Загруженные клиенты"]) # Записываем заголовки столбцов

                for vehicle in self.company.vehicles: # Проходим по всем транспортным средствам в компании
                    writer.writerow([type(vehicle).__name__, vehicle.capacity, # Записываем тип транспорта, грузоподъемность и список загруженных клиентов
                                     ', '.join([client.name for client in vehicle.clients_list]) if vehicle.clients_list else "Нет загруженных клиентов"])
            
            messagebox.showinfo("Экспорт результата", f"Результаты успешно экспортированы в файл: {filename}") # Выводим сообщение об успешном экспорте результатов
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось экспортировать результаты: {e}")

    def show_about(self): # Метод для отображения информации о программе
        messagebox.showinfo("О программе", "Транспортная Компания 82TP\nЛабораторная работа №12\nВариант 2\nВыполнили: Company:82TP(Ромчик легенда, Соня вистери, Синигуб Максим, AI Copilot и бездарь(я))")

    def open_new_clientsworkwindow(self): # Для открытия нового окна работы с клиентами
        self.root.withdraw() # Скрываем главное окно приложения
        new_window = tk.Toplevel(self.root) # Создаем новое верхнее окно
        new_window.title("Действия с клиентами")
        new_window.geometry("820x595")
        new_window.resizable(width=False, height=False)
        new_window.configure(bg="white")

        self.frame = tk.Frame(new_window, bg="white")
        self.frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        self.client_table = ttk.Treeview(self.frame, columns=("Имя", "Вес", "VIP"), show='headings') # Создаем таблицу для отображения клиентов с колонками "Имя", "Вес" и "VIP статус"
        self.client_table.heading("Имя", text="Имя клиента")
        self.client_table.heading("Вес", text="Вес груза")
        self.client_table.heading("VIP", text="VIP статус")
        self.client_table.pack(side=tk.BOTTOM, fill=tk.X, padx=10, pady=10)

        frame3 = tk.Frame(new_window, bg='gray15')
        frame3.place(relx=0.08, rely=0.029, relwidth=0.85, relheight=0.2)

        info_text3 = """
        Какую именно операцию Вы бы хотели 
        совершить?"""
        main_label = tk.Label(new_window, text=info_text3, font=("Arial", 16, 'bold'), fg="white", bg="gray15")
        main_label.place(relx=0.5, rely=0.1, anchor=tk.CENTER)

        btn_add_client = tk.Button(new_window, text="Добавить клиента", width=35, height=3, bg="black", fg="white", command=self.add_client)
        btn_add_client.place(x=150, y=180)

        btn_delete_client = tk.Button(new_window, text="Удалить клиента", width=35, height=3, bg="black", fg="white", command=self.delete_client)
        btn_delete_client.place(x=300, y=250)

        btn_return = tk.Button(new_window, text="Назад", width=35, height=3, bg="black", fg="white", command=lambda: self.close_new_window(new_window))
        btn_return.place(x=450, y=180)

        self.load_clients_to_table()

    def load_clients_to_table(self): # Метод для загрузки клиентов в таблицу
        self.client_table.delete(*self.client_table.get_children()) # Очищаем таблицу перед загрузкой новых данных
        for client in self.company.clients: # Перебираем всех клиентов в компании
            self.client_table.insert("", "end", values=(client.name, client.cargo_weight, "Да" if client.is_vip else "Нет"))
        self.client_table.bind("<Double-1>", self.edit_client) # Двойной щелчок для редактирования клиента

    def add_client(self): # Метод для добавления нового клиента
        self.client_window = tk.Toplevel(self.root) # Создаем новое верхнее окно для ввода данных клиента
        self.client_window.title("Добавить клиента")
        
        tk.Label(self.client_window, text="Имя клиента:").grid(row=0, column=0)
        self.client_name_entry = tk.Entry(self.client_window)
        self.client_name_entry.grid(row=0, column=1)

        tk.Label(self.client_window, text="Вес груза:").grid(row=1, column=0)
        self.client_weight_entry = tk.Entry(self.client_window)
        self.client_weight_entry.grid(row=1, column=1)

        tk.Label(self.client_window, text="VIP статус:").grid(row=2, column=0)
        self.client_vip_var = tk.BooleanVar() # Создаем переменную для хранения состояния VIP статуса
        self.client_vip_check = tk.Checkbutton(self.client_window, variable=self.client_vip_var) # Создаем чекбокс для выбора VIP статуса
        self.client_vip_check.grid(row=2, column=1)

        tk.Button(self.client_window, text="Сохранить", command=self.save_client).grid(row=4, column=0, columnspan=1)  
        tk.Button(self.client_window, text="Отмена", command=self.client_window.destroy).grid(row=4, column=1, columnspan=2)  

    def save_client(self): # Метод для сохранения данных нового клиента 
        name = self.client_name_entry.get() # Получаем имя клиента из поля ввода 
        weight = self.client_weight_entry.get() # Получаем вес груза из поля ввода 
        vip_status = self.client_vip_var.get() # Получаем состояние VIP статуса 

        if not name.isalpha() or len(name) < 2: # Проверяем, что имя состоит только из букв и длина не менее 2
            tk.messagebox.showerror("Ошибка", "Имя клиента должно содержать только буквы и быть не менее 2 символов.")
            return

        try:
            weight = float(weight) # Пробуем преобразовать вес в число
            if weight <= 0 or weight > 10000: # Проверяем, что вес положительный и не превышает 10000
                tk.messagebox.showerror("Ошибка", "Вес груза должен быть положительным числом и не более 10000 кг.")
                return
        except ValueError:
            tk.messagebox.showerror("Ошибка", "Вес груза должен быть числом.")
            return

        client = Client(name, weight, vip_status) # Создаем объект клиента с введенными данными 
        self.company.add_client(client) # Добавляем клиента в компанию 

        self.client_table.insert("", "end", values=(name, weight, "Да" if vip_status else "Нет")) # Вставляем данные клиента в таблицу 
        self.save_data_to_json_clients(self.company.clients) 

        self.client_window.destroy() # Закрываем окно добавления клиента 
        self.status.config(text="Клиент добавлен") # Обновляем статус с сообщением о добавлении клиента 

    def edit_client(self, event): # Метод для редактирования выбранного клиента
        selected_item = self.client_table.selection() # Получаем выбранный элемент из таблицы клиентов
        if not selected_item: # Если ничего не выбрано, выходим из метода
            return

        client_data = self.client_table.item(selected_item)['values'] # Получаем данные выбранного клиента
        self.client_window = tk.Toplevel(self.root) # Создаем новое окно для редактирования клиента
        self.client_window.title("Редактировать клиента") # Устанавливаем заголовок нового окна

        tk.Label(self.client_window, text="Имя клиента:").grid(row=0, column=0) # Создаем метку для имени клиента
        self.client_name_entry = tk.Entry(self.client_window) # Создаем поле ввода для имени клиента
        self.client_name_entry.insert(0, client_data[0]) # Заполняем поле ввода текущим именем клиента
        self.client_name_entry.grid(row=0, column=1) # Устанавливаем положение поля ввода

        tk.Label(self.client_window, text="Вес груза:").grid(row=1, column=0) # Создаем метку для веса груза
        self.client_weight_entry = tk.Entry(self.client_window) # Создаем поле ввода для веса груза
        self.client_weight_entry.insert(0, client_data[1]) # Заполняем поле ввода текущим весом груза
        self.client_weight_entry.grid(row=1, column=1) # Устанавливаем положение поля ввода

        tk.Label(self.client_window, text="VIP статус:").grid(row=2, column=0) # Создаем метку для выбора VIP статуса
        self.client_vip_var = tk.BooleanVar(value=(client_data[2] == "Да")) # Устанавливаем состояние VIP статуса
        self.client_vip_check = tk.Checkbutton(self.client_window, variable=self.client_vip_var) # Создаем чекбокс для выбора VIP статуса
        self.client_vip_check.grid(row=2, column=1)

        tk.Button(self.client_window, text="Сохранить", command=lambda: self.save_edited_client(client_data[0])).grid(row=4, column=0, columnspan=1) # Создаем кнопку "Сохранить" для сохранения изменений клиента
        tk.Button(self.client_window, text="Отмена", command=self.client_window.destroy).grid(row=4, column=1, columnspan=2) # Создаем кнопку "Отмена" для закрытия окна без сохранения

    def delete_client(self): # Метод для удаления выбранного клиента
        selected_item = self.client_table.selection() # Получаем выбранный элемент из таблицы клиентов
        if not selected_item: # Если ничего не выбрано, выводим предупреждение
            tk.messagebox.showwarning("Предупреждение", "Пожалуйста, выберите клиента для удаления.")
            return

        client_name = self.client_table.item(selected_item)['values'][0] # Получаем имя клиента для удаления
        self.company.clients = [client for client in self.company.clients if client.name != client_name] # Удаляем клиента из списка клиентов компании 
        self.load_clients_to_table() # Обновляем таблицу клиентов
        self.save_data_to_json_clients(self.company.clients) # Сохраняем обновленный список клиентов в JSON файл
        self.status.config(text="Клиент удален") # Обновляем статус с сообщением о удалении клиента

    def save_edited_client(self, old_name): # Метод для сохранения изменений клиента
        name = self.client_name_entry.get() # Получаем новое имя клиента из поля ввода
        weight = self.client_weight_entry.get() # Получаем новый вес груза из поля ввода
        vip_status = self.client_vip_var.get() # получаем новое состояние VIP статуса

        if not name.isalpha() or len(name) < 2: # Проверяем, что имя состоит только из букв и длина не менее 2
            tk.messagebox.showerror("Ошибка", "Имя клиента должно содержать только буквы и быть не менее 2 символов.")
            return

        try:
            weight = float(weight) # Пробуем преобразовать вес в число
            if weight <= 0 or weight > 10000: # Проверяем, что вес положительный и не превышает 10000
                tk.messagebox.showerror("Ошибка", "Вес груза должен быть положительным числом и не более 10000 кг.")
                return
        except ValueError:
            tk.messagebox.showerror("Ошибка", "Вес груза должен быть числом.")
            return

        for client in self.company.clients: # Перебираем список клиентов компании для обновления данных
            if client.name == old_name: # Если имя клиента совпадает с именем редактируемого клиента
                client.name = name # Обновляем имя клиента
                client.cargo_weight = float(weight) # Обновляем вес груза клиента
                client.is_vip = vip_status # Обновляем статус VIP клиента
                break

        self.load_clients_to_table() # Рбновляем таблицу клиентов для отображения измененных данных
        self.save_data_to_json_clients(self.company.clients) # Сохраняем обновленный список клиентов в JSON файл
        self.client_window.destroy() # Закрываем окно редактирования клиента
        self.status.config(text="Данные клиента обновлены") # Обновляем статус с сообщением об успешном обновлении данных клиента

    def open_new_vehidesworkwindow(self): # Метод для открытия окна работы с транспортными средствами
        self.root.withdraw() # Скрываем главное окно приложения
        new_window = tk.Toplevel(self.root) # Создаем новое верхнее окно для работы с транспортом
        new_window.title("Действия с транспортными средствами")
        new_window.geometry("820x595")
        new_window.resizable(width=False, height=False)
        new_window.configure(bg="white")

        self.frame = tk.Frame(new_window, bg="white")
        self.frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        self.transport_table = ttk.Treeview(self.frame, columns=("ID", "Тип", "Грузоподъемность"), show='headings') # Создаем таблицу для отображения транспортных средств с указанными столбиками
        self.transport_table.heading("ID", text="ID")
        self.transport_table.heading("Тип", text="Тип транспорта")
        self.transport_table.heading("Грузоподъемность", text="Грузоподъемность")
        self.transport_table.pack(side=tk.BOTTOM, fill=tk.X, padx=10, pady=10)

        frame4 = tk.Frame(new_window, bg='gray15')
        frame4.place(relx=0.08, rely=0.029, relwidth=0.85, relheight=0.2)

        info_text4 = """
        Какую именно операцию Вы бы хотели 
        совершить?"""
        main_label = tk.Label(new_window, text=info_text4, font=("Arial", 16, 'bold'), fg="white", bg="gray15")
        main_label.place(relx=0.5, rely=0.1, anchor=tk.CENTER)

        btn_add_vehicle = tk.Button(new_window, text="Добавить транспорт", width=35, height=3, bg="black", fg="white", command=self.add_vehicle)
        btn_add_vehicle.place(x=150, y=180)

        btn_delete_vehicle = tk.Button(new_window, text="Удалить транспорт", width=35, height=3, bg="black", fg="white", command=self.delete_vehicle)
        btn_delete_vehicle.place(x=300, y=250)

        btn_return = tk.Button(new_window, text="Назад", width=35, height=3, bg="black", fg="white", command=lambda: self.close_new_window(new_window))
        btn_return.place(x=450, y=180)

        self.load_transport_table() # Загружаем данные о транспортных средствах в таблицу

    def load_transport_table(self): # Метод для загрузки данных о транспортных средствах в таблицу
        self.transport_table.delete(*self.transport_table.get_children()) # Очищаем таблицу перед загрузкой новых данных
        for vehicle in self.company.vehicles:
            if isinstance(vehicle, Truck):
                self.transport_table.insert("", "end", values=(len(self.transport_table.get_children()) + 1, "Грузовик", vehicle.capacity, vehicle.color))
            elif isinstance(vehicle, Ship):
                self.transport_table.insert("", "end", values=(len(self.transport_table.get_children()) + 1, "Судно", vehicle.capacity, vehicle.name_ship))
        self.transport_table.bind("<Double-1>", self.edit_vehicle) # Двойной щелчок для редактирования транспортного средства

    def add_vehicle(self): # Метод для добавления нового транспортного средства
        self.transport_window = tk.Toplevel(self.root)
        self.transport_window.title("Добавить транспорт")

        tk.Label(self.transport_window, text="Тип транспорта:").grid(row=0, column=0) # Создаем метку для выбора типа транспорта
        self.transport_type = ttk.Combobox(self.transport_window, values=["Грузовик", "Судно"]) # Создаем выпадающий список для выбора типа транспорта
        self.transport_type.grid(row=0, column=1)
        self.transport_type.bind("<<ComboboxSelected>>", self.on_transport_type_selected) # Привязываем обработчик выбора типа транспорта

        tk.Label(self.transport_window, text="Грузоподъемность:").grid(row=1, column=0) # Создаем метку для грузоподъемности
        self.capacity = tk.Entry(self.transport_window) # Создаем поле ввода для грузоподъемности
        self.capacity.grid(row=1, column=1)

        self.color_label = tk.Label(self.transport_window, text="Цвет:") # Создаем метку для цвета
        self.color_label.grid(row=2, column=0)
        self.color_entry = tk.Entry(self.transport_window)
        self.color_entry.grid(row=2, column=1)

        self.cars_label = tk.Label(self.transport_window, text="Название:") # Создаем метку для названия судна
        self.cars_label.grid(row=3, column=0)
        self.cars_entry = tk.Entry(self.transport_window) # Создаем поле ввода для количества вагонов
        self.cars_entry.grid(row=3, column=1) # Устанавливаем положение поля ввода

        tk.Button(self.transport_window, text="Сохранить", command=self.save_transport).grid(row=4, column=0, columnspan=1)  
        tk.Button(self.transport_window, text="Отмена", command=self.transport_window.destroy).grid(row=4, column=1, columnspan=2)  

    def delete_vehicle(self): # Метод для удаления транспортного средства
        selected_item = self.transport_table.selection() # Получаем выбранный элемент из таблицы
        if not selected_item:
            tk.messagebox.showwarning("Предупреждение", "Пожалуйста, выберите транспорт для удаления.")
            return

        vehicle_id = self.transport_table.item(selected_item)['values'][0] # Получаем ID транспортного средства
        self.company.vehicles = [vehicle for vehicle in self.company.vehicles if vehicle.id != vehicle_id] # Удаляем транспорт из списка, оставляя только те, у которых ID не совпадает с выбранным
        self.load_transport_table() # Обновляем таблицу, чтобы отобразить изменения
        self.save_data_to_json_vehicles(self.company.vehicles) # Сохраняем обновленный список транспортных средств в JSON файл
        self.status.config(text="Транспорт удален") # Обновляем статус с сообщением об удалении транспорта

    def on_transport_type_selected(self, event): # Метод для обработки выбора типа транспорта
        transport_type = self.transport_type.get() # Получаем выбранный тип транспорта
        if transport_type == "Судно": # Если выбран судно
            self.color_label.grid_remove() # Скрываем метку и поле ввода для цвета
            self.color_entry.grid_remove() # Скрываем поле ввода для цвета
            self.cars_label.grid() # Показываем метку для количества вагонов
            self.cars_entry.grid() # Показываем поле ввода для количества вагонов
        elif transport_type == "Грузовик": # Если выбран грузовик
            self.cars_label.grid_remove()  # Скрываем метку и поле ввода для количества вагонов
            self.cars_entry.grid_remove()  # скрываем поле ввода для названия судна
            self.color_label.grid() # Показываем метку для цвета
            self.color_entry.grid() # Показываем поле ввода для цвета

    def save_transport(self): # Метод для сохранения нового транспортного средства
        transport_type = self.transport_type.get() # Получаем тип транспорта из выпадающего списка
        capacity = self.capacity.get() # Получаем грузоподъемность из поля ввода
        color = self.color_entry.get() # Получаем цвет из поля ввода
        name_ship = self.cars_entry.get() # Получаем название судна из поля ввода

        try:
            capacity = float(capacity)
            if capacity <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Ошибка", "Грузоподъемность должна быть положительным числом.")
            return

        if transport_type == "Грузовик":
            if color.strip() == "":
                messagebox.showerror("Ошибка", "Цвет не может быть пустым.")
                return
            new_truck = Truck(capacity, color) # Создаем новый объект грузовика с указанной грузоподъемностью и цветом
            self.company.add_vehicle(new_truck) # Добавляем грузовик в компанию
            self.transport_table.insert("", "end", values=(new_truck.id, transport_type, capacity, color)) # Вставляем данные о грузовике в таблицу
        
        elif transport_type == "Судно":
            try:
                name_ship = str(name_ship)
                if not isinstance(name_ship, str) or not name_ship.strip():
                    raise ValueError
            except ValueError:
                messagebox.showerror("Ошибка", "Название вагона должно быть строкой.")
                return
            
            new_ship = Ship(capacity, name_ship)
            self.company.add_vehicle(new_ship)
            self.transport_table.insert("", "end", values=(new_ship.id, transport_type, capacity, name_ship))

        self.save_data_to_json_vehicles(self.company.vehicles) # Сохраняем данные о транспортных средствах в JSON файл
        self.transport_window.destroy() # Закрываем окно добавления транспорта
        self.status.config(text="Транспорт добавлен") # Обновляем статус с сообщением о добавлении транспорта

    def edit_vehicle(self, event): # Метод для редактирования выбранного транспортного средства
        selected_item = self.transport_table.selection() # Получаем выбранный элемент из таблицы
        if not selected_item:
            return

        vehicle_data = self.transport_table.item(selected_item)['values'] # Получаем данные о выбранном транспортном средстве
        self.transport_window = tk.Toplevel(self.root) # Создаем новое окно для редактирования транспорта
        self.transport_window.title("Редактировать транспорт")

        tk.Label(self.transport_window, text="Тип транспорта:").grid(row=0, column=0)
        self.transport_type = ttk.Combobox(self.transport_window, values=["Грузовик", "Судно"])
        self.transport_type.set(vehicle_data[1])
        self.transport_type.grid(row=0, column=1)
        self.transport_type.bind("<<ComboboxSelected>>", self.on_transport_type_selected)

        tk.Label(self.transport_window, text="Грузоподъемность:").grid(row=1, column=0)
        self.capacity = tk.Entry(self.transport_window)
        self.capacity.insert(0, vehicle_data[2])
        self.capacity.grid(row=1, column=1)
        

        self.color_label = tk.Label(self.transport_window, text="Цвет:")
        self.color_label.grid(row=2, column=0)
        self.color_entry = tk.Entry(self.transport_window)
        self.color_entry.insert(0, vehicle_data[3] if len(vehicle_data) > 3 else "")
        self.color_entry.grid(row=2, column=1)

        self.cars_label = tk.Label(self.transport_window, text="Название судна:")
        self.cars_label.grid(row=3, column=0)
        self.cars_entry = tk.Entry(self.transport_window)
        self.cars_entry.insert(0, vehicle_data[4] if len(vehicle_data) > 4 else "")
        self.cars_entry.grid(row=3, column=1)
        self.on_transport_type_selected(None)

        tk.Button(self.transport_window, text="Сохранить", command=lambda: self.save_edited_vehicle(vehicle_data[0])).grid(row=4, column=0, columnspan=1)  
        tk.Button(self.transport_window, text="Отмена", command=self.transport_window.destroy).grid(row=4, column=1, columnspan=2)

    def save_edited_vehicle(self, vehicle_id): # Метод для сохранения изменений в редактируемом транспортном средстве
        transport_type = self.transport_type.get() # Получаем тип транспорта из выпадающего списка
        capacity = self.capacity.get() # Получаем грузоподъемность из поля ввода
        color = self.color_entry.get() # Получаем цвет из поля ввода
        number_of_cars = self.cars_entry.get() # Получаем количество вагонов из поля ввода

        try:
            capacity = float(capacity)
            if capacity <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Ошибка", "Грузоподъемность должна быть положительным числом.")
            return 

        if transport_type == "Грузовик":
            if color.strip() == "":
                messagebox.showerror("Ошибка", "Цвет не может быть пустым.")
                return
            for vehicle in self.company.vehicles:
                if isinstance(vehicle, Truck) and vehicle_id == vehicle_id:
                    vehicle.capacity = capacity
                    vehicle.color = color
                    break
                
        elif transport_type == "Судно":
            try:
                name_ship = str(name_ship)
                if not isinstance(name_ship, str) or not name_ship:
                    raise ValueError
            except ValueError:
                messagebox.showerror("Ошибка", "Название судна должно быть строкой.")
                return
            
            for vehicle in self.company.vehicles:
                if isinstance(vehicle, Ship) and vehicle_id == vehicle_id:
                    vehicle.capacity = capacity
                    vehicle.number_of_cars = name_ship
                    break

        self.load_transport_table() # Обновляем таблицу, перезагружаем ее, чтобы отобразить обновленные данные
        self.save_data_to_json_vehicles(self.company.vehicles) # Сохраняем данные о транспортных средствах в JSON файл
        self.transport_window.destroy() # Закрываем окно редактирования транспорта
        self.status.config(text="Данные транспорта обновлены") # Обновляем статус с сообщением об успешном обновлении данных

    def open_new_cargo_distribution(self): # Метод для открытия окна распределения груза
        self.root.withdraw()
        new_window = tk.Toplevel(self.root)
        new_window.title("Распределение груза")
        new_window.geometry("820x595")

        btn_return = tk.Button(new_window, text="Назад", width=30, height=2, bg="black", fg="white", command=lambda: self.close_new_window(new_window))
        btn_return.pack(pady=20)

        self.result_text = tk.Text(new_window, height=20, width=80)
        self.result_text.pack(pady=10)

        # Проверяем, есть ли клиенты для распределения грузов
        if not self.company.clients and not self.company.vehicles:
            self.result_text.insert(tk.END, "В данный момент нет клиентов и транспортных средств для распределения грузов.\n")
        elif not self.company.clients:  # Если список клиентов пуст
            self.result_text.insert(tk.END, "В данный момент нет клиентов для распределения грузов.\n")
        elif not self.company.vehicles:  # Если список транспортных средств пуст
            self.result_text.insert(tk.END, "В данный момент нет транспортных средств для распределения грузов.\n")
        else:  # Если есть и клиенты, и транспортные средства
            self.company.optimize_cargo_distribution()  # Распределяем груз между транспортными средствами
            self.result_text.insert(tk.END, "Распределение грузов выполнено:\n")
            for vehicle in self.company.vehicles: # Проходим по всем транспортным средствам
                self.result_text.insert(tk.END, f"Транспортное средство: {vehicle}\n")
                if vehicle.clients_list: # Если у транспортного средства есть загруженные клиенты
                    self.result_text.insert(tk.END, "Загруженные клиенты:\n")
                    for client in vehicle.clients_list: # Проходим по списку загруженных клиентов
                        self.result_text.insert(tk.END, f" - Имя: {client.name}, Вес груза: {client.cargo_weight}, VIP-статус: {client.is_vip}\n")
                else: # Если у транспортного средства нет загруженных клиентов
                    self.result_text.insert(tk.END, " - Не загружено ни одного клиента. Не хватает грузоподъемности или все клиенты уже загружены в другие транспортные средства :( \n")

    def close_new_window(self, window): # Метод для закрытия указанного окна
        window.destroy() # Закрываем указанное окно
        self.root.deiconify() # Возвращаем главное окно на передний план (отображаем его)

if __name__ == "__main__": # Проверяем, является ли данный файл основным модулем, который запускается
    root = tk.Tk() # Создаем главное окно приложения
    app = TransportCompanyApp(root) # Создаем экземпляр класса TransportCompanyApp, передавая главное окно в качестве аргумента
    root.mainloop()