from transport.client import Client
from transport.vehicle import Vehicle
from transport.van import Van
from transport.ship import Ship
from transport.transport_company import TransportCompany


def display_header(title: str):
    """Отображение заголовка раздела"""
    print("\n" + "="*60)
    print(f"{title:^60}")
    print("="*60)


def create_client_interactive():
    """
    Интерактивное создание клиента с запросом данных у пользователя
    """
    display_header("СОЗДАНИЕ НОВОГО КЛИЕНТА")
    
    # Запрос имени клиента
    while True:
        name = input("Введите имя клиента: ").strip()
        if len(name.strip()) < 2:
            print("Ошибка: имя должно содержать минимум 2 символа.")
            continue
        break
    
    # Запрос веса груза
    while True:
        weight_input = input("Введите вес груза (в кг): ").strip()
        try:
            cargo_weight = float(weight_input)
            if cargo_weight <= 0:
                print("Ошибка: вес должен быть положительным числом.")
                continue
            if cargo_weight > 100000:
                print("Ошибка: вес слишком большой (максимум 100000 кг).")
                continue
            break
        except ValueError:
            print("Ошибка: вес должен быть числом.")
    
    # Запрос VIP-статуса
    while True:
        vip_input = input("Клиент является VIP? (да/нет): ").strip().lower()
        if vip_input in ['да', 'д', 'yes', 'y']:
            is_vip = True
            break
        elif vip_input in ['нет', 'н', 'no', 'n']:
            is_vip = False
            break
        else:
            print("Пожалуйста, ответьте 'да' или 'нет'.")
    
    try:
        client = Client(name, cargo_weight, is_vip)
        display_header("КЛИЕНТ УСПЕШНО СОЗДАН!")
        print(f"Имя: {client.name}")
        print(f"Вес груза: {client.cargo_weight:.2f} кг")
        print(f"Статус: {'VIP' if client.is_vip else 'Обычный'}")
        return client
    except (ValueError, TypeError) as e:
        print(f"\nОшибка при создании клиента: {e}")
        return None


def create_vehicle_interactive():
    """
    Интерактивное создание базового транспортного средства
    """
    display_header("СОЗДАНИЕ ТРАНСПОРТНОГО СРЕДСТВА")
    
    # Запрос грузоподъемности
    while True:
        capacity_input = input("Введите грузоподъемность (в тоннах): ").strip()
        try:
            capacity = float(capacity_input)
            if capacity <= 0:
                print("Ошибка: грузоподъемность должна быть положительной.")
                continue
            if capacity > 1000:
                print("Ошибка: грузоподъемность слишком большая (максимум 1000 тонн).")
                continue
            break
        except ValueError:
            print("Ошибка: грузоподъемность должна быть числом.")
    
    try:
        vehicle = Vehicle(capacity)
        display_header("ТРАНСПОРТ УСПЕШНО СОЗДАН!")
        print(f"ID транспорта: {vehicle.vehicle_id}")
        print(f"Грузоподъемность: {vehicle.capacity:.2f} тонн")
        print(f"Текущая загрузка: {vehicle.current_load:.2f} тонн")
        return vehicle
    except (ValueError, TypeError) as e:
        print(f"\nОшибка при создании транспорта: {e}")
        return None


def create_van_interactive():
    """
    Интерактивное создание фургона
    """
    display_header("СОЗДАНИЕ ФУРГОНА")
    
    # Запрос грузоподъемности
    while True:
        capacity_input = input("Введите грузоподъемность фургона (в тоннах): ").strip()
        try:
            capacity = float(capacity_input)
            if capacity <= 0:
                print("Ошибка: грузоподъемность должна быть положительной.")
                continue
            break
        except ValueError:
            print("Ошибка: грузоподъемность должна быть числом.")
    
    # Запрос информации о холодильнике
    while True:
        refrigerated_input = input("Фургон имеет холодильник? (да/нет): ").strip().lower()
        if refrigerated_input in ['да', 'д', 'yes', 'y']:
            is_refrigerated = True
            break
        elif refrigerated_input in ['нет', 'н', 'no', 'n']:
            is_refrigerated = False
            break
        else:
            print("Пожалуйста, ответьте 'да' или 'нет'.")
    
    try:
        van = Van(capacity, is_refrigerated)
        display_header("ФУРГОН УСПЕШНО СОЗДАН!")
        print(f"ID фургона: {van.vehicle_id}")
        print(f"Грузоподъемность: {van.capacity:.2f} тонн")
        print(f"Холодильник: {'Да' if van.is_refrigerated else 'Нет'}")
        return van
    except (ValueError, TypeError) as e:
        print(f"\nОшибка при создании фургона: {e}")
        return None


