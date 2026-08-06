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
        self.newSet = QPushButton('New Set')
        self.setsIO.addWidget(self.openSet)
        self.setsIO.addWidget(self.openDirectory)
        self.setsIO.addWidget(self.newSet)
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
    
    def _loadFile(fileName: str) -> dict:
        with open(fileName,'r') as f:
            items = json.loads(f.read())
        return items
    
    def _openSet(self, fileName: str | None = None):
        refresh = False
        if fileName is not None:
            fileName = QFileDialog.getOpenFileName(self,'',self.currentDirectory)[0]
            refresh = True
        if not fileName=='':
            self.currentDirectory = fileName[:-len(fileName.split('/')[-1])]
            try:
                setData = self._loadFile(fileName)
                self.sets.update({fileName.split('/')[-1].split('.flashcard')[0]: setData})
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
        files = glob.glob(f'{self.currentDirectory}/**/*.flashcard')
        for fileName in files:
            self._openSet(fileName)
        self._displaySets()
    
    def _newSet(self):
        self.setWindow = setBuilder(self)
        self.setWindow.setWindowTitle('New Set')
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
        layout = QVBoxLayout()
        self.fileLayout = QHBoxLayout()
        self.fileField = QLineEdit()
        self.fileDialog = QPushButton('Select File')
        self.fileLayout.addWidget(self.fileField)
        self.fileLayout.addWidget(self.fileDialog)
        layout.addLayout(self.fileLayout)
        self.fieldForm = QScrollArea(self)
        layout.addWidget(self.fieldForm)
        self.addCard = QPushButton('Add Card')
        layout.addWidget(self.addCard)
        self.setLayout(layout)

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
        self._view.newSet.clicked.connect(self._view._newSet)
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