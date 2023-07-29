import sys, os
from pathlib import Path
from PyQt6 import QtWidgets, QtGui, QtCore
from mp3_gui_widget import MusWind
from tag_musfile import MusFile
from flac_gui_widget import FlacWind
from tag_flacfile import FlacFile

class MusMainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.w = None

        layout = QtWidgets.QHBoxLayout()

        leftlayout = QtWidgets.QVBoxLayout()

        self.file_list = QtWidgets.QTreeView()
        self.filesystem = QtGui.QFileSystemModel()
        self.filesystem.setRootPath('C:\\Users\\Jakob\\Music')
        self.file_list.setModel(self.filesystem)
        self.file_list.setRootIndex(self.filesystem.index('C:\\Users\\Jakob\\projectsvs\\py_qt\\id3_tag_edit\\music'))
        self.file_list.setColumnWidth(0, 300)
        self.file_list.resizeColumnToContents(1)
        self.file_list.hideColumn(3)
        self.file_list.hideColumn(2)
        self.file_list.setMinimumSize(360, 300)

        self.select_files_btn = QtWidgets.QPushButton('Select File/Folder for Editing')
        self.select_files_btn.clicked.connect(self.file_select)
    
        leftlayout.addWidget(self.file_list)
        leftlayout.addWidget(self.select_files_btn)

        self.rightcontainer = QtWidgets.QWidget()
    
        
        rightlayout = QtWidgets.QVBoxLayout()
        rightlayout.setAlignment(QtCore.Qt.AlignmentFlag.AlignTop)
        rightlayout.addWidget(self.rightcontainer)
        self.rightlabeltop = QtWidgets.QLabel('<h1>This a Label</h1>')
        self.rightlabelmid = QtWidgets.QLabel('This a Label')
        self.rightlabelbot = QtWidgets.QLabel('<h1>This a Label</h1>')
        rightlayout.addWidget(self.rightlabeltop)
        rightlayout.addWidget(self.rightlabelmid)
        rightlayout.addWidget(self.rightlabelbot)



        layout.addLayout(leftlayout)
        layout.addLayout(rightlayout)

    
        self.container = QtWidgets.QWidget()
        self.container.setLayout(layout)
        self.setCentralWidget(self.container)

    def file_select(self):
        index = self.file_list.currentIndex()
        selected_file = self.filesystem.filePath(index)
        selected_file_path = Path(selected_file)
        if selected_file_path.suffix.lower() == '.mp3':
            musfile = MusFile(selected_file)
            self.w = MusWind(musfile)
            self.w.show()
        elif selected_file_path.suffix.lower() == '.flac':
            flacfile = FlacFile(selected_file)
            self.w = FlacWind(flacfile)
            self.w.show()


app = QtWidgets.QApplication(sys.argv)

mus_main = MusMainWindow()
mus_main.show()

sys.exit(app.exec())