def create_ship_interactive():
    """
    Интерактивное создание судна
    """
    display_header("СОЗДАНИЕ СУДНА")
    
    # Запрос грузоподъемности
    while True:
        capacity_input = input("Введите грузоподъемность судна (в тоннах): ").strip()
        try:
            capacity = float(capacity_input)
            if capacity <= 0:
                print("Ошибка: грузоподъемность должна быть положительной.")
                continue
            break
        except ValueError:
            print("Ошибка: грузоподъемность должна быть числом.")
    
    # Запрос названия судна
    while True:
        name = input("Введите название судна: ").strip()
        if len(name.strip()) < 2:
            print("Ошибка: название должно содержать минимум 2 символа.")
            continue
        break
    
    try:
        ship = Ship(capacity, name)
        display_header("СУДНО УСПЕШНО СОЗДАН!")
        print(f"ID судна: {ship.vehicle_id}")
        print(f"Название: {ship.name}")
        print(f"Грузоподъемность: {ship.capacity:.2f} тонн")
        return ship
    except (ValueError, TypeError) as e:
        print(f"\nОшибка при создании судна: {e}")
        return None


def create_company_interactive():
    """
    Интерактивное создание транспортной компании
    """
    display_header("СОЗДАНИЕ ТРАНСПОРТНОЙ КОМПАНИИ")
    
    while True:
        name = input("Введите название транспортной компании: ").strip()
        if len(name.strip()) < 2:
            print("Ошибка: название должно содержать минимум 2 символа.")
            continue
        break
    
    try:
        company = TransportCompany(name)
        display_header(f"КОМПАНИЯ '{name}' СОЗДАНА!")
        print(f"Название: {company.name}")
        print("Клиентов: 0")
        print("Транспортных средств: 0")
        return company
    except (ValueError, TypeError) as e:
        print(f"\nОшибка при создании компании: {e}")
        return None


