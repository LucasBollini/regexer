from PyQt5.QtWidgets import QTextEdit



def clear_all(text_area: QTextEdit, regex_area: QTextEdit):
    text_area.setText('')
    regex_area.setText('')