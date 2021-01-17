from PyQt5 import QtWidgets, uic
from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import sys
import time
import sched
from random import randrange
import threading
import os
sys.path.append(os.path.dirname('./ripv2/'))
from gui.mainwindow import Ui_MainWindow
from ripv2.router import Node

class App(Ui_MainWindow):

	def __init__(self, MainWindow):
		self.setupUi(MainWindow)
		MainWindow.setFixedSize(1067, 866)
		self.setActions()	
		self.node = Node()
		self.checkThreadTimer = QtCore.QTimer()
		self.checkThreadTimer.setInterval(100)
		self.checkThreadTimer.timeout.connect(self.print_table)
		self.stopButton.setDisabled(True)
		self.timers = []
			
	def setActions(self):
		self.startButton.clicked.connect(self.start)
		self.stopButton.clicked.connect(self.stop)

	def start(self):
		self.startButton.setDisabled(True)
		self.timerSpinBox.setDisabled(True)
		self.maxHopSpinBox.setDisabled(True)
		self.spinBox.setDisabled(True)
		self.sendFirstButton.setDisabled(True)
		self.sendAllButton.setDisabled(True)
		self.stopButton.setDisabled(False)
		self.start_timers()
		self.checkThreadTimer.start()
		

	def stop(self):
		self.startButton.setDisabled(False)
		self.timerSpinBox.setDisabled(False)
		self.maxHopSpinBox.setDisabled(False)
		self.spinBox.setDisabled(False)
		self.sendFirstButton.setDisabled(False)
		self.sendAllButton.setDisabled(False)
		self.stopButton.setDisabled(True)
		self.checkThreadTimer.stop()
		[t.cancel() for t in self.timers]

	def print_table(self):
		self.tableText.clear()
		self.tableText.appendPlainText(self.node.print_routing_table())


	def timer(self, function, param=None):
		function()
		t = threading.Timer(3, self.timer, [function, param])
		self.timers.append(t)
		t.start()


	def start_timers(self):
		self.timer(self.node.send_pack)
		self.timer(self.node.receive_pack)


def main():
	app = QtWidgets.QApplication(sys.argv)
	MainWindow = QtWidgets.QMainWindow()
	ui = App(MainWindow)
	MainWindow.show()
	sys.exit(app.exec_())


if __name__ == '__main__':
	main()
