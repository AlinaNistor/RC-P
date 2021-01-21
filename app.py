from ripv2.router import Router
from gui.mainwindow import Ui_MainWindow
from PyQt5 import QtWidgets, uic
from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import sys
import time
import threading
import os
from route_entry import RouteEntry


class App(Ui_MainWindow):

	def __init__(self, MainWindow):
		self.setupUi(MainWindow)
		self.setActions()
		self.timers = []
		

	def setActions(self):
		self.startButton.clicked.connect(self.start)
		self.stopButton.clicked.connect(self.stop)

	def start(self):
		Router.UPDATE_TIME = self.spinBoxUpdateTime.value()
		RouteEntry.GARBAGE = self.spinBoxGarbageTime.value()
		RouteEntry.TIMEOUT = self.spinBoxTimeout.value()
		
		self.node = Router()
		self.checkThreadTimer = QtCore.QTimer()
		self.checkThreadTimer.setInterval(100)
		self.checkThreadTimer.timeout.connect(self.print_table)
		
		self.start_timers()
		self.checkThreadTimer.start()
		self.startButton.setDisabled(True)
		self.stopButton.setDisabled(False)

	def stop(self):
		[t.cancel() for t in self.timers]
		self.timers = None
		self.checkThreadTimer.stop()
		self.startButton.setDisabled(False)
		self.stopButton.setDisabled(True)
		
	def print_table(self):
		self.tableText.clear()
		self.tableText.appendPlainText(self.node.print_routing_table())

	def timer(self, function, param=None):
		function()
		delay = 2
		if function == self.node.send_routing_table:
			delay = Router.UPDATE_TIME

		t = threading.Timer(delay, self.timer, [function, param])
		try:
			self.timers.append(t)
			t.start()
		except:
			pass

	def start_timers(self):
		self.timer(self.node.send_routing_table)
		self.timer(self.node.receive_pack)
		self.timer(self.node.update_timers)


def main():
	app = QtWidgets.QApplication(sys.argv)
	MainWindow = QtWidgets.QMainWindow()
	ui = App(MainWindow)
	MainWindow.show()
	sys.exit(app.exec_())


if __name__ == '__main__':
	main()