def manage_clients_menu(clients):
    """Меню управления клиентами"""
    while True:
        display_header(f"УПРАВЛЕНИЕ КЛИЕНТАМИ ({len(clients)} клиентов)")
        
        print("1. Создать нового клиента")
        print("2. Просмотреть всех клиентов")
        print("3. Изменить данные клиента")
        print("4. Найти клиента по имени")
        print("5. Показать статистику по клиентам")
        print("6. Вернуться в главное меню")
        
        choice = input("\nВыберите действие (1-6): ").strip()
        
        if choice == "1":
            client = create_client_interactive()
            if client:
                clients.append(client)
                print(f"\nКлиент '{client.name}' добавлен. Всего клиентов: {len(clients)}")
        
        elif choice == "2":
            if not clients:
                print("\nСписок клиентов пуст.")
                continue
            
            display_header(f"СПИСОК КЛИЕНТОВ ({len(clients)})")
            
            vip_clients = [c for c in clients if c.is_vip]
            regular_clients = [c for c in clients if not c.is_vip]
            
            if vip_clients:
                print("\n★ VIP КЛИЕНТЫ:")
                for i, client in enumerate(vip_clients, 1):
                    print(f"{i:3}. {client.name:20} | Вес: {client.cargo_weight:8.2f} кг")
            
            if regular_clients:
                print("\n○ ОБЫЧНЫЕ КЛИЕНТЫ:")
                start_num = len(vip_clients) + 1
                for i, client in enumerate(regular_clients, start_num):
                    print(f"{i:3}. {client.name:20} | Вес: {client.cargo_weight:8.2f} кг")
        
        elif choice == "3":
            if not clients:
                print("\nСписок клиентов пуст.")
                continue
            
            print("\nВыберите клиента для изменения:")
            for i, client in enumerate(clients, 1):
                print(f"{i}. {client.name} - {client.cargo_weight:.2f} кг")
            
            try:
                idx = int(input("\nНомер клиента: ")) - 1
                if 0 <= idx < len(clients):
                    client = clients[idx]
                    display_header(f"ИЗМЕНЕНИЕ КЛИЕНТА: {client.name}")
                    
                    # Изменение веса груза
                    change_weight = input("Изменить вес груза? (да/нет): ").strip().lower()
                    if change_weight in ['да', 'д', 'yes', 'y']:
                        while True:
                            try:
                                new_weight = float(input("Новый вес (кг): ").strip())
                                if new_weight <= 0:
                                    print("Вес должен быть положительным.")
                                    continue
                                client.update_cargo_weight(new_weight)
                                print(f"Вес изменен на {new_weight:.2f} кг")
                                break
                            except ValueError:
                                print("Ошибка: введите число.")
                    
                    # Изменение VIP-статуса
                    current_status = "VIP" if client.is_vip else "Обычный"
                    change_status = input(f"Изменить VIP-статус (сейчас: {current_status})? (да/нет): ").strip().lower()
                    if change_status in ['да', 'д', 'yes', 'y']:
                        if client.is_vip:
                            client.downgrade_from_vip()
                            print("Клиент понижен до обычного статуса")
                        else:
                            client.upgrade_to_vip()
                            print("Клиент повышен до VIP статуса")
                    
                    print("\nДанные клиента обновлены:")
                    print(client.get_info())
                else:
                    print("Неверный номер клиента.")
            except ValueError:
                print("Ошибка: введите номер.")
        
        elif choice == "4":
            if not clients:
                print("\nСписок клиентов пуст.")
                continue
            
            search_name = input("Введите имя клиента для поиска: ").strip().lower()
            found_clients = [c for c in clients if search_name in c.name.lower()]
            
            if not found_clients:
                print(f"\nКлиенты с именем '{search_name}' не найдены.")
            else:
                display_header(f"НАЙДЕНО КЛИЕНТОВ: {len(found_clients)}")
                for i, client in enumerate(found_clients, 1):
                    print(f"\n{i}. {client.get_info()}")
        
        elif choice == "5":
            if not clients:
                print("\nНет данных для статистики.")
                continue
            
            total_clients = len(clients)
            vip_count = sum(1 for c in clients if c.is_vip)
            regular_count = total_clients - vip_count
            total_weight = sum(c.cargo_weight for c in clients)
            avg_weight = total_weight / total_clients if total_clients > 0 else 0
            
            display_header("СТАТИСТИКА КЛИЕНТОВ")
            print(f"Всего клиентов: {total_clients}")
            print(f"VIP клиентов: {vip_count} ({vip_count/total_clients*100:.1f}%)")
            print(f"Обычных клиентов: {regular_count} ({regular_count/total_clients*100:.1f}%)")
            print(f"Общий вес грузов: {total_weight:.2f} кг")
            print(f"Средний вес груза: {avg_weight:.2f} кг")
            
            if clients:
                max_client = max(clients, key=lambda c: c.cargo_weight)
                min_client = min(clients, key=lambda c: c.cargo_weight)
                print(f"Самый тяжелый груз: {max_client.cargo_weight:.2f} кг ({max_client.name})")
                print(f"Самый легкий груз: {min_client.cargo_weight:.2f} кг ({min_client.name})")
        
        elif choice == "6":
            break
        
        else:
            print("\nНеверный выбор. Пожалуйста, выберите действие от 1 до 6.")


