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





class MarkButton(QFrame):
	wButton = None
	wTrigger = None

	sigChangedMark = Signal(object, str, object)


	fieldWColor = ''

	mark = None
	activeMB = None



	def __init__(self, _contLay, _mark, fieldWColor=''):
		QFrame.__init__(self)

		
		self.mark = _mark
		self.fieldWColor = fieldWColor

		mainColor = self.mark.getData(self.fieldWColor) or QColor()


		cLayout = QHBoxLayout()
		self.setLayout(cLayout)


		self.wButton = QPushButton()
		self.wButton.setCheckable(True)
		cLayout.addWidget(self.wButton)


		self.wFrameHighlight = QFrame(self.wButton)
		self.wFrameHighlight.resize(self.wButton.sizeHint())
		self.wFrameHighlight.setStyleSheet(f"border: 2px solid #eee; border-radius:2px")
		self.wFrameHighlight.hide()


		self.wFrameTool = MarkTool(_mark)
		self.wFrameTool.hide()

		_contLay.addWidget(self.wFrameTool)


		self.setColor(mainColor)

		self.wButton.clicked.connect(self.toolPop)
		self.wFrameTool.sigChangedField.connect(self.changedMark)



	def changedMark(self, _name, _val):
		if self.fieldWColor and _name==self.fieldWColor:
			self.setColor(_val)


		self.sigChangedMark.emit(self.mark, _name, _val)



	def setColor(self, _color):
		cColor = _color.getRgb()[:-1]
#??		self.wButton.setPalette(QColor.fromRgb(color[0],color[1],color[2]))
		self.wButton.setStyleSheet(f"background-color: rgb{cColor}")

		self.wFrameTool.setBackground(_color)



	def toolPop(self):
		if MarkButton.activeMB:
			MarkButton.activeMB.wButton.setChecked(False)
			MarkButton.activeMB.wFrameHighlight.hide()
			MarkButton.activeMB.wFrameTool.hide()

		MarkButton.activeMB = self


		self.wButton.setChecked(True)
		self.wFrameHighlight.show()
		self.wFrameTool.show()
