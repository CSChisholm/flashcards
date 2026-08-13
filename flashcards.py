#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug  4 21:50:16 2026

@author: craig
"""

import json
import os
import glob
import sys
import copy
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QLineEdit, QPushButton, QHBoxLayout, QListWidget, QVBoxLayout, QLabel, QGridLayout, QScrollArea, QComboBox, QFileDialog, QDialog, QAbstractItemView

#GUI classes
class mainWindow(QMainWindow):
    '''Main window'''
    def __init__(self):
        super().__init__()
        self.sets = {}
        #Set default directory
        self.currentDirectory = f'{os.path.expanduser("~")}/Documents/'
        #Create layout
        self._setTitle()
        self._createMenu()
        self.generalLayout = QHBoxLayout()
        centralWidget = QWidget(self)
        centralWidget.setLayout(self.generalLayout)
        self.setCentralWidget(centralWidget)
        self._setsLayout()
        self._gameArea()
        self._displayList()
        
    def _setsLayout(self):
        self.setsLayout = QVBoxLayout()
        setsTitle = QLabel('Sets')
        self.setsLayout.addWidget(setsTitle)
        self.setsList = QListWidget()
        self.setsList.setSelectionMode(QAbstractItemView.MultiSelection)
        self.setsLayout.addWidget(self.setsList)
        self.setsIO = QHBoxLayout()
        self.openSet = QPushButton('Open Set')
        self.openDirectory = QPushButton('Open Directory')
        self.buildSet = QPushButton('Build Set')
        self.setsIO.addWidget(self.openSet)
        self.setsIO.addWidget(self.openDirectory)
        self.setsIO.addWidget(self.buildSet)
        self.setsLayout.addLayout(self.setsIO)
        self.selectionIO = QHBoxLayout()
        self.selectAll = QPushButton('Select All')
        self.deselectAll = QPushButton('Deselect All')
        self.selectionIO.addWidget(self.selectAll)
        self.selectionIO.addWidget(self.deselectAll)
        self.setsLayout.addLayout(self.selectionIO)
        self.generalLayout.addLayout(self.setsLayout)
    
    def _gameArea(self):
        self.gameLayout = QVBoxLayout()
        self.gameStart = QHBoxLayout()
        self.gameMode = QComboBox()
        self.gameMode.addItems(['A side', 'B side', 'Random'])
        self.gameStart.addWidget(self.gameMode)
        self.startButton = QPushButton('Start')
        self.gameStart.addWidget(self.startButton)
        self.gameLayout.addLayout(self.gameStart)
        self.gameCard = QLabel()
        self.gameCard.setStyleSheet('border: 1px solid black;')
        self.gameCard.setScaledContents(True)
        self.gameLayout.addWidget(self.gameCard)
        self.entryLayout = QHBoxLayout()
        self.answerField = QLineEdit()
        self.entryLayout.addWidget(self.answerField)
        self.answerButton = QPushButton('Go')
        self.entryLayout.addWidget(self.answerButton)
        self.gameLayout.addLayout(self.entryLayout)
        self.generalLayout.addLayout(self.gameLayout)
    
    def _displayList(self):
        self.displayList = QListWidget()
        self.generalLayout.addWidget(self.displayList)
    
    def _createMenu(self):
        menu = self.menuBar().addMenu('&Menu')
        menu.addAction('&Exit', self.close, shortcut='Alt+F4')
        menu.addAction('&Information', self._helpPopUp, shortcut='Ctrl+H')
    
    def _getVersion(self):
        with open('helptext.txt','r') as f:
            lines = f.readlines()
        for line in lines:
            if 'Version - ' in line:
                return line.split('Version - ')[-1].strip('\n')
    
    def _setTitle(self):
        self.setWindowTitle(f'Flash Cards {self._getVersion()}')
    
    def _loadFile(self, fileName: str):
        with open(fileName,'r') as f:
            setData = json.loads(f.read())
        self.sets.update({self._file2key(fileName):
                          {'pairs': setData, 'fileName': fileName}})
    
    def _openSet(self, fileName: str | None = None):
        refresh = False
        if fileName is None:
            fileName = QFileDialog.getOpenFileName(self,'',self.currentDirectory)[0]
            refresh = True
            if not fileName=='':
                self.currentDirectory = fileName[:-len(fileName.split('/')[-1])]
        try:
            self._loadFile(fileName)
        except:
            pass
        if refresh:
            self._displaySets()
    
    def _displaySets(self):
        previousSelected = [selected.text() for selected in self.setsList.selectedItems()]
        self.setsList.clear()
        for itr, key in enumerate(sorted(self.sets.keys())):
            self.setsList.addItem(key)
            if key in previousSelected:
                self.setsList.setCurrentRow(itr)
    
    def _openDirectory(self):
        self.currentDirectory = QFileDialog.getExistingDirectory(self,'',self.currentDirectory)
        files = glob.glob(f'{self.currentDirectory}/**/*.flashcard',recursive=True)
        for fileName in files:
            self._openSet(fileName)
        self._displaySets()
    
    def _file2key(self, fileName: str) -> str:
        '''Returns a unique key form a file name'''
        baseRemoved = fileName.split(f'{os.path.expanduser("~")}/Documents/')[1]
        return baseRemoved.replace('/','>').split('.flashcard')[0]
    
    def _buildSet(self):
        self.setWindow = setBuilder(self)
        self.setWindow.setWindowTitle('Set Builder')
        self.setWindow.setWindowModality(Qt.ApplicationModal)
        self.setWindow.show()
    
    def _start(self):
        return
    
    def _submit(self):
        return
    
    def _helpPopUp(self):
        self.hWindow = helpWindow()
        self.hWindow.setWindowTitle(f'Activity Logger {self._getVersion()} - Information')
        self.hWindow.show()

class helpWindow(QWidget):
    '''General information called by Help menu'''
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        helpText = self._helpText()
        for line in helpText:
            label = QLabel(line)
            label.setOpenExternalLinks(True)
            layout.addWidget(label)
        self.closeButton = QPushButton('OK')
        layout.addWidget(self.closeButton)
        self.setLayout(layout)
        self.closeButton.clicked.connect(self.close)
    
    def _helpText(self):
        with open('helptext.txt','r') as f:
            lines = f.readlines()
        return lines

class setBuilder(QWidget):
    '''Set builder window'''
    def __init__(self,parent):
        super().__init__()
        self.parent = parent
        self.tempSets = copy.deepcopy(self.parent.sets)
        layout = QVBoxLayout()
        self.fileLayout = QHBoxLayout()
        self.fileField = QComboBox()
        self.fileField.addItems(list(self.parent.sets.keys()))
        self.fileName = None
        self.fileDialog = QPushButton('New Set')
        self.fileLayout.addWidget(self.fileField)
        self.fileLayout.addWidget(self.fileDialog)
        layout.addLayout(self.fileLayout)
        self.fieldFormScroll = QScrollArea(self)
        layout.addWidget(self.fieldFormScroll)
        self._displayPairs()
        self.addCard = QPushButton('Add Card')
        layout.addWidget(self.addCard)
        self.ioLayout = QHBoxLayout()
        self.cancelButton = QPushButton('Cancel')
        self.confirmButton = QPushButton('Confirm')
        self.ioLayout.addWidget(self.cancelButton)
        self.ioLayout.addWidget(self.confirmButton)
        layout.addLayout(self.ioLayout)
        self.setLayout(layout)
        self.fileField.currentIndexChanged.connect(self._displayPairs)
        self.fileDialog.clicked.connect(self._fileDialog)
        self.addCard.clicked.connect(self._addCard)
        self.cancelButton.clicked.connect(self.close)
        self.confirmButton.clicked.connect(self._confirm)
    
    def _fileDialog(self):
        fileName = QFileDialog.getSaveFileName(self,'',self.parent.currentDirectory)[0]
        self._newSet(fileName)
    
    def _newSet(self, fileName: str):
        if not os.path.exists(fileName):
            if not fileName.split('.')[-1]=='flashcard':
                fileName+='.flashcard'
            self.parent.currentDirectory = fileName[:-len(fileName.split('/')[-1])]
            self.tempSets.update({self.parent._file2key(fileName): {'pairs': {'a': 'b'}, 'fileName': fileName}})
            self.fileField.addItem(self.parent._file2key(fileName))
        self.fileField.setCurrentText(self.parent._file2key(fileName))
        self._displayPairs()
    
    def _displayPairs(self):
        fieldFormScrollContents = QWidget()
        self.fieldForm = QGridLayout(fieldFormScrollContents)
        self.currentSet = self.fileField.currentText()
        if not self.currentSet=='':
            self.editBoxes = []
            for row, (a, b) in enumerate(self.tempSets[self.currentSet]['pairs'].items()):
                self.editBoxes.append([QLineEdit(a), QLineEdit(b)])
                self.fieldForm.addWidget(self.editBoxes[row][0],row,0)
                self.fieldForm.addWidget(self.editBoxes[row][1],row,1)
                for editBox in self.editBoxes[-1]:
                    editBox.textChanged.connect(self._updateSet)
        self.fieldFormScroll.setWidget(fieldFormScrollContents)
    
    def _updateSet(self):
        self.tempSets[self.currentSet]['pairs'] = {}
        for (aBox, bBox) in self.editBoxes:
            self.tempSets[self.currentSet]['pairs'].update({aBox.text(): bBox.text()})
    
    def _addCard(self):
        self.tempSets[self.currentSet]['pairs'].update({'a': 'b'})
        self._displayPairs()
    
    def _confirm(self):
        for saveSet in self.tempSets.values():
            for key in saveSet.keys():
                if '' in [key, saveSet[key]]:
                    saveSet.pop(key)
                with open(saveSet['fileName'],'w') as f:
                    f.write(json.dumps(saveSet['pairs']))
        self.parent.sets = copy.deepcopy(self.tempSets)
        self.parent._displaySets()
        self.close()

#Run loop
class controller:
    '''Controller module'''
    def __init__(self,model,view):
        self._evaluate = model
        self._view = view
        self._connectSignalsAndSlots()
    
    def _connectSignalsAndSlots(self):
        self._view.openSet.clicked.connect(self._view._openSet)
        self._view.openDirectory.clicked.connect(self._view._openDirectory)
        self._view.buildSet.clicked.connect(self._view._buildSet)
        self._view.selectAll.clicked.connect(self._view.setsList.selectAll)
        self._view.deselectAll.clicked.connect(self._view.setsList.clearSelection)
        self._view.startButton.clicked.connect(self._view._start)
        self._view.answerField.returnPressed.connect(self._view._submit)
        self._view.answerButton.clicked.connect(self._view._submit)

def main():
    '''Main loop'''
    elApp = QApplication([])
    elWindow = mainWindow()
    elWindow.show()
    controller(model=None,view=elWindow)
    sys.exit(elApp.exec())

if (__name__=='__main__'):
    main()