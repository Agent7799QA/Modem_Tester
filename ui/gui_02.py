# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'gui_02.ui'
##
## Created by: Qt User Interface Compiler version 6.8.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QComboBox, QHBoxLayout, QLCDNumber,
    QLabel, QMainWindow, QSizePolicy, QVBoxLayout,
    QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(860, 307)
        MainWindow.setMinimumSize(QSize(772, 100))
        MainWindow.setMaximumSize(QSize(1000, 1000))
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.widget = QWidget(self.centralwidget)
        self.widget.setObjectName(u"widget")
        self.widget.setGeometry(QRect(10, 10, 840, 285))
        self.horizontalLayout_3 = QHBoxLayout(self.widget)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.rx_port_label = QLabel(self.widget)
        self.rx_port_label.setObjectName(u"rx_port_label")
        font = QFont()
        font.setPointSize(20)
        self.rx_port_label.setFont(font)

        self.verticalLayout.addWidget(self.rx_port_label)

        self.serial_label = QLabel(self.widget)
        self.serial_label.setObjectName(u"serial_label")
        self.serial_label.setFont(font)

        self.verticalLayout.addWidget(self.serial_label)

        self.rx_link_label = QLabel(self.widget)
        self.rx_link_label.setObjectName(u"rx_link_label")
        self.rx_link_label.setFont(font)

        self.verticalLayout.addWidget(self.rx_link_label)

        self.rx_rssi_label = QLabel(self.widget)
        self.rx_rssi_label.setObjectName(u"rx_rssi_label")
        self.rx_rssi_label.setFont(font)

        self.verticalLayout.addWidget(self.rx_rssi_label)

        self.rx_lq_label = QLabel(self.widget)
        self.rx_lq_label.setObjectName(u"rx_lq_label")
        self.rx_lq_label.setFont(font)

        self.verticalLayout.addWidget(self.rx_lq_label)


        self.horizontalLayout.addLayout(self.verticalLayout)

        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.rx_comports = QComboBox(self.widget)
        self.rx_comports.addItem("")
        self.rx_comports.setObjectName(u"rx_comports")
        self.rx_comports.setMinimumSize(QSize(171, 61))
        self.rx_comports.setMaximumSize(QSize(171, 61))

        self.verticalLayout_2.addWidget(self.rx_comports)

        self.rx_serial_indicator = QLabel(self.widget)
        self.rx_serial_indicator.setObjectName(u"rx_serial_indicator")
        font1 = QFont()
        font1.setPointSize(11)
        self.rx_serial_indicator.setFont(font1)
        self.rx_serial_indicator.setStyleSheet(u"border-radius: 50%;\n"
"min-width: 34px;\n"
"min-height: 34px;\n"
"max-width: 34px;\n"
"max-height: 34px;\n"
"background-color: white;\n"
"border: 1px solid black;\n"
"")

        self.verticalLayout_2.addWidget(self.rx_serial_indicator)

        self.rx_link_indicator = QLabel(self.widget)
        self.rx_link_indicator.setObjectName(u"rx_link_indicator")
        self.rx_link_indicator.setMinimumSize(QSize(36, 36))
        self.rx_link_indicator.setMaximumSize(QSize(36, 36))
        self.rx_link_indicator.setStyleSheet(u"border-radius: 50%;\n"
"min-width: 34px;\n"
"min-height: 34px;\n"
"max-width: 34px;\n"
"max-height: 34px;\n"
"background-color: white;\n"
"border: 1px solid black;\n"
"")

        self.verticalLayout_2.addWidget(self.rx_link_indicator)

        self.rx_rssi_lcd = QLCDNumber(self.widget)
        self.rx_rssi_lcd.setObjectName(u"rx_rssi_lcd")
        self.rx_rssi_lcd.setMinimumSize(QSize(171, 61))
        self.rx_rssi_lcd.setMaximumSize(QSize(171, 61))

        self.verticalLayout_2.addWidget(self.rx_rssi_lcd)

        self.rx_link_lcd = QLCDNumber(self.widget)
        self.rx_link_lcd.setObjectName(u"rx_link_lcd")
        self.rx_link_lcd.setMinimumSize(QSize(171, 61))
        self.rx_link_lcd.setMaximumSize(QSize(171, 61))

        self.verticalLayout_2.addWidget(self.rx_link_lcd)


        self.horizontalLayout.addLayout(self.verticalLayout_2)


        self.horizontalLayout_3.addLayout(self.horizontalLayout)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.verticalLayout_3 = QVBoxLayout()
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.tx_link_label_4 = QLabel(self.widget)
        self.tx_link_label_4.setObjectName(u"tx_link_label_4")
        self.tx_link_label_4.setFont(font)

        self.verticalLayout_3.addWidget(self.tx_link_label_4)

        self.tx_link_label_5 = QLabel(self.widget)
        self.tx_link_label_5.setObjectName(u"tx_link_label_5")
        self.tx_link_label_5.setFont(font)

        self.verticalLayout_3.addWidget(self.tx_link_label_5)

        self.tx_link_label = QLabel(self.widget)
        self.tx_link_label.setObjectName(u"tx_link_label")
        self.tx_link_label.setFont(font)

        self.verticalLayout_3.addWidget(self.tx_link_label)

        self.tx_rssi_label = QLabel(self.widget)
        self.tx_rssi_label.setObjectName(u"tx_rssi_label")
        self.tx_rssi_label.setFont(font)

        self.verticalLayout_3.addWidget(self.tx_rssi_label)

        self.tx_lq_label = QLabel(self.widget)
        self.tx_lq_label.setObjectName(u"tx_lq_label")
        self.tx_lq_label.setFont(font)

        self.verticalLayout_3.addWidget(self.tx_lq_label)


        self.horizontalLayout_2.addLayout(self.verticalLayout_3)

        self.verticalLayout_5 = QVBoxLayout()
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.tx_link_label_3 = QLabel(self.widget)
        self.tx_link_label_3.setObjectName(u"tx_link_label_3")
        self.tx_link_label_3.setFont(font)

        self.verticalLayout_5.addWidget(self.tx_link_label_3)

        self.tx_link_label_2 = QLabel(self.widget)
        self.tx_link_label_2.setObjectName(u"tx_link_label_2")
        self.tx_link_label_2.setFont(font)

        self.verticalLayout_5.addWidget(self.tx_link_label_2)

        self.tx_link_indicator = QLabel(self.widget)
        self.tx_link_indicator.setObjectName(u"tx_link_indicator")
        self.tx_link_indicator.setStyleSheet(u"border-radius: 50%;\n"
"min-width: 34px;\n"
"min-height: 34px;\n"
"max-width: 34px;\n"
"max-height: 34px;\n"
"background-color: white;\n"
"border: 1px solid black;\n"
"")

        self.verticalLayout_5.addWidget(self.tx_link_indicator)

        self.tx_rssi_lcd = QLCDNumber(self.widget)
        self.tx_rssi_lcd.setObjectName(u"tx_rssi_lcd")
        self.tx_rssi_lcd.setMinimumSize(QSize(171, 61))
        self.tx_rssi_lcd.setMaximumSize(QSize(171, 61))

        self.verticalLayout_5.addWidget(self.tx_rssi_lcd)

        self.tx_link_lcd = QLCDNumber(self.widget)
        self.tx_link_lcd.setObjectName(u"tx_link_lcd")
        self.tx_link_lcd.setMinimumSize(QSize(171, 61))
        self.tx_link_lcd.setMaximumSize(QSize(171, 61))

        self.verticalLayout_5.addWidget(self.tx_link_lcd)


        self.horizontalLayout_2.addLayout(self.verticalLayout_5)


        self.horizontalLayout_3.addLayout(self.horizontalLayout_2)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"Modem Tester", None))
        self.rx_port_label.setText(QCoreApplication.translate("MainWindow", u"RX COMPort", None))
        self.serial_label.setText(QCoreApplication.translate("MainWindow", u"Serial status", None))
        self.rx_link_label.setText(QCoreApplication.translate("MainWindow", u"Downlink status", None))
        self.rx_rssi_label.setText(QCoreApplication.translate("MainWindow", u"Downlink RSSI (dBm)", None))
        self.rx_lq_label.setText(QCoreApplication.translate("MainWindow", u"Downlink LQ (%)", None))
        self.rx_comports.setItemText(0, QCoreApplication.translate("MainWindow", u"None", None))

        self.rx_serial_indicator.setText("")
        self.rx_link_indicator.setText("")
        self.tx_link_label_4.setText("")
        self.tx_link_label_5.setText("")
        self.tx_link_label.setText(QCoreApplication.translate("MainWindow", u"Uplink status", None))
        self.tx_rssi_label.setText(QCoreApplication.translate("MainWindow", u"Uplink RSSI (dBm)", None))
        self.tx_lq_label.setText(QCoreApplication.translate("MainWindow", u"Uplink LQ (%)", None))
        self.tx_link_label_3.setText("")
        self.tx_link_label_2.setText("")
        self.tx_link_indicator.setText("")
    # retranslateUi

