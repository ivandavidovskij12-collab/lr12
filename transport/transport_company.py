from typing import List, Dict, Tuple
from .client import Client
from .vehicle import Vehicle
from .van import Van
from .ship import Ship


class TransportCompany:
    """Класс транспортной компании"""
    
    def __init__(self, name: str):
        """
        Инициализация транспортной компании
        
        Args:
            name (str): Название компании
        """
        self.name = self._validate_name(name)
        self.vehicles: List[Vehicle] = []
        self.clients: List[Client] = []
    
    def _validate_name(self, name: str) -> str:
        """
        Валидация названия компании
        
        Args:
            name (str): Название для проверки
            
        Returns:
            str: Проверенное название
            
        Raises:
            ValueError: Если название пустое
        """
        if not isinstance(name, str):
            raise TypeError(f"Название компании должно быть строкой, получен тип: {type(name)}")
        
        cleaned_name = name.strip()
        if not cleaned_name:
            raise ValueError("Название компании не может быть пустым")
        
        return cleaned_name
    
    def _validate_vehicle(self, vehicle) -> None:
        """
        Валидация транспортного средства
        
        Args:
            vehicle: Объект для проверки
            
        Raises:
            TypeError: Если объект не является транспортным средством
        """
        if not isinstance(vehicle, Vehicle):
            raise TypeError(f"Ожидается объект класса Vehicle или его наследника, "
                          f"получен тип: {type(vehicle)}")
    
    def _validate_client(self, client) -> None:
        """
        Валидация клиента
        
        Args:
            client: Объект для проверки
            
        Raises:
            TypeError: Если объект не является клиентом
        """
        if not isinstance(client, Client):
            raise TypeError(f"Ожидается объект класса Client, получен тип: {type(client)}")
    
    def add_vehicle(self, vehicle: Vehicle) -> bool:
        """
        Добавление транспортного средства в компанию
        
        Args:
            vehicle (Vehicle): Транспортное средство
            
        Returns:
            bool: True если успешно добавлено, False если уже существует
        """
        try:
            self._validate_vehicle(vehicle)
            
            # Проверка на дубликат (по ID)
            for existing_vehicle in self.vehicles:
                if existing_vehicle.vehicle_id == vehicle.vehicle_id:
                    print(f"Транспортное средство с ID {vehicle.vehicle_id} уже существует в компании")
                    return False
            
            self.vehicles.append(vehicle)
            print(f"Транспортное средство {vehicle.vehicle_id} успешно добавлено в компанию '{self.name}'")
            return True
            
        except (TypeError, ValueError) as e:
            print(f"Ошибка при добавлении транспортного средства: {e}")
            return False
    
    def add_client(self, client: Client) -> bool:
        """
        Добавление клиента в компанию
        
        Args:
            client (Client): Клиент
            
        Returns:
            bool: True если успешно добавлен, False если уже существует
        """
        try:
            self._validate_client(client)
            
            # Проверка на дубликат (по имени)
            for existing_client in self.clients:
                if existing_client.name.lower() == client.name.lower():
                    print(f"Клиент с именем '{client.name}' уже существует в компании")
                    return False
            
            self.clients.append(client)
            print(f"Клиент '{client.name}' успешно добавлен в компанию '{self.name}'")
            return True
            
        except (TypeError, ValueError) as e:
            print(f"Ошибка при добавлении клиента: {e}")
            return False
    
    def remove_vehicle(self, vehicle_id: str) -> bool:
        """
        Удаление транспортного средства из компании
        
        Args:
            vehicle_id (str): ID транспортного средства
            
        Returns:
            bool: True если успешно удалено, False если не найдено
        """
        for i, vehicle in enumerate(self.vehicles):
            if vehicle.vehicle_id == vehicle_id:
                removed_vehicle = self.vehicles.pop(i)
                print(f"Транспортное средство {removed_vehicle.vehicle_id} удалено из компании")
                return True
        
        print(f"Транспортное средство с ID {vehicle_id} не найдено")
        return False
    
    def remove_client(self, client_name: str) -> bool:
        """
        Удаление клиента из компании
        
        Args:
            client_name (str): Имя клиента
            
        Returns:
            bool: True если успешно удален, False если не найден
        """
        for i, client in enumerate(self.clients):
            if client.name.lower() == client_name.lower():
                removed_client = self.clients.pop(i)
                print(f"Клиент '{removed_client.name}' удален из компании")
                return True
        
        print(f"Клиент с именем '{client_name}' не найден")
        return False
    
    def list_vehicles(self) -> str:
        """
        Получение списка всех транспортных средств
        
        Returns:
            str: Строка с информацией о транспортных средствах
        """
        if not self.vehicles:
            return f"В компании '{self.name}' нет транспортных средств"
        
        result = [f"ТРАНСПОРТНЫЕ СРЕДСТВА КОМПАНИИ '{self.name}' ({len(self.vehicles)} шт.):"]
        result.append("=" * 60)
        
        for i, vehicle in enumerate(self.vehicles, 1):
            vehicle_type = getattr(vehicle, 'vehicle_type', 'Транспорт')
            result.append(f"{i}. {vehicle_type} (ID: {vehicle.vehicle_id})")
            result.append(f"   Грузоподъемность: {vehicle.capacity:.3f} тонн")
            result.append(f"   Текущая загрузка: {vehicle.current_load:.3f} тонн")
            
            # Добавляем специфическую информацию для разных типов транспорта
            if isinstance(vehicle, Van):
                result.append(f"   Холодильник: {'Да' if vehicle.is_refrigerated else 'Нет'}")
            elif isinstance(vehicle, Ship):
                result.append(f"   Название: {vehicle.name}")
            
            result.append("-" * 40)
        
        total_capacity = sum(v.capacity for v in self.vehicles)
        total_load = sum(v.current_load for v in self.vehicles)
        result.append(f"\nИтого: {len(self.vehicles)} транспортных средств")
        result.append(f"Общая грузоподъемность: {total_capacity:.3f} тонн")
        result.append(f"Общая загрузка: {total_load:.3f} тонн ({total_load/total_capacity*100:.1f}%)" if total_capacity > 0 else "Общая загрузка: 0 тонн")
        
        return "\n".join(result)
    
    def list_clients(self) -> str:
        """
        Получение списка всех клиентов
        
        Returns:
            str: Строка с информацией о клиентах
        """
        if not self.clients:
            return f"В компании '{self.name}' нет клиентов"
        
        result = [f"КЛИЕНТЫ КОМПАНИИ '{self.name}' ({len(self.clients)} чел.):"]
        result.append("=" * 60)
        
        vip_clients = [c for c in self.clients if c.is_vip]
        regular_clients = [c for c in self.clients if not c.is_vip]
        
        if vip_clients:
            result.append("\nVIP КЛИЕНТЫ:")
            for i, client in enumerate(vip_clients, 1):
                result.append(f"{i}. {client.name}")
                result.append(f"   Вес груза: {client.cargo_weight:.2f} кг")
        
        if regular_clients:
            result.append("\nОБЫЧНЫЕ КЛИЕНТЫ:")
            start_num = len(vip_clients) + 1 if vip_clients else 1
            for i, client in enumerate(regular_clients, start_num):
                result.append(f"{i}. {client.name}")
                result.append(f"   Вес груза: {client.cargo_weight:.2f} кг")
        
        total_weight = sum(c.cargo_weight for c in self.clients)
        result.append(f"\nИтого: {len(self.clients)} клиентов")
        result.append(f"VIP клиентов: {len(vip_clients)}")
        result.append(f"Общий вес грузов: {total_weight:.2f} кг ({total_weight/1000:.3f} тонн)")
        
        return "\n".join(result)
    
    def get_available_vehicles(self) -> List[Vehicle]:
        """
        Получение списка доступных транспортных средств
        
        Returns:
            List[Vehicle]: Список транспортных средств с доступной грузоподъемностью
        """
        available_vehicles = []
        for vehicle in self.vehicles:
            if vehicle.get_available_capacity() > 0:
                available_vehicles.append(vehicle)
        return available_vehicles
    
    def optimize_cargo_distribution(self) -> Dict[str, List[Tuple[Client, float]]]:
        """
        Оптимальное распределение грузов клиентов по транспортным средствам
        
        Returns:
            Dict: Словарь с распределением {vehicle_id: [(client, weight), ...]}
        """
        print("\n" + "="*60)
        print(f"НАЧАЛО ОПТИМИЗАЦИИ РАСПРЕДЕЛЕНИЯ ГРУЗОВ")
        print("="*60)
        
        # Сбрасываем текущую загрузку всех транспортных средств
        for vehicle in self.vehicles:
            vehicle.current_load = 0.0
            vehicle.clients_list.clear()
        
        # Сортируем клиентов: VIP в первую очередь, затем по убыванию веса
        sorted_clients = sorted(self.clients, 
                              key=lambda c: (not c.is_vip, -c.cargo_weight))
        
        distribution = {}
        unloaded_clients = []
        total_cargo_weight = sum(c.cargo_weight for c in self.clients)
        
        print(f"Всего груза для распределения: {total_cargo_weight:.2f} кг")
        print(f"Клиентов для распределения: {len(self.clients)}")
        
        for client in sorted_clients:
            loaded = False
            
            # Пробуем загрузить в уже частично заполненный транспорт
            for vehicle in self.vehicles:
                if vehicle.can_load_cargo(client.cargo_weight):
                    vehicle.load_cargo(client)
                    if vehicle.vehicle_id not in distribution:
                        distribution[vehicle.vehicle_id] = []
                    distribution[vehicle.vehicle_id].append((client, client.cargo_weight))
                    loaded = True
                    print(f"✓ Груз клиента '{client.name}' ({client.cargo_weight} кг) "
                          f"загружен в транспорт {vehicle.vehicle_id}")
                    break
            
            # Если не удалось загрузить, оставляем для следующей итерации
            if not loaded:
                unloaded_clients.append(client)
        
        # Вывод результатов распределения
        print("\n" + "="*60)
        print("РЕЗУЛЬТАТЫ РАСПРЕДЕЛЕНИЯ")
        print("="*60)
        
        total_loaded_weight = 0
        used_vehicles = 0
        
        for vehicle_id, clients_list in distribution.items():
            vehicle = next(v for v in self.vehicles if v.vehicle_id == vehicle_id)
            vehicle_weight = sum(weight for _, weight in clients_list)
            total_loaded_weight += vehicle_weight
            
            print(f"\nТранспорт {vehicle_id}:")
            print(f"  Загружено груза: {vehicle_weight:.2f} кг ({vehicle.current_load:.3f} тонн)")
            print(f"  Клиентов: {len(clients_list)}")
            
            for client, weight in clients_list:
                vip_status = "VIP" if client.is_vip else "Обычный"
                print(f"    - {client.name}: {weight:.2f} кг ({vip_status})")
            
            used_vehicles += 1
        
        if unloaded_clients:
            print(f"\nНЕ ЗАГРУЖЕННЫЕ КЛИЕНТЫ ({len(unloaded_clients)}):")
            for client in unloaded_clients:
                vip_status = "VIP" if client.is_vip else "Обычный"
                print(f"  - {client.name}: {client.cargo_weight:.2f} кг ({vip_status})")
        
        # Статистика
        print("\n" + "="*60)
        print("СТАТИСТИКА РАСПРЕДЕЛЕНИЯ")
        print("="*60)
        print(f"Всего груза: {total_cargo_weight:.2f} кг")
        print(f"Распределено груза: {total_loaded_weight:.2f} кг ({total_loaded_weight/total_cargo_weight*100:.1f}%)")
        print(f"Использовано транспорта: {used_vehicles} из {len(self.vehicles)}")
        
        if unloaded_clients:
            unloaded_weight = sum(c.cargo_weight for c in unloaded_clients)
            print(f"Не распределено груза: {unloaded_weight:.2f} кг")
            print("Причина: недостаточная грузоподъемность доступного транспорта")
        
        return distribution
    
    def get_statistics(self) -> str:
        """
        Получение статистики компании
        
        Returns:
            str: Статистика в виде строки
        """
        total_capacity = sum(v.capacity for v in self.vehicles) * 1000  # в кг
        total_load = sum(v.current_load for v in self.vehicles) * 1000  # в кг
        total_clients_weight = sum(c.cargo_weight for c in self.clients)
        vip_clients_count = sum(1 for c in self.clients if c.is_vip)
        
        stats = [
            f"СТАТИСТИКА КОМПАНИИ '{self.name}'",
            "=" * 50,
            f"Клиентов: {len(self.clients)}",
            f"  - VIP: {vip_clients_count}",
            f"  - Обычные: {len(self.clients) - vip_clients_count}",
            f"Общий вес грузов клиентов: {total_clients_weight:.2f} кг",
            "",
            f"Транспортных средств: {len(self.vehicles)}",
            f"Общая грузоподъемность: {total_capacity:.2f} кг",
            f"Текущая загрузка: {total_load:.2f} кг",
        ]
        
        if total_capacity > 0:
            utilization = (total_load / total_capacity) * 100
            stats.append(f"Использование грузоподъемности: {utilization:.1f}%")
        
        # Распределение по типам транспорта
        van_count = sum(1 for v in self.vehicles if isinstance(v, Van))
        ship_count = sum(1 for v in self.vehicles if isinstance(v, Ship))
        other_count = len(self.vehicles) - van_count - ship_count
        
        stats.extend([
            "",
            "РАСПРЕДЕЛЕНИЕ ТРАНСПОРТА:",
            f"  Фургоны: {van_count}",
            f"  Судна: {ship_count}",
            f"  Другие: {other_count}"
        ])
        
        return "\n".join(stats)
    
    def __str__(self) -> str:
        """
        Строковое представление компании
        
        Returns:
            str: Информация о компании
        """
        return (f"Транспортная компания: {self.name}\n"
                f"Клиентов: {len(self.clients)}\n"
                f"Транспортных средств: {len(self.vehicles)}")