def manage_vehicles_menu(vehicles, clients=None):
    """Меню управления транспортными средствами"""
    while True:
        display_header(f"УПРАВЛЕНИЕ ТРАНСПОРТОМ ({len(vehicles)} единиц)")
        
        print("1. Создать транспортное средство")
        print("2. Создать фургон")
        print("3. Создать судно")
        print("4. Просмотреть весь транспорт")
        print("5. Загрузить груз клиента")
        print("6. Выгрузить груз клиента")
        print("7. Показать статистику по транспорту")
        print("8. Вернуться в главное меню")
        
        choice = input("\nВыберите действие (1-8): ").strip()
        
        if choice == "1":
            vehicle = create_vehicle_interactive()
            if vehicle:
                vehicles.append(vehicle)
        
        elif choice == "2":
            van = create_van_interactive()
            if van:
                vehicles.append(van)
        
        elif choice == "3":
            ship = create_ship_interactive()
            if ship:
                vehicles.append(ship)
        
        elif choice == "4":
            if not vehicles:
                print("\nСписок транспортных средств пуст.")
                continue
            
            display_header(f"ВЕСЬ ТРАНСПОРТ ({len(vehicles)} единиц)")
            
            for i, vehicle in enumerate(vehicles, 1):
                print(f"\n{i}. {vehicle.vehicle_id}")
                print(f"   Тип: {getattr(vehicle, 'vehicle_type', 'Транспорт')}")
                print(f"   Грузоподъемность: {vehicle.capacity:.2f} тонн")
                print(f"   Текущая загрузка: {vehicle.current_load:.3f} тонн")
                print(f"   Загрузка: {vehicle.get_current_load_percentage():.1f}%")
                
                if isinstance(vehicle, Van):
                    print(f"   Холодильник: {'Да' if vehicle.is_refrigerated else 'Нет'}")
                elif isinstance(vehicle, Ship):
                    print(f"   Название: {vehicle.name}")
                
                if vehicle.clients_list:
                    print(f"   Загружено клиентов: {len(vehicle.clients_list)}")
        
        elif choice == "5":
            if not vehicles:
                print("\nНет транспортных средств.")
                continue
            
            if not clients:
                print("\nНет клиентов для загрузки.")
                continue
            
            # Выбор транспорта
            print("\nВыберите транспорт:")
            for i, vehicle in enumerate(vehicles, 1):
                avail = vehicle.get_available_capacity() * 1000
                print(f"{i}. {vehicle.vehicle_id} - доступно {avail:.0f} кг")
            
            try:
                vehicle_idx = int(input("\nНомер транспорта: ")) - 1
                if not (0 <= vehicle_idx < len(vehicles)):
                    print("Неверный номер транспорта.")
                    continue
                
                vehicle = vehicles[vehicle_idx]
                
                # Выбор клиента
                print("\nВыберите клиента:")
                for i, client in enumerate(clients, 1):
                    print(f"{i}. {client.name} - {client.cargo_weight:.2f} кг")
                
                client_idx = int(input("\nНомер клиента: ")) - 1
                if not (0 <= client_idx < len(clients)):
                    print("Неверный номер клиента.")
                    continue
                
                client = clients[client_idx]
                vehicle.load_cargo(client)
                
            except ValueError:
                print("Ошибка: введите номер.")
        
        elif choice == "6":
            if not vehicles:
                print("\nНет транспортных средств.")
                continue
            
            # Выбор транспорта с загруженными клиентами
            vehicles_with_load = [v for v in vehicles if v.clients_list]
            if not vehicles_with_load:
                print("\nНет транспорта с загруженными клиентами.")
                continue
            
            print("\nВыберите транспорт:")
            for i, vehicle in enumerate(vehicles_with_load, 1):
                print(f"{i}. {vehicle.vehicle_id} - {len(vehicle.clients_list)} клиентов")
            
            try:
                vehicle_idx = int(input("\nНомер транспорта: ")) - 1
                if not (0 <= vehicle_idx < len(vehicles_with_load)):
                    print("Неверный номер транспорта.")
                    continue
                
                vehicle = vehicles_with_load[vehicle_idx]
                
                # Выбор клиента для выгрузки
                print(f"\nЗагруженные клиенты в {vehicle.vehicle_id}:")
                for i, client in enumerate(vehicle.clients_list, 1):
                    print(f"{i}. {client.name} - {client.cargo_weight:.2f} кг")
                
                client_idx = int(input("\nНомер клиента для выгрузки: ")) - 1
                if not (0 <= client_idx < len(vehicle.clients_list)):
                    print("Неверный номер клиента.")
                    continue
                
                client_name = vehicle.clients_list[client_idx].name
                vehicle.unload_cargo(client_name)
                
            except ValueError:
                print("Ошибка: введите номер.")
        
        elif choice == "7":
            if not vehicles:
                print("\nНет данных для статистики.")
                continue
            
            total_vehicles = len(vehicles)
            vans = [v for v in vehicles if isinstance(v, Van)]
            ships = [v for v in vehicles if isinstance(v, Ship)]
            others = total_vehicles - len(vans) - len(ships)
            
            total_capacity = sum(v.capacity for v in vehicles)
            total_load = sum(v.current_load for v in vehicles)
            total_available = sum(v.get_available_capacity() for v in vehicles)
            
            display_header("СТАТИСТИКА ТРАНСПОРТА")
            print(f"Всего единиц транспорта: {total_vehicles}")
            print(f"Фургонов: {len(vans)}")
            print(f"Судов: {len(ships)}")
            print(f"Других транспортных средств: {others}")
            print(f"\nОбщая грузоподъемность: {total_capacity:.2f} тонн")
            print(f"Общая загрузка: {total_load:.2f} тонн")
            print(f"Общая доступная грузоподъемность: {total_available:.2f} тонн")
            
            if total_capacity > 0:
                utilization = total_load / total_capacity * 100
                print(f"Использование грузоподъемности: {utilization:.1f}%")
            
            # Топ 5 самых загруженных
            if vehicles:
                sorted_vehicles = sorted(vehicles, key=lambda v: v.current_load, reverse=True)
                print("\nТОП-5 самых загруженных транспортных средств:")
                for i, vehicle in enumerate(sorted_vehicles[:5], 1):
                    perc = vehicle.get_current_load_percentage()
                    print(f"{i}. {vehicle.vehicle_id} - {vehicle.current_load:.2f} тонн ({perc:.1f}%)")
        
        elif choice == "8":
            break
        
        else:
            print("\nНеверный выбор. Пожалуйста, выберите действие от 1 до 8.")


