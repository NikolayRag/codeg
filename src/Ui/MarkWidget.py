from PySide2.QtWidgets import *
from PySide2.QtGui import *
from PySide2.QtCore import *

from .Widgets import *
from .BindFilter import *


# =todo 395 (marks, ui) +0: make MarksTabWidget

# =todo 180 (module-ui, mark) +0: allow to assign only when geo selected
class MarkWidgetPanel(QWidget):
	sigFieldChanged = Signal(str, object)



	def formPanel(self, _fields, _data):
		def applyConnect(_signal, _name): #not working inline, switch to QSignalMapper mb
			_signal.connect(lambda _val: self.sigFieldChanged.emit(_name, _val))


		lParent = QFormLayout(self)
		lParent.setHorizontalSpacing(12)
		lParent.setContentsMargins(0,0,0,0)


		for cName, cField in _fields.items():
			if not cField['name']:
				continue


			cVal = _data[cName]
			fieldWidget = QLabel(f"{cVal}")

			dType = cField['type']
			if dType == str:
				if (len(cVal) in [4,7]) and (cVal[0] == '#'): #color
					fieldWidget = QWidget()

					layField = QHBoxLayout()
					layField.setSpacing(0)
					layField.setContentsMargins(0,0,0,0)
					fieldWidget.setLayout(layField)

					wFiller = QSpacerItem(0,0, QSizePolicy.Expanding, QSizePolicy.Fixed)
					layField.addItem(wFiller)

					fieldWidgetCP = ColorPicker.ColorPicker(cVal)
					fieldWidgetCP.setMaximumWidth(16)
					fieldWidgetCP.setMaximumHeight(18)
					applyConnect(fieldWidgetCP.sigChangedColor, cName)
					layField.addWidget(fieldWidgetCP)

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
					applyConnect(fieldWidget.valueChanged, cName)


			fieldName = QLabel(f"{cField['name']}")
			lParent.addRow(fieldName, fieldWidget)



	def __init__(self, _fields, _data):
		QWidget.__init__(self)

		self.setContentsMargins(0,12,0,4)

		self.formPanel(_fields, _data)






class MarkWidget(QWidget):
	lButton = None
	wAssign = None

	sigChanged = Signal(object, str, object)
	sigTrigger = Signal(object, bool)
	sigSelect = Signal(object)
	sigKill = Signal(object)


	colorFieldName = ''

	mark = None
	activeMB = None
	def outAssign(self, _state):
		self.sigTrigger.emit(self.mark, _state==Qt.Checked)

		self.wAssign.setTristate(False)



	def panelTouched(self, _name, _val):
		if self.colorFieldName and _name==self.colorFieldName:
			self.setColor(_val)

		self.mark.setData({_name:_val})

		self.sigChanged.emit(self.mark, _name, _val)



	def __init__(self, _mark, fields={}, colorFieldName=''):
		QWidget.__init__(self)

		
		self.mark = _mark
		self.colorFieldName = colorFieldName
		cColor = _mark.getData(colorFieldName)


#  todo 378 (module-ui, mark) +0: use MarkWidget.ui
		self.setContentsMargins(4,4,4,4)

		self.wFrameHighlight = QFrame(self)
		self.wFrameHighlight.hide()
		self.tmpHlScale = BindFilter({
			QEvent.Type.Resize: lambda _e: self.wFrameHighlight.resize(_e.size()) })
		self.installEventFilter(self.tmpHlScale)


		cLayout = QVBoxLayout(self)
		cLayout.setContentsMargins(0,0,0,0)


		self.wTbar = QWidget()
		self.wTbar.setFixedHeight(18)
		self.wTbar.hide()

		lTbar = QHBoxLayout(self.wTbar)
		lTbar.setSpacing(4)
		lTbar.setContentsMargins(0,0,0,0)
		cLayout.addWidget(self.wTbar)

		wSelby = QToolButton()
		wSelby.setMaximumWidth(16)
		wSelby.setText('<')
		lTbar.addWidget(wSelby)

		wFiller = QSpacerItem(0,0, QSizePolicy.Expanding, QSizePolicy.Fixed)
		lTbar.addItem(wFiller)

		wKill = QToolButton()
		wKill.setMaximumWidth(14)
		wKill.setMaximumHeight(14)
		wKill.setText('X')
		lTbar.addWidget(wKill)



		wHeader = QWidget()
		wHeader.setFixedHeight(22)
		lHeader = QHBoxLayout(wHeader)
		lHeader.setSpacing(4)
		lHeader.setContentsMargins(0,0,0,0)
		cLayout.addWidget(wHeader)


		self.wAssign = QCheckBox()
		self.wAssign.setMaximumWidth(16)
		lHeader.addWidget(self.wAssign)

		self.lButton = QToolButton()
		self.lButton.setText(self.mark.label())
		self.lButton.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Ignored)
		lHeader.addWidget(self.lButton)

		self.wFrameTool = MarkWidgetPanel(fields, self.mark.getData())
		self.wFrameTool.sigFieldChanged.connect(self.panelTouched)

		self.wFrameTool.hide()
		cLayout.addWidget(self.wFrameTool)


		self.setColor(cColor)


		self.lButton.clicked.connect(self.toolPop)
		self.wAssign.stateChanged.connect(self.outAssign)
		wSelby.clicked.connect(lambda: self.sigSelect.emit(self.mark))
		wKill.clicked.connect(lambda: self.sigKill.emit(self.mark))



	#partially state have priority
	def setAssign(self, _on=None, tri=None):
		cState = Qt.Checked if _on else Qt.Unchecked

		if tri:
			cState = Qt.PartiallyChecked


		self.wAssign.blockSignals(True)
		self.wAssign.setCheckState(cState)
		self.wAssign.blockSignals(False)



	def setColor(self, _color):
#??		self.lButton.setPalette(QColor.fromRgb(color[0],color[1],color[2]))
		cColor = QColor(_color).getRgb()[:-1]

		self.lButton.setStyleSheet(f"background-color: rgba{cColor+(.5,)};border-radius:4px;")
		self.wFrameHighlight.setStyleSheet(f"background-color: rgba{cColor+(.2,)};border-radius:4px;")



#  todo 376 (mark, ui, ux) +0: pin mark widget
	def toolPop(self):
		MarkWidget.toolUnpop()


		MarkWidget.activeMB = self

		self.wFrameHighlight.show()
		self.wFrameTool.show()
		self.wTbar.show()



	#Close active onr
	def toolUnpop():
		if MarkWidget.activeMB:
			MarkWidget.activeMB.wFrameHighlight.hide()
			MarkWidget.activeMB.wFrameTool.hide()
			MarkWidget.activeMB.wTbar.hide()

		MarkWidget.activeMB = None
