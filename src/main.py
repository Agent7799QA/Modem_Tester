from project_config import *
from platform_gui import ChooseGui
import re
import sys
# import serial.tools.list_ports
from PySide6.QtWidgets import QApplication, QMainWindow
from PySide6.QtCore import QTimer, Signal, QTime
from PySide6.QtGui import QIntValidator 
from port_monitor import PortMonitorThread
from rx_parser import RxParsingThread
from stat_collector import Statistic_Collector
from command_emulator import CommandEmulator
from styles import *
GUI = ChooseGui()


class Window(QMainWindow):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = GUI.Ui_MainWindow()
        self.ui.setupUi(self)
        self.elapsed_time = QTime(0, 0, 0)
        self.saved_rx_port = "None"
        self.rx_lq_status = "_default"
        self.rx_rssi_status = "_default"
        self.tx_lq_status = "_default"
        self.tx_rssi_status = "_default"
        self.ui.rx_comports.currentTextChanged.connect(self.on_rx_port_changed)
        self.open_rx_port = Signal(str)

        self.statistic_collector_thread = None
        self.ui.timer_lcd.display("00:00:00")

        self.port_monitor = PortMonitorThread()
        self.port_monitor.ports_changed.connect(self.update_rx_ports)
        self.port_monitor.stopped.connect(self.on_port_monitor_stopped)
        self.port_monitor.start()
        self.ui.start_coll_btn.clicked.connect(self.start_stat_collecting)
        self.rx_parsing_thread = RxParsingThread()

        # status
        self.rx_parsing_thread.serial_status.connect(self.rx_serial_status)        

        # data
        self.rx_parsing_thread.rx_data_parsed.connect(self.rx_data)
        self.rx_parsing_thread.rx_data_parsed.connect(self.tx_data)
        self.rx_parsing_thread.stopped.connect(self.on_crsf_parsing_stopped)
        self.rx_parsing_thread.start()

        # emulation thread
        self.command_emulator = CommandEmulator()
        self.command_emulator.stopped.connect(self.on_emulator_stopped)
        self.command_emulator.start()
        self.ui.start_emulation.clicked.connect(self.handle_emulation_button)
        self.command_emulator.command_generated.connect(self.rx_parsing_thread.request_command)

        # LineEditValidation
        # TODO: FIXME:
        line_edit_validation_list = [ self.ui.ch1_lineEdit, self.ui.ch2_lineEdit, self.ui.ch3_lineEdit, self.ui.ch4_lineEdit, self.ui.ch5_lineEdit,
                                      self.ui.ch6_lineEdit,self.ui.ch7_lineEdit, self.ui.ch8_lineEdit, self.ui.ch9_lineEdit, self.ui.ch10_lineEdit,
                                      self.ui.ch11_lineEdit,self.ui.ch12_lineEdit, self.ui.ch13_lineEdit, self.ui.ch14_lineEdit, self.ui.ch15_lineEdit,
                                      self.ui.ch16_lineEdit ]
        
        for le in line_edit_validation_list:
            le.setValidator(QIntValidator(0, 2047, le))
            le.textChanged.connect(lambda text, le=le: self.update_channel_lineEdit_status(le, text))
        # rate validation
        rate = self.ui.rate_lineEdit
        rate.setValidator(QIntValidator(0, 50, self.ui.rate_lineEdit))
        rate.textChanged.connect(lambda text, rate=rate: self.update_rate_lineEdit_status(rate, text))

# TX and RX prots activities
    def update_rx_ports(self, com_ports) -> None:
        none_port = "None"

        self.ui.rx_comports.clear()
        self.ui.rx_comports.addItem(none_port)
        if not com_ports:
            self.ui.rx_comports.clear()
            self.ui.rx_comports.addItem(none_port)
        else:
            for port in com_ports:
                self.ui.rx_comports.addItem(port)
        self.rx_saved_port()


    def rx_saved_port(self) -> None:
        current_text = self.ui.rx_comports.currentText()
        
        if current_text != "None" and current_text != "":
            if self.saved_rx_port != current_text:
                self.saved_rx_port = current_text
                
        else: 
            index = self.ui.rx_comports.findText(self.saved_rx_port)
            self.ui.rx_comports.setCurrentIndex(index)
            if self.saved_rx_port != "None" or "":
                self.rx_parsing_thread.set_port(self.saved_rx_port)


    def on_rx_port_changed(self) -> None:
        self.rx_saved_port()

