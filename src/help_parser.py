"""
Парсинг help модема для извлечения команд и их вариантов
"""

import re
from typing import Dict, List, Union, Optional, Tuple
from dataclasses import dataclass


@dataclass
class ParamInfo:
    """Информация о параметре из help"""
    command: str
    description: str
    param_type: str  # "list", "range", "toggle"
    options: Union[List, Dict]
    current_value: Optional[any] = None
    help_line: str = ""


class HelpParser:
    """
    Парсинг help для извлечения команд и их вариантов
    """

    # Паттерны для извлечения
    PATTERN_COMMAND = r"\.([A-Za-z\s]+):\s+(\w+)\s+X"
    PATTERN_LIST = r"X is ([,\d\s]+)"
    PATTERN_OR_LIST = r"X is (\w+), (\w+) or (\w+)"
    PATTERN_RANGE = r"from (\d+) to (\d+)"
    PATTERN_OPTION_LINE = r"\.\.(\d+)\s+-"
    PATTERN_TOGGLE = r"Inversion:\s+(\w+)"

    @staticmethod
    def parse(help_response: str) -> Dict[str, ParamInfo]:
        """
        Извлечь информацию о параметрах из help

        Args:
            help_response: Ответ модема на команду help

        Returns:
            Dict[command, ParamInfo]
        """
        result = {}
        lines = help_response.split('\n')

        i = 0
        while i < len(lines):
            line = lines[i].strip()

            # Ищем строки с командами
            match = re.search(HelpParser.PATTERN_COMMAND, line)
            if match:
                description = match.group(1).strip()
                command = match.group(2).strip()

                # Определяем тип и варианты
                param_type, options = HelpParser._extract_options(line, lines, i)

                result[command] = ParamInfo(
                    command=command,
                    description=description,
                    param_type=param_type,
                    options=options,
                    help_line=line
                )

            i += 1

        return result

    @staticmethod
    def _extract_options(line: str, lines: List[str], index: int) -> Tuple[str, Union[List, Dict]]:
        """
        Извлечь варианты из строки

        Returns:
            Tuple[str, Union[List, Dict]]: (тип, варианты)
        """
        # Проверяем список значений
        match = re.search(HelpParser.PATTERN_LIST, line)
        if match:
            values_str = match.group(1)
            # Извлекаем числа
            values = re.findall(r'\d+', values_str)
            if values:
                return "list", [int(v) for v in values]

        # Проверяем OR-список
        match = re.search(HelpParser.PATTERN_OR_LIST, line)
        if match:
            return "list", [match.group(1), match.group(2), match.group(3)]

        # Проверяем диапазон
        match = re.search(HelpParser.PATTERN_RANGE, line)
        if match:
            return "range", {"min": int(match.group(1)), "max": int(match.group(2))}

        # Проверяем toggle (invert)
        if "invert" in line.lower():
            return "toggle", {}

        # Проверяем fhss/dsss (список с описанием на следующих строках)
        if "fhss" in line.lower() or "dsss" in line.lower():
            options = HelpParser._extract_option_lines(lines, index)
            if options:
                return "list", options

        # По умолчанию — строка (свободный ввод)
        return "string", {}

    @staticmethod
    def _extract_option_lines(lines: List[str], start_index: int) -> List[int]:
        """
        Извлечь варианты из строк вида "..0 - ...", "..1 - ..."
        """
        options = []
        i = start_index + 1

        while i < len(lines):
            line = lines[i].strip()
            match = re.search(HelpParser.PATTERN_OPTION_LINE, line)
            if match:
                options.append(int(match.group(1)))
                i += 1
            else:
                break

        return options