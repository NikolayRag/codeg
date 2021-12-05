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
class Tracer():
	pointTrace = 'resource\\point-trace.svg'
	pointWarning = 'resource\\point-warning.svg'
	pointError = 'resource\\point-error.svg'


	triggerDraw = 1
	triggerFocus = 5

	svgGen = None

	layShapes = None
	layFocus = None
	laySpots = None
	osd = None


	session = None

	canvasVBox = None
	lenFeed = 0
	lenPoints = 0
	lenShapes = 0
	lastSpot = (0,0)

	dtStart = 0

	args = None

	

	def __init__(self, _args, _svgGen, _osd=None):
		self.args = _args
		self.svgGen = _svgGen

		self.laySpots = []
		self.layShapes = []

		self.wViewport, self.wRoot, self.wLog, self.wStats, self.wProgress, self.wLive, self.wShapes = _osd


		self.wLive.toggled.connect(lambda v: self.showTracer(live=v))
		self.wShapes.toggled.connect(lambda v: self.showTracer(shapes=v))

		self.showTracer(live=self.args.visTracer, shapes=self.args.visTraceShapes)



	def prepare(self, _session):
		self.wLog.appendPlainText(f"Dispatch pending")



	def showTracer(self, _vis=None, live=None, shapes=None):
		self.wViewport.canvasUpdate(False)


		if _vis!=None:
			self.args.visDispatch - _vis

		self.wRoot.setVisible(self.args.visDispatch)


		if live != None:
			self.wShapes.setEnabled(live)
			self.args.visTracer = live

		live = (self.args.visDispatch and self.args.visTracer)
		self.layFocus and self.layFocus.show(live)
		for sp in self.laySpots:
			sp.show(live)


		if shapes != None:
			self.args.visTraceShapes = shapes

		shapes = (self.args.visDispatch and self.args.visTracer and self.args.visTraceShapes)
		for sp in self.layShapes:
			sp.show(shapes)


		self.wViewport.canvasUpdate(True)



	#called with no session after SvgViewport recreated
	def reset(self, _session=None):
		self.layFocus and self.layFocus.remove()
		self.layFocus = self.svgGen(1)
		self.layFocus.setXml(self.pointTrace)
		self.layFocus.ghost(True)
		self.layFocus.static(True)


		for sp in self.layShapes:
			sp.remove()

		for sp in self.laySpots:
			sp.remove()
		self.laySpots = []	



		if not _session:
			self.showTracer()
			return


		self.layShapes = []	
		self.showTracer()


		self.dtStart = datetime.now()

		self.wLog.appendPlainText(f"{str(self.dtStart)[:-5]}:\nDispatch begin")
		self.wStats.setPlainText('')
		self.wProgress.setValue(0)


		self.session = _session
		self.canvasVBox = _session.viewBox()
		#self.layResult.place(self.canvasVBox[0:2])

		self.lastSpot = (0,0)
		self.moveto((0,0))

		self.lenFeed = 0
		self.lenPoints = 0




	def feed(self, _res, _cmd):
#		self.wLog.appendPlainText(_cmd)

		dt = datetime.now()-self.dtStart
		self.wStats.setPlainText(f"+{str(dt)[:-5]}\nsh/pt: {len(self.layShapes)-1}/{self.lenPoints}")
		self.lenFeed += 1
		self.wProgress.setValue(100*self.lenFeed/self.session.pathLen())


		edge = re.findall("S([\d]+)", _cmd)
		if edge and float(edge[0])==0:
			self.triggerDraw = 1
			self.moveto(self.lastSpot, True)


		coords = re.findall("X(-?[\d\.]+)Y(-?[\d\.]+)", _cmd)
		if coords:
			self.moveto((float(coords[0][0]), -float(coords[0][1])))


		if _res != True:
			self.wLog.appendPlainText((f"{_res or 'Warning'}:\n ") + _cmd)

			cPoint = self.pointError if _res else self.pointWarning
			self.spot(self.lastSpot, cPoint)



	def final(self, _res):
		self.moveto(self.lastSpot, True)

		self.lenPoints -= 1 #last shape is park
		dt = datetime.now()-self.dtStart
		self.wStats.setPlainText(f"+{str(dt)[:-5]}\nsh/pt: {len(self.layShapes)-3}/{self.lenPoints}")
		self.wLog.appendPlainText(f"{str(datetime.now())[:-5]}:\nDispatch {'end' if _res else 'error'}\nin {str(dt)[:-5]}\nwith {len(self.layShapes)-3}/{self.lenPoints} sh/pt\n")
		if not _res:
			self.spot(self.lastSpot, self.pointError)



	def spot(self, _xy, _xml):
		cSpot = self.svgGen(2)
		cSpot.show(self.args.visDispatch and self.args.visTracer)
		cSpot.ghost(True)
		cSpot.static(True)
		cSpot.setXml(_xml)
		cSpot.place(_xy)

		self.laySpots.append(cSpot)



	def moveto(self, _xy, _new=False):
		self.lastSpot = _xy


		if not self.layShapes or _new:
			self.layShapes and self.layShapes[-1].draw()

			cShape = TraceShape(lambda:self.svgGen(0),
				self.args.visDispatch and self.args.visTracer and self.args.visTraceShapes,
				self.canvasVBox
			)
			self.layShapes.append(cShape)

		else:
			self.lenPoints += 1


		self.layShapes[-1].add((_xy[0]-self.canvasVBox[0],_xy[1]-self.canvasVBox[1]))

		
		l = self.layShapes[-1].dataLen()

		if l%self.triggerFocus == 2: #each Nth from start of shape (2nd pt)
			self.layFocus and self.layFocus.place(_xy)

		if l>self.triggerDraw and len(self.layShapes)<1000:
			self.triggerDraw = l*1.01+self.lenPoints*.01
			self.layShapes[-1].draw()