#DATA AND STATUSES         
    def rx_serial_status(self, status) -> None:

        style = serial_indicator_styles.get(status, "_default")

        self.ui.rx_serial_indicator.setStyleSheet(
        form_of_indicator + style
        )
        if status == "bad":
            self.ui.rx_link_lcd.display("-")
            self.ui.rx_rssi_lcd.display("-")
            self.ui.tx_rssi_lcd.display("-")
            self.ui.tx_link_lcd.display("-")
            self.rx_lq_status = "bad"
            style = link_indicator_styles.get(self.rx_lq_status, "_default")
            self.ui.rx_link_indicator.setStyleSheet(form_of_indicator + style)
            self.tx_lq_status = "bad"
            style = link_indicator_styles.get(self.tx_lq_status, "_default")
            self.ui.tx_link_indicator.setStyleSheet(form_of_indicator + style) 
            
#END
#PARSED DATA
    def rx_data(self, data):
        downlink_link_quality = None
        downlink_rssi = None
        pattern = r'(downlink_link_quality|downlink_rssi)\s*=\s*(-?\d+)'
        matches = re.findall(pattern, data)

        for match in matches:
            field, value = match
            value = int(value.strip())
            
            if field == 'downlink_link_quality':
                downlink_link_quality = value
            elif field == 'downlink_rssi':
                downlink_rssi = value
        if downlink_link_quality is not None:
            self.ui.rx_link_lcd.display(downlink_link_quality)
            if downlink_link_quality > 90:
                self.rx_lq_status = "good"
            elif 60 < downlink_link_quality < 90:
                self.rx_lq_status = "normal"
            elif downlink_link_quality < 60:
                self.rx_lq_status = "bad"
        if downlink_rssi is not None:
            self.ui.rx_rssi_lcd.display(-downlink_rssi)

        style = link_indicator_styles.get(self.rx_lq_status, "_default")

        self.ui.rx_link_indicator.setStyleSheet(
        form_of_indicator + style
        )
        if downlink_link_quality == 0:
            self.ui.rx_link_lcd.display("-")
            self.ui.rx_rssi_lcd.display("-")
            self.ui.tx_rssi_lcd.display("-")
            self.ui.tx_link_lcd.display("-")

        style = link_indicator_styles.get(self.tx_lq_status, "_default")

        self.ui.tx_link_indicator.setStyleSheet(
            form_of_indicator+ style
        )     


    def tx_data(self, data):
        uplink_link_quality = None
        uplink_rssi_ant_1 = None

        pattern = r'(uplink_link_quality|uplink_rssi_ant_1)\s*=\s*(-?\d+)'
        matches = re.findall(pattern, data)

        for match in matches:
            field, value = match
            value = int(value.strip())
            
            if field == 'uplink_link_quality':
                uplink_link_quality = value
            elif field == 'uplink_rssi_ant_1':
                uplink_rssi_ant_1 = value
        if uplink_link_quality is not None:
            self.ui.tx_link_lcd.display(uplink_link_quality)
            if uplink_link_quality > 90:
                self.tx_lq_status = "good"
            elif 60 < uplink_link_quality < 90:
                self.tx_lq_status = "normal"
            elif uplink_link_quality < 60:
                self.tx_lq_status = "bad"
        if uplink_rssi_ant_1 is not None:
            self.ui.tx_rssi_lcd.display(-uplink_rssi_ant_1)
        if uplink_link_quality == 0:
            self.ui.rx_link_lcd.display("-")
            self.ui.rx_rssi_lcd.display("-")
            self.ui.tx_rssi_lcd.display("-")
            self.ui.tx_link_lcd.display("-")

        style = link_indicator_styles.get(self.tx_lq_status, "_default")

        self.ui.tx_link_indicator.setStyleSheet(
            form_of_indicator+ style
        )   
#END
        
