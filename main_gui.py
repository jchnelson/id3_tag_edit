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
        self.filesystem.setRootPath('C:\\')
        self.file_list.setModel(self.filesystem)
        self.file_list.setRootIndex(self.filesystem.index('C:\\'))
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
        self.rightlabeltop = QtWidgets.QLabel('<h1>Select A File</h1>')
        self.rightlabelmid = QtWidgets.QLabel('To edit its tags/comments')
        self.rightlabelbot = QtWidgets.QLabel('mp3 and flac supported')
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
        if selected_file_path.is_dir():

            files_to_edit = []
            for file in os.listdir(selected_file_path):
                currpath = Path(file)
                if currpath.suffix == '.flac' or currpath.suffix == '.mp3':
                    files_to_edit.append(os.path.join(selected_file_path, file))

            if all(file.endswith('.flac') for file in files_to_edit):
                flacfiles = {}
                for file in files_to_edit:
                    flacfiles[Path(file).stem] = FlacFile(file)
                print(flacfiles)

            elif all((file.endswith('.mp3') for file in files_to_edit)):
                mp3files = {}
                for file in files_to_edit:
                    mp3files[Path(file).stem] = MusFile(file)
                print(mp3files)

            else:
                raise TypeError("All audio files must be same format")

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