````
src/
├── docs
│   ├── changelog.md
│   ├── project_structure.md
│   └── readme.md
├── config/                          # Конфигурационные файлы
│   ├── modem_parameters.md
│   ├── salangan_rx_default.json
│   ├── salangan_tx_default.json
│   └── setup.json
│
├── core/
│   ├── emulator/                       
│   │   └── command_emulator.py
│   ├── modem/                       # Работа с модемом
│   │   ├── config.py
│   │   ├── controller.py
│   │   ├── exceptions.py
│   │   ├── interfaces.py
│   │   ├── parameters.py
│   │   ├── port_scanner.py
│   │   └── profile_loader.py
│   ├── parser/                      # ← Парсеры
│   │   ├── help_parser.py           
│   │   ├── parser_base.py 
│   │   ├── rx_parser.py
│   │   └── tx_parser.py
│   ├── config_loader.py
│   ├── session.py
│   ├── synchronizer.py
│   ├── user_input.py
│   └── verifier.py
│
├── cli/                           # Тесты
│   ├── editor.py
│   ├── profiles.py
│   ├── read_modem.py
│   ├── test_port_scanner.py
│   ├── test_profiles.py
│   └── test_session.py
├── gui/                              # Qt UI файлы
│   ├── widgets
│   │   ├── port_monitor.py
│   │   └── stat_collector.py
│   ├── main.py
│   ├── main.spec
│   ├── gu_07_win.py
│   ├── platform_gui.py
│   └── styles.py
└── utils/                           # Утилиты
│   └── logger.py
├── project_config.py
└── requirements.txt

````