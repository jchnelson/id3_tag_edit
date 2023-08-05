import sys, re, logging
from PyQt6 import QtWidgets
from PyQt6.QtCore import Qt
from tag_flacfile import FlacFile
from id3_standard_tags import vorbis_dict
from flac_splice import write_tags

logging.basicConfig(level=logging.DEBUG, filename='flac_gui_qwidget_folder.log', 
                    format='%(asctime)s - %(levelname)s : %(message)s', force=True)


class FlacFolderWind(QtWidgets.QWidget):
    '''Create main window, also holds instance of MusFile to manipulate its data
    '''
    def __init__(self, flacfiles: dict[str, FlacFile], commontags: dict[str,str]):
        super().__init__()
        self.widgets = {}
        self.flacfiles = flacfiles
        self.fullcommontags = commontags.copy()
        self.commontags = commontags

        self.setWindowTitle('Vorbis Comment Edit')
        self.layout = QtWidgets.QFormLayout()



        self.adder = QtWidgets.QComboBox()
        self.adder.setPlaceholderText('Select Vorbis Comment to Add')
        self.adder.addItems([f'{type}: {tag}' for type,tag in vorbis_dict.items()])
        self.add_btn = QtWidgets.QPushButton('Add Vorbis Comment')
        self.add_btn.clicked.connect(self.add_tag)

        self.remover = QtWidgets.QComboBox()
        self.remover.setPlaceholderText('Select Vorbis Comment to Remove')
        for comment in self.commontags:
            self.remover.addItem(comment)
        self.remove_btn = QtWidgets.QPushButton('Remove Tag')
        self.remove_btn.clicked.connect(self.remove_tag)

        fm = self.remover.fontMetrics()
        self.remover_width = max([fm.boundingRect(self.remover.itemText(i)).width() 
                        for i in range(self.remover.count())])
        self.remover.view().setMinimumWidth(self.remover_width)

        self.max_lineedit = 0
        self.max_label = 0
        for comment in self.commontags:
            self.add_fieldrow(comment, initcall=True)

        self.layout.addRow(self.add_btn, self.adder)
        self.layout.addRow(self.remove_btn, self.remover)

        self.main_button = QtWidgets.QPushButton('Confirm')
        self.main_button.clicked.connect(self.main_clicked)
        self.layout.addRow('', self.main_button)

        self.scroll = QtWidgets.QScrollArea()
        self.scroller = self.scroll
        self.container = QtWidgets.QWidget()
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
            self.layout.insertRow(index, f"{vorbis_dict[tagtype]} :", a)
            self.remover.addItem(tagtype)
            # self.flacfile.vcomments[tagtype] = '' 
        else:
            try:
                self.layout.addRow(f"{vorbis_dict[tagtype]} :", a)
            except:
                self.layout.addRow(f'{tagtype} :', a)

        if active:
            a.setPlaceholderText(f"{self.commontags[tagtype]}")
        else:
            try:
                a.setPlaceholderText(f"{vorbis_dict[tagtype]}")
            except KeyError:
                a.setPlaceholderText(f'{tagtype}')


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
        else:
            self.update_width()

    def remove_tag(self):
        '''Confirm removal of tag from proposed and remove gui row containing it,
        as well as references to widgets and the data itself, then remove it
        '''
        confirm = QtWidgets.QMessageBox
        response = confirm.question(self, 'Confirm Removal', 'Really remove tag? \n'\
                                           '(This action cannot be undone)',
                                             confirm.StandardButton.Yes |
                                               confirm.StandardButton.No)
        
        if response == confirm.StandardButton.Yes and self.remover.currentText():
            tagname = self.remover.currentText()
            self.remover.removeItem(self.remover.currentIndex())
            a = self.layout.getWidgetPosition(self.widgets[tagname])
            self.layout.removeRow(a[0])
            self.widgets.pop(tagname)
            self.commontags.pop(tagname)

    def add_tag(self):
        '''If tag doesn't exist in the GUI already, add it through
            add_fieldrow.'''
        if self.adder.currentText():
            tagmatch = re.search(r'(.*?): (.+)', self.adder.currentText())
            tagname = tagmatch.group(1)
            remover_options = [self.remover.itemText(i) for i in range(self.remover.count())]
            if tagmatch.group(1) not in remover_options:
                if tagname in self.commontags:
                    self.add_fieldrow(tagname)
                else:
                    self.add_fieldrow(tagname, active=False)
                
        

    def main_clicked(self):
        '''If text has been entered into form layout, use that to create 
            vorbis comment structure, otherwise use placeholder text of the 
            original tag to make the comment. Send the results to write_tags.
        '''
        newtags = {}
        for tagtype, widget in self.widgets.items():
            if widget.text() == '':
                newtags[tagtype] = widget.placeholderText()
            else:
                newtags[tagtype] = widget.text()
        try:
            if self.widgets['TITLE'].text():
                self.flacfile.newtitle = self.widgets['TITLE'].text()
        except KeyError:  # Allow for case of non-standard title tag
            pass
        for tagtype, tagdata in self.fullcommontags.items():
            if tagtype in self.fullcommontags:
                if not tagtype in newtags:
                    for flac in self.flacfiles.values():
                        flac.vcomments.pop(tagtype)
        logging.debug('Handing off to write_tags...')
        logging.debug(f'newtags = {newtags}')
        full_success = 0
        for type, tag in newtags.items():
            for flac in self.flacfiles.values():
                flac.vcomments[type] = tag
        for flac in self.flacfiles.values():
            tagtext = []
            for tagtype, tagdata  in flac.vcomments.items():
                    tagtext.append(f'{tagtype}={tagdata}')               
            success = write_tags(flac, tagtext)
            if success:
                full_success += 1

        if full_success == len(list(self.flacfiles.keys())):  
            info = QtWidgets.QMessageBox
            info.information(self, "Success","Files successfully created in \n output folder!")



if __name__ == "__main__":

    app = QtWidgets.QApplication(sys.argv)
    filename = QtWidgets.QFileDialog.getExistingDirectory(directory='C:\\Users\\projectsvs\\py_qt\\id3_tag_edit\\music', 
                                     caption='Choose a Directory')
    flacfile = FlacFile(filename[0])

    window = FlacFolderWind(flacfile)
    window.show()

    sys.exit(app.exec())