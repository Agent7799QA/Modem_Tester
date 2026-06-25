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

# TODO
    # Отдельный конфигурационный файл для профилей
    # сохранение, загрузка дефолтного по завершении тестов
    # ПРОВЕРИТЬ REBOOT КОГДА И ГДЕ
    # настройки ком порта не забыть при инициализации
    # прочитать crossfire протокол, стандартные настройки com porta, пинг, архитектура пакета, тип и т.д.

✅ Добавлено
### Core / Модем
- Добавлен модуль core/modem/scanner.py с классом ModemScanner для автоматического обнаружения модемов и определения их типа (RX/TX) через команду help
- Добавлены структуры данных ModemInfo, ModemType, PortType для хранения информации о найденных модемах
- Добавлен метод stat() в ModemController для получения телеметрии через команду stat
Добавлен метод _parse_stat_output() для парсинга ответа stat (UplinkLQ, UplinkRSSI, DownlinkLQ, DownlinkRSSI)
Добавлен метод _attempt_reconnect() с экспоненциальной задержкой (1с, 2с, 4с) для автоматического восстановления соединения
Добавлена защита от бесконечной рекурсии при повторной отправке команды после переподключения
Добавлена поддержка параметра inverted в apply_config() как toggle-команды (с проверкой текущего состояния)
Добавлен парсинг всех параметров из print в _parse_print_output(): baudrate, parity, stopbits, timeslot, ttl, ack, ewtests, trim, mode, type, inverted

 - bправлен парсинг mode — убраны артефакты \r\n\tLink rate

Синхронизация
Добавлен модуль core/synchronizer.py с классом ModemSynchronizer для настройки RX по образу TX

Реализована логика формирования rx_config из tx_config + rx_overrides с автоматическим добавлением bind = tx_config["address"]

Добавлен метод sync_from_config() — применение конфигурации к TX и RX

Добавлен метод sync_from_modem() — чтение настроек с TX модема и синхронизация RX

Верификация
Добавлен модуль core/verifier.py с классом ModemVerifier для проверки синхронизации модемов

Реализована проверка ключевых параметров (freq, code, fhss, dsss, rate, pan, protocol)

Реализована проверка bind (RX.bind == TX.address)

Добавлен метод print_verification_report() для красивого вывода отчёта

Конфигурация
Добавлен модуль core/config_loader.py для загрузки/сохранения JSON-конфигурации

Добавлен файл config/setup.json с настройками по умолчанию

Создана структура: tx_config (основа), rx_overrides (переопределения для RX), test (параметры теста)

Тесты
Добавлен core/tests/test_scanner.py — тест автоматического определения портов

Добавлен core/tests/test_verify.py — тест проверки синхронизации

🔧 Изменено
Core / Модем
Модифицирован send_command(): добавлено автоматическое переподключение при SerialException

Модифицирован apply_config(): поддержка всех параметров, включая inverted как toggle

Обновлён _parse_print_output(): добавлены все параметры из реального вывода print

Исправлен парсинг mode — теперь возвращает чистое значение без артефактов

🐛 Исправлено
Исправлена ошибка в send_command() при физическом отключении модема — теперь не падает, а выбрасывает ModemConnectionError
Исправлен парсинг mode — убраны лишние символы \r\n\tLink rate
Исправлена проблема с inverted: теперь проверяется текущее состояние перед применением

📁 Структура проекта
Обновлена структура каталогов:

````
src/
├── config/
│   └── setup.json                     # новый
├── core/
│   ├── modem/
│   │   ├── config.py
│   │   ├── controller.py              # обновлён
│   │   ├── exceptions.py
│   │   ├── interfaces.py
│   │   ├── profiles.py
│   │   └── scanner.py                 # новый
│   ├── tests/
│   │   ├── profiles.py
│   │   ├── test_modem.py
│   │   ├── test_profiles.py
│   │   ├── test_scanner.py            # новый
│   │   └── test_verify.py             # новый
│   ├── config_loader.py               # новый
│   ├── synchronizer.py                # новый
│   └── verifier.py                    # новый
└── ...
````
📊 Итог
Компонент	Статус
ModemController	✅ Обновлён
ModemScanner	✅ Добавлен
ModemSynchronizer	✅ Добавлен