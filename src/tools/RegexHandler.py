import re

from PyQt5.QtWidgets import QTextEdit

from tools.FileHandler import FileHandler


class RegexHandler:

    file_handler : FileHandler


    def setup(self, file_handler_ref : FileHandler):
        self.file_handler = file_handler_ref


    def regexec(self,text_area : QTextEdit, regex_area : QTextEdit):
        instructions = regex_area.toPlainText().splitlines()
        target_text = self.file_handler.source_content if self.file_handler.source_url else text_area.toPlainText()
        num_instrs = len(instructions)
        stepper = 0

        if num_instrs % 2 != 0:
            num_instrs += 1
            instructions.append('')

        while stepper < num_instrs:
            target_text = re.sub(instructions[stepper], instructions[stepper + 1], target_text)
            stepper += 2

        if self.file_handler.source_url:
            self.file_handler.source_content = target_text
            self.file_handler.save_source()
        else:
            text_area.setText(target_text)