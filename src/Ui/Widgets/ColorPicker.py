from PySide2.QtCore import *
from PySide2.QtWidgets import *
from PySide2.QtGui import *



# =todo 143 (ui, widgets) +0: simplify color picker
class ColorPicker(QPushButton):
	
	sigChangedColor = Signal(str)

	color = None



	def __init__(self, _color):
		QPushButton.__init__(self)


		self.setColor(QColor(_color))

		self.clicked.connect(self.palettePop)


		self.lPalette = QFrame()
		self.lPalette.resize(214,100)
		self.lPalette.setWindowFlags(Qt.Popup)

		cLayout = QGridLayout(self.lPalette)
		cLayout.setSpacing(0)
		cLayout.setContentsMargins(0,0,0,0)



		def makeSample(_color):
			cSample = QPushButton()
			cSample.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)

			cColor = QColor(_color)
			cSample.setStyleSheet(f"border:0; background:{cColor.name()}")

			cSample.clicked.connect(lambda: self.picked(cColor))

			return cSample


		for iX in range(1,14):
			for iY in range(1,7):
				cSample = makeSample( QColor.fromHslF(iX/14.,1,iY/7.) )
				cLayout.addWidget(cSample, iY, iX)


		for iY in range(1,7):
			cSample = makeSample( QColor.fromHslF(0,0,iY/7.) )
			cLayout.addWidget(cSample, iY, 15)



	def picked(self, _color):
		self.lPalette.hide()


		if _color.name() == self.color.name():
			return

		self.setColor(_color)

		self.sigChangedColor.emit(_color.name())



	def palettePop(self):
		pos = self.mapToGlobal(QPoint(self.width()+2,0))
		self.lPalette.move(pos)
		self.lPalette.show()



	def setColor(self, _color):
		self.color = _color
		self.setStyleSheet( "background-color: " + self.color.name() )



	def getColor(self):
		return self.color
