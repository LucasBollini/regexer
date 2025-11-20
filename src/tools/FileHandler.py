from PyQt5.QtWidgets import QFileDialog, QTextEdit, QLabel, QComboBox
from PyQt5.QtGui import QPixmap


from tools.PageHandler import PageHandler


class FileHandler:

    file_picker = QFileDialog()
    flag_save : bool = False
    source_url : str = ''
    source_content : str = ''

    page_handler : PageHandler


    def setup(self, page_handler_ref : PageHandler):
        self.page_handler = page_handler_ref


    def load_file(self, combo_page : QComboBox, text_page : QTextEdit, regex_area : QTextEdit):
        file_url = self.file_picker.getOpenFileUrl(filter='*.rgxr')[0].url()[7:]

        if not file_url:
            return
        
        self.page_handler.clear_pages(combo_page, text_page, regex_area)

        with open(file_url) as file_ref:
            self.page_handler.load_pages(file_ref, combo_page, text_page, regex_area)
            self.flag_save = True


    def save_file(self):
        file_url = self.file_picker.getSaveFileUrl(filter='*.rgxr')[0].url()[7:]

        if not file_url:
            return

        if file_url[-5:] != '.rgxr':
            file_url += '.rgxr'

        with open(file_url, 'w') as file_ref:
            for page_id in self.page_handler.page_dict.keys():
                file_ref.write(f'\n{page_id} {self.page_handler.page_dict[page_id]['name']}\n')
                file_ref.write('\n'.join(self.page_handler.page_dict[page_id]['instructions']))
            file_ref.write('\n') # Adds a breakline to the end of the file, to prevent the PageReader from deleting the last character of the instructions


    def new_file(self, combo_page : QComboBox, text_page : QTextEdit, regex_area : QTextEdit):
        self.page_handler.clear_pages(combo_page, text_page, regex_area)
        self.page_handler.new_page(combo_page)


    def handle_button_source(self, text_area : QTextEdit, button_source : QLabel, lbl_source : QLabel):
        if self.source_content:
            self.close_source(text_area, button_source)
        else:
            self.open_source(text_area, button_source, lbl_source)
            


    def open_source(self, text_area : QTextEdit, button_source : QLabel, lbl_source : QLabel):
        file_url = self.file_picker.getOpenFileUrl()[0].url()[7:]

        if not file_url:
            return
        
        with open(file_url) as file_ref:
            self.source_url = file_url
            self.source_content = file_ref.read()
            lbl_source.setText(f'File being modified: {file_url}')
            text_area.setVisible(False)
            button_source.setPixmap(QPixmap("./src/imgs/unload_txt.png").scaledToHeight(30))
            button_source.setToolTip('Close input file')
    

    def save_source(self):
        with open(self.source_url, 'w') as file_ref:
            file_ref.write(self.source_content)


    def close_source(self, text_area : QTextEdit, button_source : QLabel):
        self.source_url = ''
        self.source_content = ''
        text_area.setVisible(True)
        button_source.setPixmap(QPixmap("./src/imgs/load_txt.png").scaledToHeight(30))
        button_source.setToolTip('Open input file')