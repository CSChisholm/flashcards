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
import random
from PyQt5 import QtCore
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QLineEdit,
                             QPushButton, QHBoxLayout, QListWidget, QVBoxLayout,
                             QLabel, QGridLayout, QScrollArea, QComboBox, QFileDialog,
                             QAbstractItemView)

#GUI classes
class mainWindow(QMainWindow):
    '''Main window'''
    def __init__(self,clipboard):
        super().__init__()
        self.clipboard = clipboard
        self.charMods = {'`': u'\u0300', "'": u'\u0301', '^': u'\u0302',
                         '~': u'\u0303', '-': u'\u0304', '⌄': u'\u0306',
                         '.': u'\u0307', '"': u'\u0308'}
        self.hintAttempts = 3
        self.passAttempts = 5
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
        self.setsTitle = QLabel('Sets')
        self.setsLayout.addWidget(self.setsTitle)
        self.setsList = QListWidget()
        self.setsList.setSelectionMode(QAbstractItemView.MultiSelection)
        self.setsLayout.addWidget(self.setsList)
        self.setsIO = QHBoxLayout()
        self.openSet = QPushButton('Open Set (Ctrl+O)', shortcut='Ctrl+O')
        self.openDirectory = QPushButton('Open Directory (Ctrl+Shift+O)', shortcut='Ctrl+Shift+O')
        self.buildSet = QPushButton('Build Set')
        self.setsIO.addWidget(self.openSet)
        self.setsIO.addWidget(self.openDirectory)
        self.setsIO.addWidget(self.buildSet)
        self.setsLayout.addLayout(self.setsIO)
        self.selectionIO = QHBoxLayout()
        self.selectAll = QPushButton('Select All (Ctrl+A)', shortcut='Ctrl+A')
        self.deselectAll = QPushButton('Deselect All (Ctrl+Shift+A)', shortcut='Ctrl+Shift+A')
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
        self.gameCard.setAlignment(QtCore.Qt.AlignCenter)
        self.gameLayout.addWidget(self.gameCard)
        self.entryLayout = QHBoxLayout()
        self.answerField = QLineEdit()
        self.entryLayout.addWidget(self.answerField)
        self.answerButton = QPushButton('Go')
        self.entryLayout.addWidget(self.answerButton)
        self.gameLayout.addLayout(self.entryLayout)
        self.modifierLayout = QHBoxLayout()
        self.letterBox = QComboBox()
        self.letterBox.addItems([x for x in 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'])
        self.modifierLayout.addWidget(self.letterBox)
        self.modifierBox = QComboBox()
        self.modifierBox.addItems(list(self.charMods.keys()))
        self.modifierLayout.addWidget(self.modifierBox)
        self.insertButton = QPushButton('Insert (Ctrl+I)', shortcut='Ctrl+I')
        self.modifierLayout.addWidget(self.insertButton)
        self.gameLayout.addLayout(self.modifierLayout)
        self.generalLayout.addLayout(self.gameLayout)
    
    def _displayList(self):
        self.displayList = QListWidget()
        self.generalLayout.addWidget(self.displayList)
    
    def _createMenu(self):
        menu = self.menuBar().addMenu('&Menu')
        menu.addAction('&Settings', self._settingsPopUp, shortcut='Ctrl+D')
        menu.addAction('&Information', self._helpPopUp, shortcut='Ctrl+H')
        menu.addAction('&Exit', self.close, shortcut='Alt+F4')
    
    def _getVersion(self):
        filePath = os.path.abspath(__file__)
        fileDirectory = '/'.join(filePath.split('/')[:-1])
        with open(f'{fileDirectory}/helptext.txt','r') as f:
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
    
    @QtCore.pyqtSlot()
    def _openSet(self, fileName: str | None = None):
        refresh = False
        if fileName is None:
            fileName = QFileDialog.getOpenFileName(self,'',self.currentDirectory)[0]
            if len(fileName):
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
        dirPath = QFileDialog.getExistingDirectory(self,'',self.currentDirectory)
        if len(dirPath):
            self.currentDirectory = dirPath
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
        '''Method to start the flash card round'''
        if len(self.setsList.selectedItems()):
            self.displayList.clear()
            gamePairs = {}
            for selected in self.setsList.selectedItems():
                gamePairs.update(self.sets[selected.text()]['pairs'])
            #Shuffle cards
            gameKeys = list(gamePairs.keys())
            random.shuffle(gameKeys)
            gamePairs = {key: gamePairs[key] for key in gameKeys}
            #Present prompts according to game mode
            gameMode = self.gameMode.currentText()
            if gameMode=='B side':
                gamePairs = {val: key for key, val in gamePairs.items()}
            elif gameMode=='Random':
                aList = list(gamePairs.keys())
                bList = list(gamePairs.values())
                gamePairs = {}
                for a, b in zip(aList, bList):
                    num = random.random()
                    if num < 0.5:
                        gamePairs.update({a: b})
                    else:
                        gamePairs.update({b: a})
            self.aList = list(gamePairs.keys())
            self.bList = list(gamePairs.values())
            self.attempts = 0
            self.gameCard.setText(self.aList[0])
        else:
            self._setSelectWarnPopUp()
    
    def _submit(self):
        '''Method for checking answer and proceeding'''
        if len(self.aList):
            answer = self.answerField.text()
            self.attempts+=1
            if answer.lower()==self.bList[0].lower(): #Success
                attemptStr = f'({self.attempts} attempt{"s" if self.attempts>1 else ""})'
                self.displayList.addItem(u'\u2713' + f'{self.aList[0]} : {self.bList[0]} {attemptStr}')
                self._nextItem()
            else:
                self.setsTitle.setText(f'Sets{" "*90}Attempts: {self.attempts}')
                if self.attempts==self.passAttempts:
                    self.displayList.addItem(u'\u2717' + f'{self.aList[0]} : {self.bList[0]} ')
                    self._nextItem()
                elif self.attempts==self.hintAttempts:
                    self.gameCard.setText(f'{self.aList[0]}\n{self.bList[0][0]}')
                    
    def _nextItem(self):
        '''Progress through the flash card round'''
        self.answerField.setText('')
        self.aList.pop(0)
        self.bList.pop(0)
        self.attempts = 0
        self.setsTitle.setText('Sets')
        if len(self.aList):
            self.gameCard.setText(self.aList[0])
        else:
            self.gameCard.setText('')
    
    def _insert(self):
        char = self.letterBox.currentText() + self.charMods[self.modifierBox.currentText()]
        self.answerField.setText(self.answerField.text() + char)
    
    def _settingsPopUp(self):
        self.sWindow = settingsWindow(self)
        self.sWindow.setWindowTitle(f'Flash Cards {self._getVersion()} - Settings')
        self.sWindow.show()
    
    def _helpPopUp(self):
        self.hWindow = helpWindow()
        self.hWindow.setWindowTitle(f'Flash Cards {self._getVersion()} - Information')
        self.hWindow.show()
    
    def _setSelectWarnPopUp(self):
        self.wWindow = setSelectWarnWindow()
        self.wWindow.setWindowTitle(f'Flash Cards {self._getVersion()} - Warning')
        self.wWindow.show()

class settingsWindow(QWidget):
    '''Window for adjusting settings'''
    def __init__(self,parent):
        super().__init__()
        self.parent = parent
        layout = QVBoxLayout()
        gridLayout = QGridLayout()
        self.label1 = QLabel('Number of attempts before a hint is given:')
        self.label2 = QLabel('Number of attempts before moving on:')
        self.hintSelector = QComboBox()
        selectorList = ['Infinite']+[f'{x}' for x in range(1,100)]
        self.hintSelector.addItems(selectorList)
        self.hintSelector.setCurrentText(f'{self.parent.hintAttempts if self.parent.hintAttempts>0 else "Infinite"}')
        self.passSelector = QComboBox()
        self.passSelector.addItems(selectorList)
        self.passSelector.setCurrentText(f'{self.parent.passAttempts if self.parent.passAttempts>0 else "Infinite"}')
        self.cancelButton = QPushButton('Cancel')
        self.confirmButton = QPushButton('Confirm')
        gridLayout.addWidget(self.label1,1,1)
        gridLayout.addWidget(self.hintSelector,1,2)
        gridLayout.addWidget(self.label2,2,1)
        gridLayout.addWidget(self.passSelector,2,2)
        layout.addLayout(gridLayout)
        buttonLayout = QHBoxLayout()
        buttonLayout.addWidget(self.cancelButton)
        buttonLayout.addWidget(self.confirmButton)
        layout.addLayout(buttonLayout)
        self.setLayout(layout)
        self.cancelButton.clicked.connect(self.close)
        self.confirmButton.clicked.connect(self._confirm)
    
    def _confirm(self):
        hintSelection = self.hintSelector.currentText()
        self.parent.hintAttempts = -1 if hintSelection=='Infinite' else int(hintSelection)
        passSelection = self.passSelector.currentText()
        self.parent.passAttempts = -1 if passSelection=='Infinite' else int(passSelection)
        self.close()

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
        filePath = os.path.abspath(__file__)
        fileDirectory = '/'.join(filePath.split('/')[:-1])
        with open(f'{fileDirectory}/helptext.txt','r') as f:
            lines = f.readlines()
        return lines

class setSelectWarnWindow(QWidget):
    '''Warn user to select one or more sets'''
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        warning = QLabel(('Select one or more sets to start!'))
        layout.addWidget(warning)
        self.confirmButton = QPushButton('OK')
        layout.addWidget(self.confirmButton)
        self.setLayout(layout)
        self.confirmButton.clicked.connect(self.close)

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
        self.addCard = QPushButton('Add Card (Ctrl+N)', shortcut='Ctrl+N')
        layout.addWidget(self.addCard)
        self.ioLayout = QHBoxLayout()
        self.cancelButton = QPushButton('Cancel')
        self.confirmButton = QPushButton('Confirm')
        self.ioLayout.addWidget(self.cancelButton)
        self.ioLayout.addWidget(self.confirmButton)
        layout.addLayout(self.ioLayout)
        modifierLayout = QHBoxLayout()
        self.letterBox = QComboBox()
        self.letterBox.addItems([x for x in 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'])
        modifierLayout.addWidget(self.letterBox)
        self.modifierBox = QComboBox()
        self.modifierBox.addItems(list(self.parent.charMods.keys()))
        modifierLayout.addWidget(self.modifierBox)
        self.copyButton = QPushButton('Copy to clipboard (Ctrl+C)', shortcut='Ctrl+C')
        modifierLayout.addWidget(self.copyButton)
        layout.addLayout(modifierLayout)
        self.setLayout(layout)
        self.fileField.currentIndexChanged.connect(self._displayPairs)
        self.fileDialog.clicked.connect(self._fileDialog)
        self.addCard.clicked.connect(self._addCard)
        self.copyButton.clicked.connect(self._copyChar)
        self.cancelButton.clicked.connect(self.close)
        self.confirmButton.clicked.connect(self._confirm)
    
    def _fileDialog(self):
        fileName = QFileDialog.getSaveFileName(self,'',self.parent.currentDirectory)[0]
        if len(fileName):
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
    
    def _copyChar(self):
        char = self.letterBox.currentText() + self.parent.charMods[self.modifierBox.currentText()]
        self.parent.clipboard.setText(char)
    
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
        self._view.insertButton.clicked.connect(self._view._insert)

def main():
    '''Main loop'''
    elApp = QApplication([])
    clipboard = elApp.clipboard()
    elWindow = mainWindow(clipboard)
    elWindow.show()
    controller(model=None,view=elWindow)
    sys.exit(elApp.exec())

if (__name__=='__main__'):
    main()