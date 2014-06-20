# fills the colors in the given range for the selected patches.
# slider to adjust the range

#import mari

import PySide
import random

QtGui = PySide.QtGui
QtCore = PySide.QtCore


class colorFiller(QtGui.QWidget):
	"""docstring for colorFiller"""
	def __init__(self):
		super(colorFiller, self).__init__()

		self.setGeometry(400, 400, 400, 100)
		#self.setTitle("Color Filler")

		self.mainLayout = QtGui.QVBoxLayout()
		self.setLayout(self.mainLayout)

		self.checkBoxLayout = QtGui.QHBoxLayout()
		self.mainLayout.addLayout(self.checkBoxLayout)

		self.foregroundCheck = QtGui.QCheckBox("Foreground")
		self.foregroundCheck.stateChanged.connect(self.updateCheckState)
		self.foregroundCheck.setCheckState(QtCore.Qt.Checked)
		self.checkBoxLayout.addWidget(self.foregroundCheck)

		self.backgroundCheck = QtGui.QCheckBox("Background")
		self.backgroundCheck.stateChanged.connect(self.updateCheckState)
		self.checkBoxLayout.addWidget(self.backgroundCheck)

		self.randomLayout = QtGui.QHBoxLayout()
		self.mainLayout.addLayout(self.randomLayout)

		# self.randomLabel = QtGui.QLabel("Seed:\t")
		# self.randomLayout.addWidget(self.randomLabel)

		# self.randomSlider = QtGui.QSlider(QtCore.Qt.Horizontal)
		# self.randomSlider.valueChanged[int].connect(self.valueChange)
		# self.randomLayout.addWidget(self.randomSlider)


		self.valueChangeLayout = QtGui.QHBoxLayout()
		self.mainLayout.addLayout(self.valueChangeLayout)

		self.valueChangeLabel = QtGui.QLabel("Contrast:\t")
		self.valueChangeLayout.addWidget(self.valueChangeLabel)

		self.contrastSlider = QtGui.QSlider(QtCore.Qt.Horizontal)
		self.contrastSlider.valueChanged[int].connect(self.valueChange)
		self.valueChangeLayout.addWidget(self.contrastSlider)

		self.buttonLayout = QtGui.QHBoxLayout()
		self.mainLayout.addLayout(self.buttonLayout)

		self.randomButton = QtGui.QPushButton("Random")
		self.randomButton.clicked.connect(self.randomize)
		self.buttonLayout.addWidget(self.randomButton)

		self.okButton = QtGui.QPushButton("Apply")
		self.okButton.clicked.connect(self.apply)
		self.buttonLayout.addWidget(self.okButton)

		self.cancelButton = QtGui.QPushButton("Cancel")
		self.cancelButton.clicked.connect(self.closeUi)
		self.buttonLayout.addWidget(self.cancelButton)

		# create a new layer for mari


	def updateCheckState(self):
		''' update the checkbox ui '''

		# if self.sender.text() == "Random" :
		# 	self.backgroundCheck.setCheckState(QtCore.Qt.Checked)

		if not self.foregroundCheck.isChecked() and not self.backgroundCheck.isChecked() and not self.foregroundCheck.isChecked():
			if self.sender().text() == "Foreground":
				self.backgroundCheck.setCheckState(QtCore.Qt.Checked)
			else:
				self.foregroundCheck.setCheckState(QtCore.Qt.Checked)


	def fillPatches(self):
		''' fill the patches '''
		for patch, color in zip(self.selPatches, self.colors):
			# assign the patch with color
			return


	def randomize(self):
		random.shuffle(self.selPatches)
		random.shuffle(self.colors)
		
		self.fillPatches()


	def valueChange(self):
		''' value chage in the slider to the color '''
		# get the selcted patches
		self.selPatches = [0,1,2,3]
		self.colors = []
		contrastValue = self.contrastSlider.value()
		for each in self.selPatches:
			randomColor = random.randint(0, contrastValue)
			self.colors.append(randomColor)
		print self.colors

		self.fillPatches()


	def apply(self):
		''' close the ui '''
		# basically has to do nothing
		print("apply")


	def closeUi(self):
		''' shut down the ui '''
		# revert back to the old state... how to?
		# simply delete the current layer
		self.close()


main = colorFiller()
main.show()
