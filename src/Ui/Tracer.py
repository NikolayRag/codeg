'''
Also tracer is optimised to be *fast*,
it blocks dispatch by single-threaded svg update if on,
that can and will interfere with entire cut proccess
at late event when there's lot of painted feed present already.
'''
# -todo 274 (ux, fix) +1: make Tracer paint nonblocking

#  todo 292 (tracer, ui) +0: apply styles to Tracer


import re
from datetime import datetime

from PySide2.QtCore import *
from PySide2.QtWidgets import *
from PySide2.QtGui import *



class TraceShape():
	outHeadInter = "<polyline vector-effect='non-scaling-stroke' stroke-width='1px' stroke='#590' stroke-dasharray='3' fill='none' points='"
	outHeadShape = "<polyline vector-effect='non-scaling-stroke' stroke-width='1px' stroke='#3b0' fill='none' points='"



	def create(self):
		if self.svgGen and not self.svgDescr:
			self.svgDescr = self.svgGen()
		
		if self.svgDescr:
			self.svgDescr.ghost(True)
			self.svgDescr.place(self.viewbox[0:2])


		return self.svgDescr



	def draw(self):
		if self.visible and self.updated and self.create():
			out = [f"<svg width='{int(self.viewbox[2])}' height='{int(self.viewbox[3])}' xmlns='http://www.w3.org/2000/svg'>"]
			out += self.snapshot()
			out += ["</svg>"]

			self.svgDescr.setXml(' '.join(out).encode())

			self.updated = False



	def __init__(self, _svgGen, _visible=True, _viewbox=(0,0,1,1)):
		self.visible = _visible
		self.drawn = False
		self.data = []
		self.viewbox = _viewbox

		self.svgDescr = None
		self.svgGen = _svgGen


		self.updated = False



	def show(self, _vis):
		self.visible = _vis
		if _vis:
			self.draw()

		self.svgDescr and self.svgDescr.show(_vis)



	def add(self, _data):
		self.data.append(f'{_data[0]},{_data[1]}')
		self.updated = True

#		self.draw() #degrade control needed



	def dataLen(self):
		return len(self.data)



	def snapshot(self):
		outSh = [self.outHeadInter] + self.data[:2] + ["'/>"]
		if len(self.data)>1:
			outSh += [f"<path d='M{self.data[1]} h0.0000001' stroke='#0f0' stroke-linecap='round' vector-effect='non-scaling-stroke' stroke-width='6px'/>"]
		outSh += [self.outHeadShape] + self.data[1:] + ["'/>"]

		return outSh



	def remove(self):
		self.svgDescr and self.svgDescr.remove()

		self.svgDescr = None
		self.updated = True




# -todo 289 (tracer, ux) +0: add clean/pin Tracer echo

'''
Dispatch ui and live tracer
'''
#  todo 273 (ux, clean) +0: rewindable trace history
#  todo 296 (tracer, fix) +0: fix Tracer live viewbox
#  todo 297 (tracer, fix) +0: fix Tracer shapes viewbox
class Tracer(QObject):
	pointTrace = 'resource\\point-trace.svg'
	pointWarning = 'resource\\point-warning.svg'
	pointError = 'resource\\point-error.svg'


	triggerDraw = 1
	triggerFocus = 5

	layShapes = None
	layFocus = None
	laySpots = None


	session = None

	lenPoints = 0
	lastSpot = (0,0)

	visLive = False
	visPaint = False



	def __init__(self, _vp, _osd=None):
		QObject.__init__(self)

		self.laySpots = []
		self.layShapes = []

		self.wViewport = _vp
		self.wLog, self.wStats = _osd



	def toggleVis(self, _live=None, _shapes=None):
		if _live!=None:
			self.visLive = _live

		if _shapes!=None:
			self.visPaint = _shapes


		self.wViewport.canvasUpdate(False)

		self.layFocus and self.layFocus.show(self.visLive)

		for sp in self.laySpots:
			sp.show(self.visLive)

		for sp in self.layShapes:
			sp.show(self.visPaint)

		self.wViewport.canvasUpdate(True)



	#called with no session after SvgViewport recreated
	def reset(self, _session=None):
		self.layFocus and self.layFocus.remove()
		self.layFocus = self.wViewport.canvasAdd(z=101)
		self.layFocus.setXml(self.pointTrace)
		self.layFocus.ghost(True)
		self.layFocus.static(True)


		for sp in self.layShapes:
			sp.remove()

		for sp in self.laySpots:
			sp.remove()
#  todo 293 (Tracer, ux) +0: leave Traced spots after reset viewport
		self.laySpots = []	


		if _session:
			self.layShapes = []	

			self.session = _session

			self.lastSpot = (0,0)
			self.moveto((0,0))

			self.lenPoints = 0


		self.toggleVis()



	def feed(self, _session, _res, _cmd):
		edge = re.findall("S([\d]+)", _cmd)
		if edge and float(edge[0])==0:
			self.triggerDraw = 1
			self.moveto(self.lastSpot, True)


		coords = re.findall("X(-?[\d\.]+)Y(-?[\d\.]+)", _cmd)
		if coords:
			self.moveto((float(coords[0][0]), -float(coords[0][1])))



	def spot(self, _session, _res):
		cPoint = self.pointError if _res else self.pointWarning
		self.spotto(self.lastSpot, cPoint)



	def final(self, _session, _res):
		self.moveto(self.lastSpot, True)

		if not _res:
			self.spotto(self.lastSpot, self.pointError)



	def spotto(self, _xy, _xml):
		cSpot = self.wViewport.canvasAdd(z=102)
		cSpot.show(self.visLive)
		cSpot.ghost(True)
		cSpot.static(True)
		cSpot.setXml(_xml)
		cSpot.place(_xy)

		self.laySpots.append(cSpot)



	def moveto(self, _xy, _new=False):
		self.lastSpot = _xy


		vBox = self.session.viewBox()

		if not self.layShapes or _new:
			self.layShapes and self.layShapes[-1].draw()

			cShape = TraceShape(lambda: self.wViewport.canvasAdd(z=100),
				self.visPaint, vBox)
			self.layShapes.append(cShape)

		else:
			self.lenPoints += 1


		self.layShapes[-1].add((_xy[0]-vBox[0],_xy[1]-vBox[1]))

		
		l = self.layShapes[-1].dataLen()

		if l%self.triggerFocus == 2: #each Nth from start of shape (2nd pt)
			self.layFocus and self.layFocus.place(_xy)

		if l>self.triggerDraw and len(self.layShapes)<1000:
			self.triggerDraw = l*1.01+self.lenPoints*.01
			self.layShapes[-1].draw()
