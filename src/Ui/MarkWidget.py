from PySide2.QtWidgets import *
from PySide2.QtGui import *
from PySide2.QtCore import *

from .Widgets import *



# -todo 140 (module-ui, mark) +0: redesign
class MarkTool(QFrame):
	sigChangedField = Signal(str, object)


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
		cColor = tuple(QColor(_color).getRgb()[:-1]) +(.1,)

		self.lBgColor.setStyleSheet(f"background-color: rgba{cColor};")



	def fillFrame(self):
		def applyConnect(_field, _data): #not working inline, switch to QSignalMapper mb
			_field.sigChangedColor.connect(lambda _c: self.changedColor(_data, _c))


		mDataA = self.mark.getData()
		for cData in mDataA:
			cVal = mDataA[cData]
			fieldWidget = QLabel(f"{cVal}")

			dType = type(cVal)
			if dType == str:
				if (len(cVal) in [4,7]) and (cVal[0] == '#'):
					fieldWidget = ColorPicker.ColorPicker(cVal)
					applyConnect(fieldWidget,cData)


			fieldName = QLabel(f"{cData}")
			self.lLayout.addRow(fieldName, fieldWidget)



	def changedColor(self, _name, _val):
		self.mark.setData({_name:_val})
	
		self.sigChangedField.emit(_name, _val)





class MarkWidget(QFrame):
	lButton = None
	lTrigger = None

	sigChanged = Signal(object, str, object)
	sigTrigger = Signal(object, bool)


	fieldWColor = ''

	mark = None
	activeMB = None

	doEmitTrigger = True


	def __init__(self, _contLay, _mark, fieldWColor=''):
		QFrame.__init__(self)

		
		self.mark = _mark
		self.fieldWColor = fieldWColor

		mainColor = self.mark.getData(self.fieldWColor)


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
		self.lTrigger.stateChanged.connect(self.markTrigger)
		self.wFrameTool.sigChangedField.connect(self.markChanged)



	def setTrigger(self, _on=None, tri=None, emit=True):
		cState = Qt.Checked if _on else Qt.Unchecked

		if tri:
			cState = Qt.PartiallyChecked

		self.doEmitTrigger = emit
		self.lTrigger.setCheckState(cState)
		self.doEmitTrigger = True



	def markTrigger(self, _state):
		if self.doEmitTrigger:
			self.sigTrigger.emit(self.mark, _state==Qt.Checked)

			self.lTrigger.setTristate(False)



	def markChanged(self, _name, _val):
		if self.fieldWColor and _name==self.fieldWColor:
			self.setColor(_val)


		self.sigChanged.emit(self.mark, _name, _val)



	def setColor(self, _color):
#??		self.lButton.setPalette(QColor.fromRgb(color[0],color[1],color[2]))
		self.lButton.setStyleSheet(f"background-color: {_color};border-radius:4px;")

		self.wFrameTool.setBackground(_color)



	def toolPop(self):
		if MarkWidget.activeMB:
			MarkWidget.activeMB.lButton.setChecked(False)
			MarkWidget.activeMB.wFrameHighlight.hide()
			MarkWidget.activeMB.wFrameTool.hide()

		MarkWidget.activeMB = self


		self.lButton.setChecked(True)
		self.wFrameHighlight.show()
		self.wFrameTool.show()
