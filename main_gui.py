import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import json
import os
import sys

# Добавляем текущую директорию в путь для импорта
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

# Импортируем наши классы
try:
    from transport.client import Client
    from transport.vehicle import Vehicle
    from transport.van import Van
    from transport.ship import Ship
    from transport.transport_company import TransportCompany
    IMPORT_SUCCESS = True
except ImportError as e:
    print(f"Внимание: {e}")
    print("Используются заглушки для классов")
    IMPORT_SUCCESS = False
    
    # Создаем заглушки для классов
    class Client:
        def __init__(self, name, cargo_weight, is_vip=False):
            self.name = name
            self.cargo_weight = cargo_weight
            self.is_vip = is_vip
        
        def update_cargo_weight(self, weight):
            self.cargo_weight = weight
    
    class Vehicle:
        def __init__(self, capacity):
            self.vehicle_id = f"V{hash(str(capacity)) % 10000:04d}"
            self.capacity = capacity
            self.current_load = 0.0
            self.clients_list = []
        
        def get_current_load_percentage(self):
            return (self.current_load / self.capacity * 100) if self.capacity > 0 else 0
        
        def load_cargo(self, client):
            weight_tons = client.cargo_weight / 1000
            if self.current_load + weight_tons <= self.capacity:
                self.current_load += weight_tons
                self.clients_list.append(client)
                return True
            return False
    
    class Van(Vehicle):
        def __init__(self, capacity, is_refrigerated=False):
            super().__init__(capacity)
            self.is_refrigerated = is_refrigerated
            self.vehicle_type = "Фургон"
    
    class Ship(Vehicle):
        def __init__(self, capacity, name):
            super().__init__(capacity)
            self.name = name
            self.vehicle_type = "Судно"
    
    class TransportCompany:
        def __init__(self, name):
            self.name = name
            self.vehicles = []
            self.clients = []
        
        def add_vehicle(self, vehicle):
            self.vehicles.append(vehicle)
            return True
        
        def add_client(self, client):
            self.clients.append(client)
            return True
        
        def remove_vehicle(self, vehicle_id):
            for i, v in enumerate(self.vehicles):
                if v.vehicle_id == vehicle_id:
                    self.vehicles.pop(i)
                    return True
            return False
        
        def remove_client(self, client_name):
            for i, c in enumerate(self.clients):
                if c.name == client_name:
                    self.clients.pop(i)
                    return True
            return False
        
        def optimize_cargo_distribution(self):
            # Простая логика распределения
            for vehicle in self.vehicles:
                vehicle.current_load = 0.0
                vehicle.clients_list = []
            
            # Сортируем клиентов: VIP в первую очередь
            sorted_clients = sorted(self.clients, key=lambda c: (not c.is_vip, -c.cargo_weight))
            
            distribution = {}
            for client in sorted_clients:
                for vehicle in self.vehicles:
                    if vehicle.load_cargo(client):
                        if vehicle.vehicle_id not in distribution:
                            distribution[vehicle.vehicle_id] = []
                        distribution[vehicle.vehicle_id].append(client)
                        break
            
            return distribution


