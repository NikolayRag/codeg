from PySide2.QtCore import *
from PySide2.QtWidgets import *
from PySide2.QtGui import *

from ..BindFilter import *



class ColorGrid(QFrame):
	sigPicked = Signal(object)



	def	__init__(self, _gridX, _gridY, _gridSize):
		QFrame.__init__(self)

		self.setWindowFlags(Qt.Popup)


		cLayout = QGridLayout(self)
		cLayout.setSpacing(0)
		cLayout.setContentsMargins(0,0,0,0)

		self.tmpFilter = BindFilter({
			QEvent.Type.KeyPress: lambda _e: self.close() })
		self.installEventFilter(self.tmpFilter)



		def makeSample(_color): #inline to scope signal lambda
			cSample = QPushButton()
			cSample.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)

			cColor = QColor(_color)
			cSample.setStyleSheet(f"border:0; background:{cColor.name()}")

			cSample.clicked.connect(lambda: self.sigPicked.emit(cColor))

			return cSample


		for iX in range(1,_gridX+1):
			for iY in range(1,_gridY+1):
				cSample = makeSample( QColor.fromHslF(1.*(iX-1)/_gridX,1,1.*iY/(_gridY+1)) )
				cLayout.addWidget(cSample, iY, iX)


		_gridX += 1

		for iY in range(1,_gridY+1):
			cSample = makeSample( QColor.fromHslF(0,0,1.*iY/(_gridY+1)) )
			cLayout.addWidget(cSample, iY, _gridX+1)


		self.resize(_gridX*_gridSize, _gridY*_gridSize)






class ColorPicker(QPushButton):

	sigChangedColor = Signal(str)

	color = None



	def __init__(self, _color):
		QPushButton.__init__(self)


		self.setColor(QColor(_color))

		self.clicked.connect(self.palettePop)


		self.lPalette = ColorGrid(12, 6, 15)
		self.lPalette.sigPicked.connect(self.picked)



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
		self.lPalette.setFocus()
		self.lPalette.show()



	def setColor(self, _color):
		self.color = _color
		self.setStyleSheet( "background-color: " + self.color.name() )



	def getColor(self):
		return self.color