def manage_company_operations(company):
    """
    Управление операциями транспортной компании
    """
    while True:
        display_header(f"КОМПАНИЯ: {company.name}")
        
        print("1. Управление клиентами")
        print("2. Управление транспортом")
        print("3. Оптимизировать распределение грузов")
        print("4. Показать полную статистику")
        print("5. Просмотреть распределение грузов")
        print("6. Вернуться в главное меню")
        
        choice = input("\nВыберите действие (1-6): ").strip()
        
        if choice == "1":
            manage_clients_menu(company.clients)
        
        elif choice == "2":
            manage_vehicles_menu(company.vehicles, company.clients)
        
        elif choice == "3":
            if not company.clients:
                print("\n❌ Ошибка: нет клиентов для распределения.")
                continue
            if not company.vehicles:
                print("\n❌ Ошибка: нет транспортных средств.")
                continue
            
            display_header("ОПТИМИЗАЦИЯ РАСПРЕДЕЛЕНИЯ ГРУЗОВ")
            
            print("Выберите стратегию распределения:")
            print("1. Стандартная (VIP в первую очередь)")
            print("2. Минимизация транспорта")
            print("3. Сбалансированная загрузка")
            
            strategy = input("\nСтратегия (1-3): ").strip()
            
            if strategy == "1":
                print("\nИспользуется стандартная стратегия...")
                company.optimize_cargo_distribution()
            elif strategy == "2":
                print("\nМинимизация количества транспорта...")
                # Здесь можно добавить специальную логику
                company.optimize_cargo_distribution()
            elif strategy == "3":
                print("\nСбалансированная загрузка транспорта...")
                # Здесь можно добавить специальную логику
                company.optimize_cargo_distribution()
            else:
                print("Используется стандартная стратегия...")
                company.optimize_cargo_distribution()
        
        elif choice == "4":
            display_header(f"СТАТИСТИКА КОМПАНИИ '{company.name}'")
            print(company.get_statistics())
            
            # Дополнительная статистика
            if company.clients and company.vehicles:
                total_cargo = sum(c.cargo_weight for c in company.clients) / 1000  # в тоннах
                total_capacity = sum(v.capacity for v in company.vehicles)
                
                print(f"\n{'='*50}")
                print("АНАЛИЗ ЗАГРУЗКИ:")
                print(f"Общий вес грузов клиентов: {total_cargo:.2f} тонн")
                print(f"Общая грузоподъемность транспорта: {total_capacity:.2f} тонн")
                
                if total_capacity > 0:
                    coverage = total_cargo / total_capacity * 100
                    print(f"Покрытие грузоподъемности: {coverage:.1f}%")
                    
                    if coverage > 100:
                        print("⚠️  Внимание: общий вес грузов превышает грузоподъемность транспорта!")
                        needed = total_cargo - total_capacity
                        print(f"   Необходимо дополнительно: {needed:.2f} тонн грузоподъемности")
                    elif coverage < 50:
                        print("ℹ️  Информация: грузоподъемность используется менее чем на 50%")
        
        elif choice == "5":
            if not company.vehicles:
                print("\nНет транспортных средств для отображения распределения.")
                continue
            
            display_header("РАСПРЕДЕЛЕНИЕ ГРУЗОВ ПО ТРАНСПОРТУ")
            
            vehicles_with_load = [v for v in company.vehicles if v.clients_list]
            if not vehicles_with_load:
                print("Нет загруженного транспорта.")
            else:
                for vehicle in vehicles_with_load:
                    print(f"\n🚚 Транспорт: {vehicle.vehicle_id}")
                    print(f"   Тип: {getattr(vehicle, 'vehicle_type', 'Транспорт')}")
                    print(f"   Загрузка: {vehicle.current_load:.3f}/{vehicle.capacity:.3f} тонн")
                    print(f"   Процент: {vehicle.get_current_load_percentage():.1f}%")
                    
                    if vehicle.clients_list:
                        print("   Загруженные клиенты:")
                        for client in vehicle.clients_list:
                            vip = "★" if client.is_vip else "○"
                            print(f"     {vip} {client.name}: {client.cargo_weight:.2f} кг")
            
            # Общая статистика распределения
            total_vehicles_used = len(vehicles_with_load)
            total_clients_loaded = sum(len(v.clients_list) for v in vehicles_with_load)
            total_weight_loaded = sum(sum(c.cargo_weight for c in v.clients_list) for v in vehicles_with_load) / 1000
            
            print(f"\n{'='*50}")
            print("ИТОГИ РАСПРЕДЕЛЕНИЯ:")
            print(f"Использовано транспорта: {total_vehicles_used}/{len(company.vehicles)}")
            print(f"Загружено клиентов: {total_clients_loaded}/{len(company.clients)}")
            print(f"Загружено груза: {total_weight_loaded:.3f} тонн")
        
        elif choice == "6":
            break
        
        else:
            print("\nНеверный выбор. Пожалуйста, выберите действие от 1 до 6.")


