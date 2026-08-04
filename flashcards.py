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
        self.addCard = QPushButton('Add Card')
        self.setsLayout.addWidget(self.addCard)
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
    
    def _getVersion(self):
        with open('helptext.txt','r') as f:
            lines = f.readlines()
        for line in lines:
            if 'Version - ' in line:
                return line.split('Version - ')[-1].strip('\n')
    
    def _setTitle(self):
        VERSION_STRING = self._getVersion()
        self.setWindowTitle(f'Activity Logger {VERSION_STRING}')
    
    def _submit(self):
        return

#Run loop
class controller:
    '''Controller module'''
    def __init__(self,model,view):
        self._evaluate = model
        self._view = view
        self._connectSignalsAndSlots()
    
    def _connectSignalsAndSlots(self):
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