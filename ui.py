from RealTimeRecognitionHandlerClass import RTFRDecoratorWebcam, RTFRDecoratorVideo

from FaceCpatureHandlerClass import FCDecorator
import re



from PyQt6.QtCore import (QCoreApplication, QMetaObject, QRect,
                          QSize, Qt, pyqtSlot)

from PyQt6.QtWidgets import (QPushButton,  QSplitter, QVBoxLayout, QScrollArea,
                             QWidget, QLabel, QMessageBox,
                             QMainWindow, QStatusBar, QInputDialog, QFrame,
                             QFileDialog)


from PyQt6.QtGui import QFont, QPixmap

from EncoderClass import EncodingAdapter
# згенерований QT desiner інтерфейс
class PersonUi(QWidget):
    def __init__(self, name, preview_source, ren_func, del_func):
        super().__init__()
        self.ren_func = ren_func
        self.del_func=del_func
        self.name = name
        font = QFont()
        font.setFamilies([u"Segoe UI Historic"])
        font.setPointSize(18)

        font1 = QFont()
        font1.setFamilies([u"Segoe UI Symbol"])
        font1.setPointSize(11)
        self.splitter = QSplitter(self)
        self.splitter.setFrameStyle(QFrame.Shape.Box | QFrame.Shadow.Plain)
        self.splitter.setOrientation(Qt.Orientation.Horizontal)
        self.image_label = QLabel(self.splitter)
        self.image_label.setObjectName(u"person_image_label")
        self.image_label.setMaximumSize(QSize(110, 150))
        self.image_label.setMinimumSize(QSize(110, 150))
        self.splitter.addWidget(self.image_label)

        self.person_name_label = QLabel(self.splitter)
        self.person_name_label.setObjectName(u"person_name_label")
        self.person_name_label.setMinimumSize(QSize(300, 0))
        self.person_name_label.setFont(font)
        self.person_name_label.setAlignment(
            Qt.AlignmentFlag.AlignLeading | Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        self.splitter.addWidget(self.person_name_label)

        self.button_vbox = QWidget(self.splitter)
        self.button_vbox.setObjectName(u"horizontalLayoutWidget")
        self.verticalLayout = QVBoxLayout(self.button_vbox)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)

        self.rename_button = QPushButton(self.button_vbox)
        self.rename_button.setObjectName(u"rename_button")
        self.rename_button.setMinimumSize(QSize(100, 30))
        self.rename_button.setMaximumSize(QSize(150, 30))
        self.rename_button.setFont(font1)
        self.verticalLayout.addWidget(self.rename_button)

        self.delete_button = QPushButton(self.button_vbox)
        self.delete_button.setObjectName(u"delete_button")
        self.delete_button.setMinimumSize(QSize(100, 30))
        self.delete_button.setMaximumSize(QSize(150, 30))
        self.delete_button.setFont(font1)

        self.verticalLayout.addWidget(self.delete_button)

        self.splitter.addWidget(self.button_vbox)


        pixmap = QPixmap(preview_source)
        self.image_label.setPixmap(pixmap)
        self.person_name_label.setText(name)
        self.rename_button.setText("Rename")
        self.delete_button.setText("Delete")

        self.splitter.setFixedSize(500, 150)
        self.setFixedSize(502, 152)

        self.rename_button.clicked.connect(self.rename_button_handler)
        self.delete_button.clicked.connect(self.delete_button_handler)

    # діалог для введення мітки
    def open_input_dialog(self):
        name, ok = QInputDialog.getText(self, 'Label setting', 'Label:')
        if ok and name:
            return name

    # перевірка валідності мітки
    def is_label_valid(self, word):
        # Перевірка, чи слово складається лише з літер латиниці або цифр
        pattern = re.compile(r'^[a-zA-Z0-9]+$')

        # Перевірка з використанням регулярного виразу
        if pattern.match(word):
            return True
        else:
            return False

    # обробник подій для відповідної кнопки
    @pyqtSlot()
    def rename_button_handler(self):
        new_name = self.open_input_dialog()
        if self.is_label_valid(new_name):
            self.person_name_label.setText(new_name)
            self.ren_func(self.name, new_name)
            self.name = new_name
        else:
            dlg = QMessageBox(self)
            dlg.setWindowTitle("Error")
            dlg.setText("Wrong label!")
            button = dlg.exec()

    # обробник подій для відповідної кнопки
    @pyqtSlot()
    def delete_button_handler(self):
        self.hide()
        self.del_func(self.name, self)

