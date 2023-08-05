import sys, re, logging
from PyQt6 import QtWidgets
from PyQt6.QtCore import Qt
from id3_standard_tags import music_tags
from tag_musfile import MusFile
from mp3_splice import write_tags

logging.basicConfig(level=logging.DEBUG, filename='mp3_gui.log', 
                    format='%(asctime)s - %(levelname)s : %(message)s', force=True)


class MusFolderWind(QtWidgets.QWidget):
    '''Create main window, also holds instance of MusFile to manipulate its data
    '''
    def __init__(self, mp3files: dict[str, MusFile], commontags: dict[str,str]):
        super().__init__()
        self.widgets = {}
        self.mp3files = mp3files
        self.fullcommontags = commontags.copy()
        self.commontags = commontags
        self.anymp3 = list(self.mp3files.values())[0]

        self.setWindowTitle('Mp3 Tag Edit')
        self.layout = QtWidgets.QFormLayout()

        self.container = QtWidgets.QWidget()
        
        self.adder = QtWidgets.QComboBox()
        self.adder.addItems([f'{key}: {value}' for key,value in self.anymp3.tagdict.items()])
        self.add_btn = QtWidgets.QPushButton('Add Tag')
        self.add_btn.clicked.connect(self.add_tag)

        self.remover = QtWidgets.QComboBox()
        self.remover.setPlaceholderText('Select Tag to Remove')
        for tagtype in self.commontags:
            try:
                self.remover.addItem(music_tags[tagtype][0])
            except KeyError:
                try:
                    self.remover.addItem(self.anymp3.tagdict[tagtype])
                except KeyError:
                    self.remover.addItem(f'Noncompliant Tag {tagtype}')
        self.remove_btn = QtWidgets.QPushButton('Remove Tag')
        self.remove_btn.clicked.connect(self.remove_tag)
        
        fm = self.remover.fontMetrics()
        self.remover_width = max([fm.boundingRect(self.remover.itemText(i)).width() 
                        for i in range(self.remover.count())])
        self.remover.view().setMinimumWidth(self.remover_width)

        self.max_lineedit = 0
        self.max_label = 0

        for tagtype in self.commontags:
            self.add_fieldrow(tagtype, initcall=True)

        self.layout.addRow(self.add_btn, self.adder)
        self.layout.addRow(self.remove_btn, self.remover)

        self.main_button = QtWidgets.QPushButton('Confirm')
        self.main_button.clicked.connect(self.main_clicked)
        self.layout.addRow(' ', self.main_button)
        

        self.scroll = QtWidgets.QScrollArea()
        self.scroller = self.scroll
        self.scroller.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        
        
        self.scroller.setWidgetResizable(True)
        self.scroller.setWidget(self.container)
        self.container.setLayout(self.layout)

        self.wlayout = QtWidgets.QVBoxLayout()
        self.setLayout(self.wlayout)
        self.wlayout.addWidget(self.scroller)
        self.update_width()

    def update_width(self):
        self.scroller.setFixedWidth(self.wlayout.sizeHint().width() + 40)
        if self.wlayout.sizeHint().height() <= 500:
            self.scroller.setFixedHeight(self.wlayout.sizeHint().height() )
            


    def add_fieldrow(self, tagtype, initcall=False, active=True):
        '''Add rows to form layout upon creation of MainWindow, insert rows
        when called by button
        '''
        a = QtWidgets.QLineEdit()
        if not initcall:
            index = self.layout.getWidgetPosition(self.add_btn)[0]
            try:
                labeltext = f"{music_tags[tagtype][0]} :"
                self.layout.insertRow(index, labeltext, a)
                self.remover.addItem(music_tags[tagtype][0])
            except KeyError:
                try:
                    labeltext = f"{self.anymp3.tagdict[tagtype]} :"
                    self.layout.insertRow(index, labeltext, a)
                    self.remover.addItem(self.anymp3.tagdict[tagtype]) 
                except KeyError:
                    labeltext = f"Noncompliant Tag {tagtype} :"
                    self.layout.insertRow(index, labeltext, a)
                    self.remover.addItem(f"Noncompliant Tag {tagtype}") 
        else:
            try:
                self.layout.addRow(f"{music_tags[tagtype][0]} :", a)
            except KeyError:
                try:
                    self.layout.addRow(f"{self.anymp3.tagdict[tagtype]} :", a)
                except KeyError:
                    self.layout.addRow(f"Noncompliant Tag {tagtype} :", a)
        if active:
            a.setPlaceholderText(f"{self.commontags[tagtype]}")
        else:
            a.setPlaceholderText(f"{self.anymp3.tagdict[tagtype]}")


        self.widgets[tagtype] = a

        if initcall:

            width = a.fontMetrics().boundingRect(a.placeholderText()).width()
            labelindex = self.layout.getWidgetPosition(a)[0]
            alabel = self.layout.itemAt(labelindex, self.layout.ItemRole(0)).widget()
            labelwidth = alabel.fontMetrics().boundingRect(alabel.text()).width()

            if labelwidth > self.max_label:
                self.max_label = labelwidth
            if self.remover_width > self.max_label:
                self.max_label = self.remover_width
            if  width > self.max_lineedit:
                self.max_lineedit = width 

        # if not initcall:
        #     self.update_width()
        

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
            for tagtype, tagtext in self.anymp3.tagdict.items():
                if self.remover.currentText() == tagtext:
                    tagname = tagtype
            if tagname == '':
                tagmatch = re.search('Noncompliant Tag (.+)', self.remover.currentText())
                tagname = tagmatch.group(1)

            self.remover.removeItem(self.remover.currentIndex())
            a = self.layout.getWidgetPosition(self.widgets[tagname])
            self.layout.removeRow(a[0])
            self.widgets.pop(tagname)
            self.commontags.pop(tagname)

    def add_tag(self):
        tagname = self.adder.currentText()[:4]
        remover_options = [self.remover.itemText(i) for i in range(self.remover.count())]
        if self.adder.currentText()[6:] not in remover_options:
            if tagname in self.commontags:
                self.add_fieldrow(tagname)
            else:
                self.add_fieldrow(tagname, active=False)
                
        

    def main_clicked(self):
        '''If text has been entered into form layout, use that to create 
                ID3 comment structure, otherwise use placeholder text of the 
                original tag to make the tag. Send the results to write_tags.
        '''
        newtags = {}
        for tagtype, widget in self.widgets.items():
            if widget.text() == '':
                newtags[tagtype] = widget.placeholderText()
            else:
                newtags[tagtype] = widget.text()

        for tagtype in self.fullcommontags:
            if not tagtype in newtags:
                for mp3 in self.mp3files.values():
                    mp3.active_tags.pop(tagtype)

        for tagtype, tagdata in newtags.items():
            if not tagtype in self.fullcommontags:
                for mp3 in self.mp3files.values():
                    mp3.active_tags[tagtype] = tagdata

        logging.debug('Handing off to write_tags...')
        logging.debug(f'newtags = {newtags}')
        full_success = 0
 
        for mp3 in self.mp3files.values():
            for type, tag in newtags.items():
                mp3.active_tags[type] = tag            
            success = write_tags(mp3, mp3.active_tags)
            if success:
                full_success += 1

        if full_success == len(list(self.mp3files.keys())):  
            info = QtWidgets.QMessageBox
            info.information(self, "Success","Files successfully created in \n output folder!")
    

if __name__ == "__main__":

    app = QtWidgets.QApplication(sys.argv)
    filename = QtWidgets.QFileDialog.getOpenFileName(directory='C:\\Users\\Jakob\\Music', 
                                     caption='Choose a Song', filter="Mp3 Files (*.mp3)")
    musfile = MusFile(filename[0])

    window = MusFolderWind(musfile)
    window.show()

    sys.exit(app.exec())