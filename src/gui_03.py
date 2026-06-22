# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'gui_03.ui'
##
## Created by: Qt User Interface Compiler version 6.5.2
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
from PySide6.QtWidgets import (QApplication, QComboBox, QFrame, QHBoxLayout,
    QLCDNumber, QLabel, QLineEdit, QMainWindow,
    QPushButton, QSizePolicy, QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(988, 820)
        MainWindow.setMinimumSize(QSize(772, 100))
        MainWindow.setMaximumSize(QSize(988, 820))
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.layoutWidget = QWidget(self.centralwidget)
        self.layoutWidget.setObjectName(u"layoutWidget")
        self.layoutWidget.setGeometry(QRect(10, 10, 961, 292))
        self.horizontalLayout_3 = QHBoxLayout(self.layoutWidget)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.rx_port_label = QLabel(self.layoutWidget)
        self.rx_port_label.setObjectName(u"rx_port_label")
        font = QFont()
        font.setPointSize(20)
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
        self.rx_comports = QComboBox(self.layoutWidget)
        self.rx_comports.addItem("")
        self.rx_comports.setObjectName(u"rx_comports")
        self.rx_comports.setMinimumSize(QSize(171, 61))
        self.rx_comports.setMaximumSize(QSize(171, 61))

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

        self.rx_rssi_lcd = QLCDNumber(self.layoutWidget)
        self.rx_rssi_lcd.setObjectName(u"rx_rssi_lcd")
        self.rx_rssi_lcd.setMinimumSize(QSize(171, 61))
        self.rx_rssi_lcd.setMaximumSize(QSize(171, 61))

        self.verticalLayout_2.addWidget(self.rx_rssi_lcd)

        self.rx_link_lcd = QLCDNumber(self.layoutWidget)
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
        self.tx_link_label_4 = QLabel(self.layoutWidget)
        self.tx_link_label_4.setObjectName(u"tx_link_label_4")
        self.tx_link_label_4.setFont(font)

        self.verticalLayout_3.addWidget(self.tx_link_label_4)

        self.tx_link_label_5 = QLabel(self.layoutWidget)
        self.tx_link_label_5.setObjectName(u"tx_link_label_5")
        self.tx_link_label_5.setFont(font)

        self.verticalLayout_3.addWidget(self.tx_link_label_5)

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

        self.verticalLayout_5 = QVBoxLayout()
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.tx_link_label_3 = QLabel(self.layoutWidget)
        self.tx_link_label_3.setObjectName(u"tx_link_label_3")
        self.tx_link_label_3.setFont(font)

        self.verticalLayout_5.addWidget(self.tx_link_label_3)

        self.tx_link_label_2 = QLabel(self.layoutWidget)
        self.tx_link_label_2.setObjectName(u"tx_link_label_2")
        self.tx_link_label_2.setFont(font)

        self.verticalLayout_5.addWidget(self.tx_link_label_2)

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

        self.verticalLayout_5.addWidget(self.tx_link_indicator)

        self.tx_rssi_lcd = QLCDNumber(self.layoutWidget)
        self.tx_rssi_lcd.setObjectName(u"tx_rssi_lcd")
        self.tx_rssi_lcd.setMinimumSize(QSize(171, 61))
        self.tx_rssi_lcd.setMaximumSize(QSize(171, 61))

        self.verticalLayout_5.addWidget(self.tx_rssi_lcd)

        self.tx_link_lcd = QLCDNumber(self.layoutWidget)
        self.tx_link_lcd.setObjectName(u"tx_link_lcd")
        self.tx_link_lcd.setMinimumSize(QSize(171, 61))
        self.tx_link_lcd.setMaximumSize(QSize(171, 61))

        self.verticalLayout_5.addWidget(self.tx_link_lcd)


        self.horizontalLayout_2.addLayout(self.verticalLayout_5)


        self.horizontalLayout_3.addLayout(self.horizontalLayout_2)

        self.Statistic_frame = QFrame(self.centralwidget)
        self.Statistic_frame.setObjectName(u"Statistic_frame")
        self.Statistic_frame.setGeometry(QRect(0, 310, 991, 351))
        self.Statistic_frame.setStyleSheet(u"QFrame {\n"
"    background-color: #eaf4fd;\n"
"}")
        self.Statistic_frame.setFrameShape(QFrame.StyledPanel)
        self.Statistic_frame.setFrameShadow(QFrame.Raised)
        self.widget = QWidget(self.Statistic_frame)
        self.widget.setObjectName(u"widget")
        self.widget.setGeometry(QRect(10, 60, 961, 280))
        self.horizontalLayout_6 = QHBoxLayout(self.widget)
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.horizontalLayout_6.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.verticalLayout_4 = QVBoxLayout()
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.rx_max_rssi_label = QLabel(self.widget)
        self.rx_max_rssi_label.setObjectName(u"rx_max_rssi_label")
        self.rx_max_rssi_label.setFont(font)

        self.verticalLayout_4.addWidget(self.rx_max_rssi_label)

        self.rx_min_rssi_label = QLabel(self.widget)
        self.rx_min_rssi_label.setObjectName(u"rx_min_rssi_label")
        self.rx_min_rssi_label.setFont(font)

        self.verticalLayout_4.addWidget(self.rx_min_rssi_label)

        self.rx_max_lq_label = QLabel(self.widget)
        self.rx_max_lq_label.setObjectName(u"rx_max_lq_label")
        self.rx_max_lq_label.setFont(font)

        self.verticalLayout_4.addWidget(self.rx_max_lq_label)

        self.rx_min_lq_label = QLabel(self.widget)
        self.rx_min_lq_label.setObjectName(u"rx_min_lq_label")
        self.rx_min_lq_label.setFont(font)

        self.verticalLayout_4.addWidget(self.rx_min_lq_label)


        self.horizontalLayout_4.addLayout(self.verticalLayout_4)

        self.verticalLayout_6 = QVBoxLayout()
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.rx_max_rssi_lcd = QLCDNumber(self.widget)
        self.rx_max_rssi_lcd.setObjectName(u"rx_max_rssi_lcd")
        self.rx_max_rssi_lcd.setMinimumSize(QSize(171, 61))
        self.rx_max_rssi_lcd.setMaximumSize(QSize(171, 61))

        self.verticalLayout_6.addWidget(self.rx_max_rssi_lcd)

        self.rx_min_rssi_lcd = QLCDNumber(self.widget)
        self.rx_min_rssi_lcd.setObjectName(u"rx_min_rssi_lcd")
        self.rx_min_rssi_lcd.setMinimumSize(QSize(171, 61))
        self.rx_min_rssi_lcd.setMaximumSize(QSize(171, 61))

        self.verticalLayout_6.addWidget(self.rx_min_rssi_lcd)

        self.rx_max_lq_lcd = QLCDNumber(self.widget)
        self.rx_max_lq_lcd.setObjectName(u"rx_max_lq_lcd")
        self.rx_max_lq_lcd.setMinimumSize(QSize(171, 61))
        self.rx_max_lq_lcd.setMaximumSize(QSize(171, 61))

        self.verticalLayout_6.addWidget(self.rx_max_lq_lcd)

        self.rx_min_lq_lcd = QLCDNumber(self.widget)
        self.rx_min_lq_lcd.setObjectName(u"rx_min_lq_lcd")
        self.rx_min_lq_lcd.setMinimumSize(QSize(171, 61))
        self.rx_min_lq_lcd.setMaximumSize(QSize(171, 61))

        self.verticalLayout_6.addWidget(self.rx_min_lq_lcd)


        self.horizontalLayout_4.addLayout(self.verticalLayout_6)


        self.horizontalLayout_6.addLayout(self.horizontalLayout_4)

        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.verticalLayout_7 = QVBoxLayout()
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.tx_max_rssi_label = QLabel(self.widget)
        self.tx_max_rssi_label.setObjectName(u"tx_max_rssi_label")
        self.tx_max_rssi_label.setFont(font)

        self.verticalLayout_7.addWidget(self.tx_max_rssi_label)

        self.tx_min_rssi_label = QLabel(self.widget)
        self.tx_min_rssi_label.setObjectName(u"tx_min_rssi_label")
        self.tx_min_rssi_label.setFont(font)

        self.verticalLayout_7.addWidget(self.tx_min_rssi_label)

        self.tx_max_lq_label = QLabel(self.widget)
        self.tx_max_lq_label.setObjectName(u"tx_max_lq_label")
        self.tx_max_lq_label.setFont(font)

        self.verticalLayout_7.addWidget(self.tx_max_lq_label)

        self.tx_min_lq_label = QLabel(self.widget)
        self.tx_min_lq_label.setObjectName(u"tx_min_lq_label")
        self.tx_min_lq_label.setFont(font)

        self.verticalLayout_7.addWidget(self.tx_min_lq_label)


        self.horizontalLayout_5.addLayout(self.verticalLayout_7)

        self.verticalLayout_8 = QVBoxLayout()
        self.verticalLayout_8.setObjectName(u"verticalLayout_8")
        self.tx_max_rssi_lcd = QLCDNumber(self.widget)
        self.tx_max_rssi_lcd.setObjectName(u"tx_max_rssi_lcd")
        self.tx_max_rssi_lcd.setMinimumSize(QSize(171, 61))
        self.tx_max_rssi_lcd.setMaximumSize(QSize(171, 61))

        self.verticalLayout_8.addWidget(self.tx_max_rssi_lcd)

        self.tx_min_rssi_lcd = QLCDNumber(self.widget)
        self.tx_min_rssi_lcd.setObjectName(u"tx_min_rssi_lcd")
        self.tx_min_rssi_lcd.setMinimumSize(QSize(171, 61))
        self.tx_min_rssi_lcd.setMaximumSize(QSize(171, 61))

        self.verticalLayout_8.addWidget(self.tx_min_rssi_lcd)

        self.tx_max_lq_lcd = QLCDNumber(self.widget)
        self.tx_max_lq_lcd.setObjectName(u"tx_max_lq_lcd")
        self.tx_max_lq_lcd.setMinimumSize(QSize(171, 61))
        self.tx_max_lq_lcd.setMaximumSize(QSize(171, 61))

        self.verticalLayout_8.addWidget(self.tx_max_lq_lcd)

        self.tx_min_lq_lcd = QLCDNumber(self.widget)
        self.tx_min_lq_lcd.setObjectName(u"tx_min_lq_lcd")
        self.tx_min_lq_lcd.setMinimumSize(QSize(171, 61))
        self.tx_min_lq_lcd.setMaximumSize(QSize(171, 61))

        self.verticalLayout_8.addWidget(self.tx_min_lq_lcd)


        self.horizontalLayout_5.addLayout(self.verticalLayout_8)


        self.horizontalLayout_6.addLayout(self.horizontalLayout_5)

        self.widget1 = QWidget(self.Statistic_frame)
        self.widget1.setObjectName(u"widget1")
        self.widget1.setGeometry(QRect(0, 0, 981, 63))
        self.horizontalLayout_10 = QHBoxLayout(self.widget1)
        self.horizontalLayout_10.setObjectName(u"horizontalLayout_10")
        self.horizontalLayout_10.setContentsMargins(0, 0, 0, 0)
        self.stat_coll_label = QLabel(self.widget1)
        self.stat_coll_label.setObjectName(u"stat_coll_label")
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.stat_coll_label.sizePolicy().hasHeightForWidth())
        self.stat_coll_label.setSizePolicy(sizePolicy)
        self.stat_coll_label.setMinimumSize(QSize(230, 51))
        self.stat_coll_label.setMaximumSize(QSize(230, 51))
        self.stat_coll_label.setFont(font)
        self.stat_coll_label.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.horizontalLayout_10.addWidget(self.stat_coll_label)

        self.start_coll_btn = QPushButton(self.widget1)
        self.start_coll_btn.setObjectName(u"start_coll_btn")
        sizePolicy.setHeightForWidth(self.start_coll_btn.sizePolicy().hasHeightForWidth())
        self.start_coll_btn.setSizePolicy(sizePolicy)
        self.start_coll_btn.setMinimumSize(QSize(170, 51))
        self.start_coll_btn.setMaximumSize(QSize(170, 51))
        self.start_coll_btn.setFont(font)

        self.horizontalLayout_10.addWidget(self.start_coll_btn)

        self.clear_coll_btn = QPushButton(self.widget1)
        self.clear_coll_btn.setObjectName(u"clear_coll_btn")
        sizePolicy.setHeightForWidth(self.clear_coll_btn.sizePolicy().hasHeightForWidth())
        self.clear_coll_btn.setSizePolicy(sizePolicy)
        self.clear_coll_btn.setMinimumSize(QSize(170, 51))
        self.clear_coll_btn.setMaximumSize(QSize(170, 51))
        self.clear_coll_btn.setFont(font)

        self.horizontalLayout_10.addWidget(self.clear_coll_btn)

        self.save_coll_btn = QPushButton(self.widget1)
        self.save_coll_btn.setObjectName(u"save_coll_btn")
        sizePolicy.setHeightForWidth(self.save_coll_btn.sizePolicy().hasHeightForWidth())
        self.save_coll_btn.setSizePolicy(sizePolicy)
        self.save_coll_btn.setMinimumSize(QSize(170, 51))
        self.save_coll_btn.setMaximumSize(QSize(170, 51))
        self.save_coll_btn.setFont(font)

        self.horizontalLayout_10.addWidget(self.save_coll_btn)

        self.timer_lcd = QLCDNumber(self.widget1)
        self.timer_lcd.setObjectName(u"timer_lcd")
        sizePolicy1 = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.timer_lcd.sizePolicy().hasHeightForWidth())
        self.timer_lcd.setSizePolicy(sizePolicy1)
        self.timer_lcd.setMinimumSize(QSize(171, 51))
        self.timer_lcd.setMaximumSize(QSize(171, 51))
        self.timer_lcd.setDigitCount(8)

        self.horizontalLayout_10.addWidget(self.timer_lcd)

        self.frame = QFrame(self.centralwidget)
        self.frame.setObjectName(u"frame")
        self.frame.setGeometry(QRect(0, 660, 991, 151))
        font2 = QFont()
        font2.setPointSize(17)
        self.frame.setFont(font2)
        self.frame.setFrameShape(QFrame.StyledPanel)
        self.frame.setFrameShadow(QFrame.Raised)
        self.widget2 = QWidget(self.frame)
        self.widget2.setObjectName(u"widget2")
        self.widget2.setGeometry(QRect(10, 50, 954, 98))
        self.verticalLayout_9 = QVBoxLayout(self.widget2)
        self.verticalLayout_9.setObjectName(u"verticalLayout_9")
        self.verticalLayout_9.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_8 = QHBoxLayout()
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")
        self.ch1_label = QLabel(self.widget2)
        self.ch1_label.setObjectName(u"ch1_label")
        sizePolicy1.setHeightForWidth(self.ch1_label.sizePolicy().hasHeightForWidth())
        self.ch1_label.setSizePolicy(sizePolicy1)
        self.ch1_label.setMinimumSize(QSize(50, 41))
        self.ch1_label.setMaximumSize(QSize(50, 41))
        font3 = QFont()
        font3.setPointSize(18)
        self.ch1_label.setFont(font3)
        self.ch1_label.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_8.addWidget(self.ch1_label)

        self.ch2_label = QLabel(self.widget2)
        self.ch2_label.setObjectName(u"ch2_label")
        sizePolicy1.setHeightForWidth(self.ch2_label.sizePolicy().hasHeightForWidth())
        self.ch2_label.setSizePolicy(sizePolicy1)
        self.ch2_label.setMinimumSize(QSize(50, 41))
        self.ch2_label.setMaximumSize(QSize(50, 41))
        self.ch2_label.setFont(font3)
        self.ch2_label.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_8.addWidget(self.ch2_label)

        self.ch3_label = QLabel(self.widget2)
        self.ch3_label.setObjectName(u"ch3_label")
        sizePolicy1.setHeightForWidth(self.ch3_label.sizePolicy().hasHeightForWidth())
        self.ch3_label.setSizePolicy(sizePolicy1)
        self.ch3_label.setMinimumSize(QSize(50, 41))
        self.ch3_label.setMaximumSize(QSize(50, 41))
        self.ch3_label.setFont(font3)
        self.ch3_label.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_8.addWidget(self.ch3_label)

        self.ch4_label = QLabel(self.widget2)
        self.ch4_label.setObjectName(u"ch4_label")
        sizePolicy1.setHeightForWidth(self.ch4_label.sizePolicy().hasHeightForWidth())
        self.ch4_label.setSizePolicy(sizePolicy1)
        self.ch4_label.setMinimumSize(QSize(50, 41))
        self.ch4_label.setMaximumSize(QSize(50, 41))
        self.ch4_label.setFont(font3)
        self.ch4_label.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_8.addWidget(self.ch4_label)

        self.ch5_label = QLabel(self.widget2)
        self.ch5_label.setObjectName(u"ch5_label")
        sizePolicy1.setHeightForWidth(self.ch5_label.sizePolicy().hasHeightForWidth())
        self.ch5_label.setSizePolicy(sizePolicy1)
        self.ch5_label.setMinimumSize(QSize(50, 41))
        self.ch5_label.setMaximumSize(QSize(50, 41))
        self.ch5_label.setFont(font3)
        self.ch5_label.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_8.addWidget(self.ch5_label)

        self.ch6_label = QLabel(self.widget2)
        self.ch6_label.setObjectName(u"ch6_label")
        sizePolicy1.setHeightForWidth(self.ch6_label.sizePolicy().hasHeightForWidth())
        self.ch6_label.setSizePolicy(sizePolicy1)
        self.ch6_label.setMinimumSize(QSize(50, 41))
        self.ch6_label.setMaximumSize(QSize(50, 41))
        self.ch6_label.setFont(font3)
        self.ch6_label.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_8.addWidget(self.ch6_label)

        self.ch7_label = QLabel(self.widget2)
        self.ch7_label.setObjectName(u"ch7_label")
        sizePolicy1.setHeightForWidth(self.ch7_label.sizePolicy().hasHeightForWidth())
        self.ch7_label.setSizePolicy(sizePolicy1)
        self.ch7_label.setMinimumSize(QSize(50, 41))
        self.ch7_label.setMaximumSize(QSize(50, 41))
        self.ch7_label.setFont(font3)
        self.ch7_label.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_8.addWidget(self.ch7_label)

        self.ch8_label = QLabel(self.widget2)
        self.ch8_label.setObjectName(u"ch8_label")
        sizePolicy1.setHeightForWidth(self.ch8_label.sizePolicy().hasHeightForWidth())
        self.ch8_label.setSizePolicy(sizePolicy1)
        self.ch8_label.setMinimumSize(QSize(50, 41))
        self.ch8_label.setMaximumSize(QSize(50, 41))
        self.ch8_label.setFont(font3)
        self.ch8_label.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_8.addWidget(self.ch8_label)

        self.ch9_label = QLabel(self.widget2)
        self.ch9_label.setObjectName(u"ch9_label")
        sizePolicy1.setHeightForWidth(self.ch9_label.sizePolicy().hasHeightForWidth())
        self.ch9_label.setSizePolicy(sizePolicy1)
        self.ch9_label.setMinimumSize(QSize(50, 41))
        self.ch9_label.setMaximumSize(QSize(50, 41))
        self.ch9_label.setFont(font3)
        self.ch9_label.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_8.addWidget(self.ch9_label)

        self.ch10_label = QLabel(self.widget2)
        self.ch10_label.setObjectName(u"ch10_label")
        sizePolicy1.setHeightForWidth(self.ch10_label.sizePolicy().hasHeightForWidth())
        self.ch10_label.setSizePolicy(sizePolicy1)
        self.ch10_label.setMinimumSize(QSize(50, 41))
        self.ch10_label.setMaximumSize(QSize(50, 41))
        self.ch10_label.setFont(font3)
        self.ch10_label.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_8.addWidget(self.ch10_label)

        self.ch11_label = QLabel(self.widget2)
        self.ch11_label.setObjectName(u"ch11_label")
        sizePolicy1.setHeightForWidth(self.ch11_label.sizePolicy().hasHeightForWidth())
        self.ch11_label.setSizePolicy(sizePolicy1)
        self.ch11_label.setMinimumSize(QSize(50, 41))
        self.ch11_label.setMaximumSize(QSize(50, 41))
        self.ch11_label.setFont(font3)
        self.ch11_label.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_8.addWidget(self.ch11_label)

        self.ch12_label = QLabel(self.widget2)
        self.ch12_label.setObjectName(u"ch12_label")
        sizePolicy1.setHeightForWidth(self.ch12_label.sizePolicy().hasHeightForWidth())
        self.ch12_label.setSizePolicy(sizePolicy1)
        self.ch12_label.setMinimumSize(QSize(50, 41))
        self.ch12_label.setMaximumSize(QSize(50, 41))
        self.ch12_label.setFont(font3)
        self.ch12_label.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_8.addWidget(self.ch12_label)

        self.ch13_label = QLabel(self.widget2)
        self.ch13_label.setObjectName(u"ch13_label")
        sizePolicy1.setHeightForWidth(self.ch13_label.sizePolicy().hasHeightForWidth())
        self.ch13_label.setSizePolicy(sizePolicy1)
        self.ch13_label.setMinimumSize(QSize(50, 41))
        self.ch13_label.setMaximumSize(QSize(50, 41))
        self.ch13_label.setFont(font3)
        self.ch13_label.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_8.addWidget(self.ch13_label)

        self.ch14_label = QLabel(self.widget2)
        self.ch14_label.setObjectName(u"ch14_label")
        sizePolicy1.setHeightForWidth(self.ch14_label.sizePolicy().hasHeightForWidth())
        self.ch14_label.setSizePolicy(sizePolicy1)
        self.ch14_label.setMinimumSize(QSize(50, 41))
        self.ch14_label.setMaximumSize(QSize(50, 41))
        self.ch14_label.setFont(font3)
        self.ch14_label.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_8.addWidget(self.ch14_label)

        self.ch15_label = QLabel(self.widget2)
        self.ch15_label.setObjectName(u"ch15_label")
        sizePolicy1.setHeightForWidth(self.ch15_label.sizePolicy().hasHeightForWidth())
        self.ch15_label.setSizePolicy(sizePolicy1)
        self.ch15_label.setMinimumSize(QSize(50, 41))
        self.ch15_label.setMaximumSize(QSize(50, 41))
        self.ch15_label.setFont(font3)
        self.ch15_label.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_8.addWidget(self.ch15_label)

        self.ch16_label = QLabel(self.widget2)
        self.ch16_label.setObjectName(u"ch16_label")
        sizePolicy1.setHeightForWidth(self.ch16_label.sizePolicy().hasHeightForWidth())
        self.ch16_label.setSizePolicy(sizePolicy1)
        self.ch16_label.setMinimumSize(QSize(50, 41))
        self.ch16_label.setMaximumSize(QSize(50, 41))
        self.ch16_label.setFont(font3)
        self.ch16_label.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_8.addWidget(self.ch16_label)


        self.verticalLayout_9.addLayout(self.horizontalLayout_8)

        self.horizontalLayout_7 = QHBoxLayout()
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.ch1_lineEdit = QLineEdit(self.widget2)
        self.ch1_lineEdit.setObjectName(u"ch1_lineEdit")
        sizePolicy1.setHeightForWidth(self.ch1_lineEdit.sizePolicy().hasHeightForWidth())
        self.ch1_lineEdit.setSizePolicy(sizePolicy1)
        self.ch1_lineEdit.setMinimumSize(QSize(50, 41))
        self.ch1_lineEdit.setMaximumSize(QSize(50, 41))
        self.ch1_lineEdit.setFont(font)
        self.ch1_lineEdit.setMaxLength(4)

        self.horizontalLayout_7.addWidget(self.ch1_lineEdit)

        self.ch2_lineEdit = QLineEdit(self.widget2)
        self.ch2_lineEdit.setObjectName(u"ch2_lineEdit")
        sizePolicy1.setHeightForWidth(self.ch2_lineEdit.sizePolicy().hasHeightForWidth())
        self.ch2_lineEdit.setSizePolicy(sizePolicy1)
        self.ch2_lineEdit.setMinimumSize(QSize(50, 41))
        self.ch2_lineEdit.setMaximumSize(QSize(50, 41))
        self.ch2_lineEdit.setFont(font)
        self.ch2_lineEdit.setMaxLength(4)

        self.horizontalLayout_7.addWidget(self.ch2_lineEdit)

        self.ch3_lineEdit = QLineEdit(self.widget2)
        self.ch3_lineEdit.setObjectName(u"ch3_lineEdit")
        sizePolicy1.setHeightForWidth(self.ch3_lineEdit.sizePolicy().hasHeightForWidth())
        self.ch3_lineEdit.setSizePolicy(sizePolicy1)
        self.ch3_lineEdit.setMinimumSize(QSize(50, 41))
        self.ch3_lineEdit.setMaximumSize(QSize(50, 41))
        self.ch3_lineEdit.setFont(font)
        self.ch3_lineEdit.setMaxLength(4)

        self.horizontalLayout_7.addWidget(self.ch3_lineEdit)

        self.ch4_lineEdit = QLineEdit(self.widget2)
        self.ch4_lineEdit.setObjectName(u"ch4_lineEdit")
        sizePolicy1.setHeightForWidth(self.ch4_lineEdit.sizePolicy().hasHeightForWidth())
        self.ch4_lineEdit.setSizePolicy(sizePolicy1)
        self.ch4_lineEdit.setMinimumSize(QSize(50, 41))
        self.ch4_lineEdit.setMaximumSize(QSize(50, 41))
        self.ch4_lineEdit.setFont(font)
        self.ch4_lineEdit.setMaxLength(4)

        self.horizontalLayout_7.addWidget(self.ch4_lineEdit)

        self.ch5_lineEdit = QLineEdit(self.widget2)
        self.ch5_lineEdit.setObjectName(u"ch5_lineEdit")
        sizePolicy1.setHeightForWidth(self.ch5_lineEdit.sizePolicy().hasHeightForWidth())
        self.ch5_lineEdit.setSizePolicy(sizePolicy1)
        self.ch5_lineEdit.setMinimumSize(QSize(50, 41))
        self.ch5_lineEdit.setMaximumSize(QSize(50, 41))
        self.ch5_lineEdit.setFont(font)
        self.ch5_lineEdit.setMaxLength(4)

        self.horizontalLayout_7.addWidget(self.ch5_lineEdit)

        self.ch6_lineEdit = QLineEdit(self.widget2)
        self.ch6_lineEdit.setObjectName(u"ch6_lineEdit")
        sizePolicy1.setHeightForWidth(self.ch6_lineEdit.sizePolicy().hasHeightForWidth())
        self.ch6_lineEdit.setSizePolicy(sizePolicy1)
        self.ch6_lineEdit.setMinimumSize(QSize(50, 41))
        self.ch6_lineEdit.setMaximumSize(QSize(50, 41))
        self.ch6_lineEdit.setFont(font)
        self.ch6_lineEdit.setMaxLength(4)

        self.horizontalLayout_7.addWidget(self.ch6_lineEdit)

        self.ch7_lineEdit = QLineEdit(self.widget2)
        self.ch7_lineEdit.setObjectName(u"ch7_lineEdit")
        sizePolicy1.setHeightForWidth(self.ch7_lineEdit.sizePolicy().hasHeightForWidth())
        self.ch7_lineEdit.setSizePolicy(sizePolicy1)
        self.ch7_lineEdit.setMinimumSize(QSize(50, 41))
        self.ch7_lineEdit.setMaximumSize(QSize(50, 41))
        self.ch7_lineEdit.setFont(font)
        self.ch7_lineEdit.setMaxLength(4)

        self.horizontalLayout_7.addWidget(self.ch7_lineEdit)

        self.ch8_lineEdit = QLineEdit(self.widget2)
        self.ch8_lineEdit.setObjectName(u"ch8_lineEdit")
        sizePolicy1.setHeightForWidth(self.ch8_lineEdit.sizePolicy().hasHeightForWidth())
        self.ch8_lineEdit.setSizePolicy(sizePolicy1)
        self.ch8_lineEdit.setMinimumSize(QSize(50, 41))
        self.ch8_lineEdit.setMaximumSize(QSize(50, 41))
        self.ch8_lineEdit.setFont(font)
        self.ch8_lineEdit.setMaxLength(4)

        self.horizontalLayout_7.addWidget(self.ch8_lineEdit)

        self.ch9_lineEdit = QLineEdit(self.widget2)
        self.ch9_lineEdit.setObjectName(u"ch9_lineEdit")
        sizePolicy1.setHeightForWidth(self.ch9_lineEdit.sizePolicy().hasHeightForWidth())
        self.ch9_lineEdit.setSizePolicy(sizePolicy1)
        self.ch9_lineEdit.setMinimumSize(QSize(50, 41))
        self.ch9_lineEdit.setMaximumSize(QSize(50, 41))
        self.ch9_lineEdit.setFont(font)
        self.ch9_lineEdit.setMaxLength(4)

        self.horizontalLayout_7.addWidget(self.ch9_lineEdit)

        self.ch10_lineEdit = QLineEdit(self.widget2)
        self.ch10_lineEdit.setObjectName(u"ch10_lineEdit")
        sizePolicy1.setHeightForWidth(self.ch10_lineEdit.sizePolicy().hasHeightForWidth())
        self.ch10_lineEdit.setSizePolicy(sizePolicy1)
        self.ch10_lineEdit.setMinimumSize(QSize(50, 41))
        self.ch10_lineEdit.setMaximumSize(QSize(50, 41))
        self.ch10_lineEdit.setFont(font)
        self.ch10_lineEdit.setMaxLength(4)

        self.horizontalLayout_7.addWidget(self.ch10_lineEdit)

        self.ch11_lineEdit = QLineEdit(self.widget2)
        self.ch11_lineEdit.setObjectName(u"ch11_lineEdit")
        sizePolicy1.setHeightForWidth(self.ch11_lineEdit.sizePolicy().hasHeightForWidth())
        self.ch11_lineEdit.setSizePolicy(sizePolicy1)
        self.ch11_lineEdit.setMinimumSize(QSize(50, 41))
        self.ch11_lineEdit.setMaximumSize(QSize(50, 41))
        self.ch11_lineEdit.setFont(font)
        self.ch11_lineEdit.setMaxLength(4)

        self.horizontalLayout_7.addWidget(self.ch11_lineEdit)

        self.ch12_lineEdit = QLineEdit(self.widget2)
        self.ch12_lineEdit.setObjectName(u"ch12_lineEdit")
        sizePolicy1.setHeightForWidth(self.ch12_lineEdit.sizePolicy().hasHeightForWidth())
        self.ch12_lineEdit.setSizePolicy(sizePolicy1)
        self.ch12_lineEdit.setMinimumSize(QSize(50, 41))
        self.ch12_lineEdit.setMaximumSize(QSize(50, 41))
        self.ch12_lineEdit.setFont(font)
        self.ch12_lineEdit.setMaxLength(4)

        self.horizontalLayout_7.addWidget(self.ch12_lineEdit)

        self.ch13_lineEdit = QLineEdit(self.widget2)
        self.ch13_lineEdit.setObjectName(u"ch13_lineEdit")
        sizePolicy1.setHeightForWidth(self.ch13_lineEdit.sizePolicy().hasHeightForWidth())
        self.ch13_lineEdit.setSizePolicy(sizePolicy1)
        self.ch13_lineEdit.setMinimumSize(QSize(50, 41))
        self.ch13_lineEdit.setMaximumSize(QSize(50, 41))
        self.ch13_lineEdit.setFont(font)
        self.ch13_lineEdit.setMaxLength(4)

        self.horizontalLayout_7.addWidget(self.ch13_lineEdit)

        self.ch14_lineEdit = QLineEdit(self.widget2)
        self.ch14_lineEdit.setObjectName(u"ch14_lineEdit")
        sizePolicy1.setHeightForWidth(self.ch14_lineEdit.sizePolicy().hasHeightForWidth())
        self.ch14_lineEdit.setSizePolicy(sizePolicy1)
        self.ch14_lineEdit.setMinimumSize(QSize(50, 41))
        self.ch14_lineEdit.setMaximumSize(QSize(50, 41))
        self.ch14_lineEdit.setFont(font)
        self.ch14_lineEdit.setMaxLength(4)

        self.horizontalLayout_7.addWidget(self.ch14_lineEdit)

        self.ch15_lineEdit = QLineEdit(self.widget2)
        self.ch15_lineEdit.setObjectName(u"ch15_lineEdit")
        sizePolicy1.setHeightForWidth(self.ch15_lineEdit.sizePolicy().hasHeightForWidth())
        self.ch15_lineEdit.setSizePolicy(sizePolicy1)
        self.ch15_lineEdit.setMinimumSize(QSize(50, 41))
        self.ch15_lineEdit.setMaximumSize(QSize(50, 41))
        self.ch15_lineEdit.setFont(font)
        self.ch15_lineEdit.setMaxLength(4)

        self.horizontalLayout_7.addWidget(self.ch15_lineEdit)

        self.ch16_lineEdit = QLineEdit(self.widget2)
        self.ch16_lineEdit.setObjectName(u"ch16_lineEdit")
        sizePolicy1.setHeightForWidth(self.ch16_lineEdit.sizePolicy().hasHeightForWidth())
        self.ch16_lineEdit.setSizePolicy(sizePolicy1)
        self.ch16_lineEdit.setMinimumSize(QSize(50, 41))
        self.ch16_lineEdit.setMaximumSize(QSize(50, 41))
        self.ch16_lineEdit.setFont(font)
        self.ch16_lineEdit.setMaxLength(4)

        self.horizontalLayout_7.addWidget(self.ch16_lineEdit)


        self.verticalLayout_9.addLayout(self.horizontalLayout_7)

        self.widget3 = QWidget(self.frame)
        self.widget3.setObjectName(u"widget3")
        self.widget3.setGeometry(QRect(10, 0, 540, 53))
        self.horizontalLayout_9 = QHBoxLayout(self.widget3)
        self.horizontalLayout_9.setObjectName(u"horizontalLayout_9")
        self.horizontalLayout_9.setContentsMargins(0, 0, 0, 0)
        self.emulate_command_label = QLabel(self.widget3)
        self.emulate_command_label.setObjectName(u"emulate_command_label")
        self.emulate_command_label.setFont(font)

        self.horizontalLayout_9.addWidget(self.emulate_command_label)

        self.rate_lineEdit = QLineEdit(self.widget3)
        self.rate_lineEdit.setObjectName(u"rate_lineEdit")
        sizePolicy1.setHeightForWidth(self.rate_lineEdit.sizePolicy().hasHeightForWidth())
        self.rate_lineEdit.setSizePolicy(sizePolicy1)
        self.rate_lineEdit.setMinimumSize(QSize(141, 41))
        self.rate_lineEdit.setMaximumSize(QSize(141, 41))
        self.rate_lineEdit.setFont(font)
        self.rate_lineEdit.setMaxLength(3)
        self.rate_lineEdit.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_9.addWidget(self.rate_lineEdit)

        self.start_emulation = QPushButton(self.widget3)
        self.start_emulation.setObjectName(u"start_emulation")
        sizePolicy1.setHeightForWidth(self.start_emulation.sizePolicy().hasHeightForWidth())
        self.start_emulation.setSizePolicy(sizePolicy1)
        self.start_emulation.setMinimumSize(QSize(200, 52))
        self.start_emulation.setMaximumSize(QSize(200, 52))
        self.start_emulation.setFont(font)

        self.horizontalLayout_9.addWidget(self.start_emulation)

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
        self.rx_max_rssi_label.setText(QCoreApplication.translate("MainWindow", u"Downlink Max RSSI (dBm)", None))
        self.rx_min_rssi_label.setText(QCoreApplication.translate("MainWindow", u"Downlink Min RSSI (dBm)", None))
        self.rx_max_lq_label.setText(QCoreApplication.translate("MainWindow", u"Downlink Max LQ (%)", None))
        self.rx_min_lq_label.setText(QCoreApplication.translate("MainWindow", u"Downlink Min LQ (%)", None))
        self.tx_max_rssi_label.setText(QCoreApplication.translate("MainWindow", u"Uplink Max RSSI (dBm)", None))
        self.tx_min_rssi_label.setText(QCoreApplication.translate("MainWindow", u"Uplink Min RSSI (dBm)", None))
        self.tx_max_lq_label.setText(QCoreApplication.translate("MainWindow", u"Uplink Max LQ (%)", None))
        self.tx_min_lq_label.setText(QCoreApplication.translate("MainWindow", u"Uplink Min LQ (%)", None))
        self.stat_coll_label.setText(QCoreApplication.translate("MainWindow", u"Statistics:", None))
        self.start_coll_btn.setText(QCoreApplication.translate("MainWindow", u"Start Collecting", None))
        self.clear_coll_btn.setText(QCoreApplication.translate("MainWindow", u"Clear Collection", None))
        self.save_coll_btn.setText(QCoreApplication.translate("MainWindow", u"Save to File", None))
        self.ch1_label.setText(QCoreApplication.translate("MainWindow", u"CH 1", None))
        self.ch2_label.setText(QCoreApplication.translate("MainWindow", u"CH 2", None))
        self.ch3_label.setText(QCoreApplication.translate("MainWindow", u"CH 3", None))
        self.ch4_label.setText(QCoreApplication.translate("MainWindow", u"CH 4", None))
        self.ch5_label.setText(QCoreApplication.translate("MainWindow", u"CH 5", None))
        self.ch6_label.setText(QCoreApplication.translate("MainWindow", u"CH 6", None))
        self.ch7_label.setText(QCoreApplication.translate("MainWindow", u"CH 7", None))
        self.ch8_label.setText(QCoreApplication.translate("MainWindow", u"CH 8", None))
        self.ch9_label.setText(QCoreApplication.translate("MainWindow", u"CH 9", None))
        self.ch10_label.setText(QCoreApplication.translate("MainWindow", u"CH 10", None))
        self.ch11_label.setText(QCoreApplication.translate("MainWindow", u"CH 11", None))
        self.ch12_label.setText(QCoreApplication.translate("MainWindow", u"CH 12", None))
        self.ch13_label.setText(QCoreApplication.translate("MainWindow", u"CH 13", None))
        self.ch14_label.setText(QCoreApplication.translate("MainWindow", u"CH 14", None))
        self.ch15_label.setText(QCoreApplication.translate("MainWindow", u"CH 15", None))
        self.ch16_label.setText(QCoreApplication.translate("MainWindow", u"CH 16", None))
        self.emulate_command_label.setText(QCoreApplication.translate("MainWindow", u"Command Emulation:", None))
        self.rate_lineEdit.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Rate Hz", None))
        self.start_emulation.setText(QCoreApplication.translate("MainWindow", u"Emulate", None))
    # retranslateUi

