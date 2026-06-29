import re

from PySide6.QtCore import QThread, Signal, QMutex


class Statistic_Collector(QThread):
    data_parsed = Signal(str)
    stat_updated = Signal(dict)
    clear_collection = Signal()
    collection_cleared = Signal()
    stopped = Signal()

    def __init__(self):
        super().__init__()
        self.running = True
        self.mutex = QMutex()
        self.data_parsed.connect(self.collect_data)
        self.clear_collection.connect(self.clear_lists)
        # downlink stat
        self.downlink_link_quality = []
        self.downlink_rssi = []
        # uplink stat
        self.uplink_link_quality = []
        self.uplink_rssi_ant_1 = []

    def run(self):
        while self.running:
            self.msleep(100)
        print("Thread stopped\n")

    def collect_data(self, data):
        pattern = r'(downlink_link_quality|downlink_rssi|uplink_link_quality|uplink_rssi_ant_1)\s*=\s*(-?\d+)'
        matches = re.findall(pattern, data)

        self.mutex.lock()
        try:
            for match in matches:
                field, value = match
                value = int(value.strip())
                if field == 'downlink_link_quality':
                    self.downlink_link_quality.append(value)
                elif field == 'downlink_rssi' and value != 0:
                    self.downlink_rssi.append(value)
                elif field == 'uplink_link_quality':
                    self.uplink_link_quality.append(value)
                elif field == 'uplink_rssi_ant_1' and value != 0:
                    self.uplink_rssi_ant_1.append(value)
                else:
                    print("SC: no matches in data\n")

            self.get_min_max_values()
        finally:
            self.mutex.unlock()

    def get_min_max_values(self):

        min_max_dict = {
            'downlink_rssi': {
                'min': min(self.downlink_rssi) if self.downlink_rssi else None,
                'max': max(self.downlink_rssi) if self.downlink_rssi else None
            },
            'downlink_link_quality': {
                'min': min(self.downlink_link_quality) if self.downlink_link_quality else None,
                'max': max(self.downlink_link_quality) if self.downlink_link_quality else None
            },
            'uplink_rssi_ant_1': {
                'min': min(self.uplink_rssi_ant_1) if self.uplink_rssi_ant_1 else None,
                'max': max(self.uplink_rssi_ant_1) if self.uplink_rssi_ant_1 else None
            },
            'uplink_link_quality': {
                'min': min(self.uplink_link_quality) if self.uplink_link_quality else None,
                'max': max(self.uplink_link_quality) if self.uplink_link_quality else None
            }
        }
        statistic = min_max_dict
        self.stat_updated.emit(statistic)

    def clear_lists(self):
        self.uplink_link_quality.clear()
        self.uplink_rssi_ant_1.clear()
        self.downlink_link_quality.clear()
        self.downlink_rssi.clear()
        self.collection_cleared.emit()

    def stop(self) -> Signal:
        self.running = False
        self.stopped.emit()
        self.quit()
        self.wait()
