"""
Исключения для работы с модемом Салангана-К3
"""


class ModemError(Exception):
    """Базовое исключение для ошибок модема"""
    pass


class ModemConnectionError(ModemError):
    """Ошибка подключения к модему"""
    pass


class ModemCommandError(ModemError):
    """Ошибка выполнения команды"""
    pass


class ModemTimeoutError(ModemError):
    """Таймаут при выполнении команды"""
    pass


class ModemConfigError(ModemError):
    """Ошибка конфигурации модема"""
    pass


class ModemNotConnectedError(ModemError):
    """Попытка выполнить операцию без подключения"""
    pass
