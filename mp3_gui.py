import sys, re, logging
from PyQt6 import QtWidgets
from id3_standard_tags import music_tags
from tag_musfile import MusFile
from mp3_splice import write_tags

logging.basicConfig(level=logging.DEBUG, filename='mp3_gui.log', 
                    format='%(asctime)s - %(levelname)s : %(message)s', force=True)


class MusWind(QtWidgets.QMainWindow):
    '''Create main window, also holds instance of MusFile to manipulate its data
    '''
    def __init__(self, taglist, musfile:MusFile):
        super().__init__()
        self.taglist = taglist
        self.widgets = {}
        self.musfile = musfile

        self.setWindowTitle('Mp3 Tag Edit')
        self.layout = QtWidgets.QFormLayout()

        self.max_lineedit = 0
        for tagtype in taglist:
            self.add_fieldrow(tagtype, initcall=True)

        self.adder = QtWidgets.QComboBox()
        self.adder.addItems([f'{key}: {value}' for key,value in self.musfile.tagdict.items()])
        self.add_btn = QtWidgets.QPushButton('Add Tag')
        self.add_btn.clicked.connect(self.add_tag)

        self.remover = QtWidgets.QComboBox()
        self.remover.setPlaceholderText('Select Tag to Remove')
        for tagtype in taglist:
            try:
                self.remover.addItem(music_tags[tagtype][0])
            except KeyError:
                try:
                    self.remover.addItem(self.musfile.tagdict[tagtype])
                except KeyError:
                    self.remover.addItem(f'Noncompliant Tag {tagtype}')
        self.remove_btn = QtWidgets.QPushButton('Remove Tag')
        self.remove_btn.clicked.connect(self.remove_tag)

        self.layout.addRow(self.adder, self.add_btn)
        self.layout.addRow(self.remover, self.remove_btn)

        self.main_button = QtWidgets.QPushButton('Confirm')
        self.main_button.clicked.connect(self.main_clicked)
        self.layout.addRow('', self.main_button)

        self.container = QtWidgets.QWidget()
        self.container.setLayout(self.layout)
        self.setCentralWidget(self.container)

    def add_fieldrow(self, tagtype, initcall=False, active=True):
        '''Add rows to form layout upon creation of MainWindow, insert rows
        when called by button
        '''
        a = QtWidgets.QLineEdit()
        if not initcall:
            index = self.layout.getWidgetPosition(self.add_btn)[0]
            try:
                self.layout.insertRow(index, f"{music_tags[tagtype][0]} :", a)
                self.remover.addItem(music_tags[tagtype][0])
            except KeyError:
                try:
                    self.layout.insertRow(index, f"{self.musfile.tagdict[tagtype]} :", a)
                    self.remover.addItem(self.musfile.tagdict[tagtype]) 
                except KeyError:
                    self.layout.insertRow(index, f"Noncompliant Tag {tagtype} :", a)
                    self.remover.addItem(f"Noncompliant Tag {tagtype}")
            self.musfile.active_tags[tagtype] = '' 
        else:
            try:
                self.layout.addRow(f"{music_tags[tagtype][0]} :", a)
            except KeyError:
                try:
                    self.layout.addRow(f"{self.musfile.tagdict[tagtype]} :", a)
                except KeyError:
                    self.layout.addRow(f"Noncompliant Tag {tagtype} :", a)
        if active:
            a.setPlaceholderText(f"{self.musfile.active_tags[tagtype]}")
        else:
            a.setPlaceholderText(f"{self.musfile.tagdict[tagtype]}")


        self.widgets[tagtype] = a
        width = a.fontMetrics().boundingRect(a.placeholderText()).width()
        if  width > self.max_lineedit:
            self.max_lineedit = width + 10
            a.setMinimumWidth(self.max_lineedit)

    def remove_tag(self):
        '''Confirm removal of tag from proposed and remove gui row containing it,
        as well as references to widgets and the data itself, then remove it
        '''
        confirm = QtWidgets.QMessageBox
        response = confirm.question(self, 'Confirm Removal', 'Really remove tag? \n'\
                                           '(This action cannot be undone)',
                                             confirm.StandardButton.Yes |
                                               confirm.StandardButton.No)
        
        if response == confirm.StandardButton.Yes:
            tagname = ''
            for tagtype, tagtext in music_tags.items():
                if self.remover.currentText() == tagtext[0]:
                    tagname = tagtype
            for tagtype, tagtext in self.musfile.tagdict.items():
                if self.remover.currentText() == tagtext:
                    tagname = tagtype
            if tagname == '':
                tagmatch = re.search('Noncompliant Tag (.+)', self.remover.currentText())
                tagname = tagmatch.group(1)

            self.remover.removeItem(self.remover.currentIndex())
            a = self.layout.getWidgetPosition(self.widgets[tagname])
            self.layout.removeRow(a[0])
            self.widgets.pop(tagname)
            self.musfile.active_tags.pop(tagname)

    def add_tag(self):
        tagname = self.adder.currentText()[:4]
        remover_options = [self.remover.itemText(i) for i in range(self.remover.count())]
        if self.adder.currentText()[6:] not in remover_options:
            if tagname in self.musfile.active_tags:
                self.add_fieldrow(tagname)
            else:
                self.add_fieldrow(tagname, active=False)
                
        

    def main_clicked(self):
        formtext = {}
        for tagtype, widget in self.widgets.items():
            formtext[tagtype] = widget.text()
            if widget.text() == '':
                formtext[tagtype] = widget.placeholderText()
        logging.debug('Handing off to write_tags...')
        logging.debug(f'formtext = {formtext}')
        write_tags(self.musfile, formtext)
        print(formtext)


if __name__ == "__main__":

    app = QtWidgets.QApplication(sys.argv)
    filename = QtWidgets.QFileDialog.getOpenFileName(directory='C:\\Users\\Jakob\\Music', 
                                     caption='Choose a Song', filter="Mp3 Files (*.mp3)")
    musfile = MusFile(filename[0])

    window = MusWind(list(musfile.active_tags.keys()), musfile)
    window.show()

    sys.exit(app.exec())