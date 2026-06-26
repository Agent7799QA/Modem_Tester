"""
Управление параметрами модема Салангана-К3
Единый источник истины для всех параметров
"""

import re
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, field


@dataclass
class ParamDef:
    """Определение параметра"""
    command: str  # команда для отправки
    description: str  # описание для отображения
    param_type: str  # "list", "range", "toggle", "string"
    options: Optional[Any] = None  # список значений или {"min": X, "max": Y}
    default: Any = None  # значение по умолчанию


class ModemParameters:
    """
    Единый источник информации о параметрах модема
    """

    # ============================================================
    # СХЕМА ПАРАМЕТРОВ
    # ============================================================

    # Общие параметры для TX и RX
    COMMON_PARAMS = {
        "freq": ParamDef(
            command="freq",
            description="Central frequency (МГц)",
            param_type="list",
            options=[3500, 4000, 4500, 6500],
            default=3500
        ),
        "code": ParamDef(
            command="code",
            description="Channel code",
            param_type="range",
            options={"min": 1, "max": 24},
            default=11
        ),
        "fhss": ParamDef(
            command="fhss",
            description="FHSS mode",
            param_type="list",
            options=[0, 1, 2, 3, 4],
            default=0
        ),
        "dsss": ParamDef(
            command="dsss",
            description="DSSS mode",
            param_type="list",
            options=[0, 1, 2, 3, 4, 7],
            default=0
        ),
        "rate": ParamDef(
            command="rate",
            description="Link rate (Hz)",
            param_type="list",
            options=[5, 10, 25, 40, 50],
            default=50
        ),
        "attenuation": ParamDef(
            command="attenuation",
            description="Attenuation (dB)",
            param_type="range",
            options={"min": 0, "max": 30},
            default=0
        ),
        "address": ParamDef(
            command="address",
            description="Module address",
            param_type="range",
            options={"min": 0, "max": 65534},
            default=65535
        ),
        "pan": ParamDef(
            command="pan",
            description="Network address",
            param_type="range",
            options={"min": 0, "max": 65534},
            default=56064
        ),
        "baudrate": ParamDef(
            command="baudrate",
            description="Baudrate",
            param_type="list",
            options=[57600, 100000, 115200, 400000, 420000],
            default=420000
        ),
        "parity": ParamDef(
            command="parity",
            description="Parity",
            param_type="list",
            options=["none", "even", "odd"],
            default="none"
        ),
        "stopbits": ParamDef(
            command="stopbits",
            description="Stop bits",
            param_type="list",
            options=[1, 2],
            default=1
        ),
        "mode": ParamDef(
            command="mode",
            description="Mode",
            param_type="list",
            options=["swarm+", "swarm", "longrange", "100kbps"],
            default="longrange"
        ),
        "protocol": ParamDef(
            command="protocol",
            description="Protocol",
            param_type="list",
            options=["crsf", "sbus", "mavlink", "raw"],
            default="crsf"
        ),
        "timeslot": ParamDef(
            command="timeslot",
            description="Time slotting",
            param_type="list",
            options=[0, 1, 2],
            default=0
        ),
        "trim": ParamDef(
            command="trim",
            description="Crystal trim (calibration)",
            param_type="range",
            options={"min": 0, "max": 255},
            default=111
        ),
        "invert": ParamDef(
            command="invert",
            description="Inversion (toggle)",
            param_type="toggle",
            options=None,
            default=False
        ),
        "led": ParamDef(
            command="led",
            description="LED (on/off)",
            param_type="list",
            options=["on", "off"],
            default="on"
        ),
        "extmode": ParamDef(
            command="extmode",
            description="External mode",
            param_type="list",
            options=["off", "bk", "drop", "rssi"],
            default="off"
        ),
        "extpinmode0": ParamDef(
            command="extpinmode0",
            description="Pin 0 mode",
            param_type="list",
            options=["off", "pwm", "servo", "mg90s", "syncout", "debug"],
            default="off"
        ),
        "extpindep0": ParamDef(
            command="extpindep0",
            description="Pin 0 dependency",
            param_type="range",
            options={"min": 1, "max": 70},
            default=13
        ),
        "extpinmode1": ParamDef(
            command="extpinmode1",
            description="Pin 1 mode",
            param_type="list",
            options=["off", "pwm", "servo", "mg90s", "syncout", "debug"],
            default="off"
        ),
        "extpindep1": ParamDef(
            command="extpindep1",
            description="Pin 1 dependency",
            param_type="range",
            options={"min": 1, "max": 70},
            default=14
        ),
    }

    # TX-специфичные параметры
    TX_ONLY_PARAMS = {
        "ack": ParamDef(
            command="ack",
            description="Acknowledge (0=off, 1=on)",
            param_type="list",
            options=[0, 1],
            default=1
        ),
        "ttl": ParamDef(
            command="ttl",
            description="Retransmissions (0=off, 1=on)",
            param_type="list",
            options=[0, 1],
            default=0
        ),
        "max_clients": ParamDef(
            command="max_clients",
            description="Max clients",
            param_type="range",
            options={"min": 1, "max": 8},
            default=1
        ),
    }

    # RX-специфичные параметры
    RX_ONLY_PARAMS = {
        "bind": ParamDef(
            command="bind",
            description="Binded address",
            param_type="range",
            options={"min": 0, "max": 65535},
            default=0
        ),
        "ewtests": ParamDef(
            command="ewtests",
            description="EW tests (0=off, 1=on)",
            param_type="list",
            options=[0, 1],
            default=0
        ),
    }

    # Паттерны для парсинга print
    PRINT_PATTERNS = {
        "protocol": r"RC protocol:\s+(\w+)",
        "freq": r"Central frequency:\s*(\d+)",
        "code": r"Channel code:\s*(\d+)",
        "attenuation": r"Attenuation:\s*(\d+)\s+dB",
        "address": r"Module address:\s*(\d+)",
        "pan": r"Network address:\s*(\d+)",
        "bind": r"Binded address:\s*(\d+)",
        "rate": r"Link rate:\s*(\d+)",
        "fhss": r"FHSS mode:\s*(\d+)",
        "dsss": r"DSSS mode:\s*(\d+)",
        "mode": r"Mode:\s*([\w\s]+?)(?:\n|$|\r)",
        "type": r"Drone RC \(([A-Z]+)\)",
        "baudrate": r"Baudrate:\s*(\d+)",
        "parity": r"Parity:\s*(\w+)",
        "stopbits": r"Stop bits:\s*(\d+)",
        "timeslot": r"Time slotting:\s*(\w+)",
        "ttl": r"Retransmissions:\s*(\w+)",
        "ack": r"Acknowledge:\s*(\w+)",
        "ewtests": r"EW tests:\s*(\w+)",
        "trim": r"Crystal trim:\s*(\d+)",
        "led": r"Onboard LED is (ON|OFF)",
        "max_clients": r"Max clients:\s*(\d+)",
        "extmode": r"Interface mode:\s*(\w+)",
        "extpinmode0": r"Pin 0:\s*Mode:\s*(\w+)",
        "extpindep0": r"Pin 0:\s*Dependency:\s*(\d+)",
        "extpinmode1": r"Pin 1:\s*Mode:\s*(\w+)",
        "extpindep1": r"Pin 1:\s*Dependency:\s*(\d+)",
    }

    @classmethod
    def get_all_params(cls, modem_type: str) -> Dict[str, ParamDef]:
        """
        Получить все параметры для типа модема

        Args:
            modem_type: "TX" или "RX"

        Returns:
            Dict[str, ParamDef]: Словарь параметров
        """
        params = cls.COMMON_PARAMS.copy()

        if modem_type == "TX":
            params.update(cls.TX_ONLY_PARAMS)
        elif modem_type == "RX":
            params.update(cls.RX_ONLY_PARAMS)

        return params

    @classmethod
    def get_param_names(cls, modem_type: str) -> List[str]:
        """Получить список имён параметров для типа модема"""
        return list(cls.get_all_params(modem_type).keys())

    @classmethod
    def get_param_def(cls, param_name: str) -> Optional[ParamDef]:
        """Получить определение параметра по имени"""
        for params in [cls.COMMON_PARAMS, cls.TX_ONLY_PARAMS, cls.RX_ONLY_PARAMS]:
            if param_name in params:
                return params[param_name]
        return None

    @classmethod
    def validate_value(cls, param_name: str, value: Any) -> bool:
        """
        Проверить, что значение допустимо для параметра

        Args:
            param_name: Имя параметра
            value: Значение для проверки

        Returns:
            bool: True если значение допустимо
        """
        param_def = cls.get_param_def(param_name)
        if not param_def:
            return False

        if param_def.param_type == "list":
            return value in param_def.options

        elif param_def.param_type == "range":
            options = param_def.options
            return options["min"] <= value <= options["max"]

        elif param_def.param_type == "toggle":
            return isinstance(value, bool)

        return True

    @classmethod
    def format_options(cls, param_name: str) -> str:
        """Форматировать варианты для отображения"""
        param_def = cls.get_param_def(param_name)
        if not param_def:
            return ""

        if param_def.param_type == "list":
            return ", ".join(str(o) for o in param_def.options)
        elif param_def.param_type == "range":
            return f"{param_def.options['min']}-{param_def.options['max']}"
        elif param_def.param_type == "toggle":
            return "toggle (on/off)"
        return ""

    @classmethod
    def parse_print_output(cls, output: str) -> Dict:
        """
        Парсинг вывода команды print

        Args:
            output: Вывод команды print

        Returns:
            Dict: Распарсенные настройки
        """
        config = {}

        for key, pattern in cls.PRINT_PATTERNS.items():
            match = re.search(pattern, output, re.IGNORECASE)
            if match:
                value = match.group(1).strip()

                if value.isdigit():
                    config[key] = int(value)
                elif value.lower() in ["enable", "enabled", "on"]:
                    config[key] = 1
                elif value.lower() in ["disable", "disabled", "off"]:
                    config[key] = 0
                else:
                    config[key] = value

        # led: ON/OFF → 1/0
        if "led" in config:
            config["led"] = 1 if config["led"] == "ON" else 0

        # inverted: определяем из текста
        if "Not inverted" in output:
            config["inverted"] = False
        elif "Inverted" in output:
            config["inverted"] = True

        return config

    @classmethod
    def parse_stat_output(cls, output: str) -> Dict:
        """
        Парсинг вывода команды stat

        Формат:
            Uplink LQ : 100, UplinkRSSI : 94dBm, DownlinkLQ : 100, DownlinkRSSI : 100dBm

        Returns:
            Dict: {"uplink_lq", "uplink_rssi", "downlink_lq", "downlink_rssi"}
        """
        result = {}

        patterns = {
            "uplink_lq": r"Uplink LQ\s*:\s*(\d+)",
            "uplink_rssi": r"UplinkRSSI\s*:\s*(-?\d+)",
            "downlink_lq": r"DownlinkLQ\s*:\s*(\d+)",
            "downlink_rssi": r"DownlinkRSSI\s*:\s*(-?\d+)",
        }

        for key, pattern in patterns.items():
            match = re.search(pattern, output)
            if match:
                result[key] = int(match.group(1))

        return result

    @classmethod
    def get_default_config(cls, modem_type: str) -> Dict:
        """
        Получить конфигурацию по умолчанию для типа модема

        Args:
            modem_type: "TX" или "RX"

        Returns:
            Dict: Словарь со значениями по умолчанию
        """
        config = {}
        for name, param_def in cls.get_all_params(modem_type).items():
            if param_def.default is not None:
                config[name] = param_def.default
        return config