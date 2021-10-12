from PySide2.QtCore import *
from PySide2.QtWidgets import *
from PySide2.QtGui import *



class DragList(QTabBar):
	allW = []


	def __init__(self, _parent=None):
		QTabBar.__init__(self, _parent)

		self.setMovable(True)
		self.setExpanding(False)
		self.setShape(QTabBar.RoundedEast)

		self.setStyleSheet('border: none;')
		self.setDrawBase(False)



	def addTab(self, _widget, dragWidget=None, widgetLeft=None):
		QTabBar.addTab(self,None)

		tabFrame = QFrame()
		self.allW.append(tabFrame)


		tabLayout = QHBoxLayout()
		tabLayout.setSpacing(0)
		tabLayout.setContentsMargins(0,0,0,0)
		tabFrame.setLayout(tabLayout)

		if not dragWidget:
			dragWidget = QLabel('=')


		wFiller = QLabel('a')
		wFiller.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

		tabLayout.addWidget(wFiller)

		tabLayout.addWidget(_widget)
		tabLayout.addWidget(dragWidget)

		self.setTabButton(self.count()-1, QTabBar.LeftSide, tabFrame)

