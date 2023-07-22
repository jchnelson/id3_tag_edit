import sys
from PyQt6 import QtWidgets
from id3_standard_tags import tagdict as full_tagdict
from id3_standard_tags import music_tags
from tag_musfile import MusFile

class MainWind(QtWidgets.QMainWindow):
    global initated
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
        self.adder.addItems([f'{key}: {value}' for key,value in full_tagdict.items()])
        self.add_btn = QtWidgets.QPushButton('Add Tag')
        self.add_btn.clicked.connect(self.add_tag)

        self.remover = QtWidgets.QComboBox()
        self.remover.setPlaceholderText('Select Tag to Remove')
        for tagtype in taglist:
            try:
                self.remover.addItem(music_tags[tagtype][0])
            except KeyError:
                self.remover.addItem(full_tagdict[tagtype])
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
        a = QtWidgets.QLineEdit()
        if not initcall:
            index = self.layout.getWidgetPosition(self.add_btn)[0]
            try:
                self.layout.insertRow(index, f"{music_tags[tagtype][0]} :", a)
                self.remover.addItem(music_tags[tagtype][0])
            except KeyError:
                self.layout.insertRow(index, f"{full_tagdict[tagtype]} :", a)
                self.remover.addItem(full_tagdict[tagtype]) 
            self.musfile.active_tags[tagtype] = '' 
        else:
            try:
                self.layout.addRow(f"{music_tags[tagtype][0]} :", a)
            except KeyError:
                self.layout.addRow(f"{full_tagdict[tagtype]} :", a)
        if active:
            a.setPlaceholderText(f"{self.musfile.active_tags[tagtype]}")
        else:
            a.setPlaceholderText(f"{full_tagdict[tagtype]}")


        self.widgets[tagtype] = a
        width = a.fontMetrics().boundingRect(a.placeholderText()).width()
        if  width > self.max_lineedit:
            self.max_lineedit = width + 10
            a.setMinimumWidth(self.max_lineedit)

    def remove_tag(self):
        tagname = ''
        for tagtype, tagtext in music_tags.items():
            if self.remover.currentText() == tagtext[0]:
                tagname = tagtype
        for tagtype, tagtext in full_tagdict.items():
            if self.remover.currentText() == tagtext:
                tagname = tagtype

        self.remover.removeItem(self.remover.currentIndex())
        a = self.layout.getWidgetPosition(self.widgets[tagname])
        self.layout.removeRow(a[0])
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
        print(formtext)


if __name__ == "__main__":

    app = QtWidgets.QApplication(sys.argv)
    filename = QtWidgets.QFileDialog.getOpenFileName(directory='C:\\Users\\Jakob\\Music', 
                                     caption='Choose a Song', filter="Mp3 Files (*.mp3)")
    musfile = MusFile(filename[0])

    window = MainWind(list(musfile.active_tags.keys()), musfile)
    window.show()

    sys.exit(app.exec())