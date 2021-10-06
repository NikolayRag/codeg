from PySide2.QtWidgets import *
from PySide2.QtGui import *
from PySide2.QtCore import *

from .Widgets import *



# -todo 140 (module-ui, mark) +0: redesign
class MarkTool(QFrame):
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
		self.setBackground(self.mark.getData()['markColor'])


		self.wLayout = QFormLayout()
		self.setLayout(self.wLayout)

		self.fillFrame()

		wBg.resize(self.sizeHint()-QSize(4,4))
		self.wBgColor.resize(self.sizeHint()-QSize(4,4))



	def setBackground(self, _color):
		cColor = tuple(_color.getRgb()[:-1]) +(.1,)
		self.wBgColor.setStyleSheet(f"background-color: rgba{cColor};")



	def fillFrame(self):
		mDataA = self.mark.getData()
		for cData in mDataA:
			fieldName = QLabel(f"{cData}")
			fieldVal = QLabel(f"{mDataA[cData]}")

			dType = type(mDataA[cData])
			if (dType==QColor):
				fieldVal = ColorPicker(mDataA[cData])

				fieldVal.sigChangedColor.connect(lambda _c: self.changedColor(cData, _c))


			self.wLayout.addRow(fieldName, fieldVal)



	def changedColor(self, _name, _val):
		self.mark[_name] = _val




class MarkButton(QToolButton):
	mark = None
	currentMB = None



	def __init__(self, _contLay, _mark):
		QToolButton.__init__(self)

		
		self.mark = _mark


		self.setCheckable(True)
#??		self.setPalette(QColor.fromRgb(color[0],color[1],color[2]))
		cColor = self.mark.getData()['markColor'].getRgb()[:-1]
		self.setStyleSheet(f"background-color: rgb{cColor}")

		self.wFrameHighlight = QFrame(self)
		self.wFrameHighlight.resize(self.sizeHint())
		self.wFrameHighlight.setStyleSheet(f"border: 2px solid #eee; border-radius:2px")
		self.wFrameHighlight.hide()


		self.wFrameTool = MarkTool(_mark)
		self.wFrameTool.hide()


		_contLay.addWidget(self.wFrameTool)

		self.clicked.connect(self.toolPop)



	def toolPop(self):
		if MarkButton.currentMB:
			MarkButton.currentMB.setChecked(False)
			MarkButton.currentMB.wFrameHighlight.hide()
			MarkButton.currentMB.wFrameTool.hide()

		MarkButton.currentMB = self


		self.setChecked(True)
		self.wFrameHighlight.show()
		self.wFrameTool.show()
