import sys, os, logging
from pathlib import Path
from PyQt6 import QtWidgets, QtGui, QtCore
from mp3_gui_widget import MusWind
from tag_musfile import MusFile
from flac_gui_widget import FlacWind
from tag_flacfile import FlacFile
from flac_gui_widget_folder import FlacFolderWind
from mp3_gui_widget_folder import MusFolderWind

logging.basicConfig(level=logging.DEBUG, filename='main_gui.log',  force=True,
                    format='%(asctime)s - %(levelname)s : %(message)s')

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
        '''Process file or directory selected through the QTreeView, get 
        tags in common and send that information to a separate window for
        editing those common tags.
        '''
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
                tagnames = set()
                for file in files_to_edit:
                    flacfiles[Path(file)] = FlacFile(file)
                for tag in flacfiles[Path(file)].vcomments.keys():
                    tagnames.add(tag)
                commontags = {}
                anyflac = list(flacfiles.values())[0]
                for tag in tagnames:
                        if all(flac.vcomments.get(tag) == anyflac.vcomments.get(tag)
                                for flac in flacfiles.values()):    
                            commontags[tag] = anyflac.vcomments[tag] 
                self.w = FlacFolderWind(flacfiles, commontags)
                self.w.show()
                                


            elif all((file.endswith('.mp3') for file in files_to_edit)):
                mp3files = {}
                tagnames = set()
                for file in files_to_edit:
                    mp3files[Path(file)] = MusFile(file)
                for tag in mp3files[Path(file)].active_tags.keys():
                    tagnames.add(tag)
                commontags = {}
                anymp3 = list(mp3files.values())[0]
                for tag in tagnames:
                        if all(mp3.active_tags.get(tag) == anymp3.active_tags.get(tag)
                                for mp3 in mp3files.values()):    
                            commontags[tag] = anymp3.active_tags[tag]
                self.w = MusFolderWind(mp3files, commontags)
                self.w.show() 

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