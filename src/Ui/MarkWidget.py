from PySide2.QtWidgets import *
from PySide2.QtGui import *
from PySide2.QtCore import *

from .Widgets import *
from .BindFilter import *



# =todo 140 (module-ui, mark) +0: show mark values
class MarkControl(QFrame):
	sigChangedField = Signal(str, object)


	data = {}


	def __init__(self, _fields, _data):
		QFrame.__init__(self)


		self.fields = _fields
		self.data = _data

#  todo 323 (ui, clean) +0: make all styles name-based

		self.fillFrame(self)
	def fillFrame(self, _parent):
		def applyConnect(_signal, _name): #not working inline, switch to QSignalMapper mb
			_signal.connect(lambda _val: self.sigChangedField.emit(_name, _val))


		lLayout = QFormLayout(_parent)
		lLayout.setSpacing(4)
		lLayout.setContentsMargins(0,0,0,0)


		for cName, cField in self.fields.items():
			if not cField['name']:
				continue


			cVal = self.data[cName]
			fieldWidget = QLabel(f"{cVal}")

			dType = cField['type']
			if dType == str:
				if (len(cVal) in [4,7]) and (cVal[0] == '#'): #color
					fieldWidget = ColorPicker.ColorPicker(cVal)
					applyConnect(fieldWidget.sigChangedColor,cName)

			if dType == float or dType == int:
					fieldWidget = QDoubleSpinBox()
					fieldWidget.fltWheel = BindFilter({
						QEvent.Wheel: lambda e: None if fieldWidget.hasFocus() else (e.ignore() or True)
					})
					fieldWidget.installEventFilter(fieldWidget.fltWheel) #suppress focus by wheel
					fieldWidget.setFocusPolicy(Qt.StrongFocus)

					fieldWidget.setDecimals(0 if dType==int else 2)
					fieldWidget.setRange(cField['range'][0], cField['range'][1])
					fieldWidget.setValue(cVal)
					applyConnect(fieldWidget.valueChanged,cName)


			fieldName = QLabel(f"{cField['name']}")
			lLayout.addRow(fieldName, fieldWidget)




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


		self.setContentsMargins(4,4,4,4)

		self.wFrameHighlight = QFrame(self)
		self.wFrameHighlight.hide()


		cLayout = QVBoxLayout(self)
		cLayout.setContentsMargins(0,0,0,0)

		wBreef = QWidget()
		lBreef = QHBoxLayout(wBreef)
		lBreef.setSpacing(4)
		lBreef.setContentsMargins(0,0,0,0)
		cLayout.addWidget(wBreef)



		self.lTrigger = QCheckBox()
		self.lTrigger.setMaximumWidth(16)
		lBreef.addWidget(self.lTrigger)


		self.lButton = QToolButton()
		self.lButton.setFixedHeight(18)
		self.lButton.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Ignored)
		lBreef.addWidget(self.lButton)


		self.wFrameTool = MarkControl(fields, self.mark.getData())
		self.wFrameTool.hide()

		cLayout.addWidget(self.wFrameTool)


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

		cColor = QColor(_color).getRgb()[:-1]
		self.wFrameHighlight.setStyleSheet(f"background-color: rgba{cColor+(.25,)};border-radius:4px;")



	def toolPop(self):
		MarkWidget.toolUnpop()


		MarkWidget.activeMB = self

		self.wFrameHighlight.show()
		self.wFrameTool.show()

		self.wFrameHighlight.resize(self.sizeHint()+QSize(8,0))



	#Close active onr
	def toolUnpop():
		if MarkWidget.activeMB:
			MarkWidget.activeMB.wFrameHighlight.hide()
			MarkWidget.activeMB.wFrameTool.hide()

		MarkWidget.activeMB = None
