from PyQt5.QtWidgets import QTextEdit, QComboBox

from _io import TextIOWrapper
import re, time



class PageHandler:

    id_list = []
    page_dict = {}
    current_page : str = ''


    def load_pages(self, file_ref : TextIOWrapper, combo_page : QComboBox, text_page : QTextEdit, regex_area : QTextEdit):
        page_id : str
        page_name : str
        page_holder : dict = {}
        file_ref.readline()

        for line in file_ref.readlines():
            if line[0] == '#':
                page_id = (re.search(r'^#\d+', line) or "")[0]
                page_name = (re.search(r'(?<=\s).+$', line) or "")[0]
                self.id_list.append(page_id)
                page_holder = {'name': page_name, 'instructions': []}
                self.page_dict[page_id] = page_holder
                combo_page.addItem(page_name)
            else:
                page_holder['instructions'].append(line[:-1])
        
        self.change_selection_event(combo_page, text_page, regex_area)


    def new_page(self, combo_page : QComboBox):
        new_id = f'#{time.time_ns()}'
        self.id_list.append(new_id)
        self.page_dict[new_id] = {'name': 'New Page', 'instructions': []}
        combo_page.addItem('New Page')
        combo_page.setCurrentIndex(len(self.id_list) - 1)
        self.current_page = new_id


    def rmv_page(self, combo_page : QComboBox):
        if len(self.id_list):
            del self.page_dict[self.current_page]
            self.id_list.remove(self.current_page)
            combo_page.removeItem(combo_page.currentIndex())
            combo_page.setCurrentIndex(0)
        else:
            self.new_page(combo_page)


    def change_selection_event(self, combo_page : QComboBox, text_page : QTextEdit, regex_area : QTextEdit):
        if len(self.id_list):
            self.current_page = self.id_list[combo_page.currentIndex()]
            text_page.setText(combo_page.currentText())
            regex_area.setText('\n'.join(self.page_dict[self.id_list[combo_page.currentIndex()]]['instructions']))


    def clear_pages(self, combo_page : QComboBox, text_page : QTextEdit, regex_area : QTextEdit):
        self.page_dict.clear()
        self.id_list.clear()
        combo_page.clear()
        text_page.setText('')
        regex_area.setText('')


    def update_instructions(self, regex_area : QTextEdit):        
        self.page_dict[self.current_page]['instructions'] = regex_area.toPlainText().splitlines()


    def update_name(self, combo_page : QComboBox, text_page : QTextEdit):
        self.page_dict[self.current_page]['name'] = text_page.toPlainText()
        combo_page.setItemText(combo_page.currentIndex(), self.page_dict[self.current_page]['name'])