from PySide2.QtWidgets import *
from PySide2.QtGui import *
from PySide2.QtCore import *

from .Widgets import *



# =todo 140 (module-ui, mark) +0: show mark values
class MarkControl(QFrame):
	sigChangedField = Signal(str, object)


	data = {}
	lLayout = None
	lBgColor = None


	def __init__(self, _fields, _data):
		QFrame.__init__(self)


		self.fields = _fields
		self.data = _data

#  todo 323 (ui, clean) +0: make all styles name-based
#		.setObjectName('...-warning' if __ else '...')
#		.setStyleSheet(.styleSheet())

		self.setStyleSheet("background-color: rgba(0,0,0,0);")

		wBg = QFrame(self)
		wBg.setStyleSheet(f"border: 2px solid rgba(128,128,128,.5); border-radius: 5px; background-color: rgba(16,16,16,.9);")

		self.lBgColor = QFrame(wBg)


		self.lLayout = QFormLayout(self)
		self.lLayout.setSpacing(12)
		self.lLayout.setContentsMargins(16,16,24,24)

		self.fillFrame()


		wBg.resize(self.sizeHint()-QSize(4,4))
		self.lBgColor.resize(self.sizeHint()-QSize(4,4))



	def setBackground(self, _color):
		cColor = tuple(QColor(_color).getRgb()[:-1]) +(.1,)

		self.lBgColor.setStyleSheet(f"background-color: rgba{cColor};")



	def fillFrame(self):
		def applyConnect(_signal, _name): #not working inline, switch to QSignalMapper mb
			_signal.connect(lambda _val: self.sigChangedField.emit(_name, _val))


		for cName, cField in self.fields.items():
			cVal = self.data[cName]
			fieldWidget = QLabel(f"{cVal}")

			dType = cField['type']
			if dType == str:
				if (len(cVal) in [4,7]) and (cVal[0] == '#'): #color
					fieldWidget = ColorPicker.ColorPicker(cVal)
					applyConnect(fieldWidget.sigChangedColor,cName)

			if dType == float or dType == int:
					fieldWidget = QDoubleSpinBox()
					fieldWidget.setMinimumWidth(60)
					fieldWidget.setDecimals(0 if dType==int else 2)
					fieldWidget.setRange(cField['range'][0], cField['range'][1])
					fieldWidget.setValue(cVal)
					applyConnect(fieldWidget.valueChanged,cName)


			fieldName = QLabel(f"{cField['name']}")
			self.lLayout.addRow(fieldName, fieldWidget)




# =todo 180 (module-ui, mark, wat) +0: allow to assign only when geo selected
class MarkWidget(QFrame):
	lButton = None
	lTrigger = None

	sigChanged = Signal(object, str, object)
	sigTrigger = Signal(object, bool)


	colorFieldName = ''

	mark = None
	activeMB = None



	def __init__(self, _contLay, _mark, fields={}, colorFieldName=''):
		QFrame.__init__(self)

		
		self.mark = _mark
		self.colorFieldName = colorFieldName


		cLayout = QHBoxLayout(self)
		cLayout.setSpacing(0)
		cLayout.setContentsMargins(0,0,0,0)


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


		self.wFrameTool = MarkControl(fields, self.mark.getData())
		self.wFrameTool.hide()

		_contLay.addWidget(self.wFrameTool)


		cColor = self.mark.getData(self.colorFieldName)
		self.setColor(cColor)

		self.lButton.clicked.connect(self.toolPop)
		self.lTrigger.stateChanged.connect(self.markTrigger)
		self.wFrameTool.sigChangedField.connect(self.markChanged)



	#partially have priority
	def setTrigger(self, _on=None, tri=None):
		cState = Qt.Checked if _on else Qt.Unchecked

		if tri:
			cState = Qt.PartiallyChecked


		self.lTrigger.blockSignals(True)
		self.lTrigger.setCheckState(cState)
		self.lTrigger.blockSignals(False)



	def markTrigger(self, _state):
		self.sigTrigger.emit(self.mark, _state==Qt.Checked)

		self.lTrigger.setTristate(False)



	def markChanged(self, _name, _val):
		if self.colorFieldName and _name==self.colorFieldName:
			self.setColor(_val)


		self.mark.setData({_name:_val})

		self.sigChanged.emit(self.mark, _name, _val)



	def setColor(self, _color):
#??		self.lButton.setPalette(QColor.fromRgb(color[0],color[1],color[2]))
		self.lButton.setStyleSheet(f"background-color: {_color};border-radius:4px;")

		self.wFrameTool.setBackground(_color)



	def toolPop(self):
		MarkWidget.toolUnpop()


		MarkWidget.activeMB = self

		self.lButton.setChecked(True)
		self.wFrameHighlight.show()
		self.wFrameTool.show()



	#Close active onr
	def toolUnpop():
		if MarkWidget.activeMB:
			MarkWidget.activeMB.lButton.setChecked(False)
			MarkWidget.activeMB.wFrameHighlight.hide()
			MarkWidget.activeMB.wFrameTool.hide()

		MarkWidget.activeMB = None