class TransportCompanyGUI:
    """Графический интерфейс транспортной компании на Tkinter"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("Транспортная компания - Управление")
        self.root.geometry("1100x700")
        
        # Инициализация данных
        self.company = TransportCompany("Моя транспортная компания")
        self.current_data_file = None
        self.selected_client = None
        self.selected_vehicle = None
        
        # Создание интерфейса
        self.create_menu()
        self.create_main_frame()
        self.create_status_bar()
        
        # Загрузка тестовых данных (для демонстрации)
        self.load_sample_data()
    
    def create_menu(self):
        """Создание меню"""
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # Меню "Файл"
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Файл", menu=file_menu)
        file_menu.add_command(label="Сохранить данные", command=self.save_data)
        file_menu.add_command(label="Загрузить данные", command=self.load_data)
        file_menu.add_separator()
        file_menu.add_command(label="Выход", command=self.root.quit)
        
        # Меню "Экспорт"
        export_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Экспорт", menu=export_menu)
        export_menu.add_command(label="Экспорт результатов", command=self.export_results)
        
        # Меню "Справка"
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Справка", menu=help_menu)
        help_menu.add_command(label="О программе", command=self.show_about)
    
    def create_main_frame(self):
        """Создание основной рабочей области"""
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Панель управления
        control_frame = ttk.LabelFrame(main_frame, text="Панель управления", padding="10")
        control_frame.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        ttk.Button(control_frame, text="Добавить клиента", 
                  command=self.add_client_dialog).grid(row=0, column=0, padx=5)
        ttk.Button(control_frame, text="Добавить транспорт", 
                  command=self.add_vehicle_dialog).grid(row=0, column=1, padx=5)
        ttk.Button(control_frame, text="Распределить грузы", 
                  command=self.optimize_distribution).grid(row=0, column=2, padx=5)
        ttk.Button(control_frame, text="Удалить выбранного", 
                  command=self.delete_selected).grid(row=0, column=3, padx=5)
        ttk.Button(control_frame, text="Очистить все", 
                  command=self.clear_all).grid(row=0, column=4, padx=5)
        
        # Создание Notebook (вкладки)
        notebook = ttk.Notebook(main_frame)
        notebook.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Вкладка клиентов
        clients_frame = ttk.Frame(notebook)
        notebook.add(clients_frame, text="Клиенты")
        self.create_clients_table(clients_frame)
        
        # Вкладка транспорта
        vehicles_frame = ttk.Frame(notebook)
        notebook.add(vehicles_frame, text="Транспорт")
        self.create_vehicles_table(vehicles_frame)
        
        # Настройка веса строк и колонок
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(1, weight=1)
    
    def create_clients_table(self, parent):
        """Создание таблицы клиентов"""
        # Заголовки таблицы
        columns = ("№", "Имя", "Вес груза (кг)", "VIP статус")
        
        # Создание Treeview
        self.clients_tree = ttk.Treeview(parent, columns=columns, show="headings", height=15)
        
        # Настройка заголовков
        for col in columns:
            self.clients_tree.heading(col, text=col)
            self.clients_tree.column(col, width=100)
        
        self.clients_tree.column("Имя", width=200)
        
        # Добавление скроллбара
        scrollbar = ttk.Scrollbar(parent, orient=tk.VERTICAL, command=self.clients_tree.yview)
        self.clients_tree.configure(yscrollcommand=scrollbar.set)
        
        # Размещение элементов
        self.clients_tree.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
        # Привязка событий
        self.clients_tree.bind("<Double-1>", self.on_client_double_click)
        self.clients_tree.bind("<<TreeviewSelect>>", self.on_client_select)
        
        # Настройка весов
        parent.columnconfigure(0, weight=1)
        parent.rowconfigure(0, weight=1)
    
    def create_vehicles_table(self, parent):
        """Создание таблицы транспорта"""
        # Заголовки таблицы
        columns = ("№", "ID", "Тип", "Грузоподъемность (т)", "Текущая загрузка (т)", "Загрузка %", "Детали")
        
        # Создание Treeview
        self.vehicles_tree = ttk.Treeview(parent, columns=columns, show="headings", height=15)
        
        # Настройка заголовков
        for col in columns:
            self.vehicles_tree.heading(col, text=col)
            self.vehicles_tree.column(col, width=80)
        
        self.vehicles_tree.column("ID", width=120)
        self.vehicles_tree.column("Детали", width=150)
        
        # Добавление скроллбара
        scrollbar = ttk.Scrollbar(parent, orient=tk.VERTICAL, command=self.vehicles_tree.yview)
        self.vehicles_tree.configure(yscrollcommand=scrollbar.set)
        
        # Размещение элементов
        self.vehicles_tree.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
        # Привязка событий
        self.vehicles_tree.bind("<Double-1>", self.on_vehicle_double_click)
        self.vehicles_tree.bind("<<TreeviewSelect>>", self.on_vehicle_select)
        
        # Настройка весов
        parent.columnconfigure(0, weight=1)
        parent.rowconfigure(0, weight=1)
    
    def create_status_bar(self):
        """Создание статусной строки"""
        self.status_var = tk.StringVar()
        self.status_var.set("Готово")
        
        status_bar = ttk.Label(self.root, textvariable=self.status_var, relief=tk.SUNKEN, anchor=tk.W)
        status_bar.grid(row=1, column=0, sticky=(tk.W, tk.E))
    
    def load_sample_data(self):
        """Загрузка тестовых данных для демонстрации"""
        # Тестовые клиенты
        sample_clients = [
            ("Иван Иванов", 500, False),
            ("Петр Петров", 1200, True),
            ("Анна Сидорова", 800, False),
            ("Мария Козлова", 2500, True),
            ("Алексей Новиков", 300, False)
        ]
        
        for name, weight, is_vip in sample_clients:
            try:
                client = Client(name, weight, is_vip)
                self.company.add_client(client)
            except:
                pass
        
        # Тестовый транспорт
        try:
            van1 = Van(2.5, True)
            ship1 = Ship(5.0, "Волга")
            vehicle1 = Vehicle(3.0)
            
            self.company.add_vehicle(van1)
            self.company.add_vehicle(ship1)
            self.company.add_vehicle(vehicle1)
        except:
            pass
        
        # Обновление таблиц
        self.update_clients_table()
        self.update_vehicles_table()
    
    def update_clients_table(self):
        """Обновление таблицы клиентов"""
        # Очистка таблицы
        for item in self.clients_tree.get_children():
            self.clients_tree.delete(item)
        
        # Заполнение данными
        for i, client in enumerate(self.company.clients, 1):
            vip_text = "★ VIP" if client.is_vip else "○ Обычный"
            self.clients_tree.insert("", tk.END, values=(
                i, client.name, f"{client.cargo_weight:.2f}", vip_text
            ))
        
        self.status_var.set(f"Клиентов: {len(self.company.clients)}")
    
    def update_vehicles_table(self):
        """Обновление таблицы транспорта"""
        # Очистка таблицы
        for item in self.vehicles_tree.get_children():
            self.vehicles_tree.delete(item)
        
        # Заполнение данными
        for i, vehicle in enumerate(self.company.vehicles, 1):
            # Определение типа транспорта и деталей
            if hasattr(vehicle, 'vehicle_type'):
                vehicle_type = vehicle.vehicle_type
                if vehicle_type == "Фургон":
                    details = f"Холодильник: {'Да' if vehicle.is_refrigerated else 'Нет'}"
                elif vehicle_type == "Судно":
                    details = f"Название: {vehicle.name}"
                else:
                    details = "Базовый транспорт"
            else:
                vehicle_type = "Транспорт"
                details = ""
            
            # Вставка строки
            self.vehicles_tree.insert("", tk.END, values=(
                i,
                vehicle.vehicle_id,
                vehicle_type,
                f"{vehicle.capacity:.2f}",
                f"{vehicle.current_load:.3f}",
                f"{vehicle.get_current_load_percentage():.1f}%",
                details
            ))
        
        self.status_var.set(f"Транспортных средств: {len(self.company.vehicles)}")
    
    def add_client_dialog(self, client_index=None):
        """Диалог добавления/редактирования клиента"""
        dialog = tk.Toplevel(self.root)
        dialog.title("Добавить клиента" if client_index is None else "Редактировать клиента")
        dialog.geometry("400x250")
        dialog.resizable(False, False)
        dialog.transient(self.root)
        dialog.grab_set()
        
        # Переменные формы
        name_var = tk.StringVar()
        weight_var = tk.StringVar()
        vip_var = tk.BooleanVar(value=False)
        
        # Заполнение данных при редактировании
        if client_index is not None and client_index < len(self.company.clients):
            client = self.company.clients[client_index]
            name_var.set(client.name)
            weight_var.set(str(client.cargo_weight))
            vip_var.set(client.is_vip)
        
        # Создание виджетов
        ttk.Label(dialog, text="Имя клиента:").grid(row=0, column=0, padx=10, pady=10, sticky=tk.W)
        name_entry = ttk.Entry(dialog, textvariable=name_var, width=30)
        name_entry.grid(row=0, column=1, padx=10, pady=10, sticky=tk.W)
        
        ttk.Label(dialog, text="Вес груза (кг):").grid(row=1, column=0, padx=10, pady=10, sticky=tk.W)
        weight_entry = ttk.Entry(dialog, textvariable=weight_var, width=30)
        weight_entry.grid(row=1, column=1, padx=10, pady=10, sticky=tk.W)
        
        vip_check = ttk.Checkbutton(dialog, text="VIP клиент", variable=vip_var)
        vip_check.grid(row=2, column=0, columnspan=2, padx=10, pady=10, sticky=tk.W)
        
        # Кнопки
        button_frame = ttk.Frame(dialog)
        button_frame.grid(row=3, column=0, columnspan=2, pady=20)
        
        def save_client():
            """Сохранение клиента"""
            name = name_var.get().strip()
            weight_str = weight_var.get().strip()
            
            # Валидация
            if not name or len(name) < 2:
                messagebox.showerror("Ошибка", "Имя должно содержать минимум 2 символа")
                name_entry.focus()
                return
            
            try:
                weight = float(weight_str)
                if weight <= 0:
                    messagebox.showerror("Ошибка", "Вес должен быть положительным числом")
                    weight_entry.focus()
                    return
                if weight > 10000:
                    messagebox.showerror("Ошибка", "Вес не может превышать 10000 кг")
                    weight_entry.focus()
                    return
            except ValueError:
                messagebox.showerror("Ошибка", "Вес должен быть числом")
                weight_entry.focus()
                return
            
            try:
                if client_index is not None:
                    # Редактирование существующего клиента
                    client = self.company.clients[client_index]
                    client.name = name
                    client.update_cargo_weight(weight)
                    client.is_vip = vip_var.get()
                    message = f"Клиент '{name}' обновлен"
                else:
                    # Добавление нового клиента
                    client = Client(name, weight, vip_var.get())
                    self.company.add_client(client)
                    message = f"Клиент '{name}' добавлен"
                
                self.update_clients_table()
                dialog.destroy()
                messagebox.showinfo("Успех", message)
                
            except Exception as e:
                messagebox.showerror("Ошибка", f"Не удалось сохранить клиента: {str(e)}")
        
        def cancel():
            dialog.destroy()
        
        ttk.Button(button_frame, text="Сохранить", command=save_client, width=15).pack(side=tk.LEFT, padx=10)
        ttk.Button(button_frame, text="Отмена", command=cancel, width=15).pack(side=tk.LEFT, padx=10)
        
        # Привязка клавиш
        dialog.bind("<Return>", lambda e: save_client())
        dialog.bind("<Escape>", lambda e: cancel())
        
        # Фокус на первом поле
        name_entry.focus()
    
    def add_vehicle_dialog(self, vehicle_index=None):
        """Диалог добавления/редактирования транспорта"""
        dialog = tk.Toplevel(self.root)
        dialog.title("Добавить транспорт" if vehicle_index is None else "Редактировать транспорт")
        dialog.geometry("450x300")
        dialog.resizable(False, False)
        dialog.transient(self.root)
        dialog.grab_set()
        
        # Переменные формы
        type_var = tk.StringVar(value="Фургон")
        capacity_var = tk.StringVar()
        name_var = tk.StringVar()
        refrigerated_var = tk.BooleanVar(value=False)
        
        # Заполнение данных при редактировании
        if vehicle_index is not None and vehicle_index < len(self.company.vehicles):
            vehicle = self.company.vehicles[vehicle_index]
            if isinstance(vehicle, Van):
                type_var.set("Фургон")
                refrigerated_var.set(vehicle.is_refrigerated)
            elif isinstance(vehicle, Ship):
                type_var.set("Судно")
                name_var.set(vehicle.name)
            else:
                type_var.set("Транспорт")
            capacity_var.set(str(vehicle.capacity))
        
        # Создание виджетов
        row = 0
        
        ttk.Label(dialog, text="Тип транспорта:").grid(row=row, column=0, padx=10, pady=10, sticky=tk.W)
        type_combo = ttk.Combobox(dialog, textvariable=type_var, 
                                 values=["Фургон", "Судно", "Транспорт"], 
                                 state="readonly", width=27)
        type_combo.grid(row=row, column=1, padx=10, pady=10, sticky=tk.W)
        row += 1
        
        ttk.Label(dialog, text="Грузоподъемность (т):").grid(row=row, column=0, padx=10, pady=10, sticky=tk.W)
        capacity_entry = ttk.Entry(dialog, textvariable=capacity_var, width=30)
        capacity_entry.grid(row=row, column=1, padx=10, pady=10, sticky=tk.W)
        row += 1
        
        # Динамические поля
        name_label = ttk.Label(dialog, text="Название судна:")
        name_entry = ttk.Entry(dialog, textvariable=name_var, width=30)
        
        refrigerated_check = ttk.Checkbutton(dialog, text="С холодильником", 
                                           variable=refrigerated_var)
        
        def update_fields(*args):
            """Обновление видимости полей в зависимости от типа транспорта"""
            vehicle_type = type_var.get()
            
            if vehicle_type == "Судно":
                name_label.grid(row=row, column=0, padx=10, pady=10, sticky=tk.W)
                name_entry.grid(row=row, column=1, padx=10, pady=10, sticky=tk.W)
                refrigerated_check.grid_forget()
            elif vehicle_type == "Фургон":
                name_label.grid_forget()
                name_entry.grid_forget()
                refrigerated_check.grid(row=row, column=0, columnspan=2, padx=10, pady=10, sticky=tk.W)
            else:
                name_label.grid_forget()
                name_entry.grid_forget()
                refrigerated_check.grid_forget()
        
        type_var.trace("w", update_fields)
        update_fields()
        
        # Кнопки
        button_frame = ttk.Frame(dialog)
        button_frame.grid(row=row+1, column=0, columnspan=2, pady=20)
        
        def save_vehicle():
            """Сохранение транспорта"""
            vehicle_type = type_var.get()
            capacity_str = capacity_var.get().strip()
            
            # Валидация грузоподъемности
            try:
                capacity = float(capacity_str)
                if capacity <= 0:
                    messagebox.showerror("Ошибка", "Грузоподъемность должна быть положительной")
                    capacity_entry.focus()
                    return
                if capacity > 1000:
                    messagebox.showerror("Ошибка", "Грузоподъемность не может превышать 1000 тонн")
                    capacity_entry.focus()
                    return
            except ValueError:
                messagebox.showerror("Ошибка", "Грузоподъемность должна быть числом")
                capacity_entry.focus()
                return
            
            # Валидация названия судна
            if vehicle_type == "Судно":
                name = name_var.get().strip()
                if not name or len(name) < 2:
                    messagebox.showerror("Ошибка", "Название судна должно содержать минимум 2 символа")
                    name_entry.focus()
                    return
            
            try:
                # Создание транспорта
                if vehicle_type == "Фургон":
                    vehicle = Van(capacity, refrigerated_var.get())
                elif vehicle_type == "Судно":
                    vehicle = Ship(capacity, name_var.get().strip())
                else:
                    vehicle = Vehicle(capacity)
                
                if vehicle_index is not None:
                    # Заменяем существующий транспорт
                    old_id = self.company.vehicles[vehicle_index].vehicle_id
                    self.company.remove_vehicle(old_id)
                
                self.company.add_vehicle(vehicle)
                self.update_vehicles_table()
                
                dialog.destroy()
                message = "Транспорт обновлен" if vehicle_index is not None else "Транспорт добавлен"
                messagebox.showinfo("Успех", message)
                
            except Exception as e:
                messagebox.showerror("Ошибка", f"Не удалось сохранить транспорт: {str(e)}")
        
        def cancel():
            dialog.destroy()
        
        ttk.Button(button_frame, text="Сохранить", command=save_vehicle, width=15).pack(side=tk.LEFT, padx=10)
        ttk.Button(button_frame, text="Отмена", command=cancel, width=15).pack(side=tk.LEFT, padx=10)
        
        # Привязка клавиш
        dialog.bind("<Return>", lambda e: save_vehicle())
        dialog.bind("<Escape>", lambda e: cancel())
        
        # Фокус на поле грузоподъемности
        capacity_entry.focus()
    
    def optimize_distribution(self):
        """Оптимизация распределения грузов"""
        if not self.company.clients:
            messagebox.showwarning("Внимание", "Нет клиентов для распределения")
            return
        
        if not self.company.vehicles:
            messagebox.showwarning("Внимание", "Нет транспортных средств")
            return
        
        try:
            # Выполняем распределение
            distribution = self.company.optimize_cargo_distribution()
            
            # Обновляем таблицу транспорта
            self.update_vehicles_table()
            
            # Показываем результаты
            self.show_distribution_results(distribution)
            
        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка при распределении грузов: {str(e)}")
    
    def show_distribution_results(self, distribution):
        """Показать результаты распределения"""
        results_dialog = tk.Toplevel(self.root)
        results_dialog.title("Результаты распределения грузов")
        results_dialog.geometry("800x500")
        
        # Заголовок
        ttk.Label(results_dialog, text="Распределение грузов по транспортным средствам", 
                 font=("Arial", 12, "bold")).pack(pady=10)
        
        # Статистика
        total_vehicles_used = len([v for v in self.company.vehicles if v.clients_list])
        total_clients_loaded = sum(len(v.clients_list) for v in self.company.vehicles)
        
        stats_text = f"Использовано транспорта: {total_vehicles_used} из {len(self.company.vehicles)}\n"
        stats_text += f"Загружено клиентов: {total_clients_loaded} из {len(self.company.clients)}"
        
        ttk.Label(results_dialog, text=stats_text).pack(pady=5)
        
        # Таблица результатов
        frame = ttk.Frame(results_dialog)
        frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Создание Treeview
        columns = ("Транспорт ID", "Тип", "Клиентов", "Общий вес (кг)", "Загрузка %")
        tree = ttk.Treeview(frame, columns=columns, show="headings", height=15)
        
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=120)
        
        # Заполнение данными
        for vehicle in self.company.vehicles:
            if vehicle.clients_list:
                total_weight = sum(client.cargo_weight for client in vehicle.clients_list)
                load_percentage = vehicle.get_current_load_percentage()
                
                vehicle_type = getattr(vehicle, 'vehicle_type', 'Транспорт')
                
                tree.insert("", tk.END, values=(
                    vehicle.vehicle_id,
                    vehicle_type,
                    len(vehicle.clients_list),
                    f"{total_weight:.2f}",
                    f"{load_percentage:.1f}%"
                ))
        
        # Добавление скроллбара
        scrollbar = ttk.Scrollbar(frame, orient=tk.VERTICAL, command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        
        tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Кнопки
        button_frame = ttk.Frame(results_dialog)
        button_frame.pack(pady=10)
        
        ttk.Button(button_frame, text="Сохранить результаты", 
                  command=lambda: self.save_distribution_results()).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Закрыть", 
                  command=results_dialog.destroy).pack(side=tk.LEFT, padx=5)
    
    def save_distribution_results(self):
        """Сохранение результатов распределения"""
        try:
            filename = filedialog.asksaveasfilename(
                defaultextension=".json",
                filetypes=[("JSON files", "*.json"), ("Text files", "*.txt"), ("All files", "*.*")],
                title="Сохранить результаты распределения"
            )
            
            if filename:
                results = {
                    "company": self.company.name,
                    "clients_count": len(self.company.clients),
                    "vehicles_count": len(self.company.vehicles),
                    "distribution": []
                }
                
                for vehicle in self.company.vehicles:
                    if vehicle.clients_list:
                        vehicle_data = {
                            "vehicle_id": vehicle.vehicle_id,
                            "type": getattr(vehicle, 'vehicle_type', 'Транспорт'),
                            "capacity": vehicle.capacity,
                            "current_load": vehicle.current_load,
                            "clients": []
                        }
                        
                        for client in vehicle.clients_list:
                            vehicle_data["clients"].append({
                                "name": client.name,
                                "cargo_weight": client.cargo_weight,
                                "is_vip": client.is_vip
                            })
                        
                        results["distribution"].append(vehicle_data)
                
                with open(filename, 'w', encoding='utf-8') as f:
                    json.dump(results, f, ensure_ascii=False, indent=2)
                
                messagebox.showinfo("Успех", f"Результаты сохранены в файл:\n{filename}")
                
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось сохранить результаты: {str(e)}")
    
    def export_results(self):
        """Экспорт результатов"""
        if not self.company.clients and not self.company.vehicles:
            messagebox.showwarning("Внимание", "Нет данных для экспорта")
            return
        
        try:
            filename = filedialog.asksaveasfilename(
                defaultextension=".json",
                filetypes=[
                    ("JSON files", "*.json"),
                    ("Text files", "*.txt"),
                    ("CSV files", "*.csv"),
                    ("All files", "*.*")
                ],
                title="Экспорт данных"
            )
            
            if filename:
                # Определяем формат по расширению
                if filename.endswith('.csv'):
                    self.export_to_csv(filename)
                elif filename.endswith('.txt'):
                    self.export_to_txt(filename)
                else:
                    self.export_to_json(filename)
                
                messagebox.showinfo("Успех", f"Данные экспортированы в файл:\n{filename}")
                
        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка при экспорте: {str(e)}")
    
    def export_to_json(self, filename):
        """Экспорт в JSON"""
        data = {
            "company": self.company.name,
            "clients": [
                {
                    "name": client.name,
                    "cargo_weight": client.cargo_weight,
                    "is_vip": client.is_vip
                }
                for client in self.company.clients
            ],
            "vehicles": [
                {
                    "id": vehicle.vehicle_id,
                    "type": getattr(vehicle, 'vehicle_type', 'Транспорт'),
                    "capacity": vehicle.capacity,
                    "current_load": vehicle.current_load
                }
                for vehicle in self.company.vehicles
            ]
        }
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    
    def export_to_txt(self, filename):
        """Экспорт в TXT"""
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(f"ТРАНСПОРТНАЯ КОМПАНИЯ: {self.company.name}\n")
            f.write("=" * 50 + "\n\n")
            
            f.write("КЛИЕНТЫ:\n")
            f.write("-" * 30 + "\n")
            for client in self.company.clients:
                vip = "VIP" if client.is_vip else "Обычный"
                f.write(f"{client.name}: {client.cargo_weight:.2f} кг ({vip})\n")
            
            f.write("\n\nТРАНСПОРТ:\n")
            f.write("-" * 30 + "\n")
            for vehicle in self.company.vehicles:
                f.write(f"{vehicle.vehicle_id}: {vehicle.capacity:.2f} т, загрузка: {vehicle.current_load:.2f} т\n")
    
    def export_to_csv(self, filename):
        """Экспорт в CSV"""
        import csv
        
        with open(filename, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            
            # Заголовки для клиентов
            writer.writerow(["Тип данных", "Имя", "Вес (кг)", "VIP"])
            for client in self.company.clients:
                writer.writerow(["Клиент", client.name, client.cargo_weight, "Да" if client.is_vip else "Нет"])
            
            # Пустая строка
            writer.writerow([])
            
            # Заголовки для транспорта
            writer.writerow(["Тип данных", "ID", "Тип", "Грузоподъемность (т)", "Текущая загрузка (т)"])
            for vehicle in self.company.vehicles:
                writer.writerow([
                    "Транспорт",
                    vehicle.vehicle_id,
                    getattr(vehicle, 'vehicle_type', 'Транспорт'),
                    vehicle.capacity,
                    vehicle.current_load
                ])
    
    def save_data(self):
        """Сохранение данных в файл"""
        try:
            filename = filedialog.asksaveasfilename(
                defaultextension=".json",
                filetypes=[("JSON files", "*.json"), ("All files", "*.*")],
                title="Сохранить данные"
            )
            
            if filename:
                data = {
                    "company_name": self.company.name,
                    "clients": [
                        {
                            "name": client.name,
                            "cargo_weight": client.cargo_weight,
                            "is_vip": client.is_vip
                        }
                        for client in self.company.clients
                    ],
                    "vehicles": []
                }
                
                for vehicle in self.company.vehicles:
                    vehicle_data = {
                        "type": vehicle.__class__.__name__,
                        "capacity": vehicle.capacity,
                        "current_load": vehicle.current_load,
                        "vehicle_id": vehicle.vehicle_id
                    }
                    
                    if isinstance(vehicle, Van):
                        vehicle_data["is_refrigerated"] = vehicle.is_refrigerated
                    elif isinstance(vehicle, Ship):
                        vehicle_data["name"] = vehicle.name
                    
                    data["vehicles"].append(vehicle_data)
                
                with open(filename, 'w', encoding='utf-8') as f:
                    json.dump(data, f, ensure_ascii=False, indent=2)
                
                self.current_data_file = filename
                messagebox.showinfo("Успех", f"Данные сохранены в файл:\n{filename}")
                
        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка при сохранении: {str(e)}")
    
    def load_data(self):
        """Загрузка данных из файла"""
        try:
            filename = filedialog.askopenfilename(
                filetypes=[("JSON files", "*.json"), ("All files", "*.*")],
                title="Загрузить данные"
            )
            
            if filename:
                with open(filename, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                # Очищаем текущие данные
                self.company.clients.clear()
                self.company.vehicles.clear()
                
                # Загружаем клиентов
                for client_data in data.get("clients", []):
                    try:
                        client = Client(
                            client_data["name"],
                            client_data["cargo_weight"],
                            client_data.get("is_vip", False)
                        )
                        self.company.clients.append(client)
                    except:
                        print(f"Ошибка при загрузке клиента: {client_data}")
                
                # Загружаем транспорт
                for vehicle_data in data.get("vehicles", []):
                    try:
                        if vehicle_data["type"] == "Van":
                            vehicle = Van(
                                vehicle_data["capacity"],
                                vehicle_data.get("is_refrigerated", False)
                            )
                        elif vehicle_data["type"] == "Ship":
                            vehicle = Ship(
                                vehicle_data["capacity"],
                                vehicle_data.get("name", "Судно")
                            )
                        else:
                            vehicle = Vehicle(vehicle_data["capacity"])
                        
                        vehicle.vehicle_id = vehicle_data.get("vehicle_id", vehicle.vehicle_id)
                        vehicle.current_load = vehicle_data.get("current_load", 0.0)
                        
                        self.company.vehicles.append(vehicle)
                    except:
                        print(f"Ошибка при загрузке транспорта: {vehicle_data}")
                
                self.current_data_file = filename
                self.update_clients_table()
                self.update_vehicles_table()
                messagebox.showinfo("Успех", f"Данные загружены из файла:\n{filename}")
                
        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка при загрузке: {str(e)}")
    
    def show_about(self):
        """Показать окно 'О программе'"""
        about_text = """Транспортная компания - система управления

