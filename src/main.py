from PyQt5.QtWidgets import QApplication
Qt5App = QApplication([])


from windows.MainWindow import MainWindow
from tools.FileHandler import FileHandler
from tools.PageHandler import PageHandler
from tools.RegexHandler import RegexHandler



main_window = MainWindow()
file_handler = FileHandler()
page_handler = PageHandler()
regex_handler = RegexHandler()

file_handler.setup(page_handler)
regex_handler.setup(file_handler)
main_window.setup(file_handler, page_handler, regex_handler)

Qt5App.exec()