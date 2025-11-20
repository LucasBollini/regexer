from PyQt5.QtWidgets import QWidget, QApplication, QHBoxLayout, QVBoxLayout, QTextEdit, QLabel, QComboBox
from PyQt5.QtGui import QPixmap, QCursor
from PyQt5 import QtCore

from tools.FileHandler import FileHandler
from tools.PageHandler import PageHandler
from tools.RegexHandler import RegexHandler


class MainWindow:

    window : QWidget = QWidget()
    cursor_pointer = QCursor(QtCore.Qt.CursorShape.PointingHandCursor)


    def setup(self, file_handler_ref : FileHandler, page_handler_ref : PageHandler, regex_handler_ref : RegexHandler):
        self.create_window(file_handler_ref, page_handler_ref, regex_handler_ref)
        self.window.show()


    def create_window(self, file_handler_ref : FileHandler, page_handler_ref : PageHandler, regex_handler_ref : RegexHandler):
        self.window.setFixedSize(1200, 700)
        self.window.setWindowTitle("RegExer")
        self.window.setStyleSheet("background-color: #231f36; color: white;")
        self.window.closeEvent = lambda a: QApplication.quit()

        lbl_source = QLabel(self.window)
        lbl_source.setText('File being modififed: ')
        lbl_source.setGeometry(10, 10, 840, 680)
        lbl_source.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        text_area = QTextEdit(self.window)
        text_area.setStyleSheet(f'background-color: #0b0917')
        text_area.setGeometry(10, 10, 840, 680)
        text_area.setPlaceholderText('• Example text input:\n\nLucas Resende Bollini\n\n\n\n\n\n• Example result:\n\nMade_by_Lucas_Resende_Bollini_2025')

        controls_container = QWidget(self.window)
        controls_layout = QVBoxLayout(controls_container)
        controls_container.setGeometry(860, 10, 330, 680)

        buttons_container = QWidget()
        buttons_layout = QHBoxLayout(buttons_container)
        buttons_container.setFixedHeight(60)
        controls_layout.addWidget(buttons_container)

        button_new_file = QLabel()
        button_new_file.setPixmap(QPixmap("./src/imgs/new_file.png").scaledToHeight(30))
        button_new_file.setFixedSize(30, 30)
        button_new_file.setCursor(self.cursor_pointer)
        button_new_file.setToolTip('New regex instructions set')
        buttons_layout.addWidget(button_new_file)

        button_load = QLabel()
        button_load.setPixmap(QPixmap("./src/imgs/load_file.png").scaledToHeight(30))
        button_load.setFixedSize(30, 30)
        button_load.setCursor(self.cursor_pointer)
        button_load.setToolTip('Load regex instructions')
        buttons_layout.addWidget(button_load)

        button_save = QLabel()
        button_save.setPixmap(QPixmap("./src/imgs/save_file.png").scaledToHeight(30))
        button_save.setFixedSize(30, 30)
        button_save.setCursor(self.cursor_pointer)
        button_save.setToolTip('Save regex instructions')
        buttons_layout.addWidget(button_save)

        button_spacer = QWidget()
        buttons_layout.addWidget(button_spacer)

        button_run = QLabel()
        button_run.setPixmap(QPixmap("./src/imgs/exec.png").scaledToHeight(30))
        button_run.setFixedSize(30, 30)
        button_run.setCursor(self.cursor_pointer)
        button_run.setToolTip('Run regex')
        buttons_layout.addWidget(button_run)

        lbl_loaded = QLabel('Loaded regex:')
        controls_layout.addWidget(lbl_loaded)

        pages_container = QWidget()
        pages_layout = QHBoxLayout(pages_container)
        controls_layout.addWidget(pages_container)

        pages_spacer = QWidget()
        pages_layout.addWidget(pages_spacer)

        button_new_page = QLabel()
        button_new_page.setPixmap(QPixmap("./src/imgs/new_page.png").scaledToHeight(30))
        button_new_page.setFixedSize(30, 30)
        button_new_page.setCursor(self.cursor_pointer)
        button_new_page.setToolTip('New instruction page')
        pages_layout.addWidget(button_new_page)

        button_del_page = QLabel()
        button_del_page.setPixmap(QPixmap("./src/imgs/rmv_page.png").scaledToHeight(30))
        button_del_page.setFixedSize(30, 30)
        button_del_page.setCursor(self.cursor_pointer)
        button_del_page.setToolTip('Delete instruction page')
        pages_layout.addWidget(button_del_page)

        combo_page = QComboBox(self.window)
        combo_page.setGeometry(875, 116, 220, 35)

        text_page = QTextEdit(self.window)
        text_page.setStyleSheet(f'background-color: #0b0917')
        text_page.setGeometry(878, 118, 195, 30)

        regex_area = QTextEdit()
        regex_area.setStyleSheet(f'background-color: #0b0917')
        regex_area.setPlaceholderText('• Example regex input:\n\n^\nMade_by_\n\\s\n_\n\\n\n_2025')
        controls_layout.addWidget(regex_area)

        button_source = QLabel(self.window)
        button_source.setPixmap(QPixmap("./src/imgs/load_txt.png").scaledToHeight(30))
        button_source.setCursor(self.cursor_pointer)
        button_source.setToolTip('Open input file')
        button_source.setGeometry(800, 20, 30, 30)

        button_new_file.mousePressEvent = lambda ev: file_handler_ref.new_file(combo_page, text_page, regex_area)
        button_load.mousePressEvent = lambda ev: file_handler_ref.load_file(combo_page, text_page, regex_area)
        button_save.mousePressEvent = lambda ev: file_handler_ref.save_file()
        button_run.mousePressEvent = lambda ev: regex_handler_ref.regexec(text_area, regex_area)
        button_new_page.mousePressEvent = lambda ev: page_handler_ref.new_page(combo_page)
        button_del_page.mousePressEvent = lambda ev: page_handler_ref.rmv_page(combo_page)

        regex_area.keyReleaseEvent = lambda e: page_handler_ref.update_instructions(regex_area)
        text_page.keyReleaseEvent = lambda e: page_handler_ref.update_name(combo_page, text_page)

        combo_page.currentIndexChanged.connect(lambda e: page_handler_ref.change_selection_event(combo_page, text_page, regex_area))

        button_source.mousePressEvent = lambda ev: file_handler_ref.handle_button_source(text_area, button_source, lbl_source)

        file_handler_ref.new_file(combo_page, text_page, regex_area)