#Statistics Collector
    def rx_stat(self, data:dict=None):
        if data is not None:
            # data
            downlink_rssi_min = data.get('downlink_rssi', {}).get('max')
            downlink_rssi_max = data.get('downlink_rssi', {}).get('min')
            downlink_min_lq = data.get('downlink_link_quality', {}).get('min')
            downlink_max_lq = data.get('downlink_link_quality', {}).get('max')
        if downlink_max_lq is not None:
            self.ui.rx_min_rssi_lcd.display(-downlink_rssi_min)
            self.ui.rx_max_rssi_lcd.display(-downlink_rssi_max)
            self.ui.rx_min_lq_lcd.display(downlink_min_lq)
            self.ui.rx_max_lq_lcd.display(downlink_max_lq)
        else:
            self.ui.rx_min_rssi_lcd.display("-")
            self.ui.rx_max_rssi_lcd.display("-")
            self.ui.rx_min_lq_lcd.display("-")
            self.ui.rx_max_lq_lcd.display("-")

    def tx_stat(self, data:dict):
        if data is not None:
            uplink_rssi_min = data.get('uplink_rssi_ant_1', {}).get('max')
            uplink_rssi_max = data.get('uplink_rssi_ant_1', {}).get('min')
            uplink_min_lq = data.get('uplink_link_quality', {}).get('min')
            uplink_max_lq = data.get('uplink_link_quality', {}).get('max')
        if uplink_max_lq is not None:
            self.ui.tx_min_rssi_lcd.display(-uplink_rssi_min)
            self.ui.tx_max_rssi_lcd.display(-uplink_rssi_max)
            self.ui.tx_min_lq_lcd.display(uplink_min_lq)
            self.ui.tx_max_lq_lcd.display(uplink_max_lq)
        else:
            self.ui.tx_min_rssi_lcd.display("-")
            self.ui.tx_max_rssi_lcd.display("-")
            self.ui.tx_min_lq_lcd.display("-")
            self.ui.tx_max_lq_lcd.display("-")
