from PySide2.QtWidgets import *
from PySide2.QtCore import *


# -todo 140 (module-ui, mark) +0: redesign
class MarkTool(QFrame):


	def __init__(self, _parent, _mark):
		QFrame.__init__(self, _parent)


		self.mark = _mark

		self.resize(100,100)
		self.setStyleSheet("background-color: rgba(0,0,0,0);")


		popFrameCover = QFrame(self)
		popFrameCover.resize(100,100)
		popFrameCover.setStyleSheet(f"border: 2px solid rgba(128,128,128,.5); border-radius: 5px; background-color: rgba(0,0,0,.9);")

		cColor = tuple(self.mark.getData()['markColor']) +(.1,)
		popFrameContent = QFrame(popFrameCover)
		popFrameContent.resize(100,100)
		popFrameContent.setStyleSheet(f"background-color: rgba{cColor};")




class MarkButton(QToolButton):
	currentMarkTool = None



	def __init__(self, _contAnchor, _contSpace, _mark):
		QToolButton.__init__(self)

		
		self.mark = _mark
		self.contAnchor = _contAnchor
		self.contSpace = _contSpace


#??		self.setPalette(QColor.fromRgb(color[0],color[1],color[2]))
		self.setStyleSheet(f"background-color: rgb{self.mark.getData()['markColor']}")

		self.toolFrame = MarkTool(self.contSpace, _mark)

		self.clicked.connect(self.toolPop)



	def toolPop(self):
		if MarkButton.currentMarkTool:
			MarkButton.currentMarkTool.hide()

		MarkButton.currentMarkTool = self.toolFrame


		toolPoint = QPoint(self.contAnchor.width()+6,0)
		self.toolFrame.move( self.contAnchor.mapTo(self.contSpace, toolPoint) )

		self.toolFrame.show()
