from PySide2.QtCore import *
from PySide2.QtWidgets import *
from PySide2.QtGui import *



#thanks to https://stackoverflow.com/users/3336423/jpo38 at https://stackoverflow.com/questions/18257281/qt-color-picker-widget
# =todo 143 (ui, widgets) +0: simplify color picker
class ColorPicker(QPushButton):
	
	sigChangedColor = Signal(QColor)

	color = None



	def __init__(self, _color):
		QPushButton.__init__(self)


		self.setColor(_color)

		self.clicked.connect(self.changeColor)



	def changeColor(self):
		newColor = QColorDialog.getColor(self.color, self.parentWidget())

		if newColor == QColor():
			return

		if newColor.name() == self.color.name():
			return


		self.setColor(newColor)

		self.sigChangedColor.emit(newColor)



	def setColor(self, _color):
		self.color = _color
		self.setStyleSheet( "background-color: " + self.color.name() )



	def getColor(self):
		return self.color