#end
    def start_stat_collecting(self) -> int:
        self.statistic_collector_thread = Statistic_Collector()
        if not self.statistic_collector_thread.isRunning():
            self.statistic_collector_thread.stat_updated.connect(self.rx_stat) 
            self.statistic_collector_thread.stat_updated.connect(self.tx_stat) 

            self.ui.clear_coll_btn.clicked.connect(self.reset_collection)
            self.rx_parsing_thread.rx_data_parsed.connect(self.statistic_collector_thread.data_parsed)

            self.statistic_collector_thread.collection_cleared.connect(self.reset_stat_displays)
            self.statistic_collector_thread.stopped.connect(self.on_stat_collector_stopped)
            self.statistic_collector_thread.start()
            self.timer = QTimer()
            self.timer.timeout.connect(self.update_time)
            self.timer.start(1000)
            self.ui.start_coll_btn.setEnabled(False)
            return 0
        else:
            return -1
        
    def reset_collection(self):
        self.elapsed_time = QTime(0, 0, 0)
        self.ui.timer_lcd.display(self.elapsed_time.toString("hh:mm:ss"))
        self.statistic_collector_thread.clear_collection.emit()

    def handle_emulation_button(self):
        if self.ui.start_emulation.text() == "Emulate":
            self.start_command_emulation()
        else:
            self.stop_emulation()

    def start_command_emulation(self):
        # command = None TODO: rebrand btn after boot, start/stop
        command = []
        command = self.get_command()
        rate = self.ui.rate_lineEdit.text()
        if rate != '':
            self.command_emulator.start_emulation.emit(command, int(rate))
            self.ui.start_emulation.setText("Stop Emulation")
            # self.ui.start_emulation.disconnect()
            # self.ui.start_emulation.clicked.connect(self.stop_emulation)
        else:
            return -1
        
    def stop_emulation(self):
        self.rx_parsing_thread.stop_writing()
        self.ui.start_emulation.setText("Emulate")
        # self.ui.start_emulation.disconnect()
        # self.ui.start_emulation.clicked.connect(self.start_command_emulation)

    def get_command(self) -> list:
        """
        Возвращает список значений с каждого из каналов
        """
        command_list = []
        try:
            command_list.append(self.ui.ch1_lineEdit.text())
            command_list.append(self.ui.ch2_lineEdit.text())
            command_list.append(self.ui.ch3_lineEdit.text())
            command_list.append(self.ui.ch4_lineEdit.text())
            command_list.append(self.ui.ch5_lineEdit.text())
            command_list.append(self.ui.ch6_lineEdit.text())
            command_list.append(self.ui.ch7_lineEdit.text())
            command_list.append(self.ui.ch8_lineEdit.text())
            command_list.append(self.ui.ch9_lineEdit.text())
            command_list.append(self.ui.ch10_lineEdit.text())
            command_list.append(self.ui.ch11_lineEdit.text())
            command_list.append(self.ui.ch12_lineEdit.text())
            command_list.append(self.ui.ch13_lineEdit.text())
            command_list.append(self.ui.ch14_lineEdit.text())
            command_list.append(self.ui.ch15_lineEdit.text())
            command_list.append(self.ui.ch16_lineEdit.text())
        except: ValueError
        return command_list
    
    def update_channel_lineEdit_status(self, line_edit, text):
        """Обновление статуса для конкретного LineEdit"""
        # TODO: check  stats valid
        if not text:
            line_edit.setStyleSheet("")
            return
        try:
            value = int(text)
            if 0 <= value <= 2047:
                line_edit.setStyleSheet("border: 2px solid green;")
            else:
                line_edit.setStyleSheet("border: 2px solid red;")
        except ValueError:
            line_edit.setStyleSheet("border: 2px solid red;")

    def update_rate_lineEdit_status(self, line_edit, text):
        # TODO: unite validate functions
        if not text:
            line_edit.setStyleSheet("")
            return
        try:
            value = int(text)
            if 0 <= value <= 50:
                line_edit.setStyleSheet("border: 2px solid green;")
            else:
                line_edit.setStyleSheet("border: 2px solid red;")
        except ValueError:
            line_edit.setStyleSheet("border: 2px solid red;")

    def reset_stat_displays(self):
        self.ui.rx_min_rssi_lcd.display(0)
        self.ui.rx_max_rssi_lcd.display(0)
        self.ui.rx_min_lq_lcd.display(0)
        self.ui.rx_max_lq_lcd.display(0)

        self.ui.tx_min_rssi_lcd.display(0)
        self.ui.tx_max_rssi_lcd.display(0)
        self.ui.tx_min_lq_lcd.display(0)
        self.ui.tx_max_lq_lcd.display(0)

    def stop_parsing(self) -> int:
        if self.rx_parsing_thread.isRunning():
            self.rx_parsing_thread.running = False
            self.rx_parsing_thread.stop()
            self.rx_parsing_thread.terminate()
            try:
                self.rx_parsing_thread.wait(2000)
                return 0
            except self.rx_parsing_thread.TimeoutError:
                print("Timeout occurred while waiting for rx_thread to stop")
                return -1


    def stop_monitoring(self) -> int:

        if self.port_monitor.isRunning():
            self.port_monitor.running = False
            self.port_monitor.stop()
            self.port_monitor.terminate()
            try:
                self.port_monitor.wait(2000)
                return 0
            except self.port_monitor.TimeoutError:
                print("Timeout occurred while waiting for thread to stop")
                return -1
            
    def stop_stat_collecting(self) -> int:

        if self.statistic_collector_thread.isRunning():
            self.statistic_collector_thread.running = False
            self.statistic_collector_thread.stop()
            self.statistic_collector_thread.terminate()
            try:
                self.statistic_collector_thread.wait(2000)
                return 0
            except self.statistic_collector_thread.TimeoutError:
                print("Timeout occurred while waiting for thread to stop")
                return -1
            
    def stop_command_emulator(self) -> int:
        self.command_emulator.running = False
        self.command_emulator.stop()
        self.command_emulator.terminate()
        try:
            self.command_emulator.wait(2000)
            return 0
        except self.command_emulator.TimeoutError:
            print("Timeout occurred while waiting for thread to stop")
            return -1
        
    def update_time(self):
        self.elapsed_time = self.elapsed_time.addSecs(1)
        self.ui.timer_lcd.display(self.elapsed_time.toString("hh:mm:ss"))

    def on_port_monitor_stopped(self) -> None:
        print("Port Monitor thread has been stopped")

    def on_crsf_parsing_stopped(self) -> None:
        print("Parsing thread has been stopped")

    def on_stat_collector_stopped(self) ->None:
        print("Stat Collector thread has been stopped")

    def on_emulator_stopped(self) -> None:
        print("Command Emulator thread has been stopped")

    def closeEvent(self, event) -> None:
        if self.statistic_collector_thread is not None:
            if self.port_monitor.isRunning() and self.rx_parsing_thread.isRunning() and self.statistic_collector_thread.isRunning() and self.command_emulator.isRunning():
                self.stop_parsing()
                self.stop_monitoring()
                self.stop_stat_collecting()
                self.stop_command_emulator()
                if not self.port_monitor.isRunning() and not self.rx_parsing_thread.isRunning() and not self.statistic_collector_thread.isRunning() and not self.command_emulator.isRunning():
                    print("threads stopped successfully")
                    event.accept()
                else:
                    print("Failed to stop threads")
                    event.ignore()
        else:
            if self.port_monitor.isRunning() and self.rx_parsing_thread.isRunning() and self.command_emulator.isRunning():
                self.stop_parsing()
                self.stop_monitoring()
                self.stop_command_emulator()
                if not self.port_monitor.isRunning() and not self.rx_parsing_thread.isRunning() and not self.command_emulator.isRunning():
                    print("threads stopped successfully")
                    event.accept()
                else:
                    print("Failed to stop threads")
                    event.ignore()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec())
