### Changelog — 23 июня 2026
- ДобавленоДобавлен модуль core/modem с классами ModemController, ModemConfig, ModemException
- Добавлен класс Profiles с предопределенными профилями настроек (basic_3500, basic_4000, basic_4500, fhss_full, dsss_full, combat, stress)
- Создан скрипт test_profiles.py для последовательного тестирования всех профилей
- Добавлен механизм переподключения при потере связи с модемом (3 попытки с экспоненциальной задержкой 1с, 2с, 4с)
- Добавлены настройки переподключения в ReconnectConfig (attempts, delays, enabled, max_retry_per_command)
- Добавлен метод _attempt_reconnect() в ModemController для автоматического восстановления соединения
- Добавлена защита от бесконечной рекурсии при повторной отправке команды после переподключения
- Добавлен метод check_connection() для проверки доступности модема

Изменено
- Обновлена структура проекта: созданы папки core/modem, core/parser, core/emulator, core/tests, gui, ui, utils
- Перемещены файлы в соответствии с новой структурой: modem/ → core/modem/, parser_base.py → core/parser/base.py, rx_parser.py → core/parser/, tx_parser.py → core/parser/, command_emulator.py → core/emulator/
- Обновлены импорты в main.py и тестовых скриптах для новой структуры
- Модифицирован send_command(): добавлено автоматическое переподключение при SerialException
- Модифицирован apply_config(): проверка соединения перед применением
- Модифицирован get_config(): использование send_command() с обработкой ошибок
- Исправлена ошибка в send_command() при отключении модема: теперь не падает, а выбрасывает ModemConnectionError
- Обновлен test_modem.py: добавлен интерактивный выбор COM-порта
- Обновлен test_profiles.py: обработка ошибок при отключении модема

Улучшено
- : добавлен вывод всех попыток переподключения в консоль
- Обработка ошибок: корректное завершение при потере связи без падения программы