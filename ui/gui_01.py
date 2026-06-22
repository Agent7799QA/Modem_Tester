# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'gui_01.ui'
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
        MainWindow.resize(772, 322)
        MainWindow.setMinimumSize(QSize(772, 322))
        MainWindow.setMaximumSize(QSize(772, 322))
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.layoutWidget = QWidget(self.centralwidget)
        self.layoutWidget.setObjectName(u"layoutWidget")
        self.layoutWidget.setGeometry(QRect(10, 10, 751, 301))
        self.horizontalLayout_3 = QHBoxLayout(self.layoutWidget)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.rx_label = QLabel(self.layoutWidget)
        self.rx_label.setObjectName(u"rx_label")
        font = QFont()
        font.setPointSize(20)
        self.rx_label.setFont(font)

        self.verticalLayout.addWidget(self.rx_label)

        self.rx_port_label = QLabel(self.layoutWidget)
        self.rx_port_label.setObjectName(u"rx_port_label")
        self.rx_port_label.setFont(font)

        self.verticalLayout.addWidget(self.rx_port_label)

        self.serial_label = QLabel(self.layoutWidget)
        self.serial_label.setObjectName(u"serial_label")
        self.serial_label.setFont(font)

        self.verticalLayout.addWidget(self.serial_label)

        self.rx_link_label = QLabel(self.layoutWidget)
        self.rx_link_label.setObjectName(u"rx_link_label")
        self.rx_link_label.setFont(font)

        self.verticalLayout.addWidget(self.rx_link_label)

        self.rx_rssi_label = QLabel(self.layoutWidget)
        self.rx_rssi_label.setObjectName(u"rx_rssi_label")
        self.rx_rssi_label.setFont(font)

        self.verticalLayout.addWidget(self.rx_rssi_label)

        self.rx_lq_label = QLabel(self.layoutWidget)
        self.rx_lq_label.setObjectName(u"rx_lq_label")
        self.rx_lq_label.setFont(font)

        self.verticalLayout.addWidget(self.rx_lq_label)


        self.horizontalLayout.addLayout(self.verticalLayout)

        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.rx_none_lable = QLabel(self.layoutWidget)
        self.rx_none_lable.setObjectName(u"rx_none_lable")
        self.rx_none_lable.setMinimumSize(QSize(32, 32))

        self.verticalLayout_2.addWidget(self.rx_none_lable)

        self.rx_comports = QComboBox(self.layoutWidget)
        self.rx_comports.addItem("")
        self.rx_comports.setObjectName(u"rx_comports")
        self.rx_comports.setMinimumSize(QSize(34, 34))

        self.verticalLayout_2.addWidget(self.rx_comports)

        self.rx_serial_indicator = QLabel(self.layoutWidget)
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

        self.rx_link_indicator = QLabel(self.layoutWidget)
        self.rx_link_indicator.setObjectName(u"rx_link_indicator")
        self.rx_link_indicator.setStyleSheet(u"border-radius: 50%;\n"
"min-width: 34px;\n"
"min-height: 34px;\n"
"max-width: 34px;\n"
"max-height: 34px;\n"
"background-color: white;\n"
"border: 1px solid black;\n"
"")

        self.verticalLayout_2.addWidget(self.rx_link_indicator)

        self.rx_rssi_lcd = QLCDNumber(self.layoutWidget)
        self.rx_rssi_lcd.setObjectName(u"rx_rssi_lcd")
        self.rx_rssi_lcd.setMinimumSize(QSize(34, 34))

        self.verticalLayout_2.addWidget(self.rx_rssi_lcd)

        self.rx_link_lcd = QLCDNumber(self.layoutWidget)
        self.rx_link_lcd.setObjectName(u"rx_link_lcd")
        self.rx_link_lcd.setMinimumSize(QSize(34, 34))

        self.verticalLayout_2.addWidget(self.rx_link_lcd)


        self.horizontalLayout.addLayout(self.verticalLayout_2)


        self.horizontalLayout_3.addLayout(self.horizontalLayout)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.verticalLayout_3 = QVBoxLayout()
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.tx_label = QLabel(self.layoutWidget)
        self.tx_label.setObjectName(u"tx_label")
        self.tx_label.setFont(font)

        self.verticalLayout_3.addWidget(self.tx_label)

        self.tx_port_label = QLabel(self.layoutWidget)
        self.tx_port_label.setObjectName(u"tx_port_label")
        self.tx_port_label.setFont(font)

        self.verticalLayout_3.addWidget(self.tx_port_label)

        self.serial_label_2 = QLabel(self.layoutWidget)
        self.serial_label_2.setObjectName(u"serial_label_2")
        self.serial_label_2.setFont(font)

        self.verticalLayout_3.addWidget(self.serial_label_2)

        self.tx_link_label = QLabel(self.layoutWidget)
        self.tx_link_label.setObjectName(u"tx_link_label")
        self.tx_link_label.setFont(font)

        self.verticalLayout_3.addWidget(self.tx_link_label)

        self.tx_rssi_label = QLabel(self.layoutWidget)
        self.tx_rssi_label.setObjectName(u"tx_rssi_label")
        self.tx_rssi_label.setFont(font)

        self.verticalLayout_3.addWidget(self.tx_rssi_label)

        self.tx_lq_label = QLabel(self.layoutWidget)
        self.tx_lq_label.setObjectName(u"tx_lq_label")
        self.tx_lq_label.setFont(font)

        self.verticalLayout_3.addWidget(self.tx_lq_label)


        self.horizontalLayout_2.addLayout(self.verticalLayout_3)

        self.verticalLayout_4 = QVBoxLayout()
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.tx_none_lable = QLabel(self.layoutWidget)
        self.tx_none_lable.setObjectName(u"tx_none_lable")
        self.tx_none_lable.setMinimumSize(QSize(32, 32))

        self.verticalLayout_4.addWidget(self.tx_none_lable)

        self.tx_comports = QComboBox(self.layoutWidget)
        self.tx_comports.addItem("")
        self.tx_comports.setObjectName(u"tx_comports")
        self.tx_comports.setMinimumSize(QSize(36, 36))

        self.verticalLayout_4.addWidget(self.tx_comports)

        self.tx_serial_indicator = QLabel(self.layoutWidget)
        self.tx_serial_indicator.setObjectName(u"tx_serial_indicator")
        self.tx_serial_indicator.setStyleSheet(u"border-radius: 50%;\n"
"min-width: 34px;\n"
"min-height: 34px;\n"
"max-width: 34px;\n"
"max-height: 34px;\n"
"background-color: black;\n"
"border: 1px solid black;\n"
"")

        self.verticalLayout_4.addWidget(self.tx_serial_indicator)

        self.tx_link_indicator = QLabel(self.layoutWidget)
        self.tx_link_indicator.setObjectName(u"tx_link_indicator")
        self.tx_link_indicator.setStyleSheet(u"border-radius: 50%;\n"
"min-width: 34px;\n"
"min-height: 34px;\n"
"max-width: 34px;\n"
"max-height: 34px;\n"
"background-color: white;\n"
"border: 1px solid black;\n"
"")

        self.verticalLayout_4.addWidget(self.tx_link_indicator)

        self.tx_rssi_lcd = QLCDNumber(self.layoutWidget)
        self.tx_rssi_lcd.setObjectName(u"tx_rssi_lcd")

        self.verticalLayout_4.addWidget(self.tx_rssi_lcd)

        self.tx_link_lcd = QLCDNumber(self.layoutWidget)
        self.tx_link_lcd.setObjectName(u"tx_link_lcd")

        self.verticalLayout_4.addWidget(self.tx_link_lcd)


        self.horizontalLayout_2.addLayout(self.verticalLayout_4)


        self.horizontalLayout_3.addLayout(self.horizontalLayout_2)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"Modem Tester", None))
        self.rx_label.setText(QCoreApplication.translate("MainWindow", u"RX", None))
        self.rx_port_label.setText(QCoreApplication.translate("MainWindow", u"COMPort", None))
        self.serial_label.setText(QCoreApplication.translate("MainWindow", u"Serial status", None))
        self.rx_link_label.setText(QCoreApplication.translate("MainWindow", u"Link status", None))
        self.rx_rssi_label.setText(QCoreApplication.translate("MainWindow", u"RSSI (dBm)", None))
        self.rx_lq_label.setText(QCoreApplication.translate("MainWindow", u"LQ (%)", None))
        self.rx_none_lable.setText("")
        self.rx_comports.setItemText(0, QCoreApplication.translate("MainWindow", u"None", None))

        self.rx_serial_indicator.setText("")
        self.rx_link_indicator.setText("")
        self.tx_label.setText(QCoreApplication.translate("MainWindow", u"TX", None))
        self.tx_port_label.setText(QCoreApplication.translate("MainWindow", u"COMPort", None))
        self.serial_label_2.setText(QCoreApplication.translate("MainWindow", u"Serial status", None))
        self.tx_link_label.setText(QCoreApplication.translate("MainWindow", u"Link status", None))
        self.tx_rssi_label.setText(QCoreApplication.translate("MainWindow", u"RSSI (dBm)", None))
        self.tx_lq_label.setText(QCoreApplication.translate("MainWindow", u"LQ (%)", None))
        self.tx_none_lable.setText("")
        self.tx_comports.setItemText(0, QCoreApplication.translate("MainWindow", u"None", None))

        self.tx_serial_indicator.setText("")
        self.tx_link_indicator.setText("")
    # retranslateUi