Лабораторная работа №12
Вариант: 2

Разработчик: Давидовский И.М.
Группа: 88ТП

Функционал:
• Управление клиентами и транспортом
• Оптимизация распределения грузов
• Экспорт данных в различные форматы
• Сохранение и загрузка состояния

© 2025 Транспортная компания"""
        
        messagebox.showinfo("О программе", about_text)
    
    def on_client_double_click(self, event):
        """Обработка двойного клика по клиенту"""
        selection = self.clients_tree.selection()
        if selection:
            item = selection[0]
            index = self.clients_tree.index(item)
            if index < len(self.company.clients):
                self.add_client_dialog(index)
    
    def on_vehicle_double_click(self, event):
        """Обработка двойного клика по транспорту"""
        selection = self.vehicles_tree.selection()
        if selection:
            item = selection[0]
            index = self.vehicles_tree.index(item)
            if index < len(self.company.vehicles):
                self.add_vehicle_dialog(index)
    
    def on_client_select(self, event):
        """Обработка выбора клиента"""
        selection = self.clients_tree.selection()
        if selection:
            item = selection[0]
            self.selected_client = self.clients_tree.index(item)
        else:
            self.selected_client = None
    
    def on_vehicle_select(self, event):
        """Обработка выбора транспорта"""
        selection = self.vehicles_tree.selection()
        if selection:
            item = selection[0]
            self.selected_vehicle = self.vehicles_tree.index(item)
        else:
            self.selected_vehicle = None
    
    def delete_selected(self):
        """Удаление выбранного элемента"""
        if self.selected_client is not None:
            client = self.company.clients[self.selected_client]
            if messagebox.askyesno("Подтверждение", f"Удалить клиента '{client.name}'?"):
                self.company.remove_client(client.name)
                self.update_clients_table()
                self.selected_client = None
        
        elif self.selected_vehicle is not None:
            vehicle = self.company.vehicles[self.selected_vehicle]
            if messagebox.askyesno("Подтверждение", f"Удалить транспорт '{vehicle.vehicle_id}'?"):
                self.company.remove_vehicle(vehicle.vehicle_id)
                self.update_vehicles_table()
                self.selected_vehicle = None
        
        else:
            messagebox.showinfo("Информация", "Не выбран элемент для удаления")
    
    def clear_all(self):
        """Очистка всех данных"""
        if messagebox.askyesno("Подтверждение", "Очистить все данные?"):
            self.company.clients.clear()
            self.company.vehicles.clear()
            self.update_clients_table()
            self.update_vehicles_table()
            self.status_var.set("Все данные очищены")


def main():
    """Главная функция"""
    root = tk.Tk()
    app = TransportCompanyGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()