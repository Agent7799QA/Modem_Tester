modem_tester-master/
├── crsf_parser/
│   ├── __init__.py
│   ├── frames.py
│   ├── handling.py
│   └── payloads.py
├── docs/
│   ├── changelog.md
│   ├── project_structure.md
│   └── readme.md
└── src/
    ├── cli/
    │   ├── editor.py
    │   ├── profiles.py
    │   ├── read_modem.py
    │   ├── test_port_scanner.py
    │   ├── test_profiles.py
    │   └── test_session.py
    ├── config/
    │   ├── modem_parameters.md
    │   ├── salangan_rx_default.json
    │   └── salangan_tx_default.json
    ├── core/
    │   ├── dto/
    │   │   ├── __init__.py
    │   │   ├── base.py
    │   │   ├── rx_config.py
    │   │   └── tx_config.py
    │   ├── emulator/
    │   │   └── command_emulator.py
    │   ├── modem/
    │   │   ├── __init__.py
    │   │   ├── config.py
    │   │   ├── controller.py
    │   │   ├── exceptions.py
    │   │   ├── interfaces.py
    │   │   ├── parameters.py
    │   │   ├── port_scanner.py
    │   │   └── profile_loader.py
    │   ├── parser/
    │   │   ├── help_parser.py
    │   │   ├── parser_base.py
    │   │   ├── rx_parser.py
    │   │   └── tx_parser.py
    │   ├── __init__.py
    │   ├── config_loader.py
    │   ├── session.py
    │   ├── synchronizer.py
    │   ├── user_input.py
    │   └── verifier.py
    ├── gui/
    │   ├── widgets/
    │   │   ├── port_monitor.py
    │   │   └── stat_collector.py
    │   ├── gui_07_win.py
    │   ├── main.py
    │   ├── main.spec
    │   ├── platform_gui.py
    │   └── styles.py
    ├── utils/
    │   └── logger.py
    ├── 1.py
    ├── project_config.py
    └── requirements.txt
