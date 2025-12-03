class Client:
    """Класс для представления клиента транспортной компании"""
    
    def __init__(self, name: str, cargo_weight: float, is_vip: bool = False):
        """
        Инициализация клиента
        
        Args:
            name (str): Имя клиента
            cargo_weight (float): Вес груза в килограммах
            is_vip (bool, optional): VIP-статус клиента. По умолчанию False.
        """
        self.name = self._validate_name(name)
        self.cargo_weight = self._validate_cargo_weight(cargo_weight)
        self.is_vip = self._validate_is_vip(is_vip)
    
    def _validate_name(self, name: str) -> str:
        """
        Валидация имени клиента
        
        Args:
            name (str): Имя клиента для проверки
            
        Returns:
            str: Проверенное имя
            
        Raises:
            ValueError: Если имя пустое или содержит только пробелы
        """
        if not isinstance(name, str):
            raise TypeError(f"Имя должно быть строкой, получен тип: {type(name)}")
        
        cleaned_name = name.strip()
        if not cleaned_name:
            raise ValueError("Имя клиента не может быть пустым")
        
        if len(cleaned_name) < 2:
            raise ValueError("Имя должно содержать минимум 2 символа")
        
        return cleaned_name
    
    def _validate_cargo_weight(self, weight: float) -> float:
        """
        Валидация веса груза
        
        Args:
            weight (float): Вес груза для проверки
            
        Returns:
            float: Проверенный вес
            
        Raises:
            ValueError: Если вес отрицательный или равен нулю
            TypeError: Если вес не является числом
        """
        if not isinstance(weight, (int, float)):
            raise TypeError(f"Вес должен быть числом, получен тип: {type(weight)}")
        
        if weight <= 0:
            raise ValueError(f"Вес груза должен быть положительным числом. Получено: {weight}")
        
        if weight > 100000:  # Ограничение на максимальный вес (100 тонн)
            raise ValueError(f"Вес груза слишком большой. Максимально допустимый вес: 100000 кг. Получено: {weight}")
        
        return float(weight)
    
    def _validate_is_vip(self, is_vip: bool) -> bool:
        """
        Валидация VIP-статуса
        
        Args:
            is_vip (bool): Статус для проверки
            
        Returns:
            bool: Проверенный статус
            
        Raises:
            TypeError: Если значение не является булевым
        """
        if not isinstance(is_vip, bool):
            raise TypeError(f"VIP-статус должен быть булевым значением, получен тип: {type(is_vip)}")
        
        return is_vip
    
    def update_cargo_weight(self, new_weight: float) -> None:
        """
        Обновление веса груза с валидацией
        
        Args:
            new_weight (float): Новый вес груза
        """
        self.cargo_weight = self._validate_cargo_weight(new_weight)
    
    def upgrade_to_vip(self) -> None:
        """Повышение клиента до VIP-статуса"""
        self.is_vip = True
    
    def downgrade_from_vip(self) -> None:
        """Понижение клиента из VIP-статуса"""
        self.is_vip = False
    
    def get_info(self) -> str:
        """
        Получение информации о клиенте в виде строки
        
        Returns:
            str: Информация о клиенте
        """
        vip_status = "VIP" if self.is_vip else "Обычный"
        return (f"Клиент: {self.name}\n"
                f"Вес груза: {self.cargo_weight:.2f} кг\n"
                f"Статус: {vip_status}")
    
    def __str__(self) -> str:
        """Строковое представление объекта"""
        vip_status = "VIP" if self.is_vip else "Обычный"
        return f"Client(name='{self.name}', cargo_weight={self.cargo_weight}, is_vip={self.is_vip})"