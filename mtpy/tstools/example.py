import sys

from PyQt5.QtWidgets import QWidget

from PyQt5.QtWidgets import QGraphicsView
from PyQt5.QtWidgets import QGraphicsScene
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtWidgets import QHBoxLayout
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtWidgets import QAbstractItemView
from PyQt5.QtWidgets import QTreeWidget
from PyQt5.QtWidgets import QTreeWidgetItem
from PyQt5.QtWidgets import QListView
from PyQt5.QtWidgets import QSplitter
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QStandardItemModel
from PyQt5.QtGui import QStandardItem


from tsscene import TSScene
from tsdata import TSData

import datetime


class TSWindow(QWidget):
    def __init__(self):
        super(TSWindow, self).__init__()

        # view
        self.scene = TSScene()
        viewWidget = QGraphicsView(self.scene)

        # control
        self.buttonOpenFile = QPushButton("open file")
        self.buttonOpenFile.clicked.connect(self.openfile)
        self.waveTree = QTreeWidget()
        self.waveTree.itemClicked.connect(self.showwave)

        controlLayout = QVBoxLayout()
        controlLayout.addWidget(self.buttonOpenFile)
        controlLayout.addWidget(self.waveTree)

        controlWidget = QWidget()
        controlWidget.setLayout(controlLayout)

        # put together
        split = QSplitter()
        split.addWidget(viewWidget)
        split.addWidget(controlWidget)

        layout = QHBoxLayout()
        layout.addWidget(split)
        self.setLayout(layout)
        self.setWindowTitle("TSView")

    def showwave(self, wave):
        if wave.childCount()==0:
            self.scene.togglewave(wave.text(0))




    def exportwave(self, wave):
        print("export",wave.wavename)
        fname = QFileDialog.getSaveFileName(self, 'Save to','/g/data1a/ge3/yuhang/code/mtpy/mtpy/tstools')
        self.scene.exportwaveform(wave.wavename, fname[0])

    # set up wave tree in control region
    def setlist(self):
        item = self.waveTree.invisibleRootItem()
        self.fillitem(item, self.scene.getlist())
        self.waveTree.setSelectionMode(QAbstractItemView.MultiSelection)
        self.waveTree.show()

    # build wave tree
    def fillitem(self, node: QTreeWidgetItem, value: object):
        node.setExpanded(False)
        if type(value) is dict:
            for key, val in sorted(value.items()):
                child = QTreeWidgetItem()
                child.setText(0, str(key))
                node.addChild(child)
                self.fillitem(child, val)
        elif type(value) is list:
            for idx, val in enumerate(value):
                child = QTreeWidgetItem()
                child.setText(0, val)
                node.addChild(child)




    def openfile(self):
        fname = QFileDialog.getOpenFileName(self,
                                            'Open file',
                                            '/g/data/ha3/Passive/_AusArray/OA/ASDF_BU/OA.h5', 'asdf file (*.h5)')

        if len(fname[0]) > 0:
            self.scene.setdata(fname[0])
            self.setlist()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = TSWindow()
    widget.resize(1680, 1050)
    widget.show()
    sys.exit(app.exec_())
