from PySide2.QtWidgets import *


class MarkWidget(QToolButton):
	

	def __init__(self, color=None):
		QToolButton.__init__(self)

		if color:
#??			self.setPalette(QColor.fromRgb(color[0],color[1],color[2]))
			self.setStyleSheet(f"background-color: rgb{color}")