class LabelsManagerWindow(QWidget):
    def __init__(self, main_window):
        self.main_window = main_window
        self.main_window.hide()
        super().__init__()
        self.persons = []
        self.setupUI()
        self.label_manager = EncodingAdapter()
        self.setup_persons()
        self.add_persons()

    def setupUI(self):
        self.scroll = QScrollArea(self)             # Scroll Area which contains the widgets, set as the centralWidget
        self.scroll.setFixedSize(539, 399)
        self.widget = QWidget()                 # Widget that contains the collection of Vertical Box
        self.vbox = QVBoxLayout()               # The Vertical Box that contains the Horizontal Boxes of  labels and buttons

        self.widget.setLayout(self.vbox)

        #Scroll Area Properties
        self.scroll.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.scroll.setWidgetResizable(True)
        self.scroll.setWidget(self.widget)



        self.setGeometry(600, 100, 540, 400)
        self.setWindowTitle('Label Manager')
        self.show()

        return

    # Створення інтерфейсу для списку міток
    def setup_persons(self):
        pers_list = self.label_manager.load_persons_preview()
        for person_data in pers_list:
            name, preview = person_data[0], person_data[1]
            tmp = PersonUi(name, preview, self.rename_person, self.del_person)
            self.persons.append(tmp)

    def add_persons(self):
        for person in self.persons:
            self.vbox.addWidget(person)

    def rename_person(self, name, new_name):
        self.label_manager.rename_person(name, new_name)


    def del_person(self, name, person):
        self.label_manager.del_person(name)
        self.persons.remove(person)

    def del_persons(self):
        for person in self.persons:
            self.vbox.removeWidget(person)
            person = None
        self.persons = []
    #збереження змін в кодуванні при закритті вікна
    def closeEvent(self, event):
        self.label_manager.save()
        self.main_window.show()
        event.accept()  # let the window close

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(611, 400)
        #MainWindow.setLocale(QLocale(QLocale.English, QLocale.UnitedStates))
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.widget = QWidget(self.centralwidget)
        self.widget.setObjectName(u"widget")
        self.widget.setGeometry(QRect(80, 30, 451, 321))
        self.verticalLayout = QVBoxLayout(self.widget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.program_name_label = QLabel(self.widget)
        self.program_name_label.setObjectName(u"program_name_label")
        font = QFont()
        font.setFamilies([u"Segoe Print"])
        font.setPointSize(36)
        font.setBold(False)
        self.program_name_label.setFont(font)
        #self.program_name_label.setLocale(PyQt6.QtCore.QLocale(PyQt6.QtCore.QLocale.English, PyQt6.QtCore.QLocale.UnitedStates))
        self.program_name_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout.addWidget(self.program_name_label)

        self.manage_button = QPushButton(self.widget)
        self.manage_button.setObjectName(u"manage_button")
        self.manage_button.setMinimumSize(QSize(40, 30))
        font1 = QFont()
        font1.setFamilies([u"Segoe UI Symbol"])
        font1.setPointSize(12)
        self.manage_button.setFont(font1)
        self.manage_button.setIconSize(QSize(16, 16))

        self.verticalLayout.addWidget(self.manage_button)

        self.capture_button = QPushButton(self.widget)
        self.capture_button.setObjectName(u"capture_button")
        self.capture_button.setMinimumSize(QSize(0, 30))
        self.capture_button.setFont(font1)

        self.verticalLayout.addWidget(self.capture_button)

        self.video_recognition_button = QPushButton(self.widget)
        self.video_recognition_button.setObjectName(u"video_recognition_button")
        self.video_recognition_button.setMinimumSize(QSize(0, 30))
        self.video_recognition_button.setFont(font1)

        self.verticalLayout.addWidget(self.video_recognition_button)

        self.webcam_recognition_button = QPushButton(self.widget)
        self.webcam_recognition_button.setObjectName(u"webcam_recognition_button")
        self.webcam_recognition_button.setMinimumSize(QSize(0, 30))
        self.webcam_recognition_button.setFont(font1)

        self.verticalLayout.addWidget(self.webcam_recognition_button)

        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"FaceFinder", None))
        self.program_name_label.setText(QCoreApplication.translate("MainWindow", u"Face Finder", None))
        self.manage_button.setText(QCoreApplication.translate("MainWindow", u"Manage labels", None))
        self.capture_button.setText(QCoreApplication.translate("MainWindow", u"Capture new face", None))
        self.video_recognition_button.setText(QCoreApplication.translate("MainWindow", u"Video face recognition", None))
        self.webcam_recognition_button.setText(QCoreApplication.translate("MainWindow", u"Webcam face recognition", None))
    # retranslateUi

class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.video_recognition_button.clicked.connect(self.video_recognition_button_handler)
        self.webcam_recognition_button.clicked.connect(self.webcam_recognition_button_handler)
        self.capture_button.clicked.connect(self.capture_button_handler)
        self.manage_button.clicked.connect(self.manage_button_handler)
    def open_file_dialog(self):
        fname = QFileDialog.getOpenFileName(
            self,
            "Select video",
            "",
            "Video Files (*.mp4)",
        )
        return fname[0]

    @pyqtSlot()
    def manage_button_handler(self):
        window = LabelsManagerWindow(self)

    @pyqtSlot()
    def video_recognition_button_handler(self):
        fname = self.open_file_dialog()
        if fname != '':
            msgBox = QMessageBox()
            msgBox.setWindowTitle("Save results")
            msgBox.setInformativeText("Do you want to save results?")
            msgBox.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
            msgBox.setDefaultButton(QMessageBox.StandardButton.Discard)
            reply = msgBox.exec()
            self.hide()
            if reply == QMessageBox.StandardButton.Yes:
                proc = RTFRDecoratorVideo(fname, to_save=True)
            else:
                proc = RTFRDecoratorVideo(fname)
            proc.run()
            self.show()

    @pyqtSlot()
    def webcam_recognition_button_handler(self):
        self.hide()
        proc = RTFRDecoratorWebcam()
        proc.run()
        self.show()


    def open_input_dialog(self):
        name, ok = QInputDialog.getText(self, 'Label Setting', 'Label:')
        if ok and name:
            return name

    def is_label_valid(self, word):
        # Перевірка, чи слово складається лише з літер латиниці або цифр
        pattern = re.compile(r'^[a-zA-Z0-9]+$')

        # Перевірка з використанням регулярного виразу
        if pattern.match(word):
            return True
        else:
            return False
    @pyqtSlot()
    def capture_button_handler(self):
        name = self.open_input_dialog()
        if self.is_label_valid(name):
            self.hide()
            proc = FCDecorator(name)
            proc.run()
            dlg = QMessageBox(self)
            dlg.setWindowTitle("Face captured")
            dlg.setText("Face was captured successfully")
            button = dlg.exec()
            self.show()
        else:
            dlg = QMessageBox(self)
            dlg.setWindowTitle("Error")
            dlg.setText("Wrong label!")
            button = dlg.exec()

