import sys, re, logging
from PyQt6 import QtWidgets
from flac_splice import FlacFile
from id3_standard_tags import vorbis_dict

logging.basicConfig(level=logging.DEBUG, filename='flac_gui.log', 
                    format='%(asctime)s - %(levelname)s : %(message)s', force=True)


class FlacWind(QtWidgets.QMainWindow):
    '''Create main window, also holds instance of MusFile to manipulate its data
    '''
    def __init__(self, flacfile:FlacFile):
        super().__init__()
        self.widgets = {}
        self.flacfile = flacfile

        self.setWindowTitle('Vorbis Comment Edit')
        self.layout = QtWidgets.QFormLayout()

        self.max_lineedit = 0
        for comment in self.flacfile.vcomments:
            self.add_fieldrow(comment, initcall=True)

        self.adder = QtWidgets.QComboBox()
        self.adder.setPlaceholderText('Select Vorbis Comment to Add')
        self.adder.addItems([f'{type}: {tag}' for type,tag in vorbis_dict.items()])
        self.add_btn = QtWidgets.QPushButton('Add Vorbis Comment')
        self.add_btn.clicked.connect(self.add_tag)

        self.remover = QtWidgets.QComboBox()
        self.remover.setPlaceholderText('Select Vorbis Comment to Remove')
        for comment in flacfile.vcomments:
            self.remover.addItem(comment)
        self.remove_btn = QtWidgets.QPushButton('Remove Tag')
        self.remove_btn.clicked.connect(self.remove_tag)

        self.layout.addRow(self.add_btn, self.adder)
        self.layout.addRow(self.remove_btn, self.remover)

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
            self.layout.insertRow(index, f"{vorbis_dict[tagtype]} :", a)
            self.remover.addItem(vorbis_dict[tagtype])
            self.flacfile.vcomments[tagtype] = '' 
        else:
            self.layout.addRow(f"{vorbis_dict[tagtype]} :", a)

        if active:
            a.setPlaceholderText(f"{self.flacfile.vcomments[tagtype]}")
        else:
            a.setPlaceholderText(f"{vorbis_dict[tagtype]}")


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
            tagname = self.remover.currentText()
            self.remover.removeItem(self.remover.currentIndex())
            a = self.layout.getWidgetPosition(self.widgets[tagname])
            self.layout.removeRow(a[0])
            self.widgets.pop(tagname)
            self.flacfile.vcomments.pop(tagname)

    def add_tag(self):
        tagmatch = re.search(r'(.*?): (.+)', self.adder.currentText())
        tagname = tagmatch.group(1)
        remover_options = [self.remover.itemText(i) for i in range(self.remover.count())]
        if tagmatch.group(2) not in remover_options:
            if tagname in self.flacfile.vcomments:
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
        # write_tags(self.musfile, formtext)
        print(formtext)


if __name__ == "__main__":

    app = QtWidgets.QApplication(sys.argv)
    filename = QtWidgets.QFileDialog.getOpenFileName(directory='C:\\Users\\projectsvs\\py_qt\\id3_tag_edit\\music', 
                                     caption='Choose a Song', filter="FLAC Files (*.flac)")
    flacfile = FlacFile(filename[0])

    window = FlacWind(flacfile)
    window.show()

    sys.exit(app.exec())