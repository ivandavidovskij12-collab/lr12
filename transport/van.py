from .vehicle import Vehicle


class Van(Vehicle):
    """Класс фургона, наследующий от Vehicle"""
    
    def __init__(self, capacity: float, is_refrigerated: bool = False):
        """
        Инициализация фургона
        
        Args:
            capacity (float): Грузоподъемность в тоннах
            is_refrigerated (bool, optional): Наличие холодильника. По умолчанию False.
        """
        super().__init__(capacity)
        self.is_refrigerated = self._validate_is_refrigerated(is_refrigerated)
        self.vehicle_type = "Фургон"
    
    def _validate_is_refrigerated(self, is_refrigerated: bool) -> bool:
        """
        Валидация флага наличия холодильника
        
        Args:
            is_refrigerated (bool): Флаг для проверки
            
        Returns:
            bool: Проверенный флаг
            
        Raises:
            TypeError: Если значение не является булевым
        """
        if not isinstance(is_refrigerated, bool):
            raise TypeError(f"Флаг наличия холодильника должен быть булевым значением, "
                          f"получен тип: {type(is_refrigerated)}")
        return is_refrigerated
    
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
        
        # Дополнительные проверки для фургона
        # Например, можно добавить проверки на температурные требования груза
        return True
    
    def get_refrigerator_info(self) -> str:
        """
        Получение информации о холодильнике
        
        Returns:
            str: Информация о холодильнике
        """
        return "С холодильником" if self.is_refrigerated else "Без холодильника"
    
    def __str__(self) -> str:
        """
        Строковое представление фургона
        
        Returns:
            str: Информация о фургоне
        """
        base_info = super().__str__()
        return (f"{base_info}\n"
                f"Тип: {self.vehicle_type}\n"
                f"Холодильник: {self.get_refrigerator_info()}")