from PySide6.QtCore import QThread, Signal
from crsf_parser.payloads import PacketsTypes
from crsf_parser.handling import crsf_build_frame


class CommandEmulator(QThread):

    command_generated = Signal(bytes, int)
    start_emulation = Signal(list, int)
    stopped = Signal()

    def __init__(self):
        super().__init__()
        self.running = True
        # self.mutex = QMutex()
        self.start_emulation.connect(self.generate_command)

    def run(self):
        while self.running:
            self.msleep(100)
        print("Emulator stopped\n")

    def generate_command(self, command: list, rate: int):
        # print(f"command_list: {command}\n")
        default_command = b"\xee\x18\x16\xb0\x84\x25\x6e\xb8\xd7\x0a\xf0\x81\x6f\xe2\xad\x98\x78\x2b\x5a\xd1\x8a\x56\x80\x0f\x7c\x25"
        # channels_payload = { "channels": [int(x) for x in command] }
        channels_payload = { "channels": [int(x) if x != '' else 0 for x in command] }
        # channels_payload = { "channels" : [400, 500, 600, 700, 800, 900, 1000, 1100, 1200, 1300, 1400, 1500, 1600, 1700, 1800, 1900]}
        if command:
            try:
                frame = crsf_build_frame(PacketsTypes.RC_CHANNELS_PACKED, channels_payload)
                self.command_generated.emit(frame, rate)

            except ValueError as e:
                print(f"ValueError: {e}")
                self.command_generated.emit(default_command, rate)
            
            except Exception as e:
                print(f"Unexpected error: {e}")
                self.command_generated.emit(default_command, rate)
        else:
            return
        
    def stop(self) -> Signal:
        self.running = False
        self.stopped.emit()
        self.quit()
        self.wait()
