from PySide2.QtCore import *
from PySide2.QtWidgets import *
from PySide2.QtGui import *



class ColorPicker(QPushButton):

	sigChangedColor = Signal(str)

	color = None



	def __init__(self, _color):
		QPushButton.__init__(self)


		self.setColor(QColor(_color))

		self.clicked.connect(self.palettePop)


		self.lPalette = QFrame()
		self.lPalette.setWindowFlags(Qt.Popup)

		cLayout = QGridLayout(self.lPalette)
		cLayout.setSpacing(0)
		cLayout.setContentsMargins(0,0,0,0)


# COLOR GRID

		def makeSample(_color): #inline to scope signal lambda
			cSample = QPushButton()
			cSample.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)

			cColor = QColor(_color)
			cSample.setStyleSheet(f"border:0; background:{cColor.name()}")

			cSample.clicked.connect(lambda: self.picked(cColor))

			return cSample


		gridX = 12
		gridY = 6
		gridSize = 15

		for iX in range(1,gridX+1):
			for iY in range(1,gridY+1):
				cSample = makeSample( QColor.fromHslF(1.*(iX-1)/gridX,1,1.*iY/(gridY+1)) )
				cLayout.addWidget(cSample, iY, iX)


		gridX += 1

		for iY in range(1,gridY+1):
			cSample = makeSample( QColor.fromHslF(0,0,1.*iY/(gridY+1)) )
			cLayout.addWidget(cSample, iY, 15)


		self.lPalette.resize(gridX*gridSize, gridY*gridSize)



	def picked(self, _color):
		self.lPalette.hide()


		if _color.name() == self.color.name():
			return

		self.setColor(_color)

		self.sigChangedColor.emit(_color.name())



	def palettePop(self):
# -todo 209 (fix, widgets) +0: bound color picker by screen borders
		pos = self.mapToGlobal(QPoint(self.width()+2,0))
		self.lPalette.move(pos)
		self.lPalette.show()



	def setColor(self, _color):
		self.color = _color
		self.setStyleSheet( "background-color: " + self.color.name() )



	def getColor(self):
		return self.color