def main():
    """
    Основная функция программы
    """
    display_header("ТРАНСПОРТНАЯ КОМПАНИЯ - СИСТЕМА УПРАВЛЕНИЯ")
    
    companies = []
    global_clients = []
    global_vehicles = []
    
    while True:
        display_header("ГЛАВНОЕ МЕНЮ")
        
        print("1. Управление клиентами")
        print("2. Управление транспортными средствами")
        print("3. Создать/управлять транспортной компанией")
        print("4. Быстрая оптимизация распределения")
        print("5. Экспорт данных")
        print("6. Выход")
        
        choice = input("\nВыберите действие (1-6): ").strip()
        
        if choice == "1":
            manage_clients_menu(global_clients)
        
        elif choice == "2":
            manage_vehicles_menu(global_vehicles, global_clients)
        
        elif choice == "3":
            display_header("ТРАНСПОРТНЫЕ КОМПАНИИ")
            
            print("1. Создать новую компанию")
            print("2. Выбрать существующую компанию")
            print("3. Просмотреть все компании")
            print("4. Импортировать клиентов в компанию")
            print("5. Импортировать транспорт в компанию")
            print("6. Вернуться в главное меню")
            
            sub_choice = input("\nВыберите действие (1-6): ").strip()
            
            if sub_choice == "1":
                company = create_company_interactive()
                if company:
                    companies.append(company)
            
            elif sub_choice == "2":
                if not companies:
                    print("\nНет созданных компаний.")
                    continue
                
                print("\nДОСТУПНЫЕ КОМПАНИИ:")
                for i, company in enumerate(companies, 1):
                    print(f"{i}. {company.name}")
                    print(f"   Клиентов: {len(company.clients)}")
                    print(f"   Транспорта: {len(company.vehicles)}")
                
                try:
                    idx = int(input("\nНомер компании: ")) - 1
                    if 0 <= idx < len(companies):
                        manage_company_operations(companies[idx])
                    else:
                        print("Неверный номер компании.")
                except ValueError:
                    print("Ошибка: введите номер.")
            
            elif sub_choice == "3":
                if companies:
                    display_header(f"ВСЕ КОМПАНИИ ({len(companies)})")
                    for i, company in enumerate(companies, 1):
                        print(f"\n{i}. {company.name}")
                        print(f"   Клиентов: {len(company.clients)}")
                        print(f"   Транспорта: {len(company.vehicles)}")
                        print(f"   Общая грузоподъемность: {sum(v.capacity for v in company.vehicles):.2f} тонн")
                else:
                    print("\nНет созданных компаний.")
            
            elif sub_choice == "4":
                if not companies:
                    print("\nНет созданных компаний.")
                    continue
                
                if not global_clients:
                    print("\nНет клиентов для импорта.")
                    continue
                
                print("\nВыберите компанию для импорта клиентов:")
                for i, company in enumerate(companies, 1):
                    print(f"{i}. {company.name} (клиентов: {len(company.clients)})")
                
                try:
                    company_idx = int(input("\nНомер компании: ")) - 1
                    if not (0 <= company_idx < len(companies)):
                        print("Неверный номер компании.")
                        continue
                    
                    company = companies[company_idx]
                    imported = 0
                    
                    for client in global_clients:
                        if company.add_client(client):
                            imported += 1
                    
                    print(f"\nИмпортировано {imported} клиентов в компанию '{company.name}'")
                    
                except ValueError:
                    print("Ошибка: введите номер.")
            
            elif sub_choice == "5":
                if not companies:
                    print("\nНет созданных компаний.")
                    continue
                
                if not global_vehicles:
                    print("\nНет транспорта для импорта.")
                    continue
                
                print("\nВыберите компанию для импорта транспорта:")
                for i, company in enumerate(companies, 1):
                    print(f"{i}. {company.name} (транспорта: {len(company.vehicles)})")
                
                try:
                    company_idx = int(input("\nНомер компании: ")) - 1
                    if not (0 <= company_idx < len(companies)):
                        print("Неверный номер компании.")
                        continue
                    
                    company = companies[company_idx]
                    imported = 0
                    
                    for vehicle in global_vehicles:
                        if company.add_vehicle(vehicle):
                            imported += 1
                    
                    print(f"\nИмпортировано {imported} транспортных средств в компанию '{company.name}'")
                    
                except ValueError:
                    print("Ошибка: введите номер.")
        
        elif choice == "4":
            display_header("БЫСТРАЯ ОПТИМИЗАЦИЯ РАСПРЕДЕЛЕНИЯ")
            
            if not global_clients:
                print("❌ Нет клиентов для распределения.")
                continue
            
            if not global_vehicles:
                print("❌ Нет транспортных средств.")
                continue
            
            # Создаем временную компанию для распределения
            temp_company = TransportCompany("Временная оптимизация")
            
            # Добавляем всех клиентов и транспорт
            for client in global_clients:
                temp_company.add_client(client)
            
            for vehicle in global_vehicles:
                temp_company.add_vehicle(vehicle)
            
            print(f"\n📊 Для распределения:")
            print(f"   Клиентов: {len(temp_company.clients)}")
            print(f"   Транспорта: {len(temp_company.vehicles)}")
            print(f"   Общий вес грузов: {sum(c.cargo_weight for c in temp_company.clients)/1000:.2f} тонн")
            print(f"   Общая грузоподъемность: {sum(v.capacity for v in temp_company.vehicles):.2f} тонн")
            
            confirm = input("\nНачать распределение? (да/нет): ").strip().lower()
            if confirm in ['да', 'д', 'yes', 'y']:
                temp_company.optimize_cargo_distribution()
            else:
                print("Распределение отменено.")
        
        elif choice == "5":
            display_header("ЭКСПОРТ ДАННЫХ")
            
            print("1. Экспорт списка клиентов")
            print("2. Экспорт списка транспорта")
            print("3. Экспорт распределения грузов")
            print("4. Вернуться в главное меню")
            
            export_choice = input("\nВыберите действие (1-4): ").strip()
            
            if export_choice == "1":
                if not global_clients:
                    print("\nНет клиентов для экспорта.")
                else:
                    print("\nСПИСОК КЛИЕНТОВ:")
                    print("Имя,Вес груза (кг),VIP статус")
                    for client in global_clients:
                        vip = "VIP" if client.is_vip else "Обычный"
                        print(f"{client.name},{client.cargo_weight:.2f},{vip}")
                    print(f"\nЭкспортировано {len(global_clients)} клиентов.")
            
            elif export_choice == "2":
                if not global_vehicles:
                    print("\nНет транспорта для экспорта.")
                else:
                    print("\nСПИСОК ТРАНСПОРТА:")
                    print("ID,Тип,Грузоподъемность (т),Текущая загрузка (т)")
                    for vehicle in global_vehicles:
                        vehicle_type = getattr(vehicle, 'vehicle_type', 'Транспорт')
                        print(f"{vehicle.vehicle_id},{vehicle_type},{vehicle.capacity:.2f},{vehicle.current_load:.2f}")
                    print(f"\nЭкспортировано {len(global_vehicles)} транспортных средств.")
            
            elif export_choice == "3":
                if not companies:
                    print("\nНет компаний с распределением грузов.")
                else:
                    print("\nРАСПРЕДЕЛЕНИЕ ГРУЗОВ:")
                    for company in companies:
                        print(f"\nКомпания: {company.name}")
                        for vehicle in company.vehicles:
                            if vehicle.clients_list:
                                print(f"  Транспорт {vehicle.vehicle_id}:")
                                for client in vehicle.clients_list:
                                    print(f"    - {client.name}: {client.cargo_weight:.2f} кг")
            
            elif export_choice == "4":
                continue
            
            else:
                print("\nНеверный выбор.")
        
        elif choice == "6":
            display_header("ВЫХОД ИЗ ПРОГРАММЫ")
            
            total_clients = len(global_clients) + sum(len(c.clients) for c in companies)
            total_vehicles = len(global_vehicles) + sum(len(c.vehicles) for c in companies)
            
            print(f"\n📈 ИТОГИ РАБОТЫ:")
            print(f"   Создано компаний: {len(companies)}")
            print(f"   Всего клиентов: {total_clients}")
            print(f"   Всего транспорта: {total_vehicles}")
            
            print("\nСпасибо за использование программы! До свидания!")
            break
        
        else:
            print("\nНеверный выбор. Пожалуйста, выберите действие от 1 до 6.")


if __name__ == "__main__":
    main()