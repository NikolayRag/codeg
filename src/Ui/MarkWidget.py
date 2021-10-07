from PySide2.QtWidgets import *
from PySide2.QtGui import *
from PySide2.QtCore import *

from .Widgets import *



# -todo 140 (module-ui, mark) +0: redesign
class MarkTool(QFrame):
	sigChangedField = Signal(str, QColor)


	mark = None
	wLayout = None
	wBgColor = None


	def __init__(self, _mark):
		QFrame.__init__(self)


		self.mark = _mark

		self.setStyleSheet("background-color: rgba(0,0,0,0);")

		wBg = QFrame(self)
		wBg.setStyleSheet(f"border: 2px solid rgba(128,128,128,.5); border-radius: 5px; background-color: rgba(16,16,16,.9);")

		self.wBgColor = QFrame(wBg)


		self.wLayout = QFormLayout()
		self.wLayout.setSpacing(12)
		self.wLayout.setContentsMargins(16,16,24,24)
		self.setLayout(self.wLayout)

		self.fillFrame()


		wBg.resize(self.sizeHint()-QSize(4,4))
		self.wBgColor.resize(self.sizeHint()-QSize(4,4))



	def setBackground(self, _color):
		cColor = tuple(_color.getRgb()[:-1]) +(.1,)
		self.wBgColor.setStyleSheet(f"background-color: rgba{cColor};")



	def fillFrame(self):
		def applyConnect(_field, _data): #not working inline, switch to QSignalMapper mb
			_field.sigChangedColor.connect(lambda _c: self.changedColor(_data, _c))


		mDataA = self.mark.getData()
		for cData in mDataA:
			fieldName = QLabel(f"{cData}")
			fieldVal = QLabel(f"{mDataA[cData]}")

			dType = type(mDataA[cData])
			if (dType==QColor):
				fieldVal = ColorPicker(mDataA[cData])
				applyConnect(fieldVal,cData)


			self.wLayout.addRow(fieldName, fieldVal)



	def changedColor(self, _name, _val):
		self.mark.setData({_name:_val})
	
		self.sigChangedField.emit(_name, _val)





class MarkButton(QToolButton):
	nameMarkColor = ''


	sigChangedMark = Signal(object, str, object)


	mark = None
	currentMB = None



	def __init__(self, _contLay, _mark, fieldWColor=''):
		QToolButton.__init__(self)

		
		self.mark = _mark
		self.nameMarkColor = fieldWColor

		mainColor = self.mark.getData(self.nameMarkColor) or QColor()


		self.setCheckable(True)
#??		self.setPalette(QColor.fromRgb(color[0],color[1],color[2]))
		self.setColor(mainColor)

		self.wFrameHighlight = QFrame(self)
		self.wFrameHighlight.resize(self.sizeHint())
		self.wFrameHighlight.setStyleSheet(f"border: 2px solid #eee; border-radius:2px")
		self.wFrameHighlight.hide()


		self.wFrameTool = MarkTool(_mark)
		self.wFrameTool.setBackground(mainColor)

		self.wFrameTool.hide()


		_contLay.addWidget(self.wFrameTool)

		self.clicked.connect(self.toolPop)

		self.wFrameTool.sigChangedField.connect(self.changedMark)



	def changedMark(self, _name, _val):
		if self.nameMarkColor and _name==self.nameMarkColor:
			self.setColor(_val)
			self.wFrameTool.setBackground(_val)


		self.sigChangedMark.emit(self.mark, _name, _val)



	def setColor(self, _color):
		cColor = _color.getRgb()[:-1]
		self.setStyleSheet(f"background-color: rgb{cColor}")



	def toolPop(self):
		if MarkButton.currentMB:
			MarkButton.currentMB.setChecked(False)
			MarkButton.currentMB.wFrameHighlight.hide()
			MarkButton.currentMB.wFrameTool.hide()

		MarkButton.currentMB = self


		self.setChecked(True)
		self.wFrameHighlight.show()
		self.wFrameTool.show()
