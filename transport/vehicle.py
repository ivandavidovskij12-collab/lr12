import uuid
from typing import List
from .client import Client


class Vehicle:
    """Базовый класс для транспортного средства"""
    
    def __init__(self, capacity: float):
        """
        Инициализация транспортного средства
        
        Args:
            capacity (float): Грузоподъемность в тоннах
        """
        self.vehicle_id = self._generate_vehicle_id()
        self.capacity = self._validate_capacity(capacity)
        self.current_load = 0.0
        self.clients_list: List[Client] = []
    
    def _generate_vehicle_id(self) -> str:
        """
        Генерация уникального идентификатора транспортного средства
        
        Returns:
            str: Уникальный идентификатор
        """
        return str(uuid.uuid4())[:8]  # Берем первые 8 символов UUID
    
    def _validate_capacity(self, capacity: float) -> float:
        """
        Валидация грузоподъемности
        
        Args:
            capacity (float): Грузоподъемность для проверки
            
        Returns:
            float: Проверенная грузоподъемность
            
        Raises:
            ValueError: Если грузоподъемность отрицательная или равна нулю
            TypeError: Если грузоподъемность не является числом
        """
        if not isinstance(capacity, (int, float)):
            raise TypeError(f"Грузоподъемность должна быть числом, получен тип: {type(capacity)}")
        
        if capacity <= 0:
            raise ValueError(f"Грузоподъемность должна быть положительным числом. Получено: {capacity}")
        
        if capacity > 1000:  # Ограничение на максимальную грузоподъемность (1000 тонн)
            raise ValueError(f"Грузоподъемность слишком большая. Максимально допустимая грузоподъемность: 1000 тонн. Получено: {capacity}")
        
        return float(capacity)
    
    def _validate_client(self, client) -> None:
        """
        Валидация объекта клиента
        
        Args:
            client: Объект для проверки
            
        Raises:
            TypeError: Если объект не является экземпляром класса Client
        """
        if not isinstance(client, Client):
            raise TypeError(f"Ожидается объект класса Client, получен тип: {type(client)}")
    
    def _validate_cargo_weight(self, weight: float) -> None:
        """
        Валидация веса груза для загрузки
        
        Args:
            weight (float): Вес груза для проверки
            
        Raises:
            ValueError: Если вес отрицательный или равен нулю
        """
        if weight <= 0:
            raise ValueError(f"Вес груза должен быть положительным числом. Получено: {weight}")
    
    def can_load_cargo(self, cargo_weight: float) -> bool:
        """
        Проверка возможности загрузки груза
        
        Args:
            cargo_weight (float): Вес груза для проверки
            
        Returns:
            bool: True если груз можно загрузить, иначе False
        """
        weight_in_tons = cargo_weight / 1000  # Конвертируем кг в тонны
        return (self.current_load + weight_in_tons) <= self.capacity
    
    def load_cargo(self, client: Client) -> bool:
        """
        Загрузка груза клиента в транспортное средство
        
        Args:
            client (Client): Объект клиента
            
        Returns:
            bool: True если груз успешно загружен, False если превышена грузоподъемность
            
        Raises:
            TypeError: Если передан не объект класса Client
            ValueError: Если вес груза клиента некорректный
        """
        # Валидация входных данных
        self._validate_client(client)
        self._validate_cargo_weight(client.cargo_weight)
        
        # Конвертируем вес из кг в тонны
        cargo_weight_tons = client.cargo_weight / 1000
        
        # Проверка на превышение грузоподъемности
        if not self.can_load_cargo(client.cargo_weight):
            available_capacity = (self.capacity - self.current_load) * 1000  # Конвертируем обратно в кг
            print(f"Нельзя загрузить груз весом {client.cargo_weight:.2f} кг. "
                  f"Доступная грузоподъемность: {available_capacity:.2f} кг")
            return False
        
        # Загрузка груза
        self.current_load += cargo_weight_tons
        self.clients_list.append(client)
        
        print(f"Груз клиента '{client.name}' успешно загружен. "
              f"Вес: {client.cargo_weight:.2f} кг")
        print(f"Текущая загрузка: {self.current_load:.3f} тонн "
              f"({self.get_current_load_percentage():.1f}% от грузоподъемности)")
        
        return True
    
    def unload_cargo(self, client_name: str) -> bool:
        """
        Выгрузка груза клиента из транспортного средства
        
        Args:
            client_name (str): Имя клиента
            
        Returns:
            bool: True если груз успешно выгружен, False если клиент не найден
        """
        for i, client in enumerate(self.clients_list):
            if client.name.lower() == client_name.lower():
                cargo_weight_tons = client.cargo_weight / 1000
                self.current_load -= cargo_weight_tons
                if self.current_load < 0:
                    self.current_load = 0
                
                removed_client = self.clients_list.pop(i)
                print(f"Груз клиента '{removed_client.name}' успешно выгружен. "
                      f"Вес: {removed_client.cargo_weight:.2f} кг")
                return True
        
        print(f"Клиент с именем '{client_name}' не найден в списке загруженных клиентов")
        return False
    
    def get_current_load_percentage(self) -> float:
        """
        Получение процента текущей загрузки
        
        Returns:
            float: Процент загрузки (0-100)
        """
        if self.capacity == 0:
            return 0.0
        return (self.current_load / self.capacity) * 100
    
    def get_available_capacity(self) -> float:
        """
        Получение доступной грузоподъемности
        
        Returns:
            float: Доступная грузоподъемность в тоннах
        """
        return self.capacity - self.current_load
    
    def get_clients_info(self) -> str:
        """
        Получение информации о загруженных клиентах
        
        Returns:
            str: Информация о клиентах
        """
        if not self.clients_list:
            return "Нет загруженных клиентов"
        
        info_lines = [f"Загруженные клиенты ({len(self.clients_list)}):"]
        total_weight_kg = 0
        
        for i, client in enumerate(self.clients_list, 1):
            info_lines.append(f"{i}. {client.name}: {client.cargo_weight:.2f} кг "
                             f"{'(VIP)' if client.is_vip else ''}")
            total_weight_kg += client.cargo_weight
        
        info_lines.append(f"\nОбщий вес груза: {total_weight_kg:.2f} кг "
                         f"({total_weight_kg / 1000:.3f} тонн)")
        
        return "\n".join(info_lines)
    
    def __str__(self) -> str:
        """
        Строковое представление транспортного средства
        
        Returns:
            str: Информация о транспортном средстве
        """
        load_percentage = self.get_current_load_percentage()
        return (f"Транспорт ID: {self.vehicle_id}\n"
                f"Грузоподъемность: {self.capacity:.3f} тонн\n"
                f"Текущая загрузка: {self.current_load:.3f} тонн ({load_percentage:.1f}%)\n"
                f"Доступно: {self.get_available_capacity():.3f} тонн\n"
                f"Клиентов загружено: {len(self.clients_list)}")