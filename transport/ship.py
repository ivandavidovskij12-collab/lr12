from .vehicle import Vehicle


class Ship(Vehicle):
    """Класс судна, наследующий от Vehicle"""
    
    def __init__(self, capacity: float, name: str):
        """
        Инициализация судна
        
        Args:
            capacity (float): Грузоподъемность в тоннах
            name (str): Название судна
        """
        super().__init__(capacity)
        self.name = self._validate_name(name)
        self.vehicle_type = "Судно"
    
    def _validate_name(self, name: str) -> str:
        """
        Валидация названия судна
        
        Args:
            name (str): Название для проверки
            
        Returns:
            str: Проверенное название
            
        Raises:
            ValueError: Если название пустое или содержит только пробелы
        """
        if not isinstance(name, str):
            raise TypeError(f"Название должно быть строкой, получен тип: {type(name)}")
        
        cleaned_name = name.strip()
        if not cleaned_name:
            raise ValueError("Название судна не может быть пустым")
        
        if len(cleaned_name) < 2:
            raise ValueError("Название должно содержать минимум 2 символа")
        
        return cleaned_name
    
    def can_transport(self, client) -> bool:
        """
        Проверка возможности транспортировки груза клиента
        
        Args:
            client: Объект клиента
            
        Returns:
            bool: True если можно транспортировать
        """
        # Базовая проверка грузоподъемности
        if not self.can_load_cargo(client.cargo_weight):
            return False
        
        # Дополнительные проверки для судна
        # Например, можно добавить проверки на морскую транспортировку
        return True
    
    def __str__(self) -> str:
        """
        Строковое представление судна
        
        Returns:
            str: Информация о судне
        """
        base_info = super().__str__()
        return (f"{base_info}\n"
                f"Тип: {self.vehicle_type}\n"
                f"Название: {self.name}")