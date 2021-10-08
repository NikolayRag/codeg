from PySide2.QtWidgets import *
from PySide2.QtGui import *
from PySide2.QtCore import *

from .Widgets import *



# -todo 140 (module-ui, mark) +0: redesign
class MarkTool(QFrame):
	sigChangedField = Signal(str, QColor)


	mark = None
	lLayout = None
	lBgColor = None


	def __init__(self, _mark):
		QFrame.__init__(self)


		self.mark = _mark

		self.setStyleSheet("background-color: rgba(0,0,0,0);")

		wBg = QFrame(self)
		wBg.setStyleSheet(f"border: 2px solid rgba(128,128,128,.5); border-radius: 5px; background-color: rgba(16,16,16,.9);")

		self.lBgColor = QFrame(wBg)


		self.lLayout = QFormLayout()
		self.lLayout.setSpacing(12)
		self.lLayout.setContentsMargins(16,16,24,24)
		self.setLayout(self.lLayout)

		self.fillFrame()


		wBg.resize(self.sizeHint()-QSize(4,4))
		self.lBgColor.resize(self.sizeHint()-QSize(4,4))



	def setBackground(self, _color):
		cColor = tuple(_color.getRgb()[:-1]) +(.1,)
		self.lBgColor.setStyleSheet(f"background-color: rgba{cColor};")



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


			self.lLayout.addRow(fieldName, fieldVal)



	def changedColor(self, _name, _val):
		self.mark.setData({_name:_val})
	
		self.sigChangedField.emit(_name, _val)





class MarkButton(QFrame):
	lButton = None
	lTrigger = None

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
		cLayout.setSpacing(0)
		cLayout.setContentsMargins(0,0,0,0)
		self.setLayout(cLayout)


		self.lTrigger = QCheckBox()
		self.lTrigger.setMaximumWidth(16)
		self.lTrigger.setStyleSheet(f"border:1px solid #777")
		cLayout.addWidget(self.lTrigger)

		sp1 = QSpacerItem(0,0, QSizePolicy.Expanding, QSizePolicy.Fixed)
		cLayout.addItem(sp1)


		self.lButton = QPushButton()
		self.lButton.setCheckable(True)
		self.lButton.setFixedWidth(24)
		self.lButton.setFixedHeight(24)
		cLayout.addWidget(self.lButton)


		self.wFrameHighlight = QFrame(self.lButton)
		self.wFrameHighlight.resize(24,24)
		self.wFrameHighlight.setStyleSheet(f"border: 2px solid #eee; border-radius:2px;")
		self.wFrameHighlight.hide()


		self.wFrameTool = MarkTool(_mark)
		self.wFrameTool.hide()

		_contLay.addWidget(self.wFrameTool)


		self.setColor(mainColor)

		self.lButton.clicked.connect(self.toolPop)
		self.wFrameTool.sigChangedField.connect(self.changedMark)



	def changedMark(self, _name, _val):
		if self.fieldWColor and _name==self.fieldWColor:
			self.setColor(_val)


		self.sigChangedMark.emit(self.mark, _name, _val)



	def setColor(self, _color):
		cColor = _color.getRgb()[:-1]
#??		self.lButton.setPalette(QColor.fromRgb(color[0],color[1],color[2]))
		self.lButton.setStyleSheet(f"background-color: rgb{cColor};border-radius:4px;")

		self.wFrameTool.setBackground(_color)



	def toolPop(self):
		if MarkButton.activeMB:
			MarkButton.activeMB.lButton.setChecked(False)
			MarkButton.activeMB.wFrameHighlight.hide()
			MarkButton.activeMB.wFrameTool.hide()

		MarkButton.activeMB = self


		self.lButton.setChecked(True)
		self.wFrameHighlight.show()
		self.wFrameTool.show()
