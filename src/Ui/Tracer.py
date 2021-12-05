'''
Also tracer is optimised to be *fast*,
it blocks dispatch by single-threaded svg update if on,
that can and will interfere with entire cut proccess
at late event when there's lot of painted feed present already.
'''
# -todo 274 (ux, fix) +1: make Tracer paint nonblocking



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





'''
Dispatch live tracer
'''
#  todo 273 (ux, clean) +0: rewindable trace history
class Tracer():
	pointTrace = 'resource\\point-trace.svg'
	pointWarning = 'resource\\point-warning.svg'
	pointError = 'resource\\point-error.svg'

#	outHeadInter = "<polyline vector-effect='non-scaling-stroke' stroke-width='1px' stroke='#590' stroke-dasharray='3' fill='none' points='"
#	outHeadShape = "<polyline vector-effect='non-scaling-stroke' stroke-width='1px' stroke='#3b0' fill='none' points='"

	triggerDraw = 1
	triggerFocus = 5

	svgGen = None

	#layResult = None
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

	visibleSpots = True
	visibleShapes = True



	def __init__(self, _svgGen, _osd=None):
		self.svgGen = _svgGen

		self.laySpots = []
		self.layShapes = []

		self.osd = _osd



# =todo 282 (ui, performance) +0: Tracer separate shapes visibility
	def show(self, spots=None, shapes=None):
		if spots != None:
			self.visibleSpots = spots

			self.layFocus and self.layFocus.show(spots)
			for sp in self.laySpots:
				sp.show(spots)


		if shapes != None:
			self.visibleShapes = shapes

			for sp in self.layShapes:
				sp.show(shapes)

			#self.layResult and self.layResult.show(shapes)




	#called with no session after SvgViewport recreated
	def reset(self, _session=None):
		self.layFocus and self.layFocus.remove()
		self.layFocus = self.svgGen(1)
		self.layFocus.setXml(self.pointTrace)
		self.layFocus.ghost(True)
		self.layFocus.static(True)

		#self.layResult and self.layResult.remove()
		#self.layResult = self.svgGen(0)
		#self.layResult.ghost(True)
		#self.canvasVBox and self.layResult.place(self.canvasVBox[0:2])


		for sp in self.layShapes:
			sp.remove()

		for sp in self.laySpots:
			sp.remove()
		self.laySpots = []	


		self.show(spots=self.visibleSpots)

		if not _session:
			self.show(shapes=self.visibleShapes)
			return


		self.layShapes = []	


		self.osd[0].appendPlainText("Dispatch begin")
		self.osd[1].setPlainText('')
		self.osd[2].setValue(0)


		self.session = _session
		self.canvasVBox = _session.viewBox()
		#self.layResult.place(self.canvasVBox[0:2])

		self.lastSpot = (0,0)
		self.moveto((0,0))

		self.lenFeed = 0
		self.lenPoints = 0

		self.dtStart = datetime.now()



	def feed(self, _res, _cmd):
#		self.osd[0].appendPlainText(_cmd)

		dt = datetime.now()-self.dtStart
		self.osd[1].setPlainText(f"time: {str(dt)[:-5]}\nsh/pt: {len(self.layShapes)-1}/{self.lenPoints}")
		self.lenFeed += 1
		self.osd[2].setValue(100*self.lenFeed/self.session.pathLen())


		edge = re.findall("S([\d]+)", _cmd)
		if edge and float(edge[0])==0:
#			self.shapesList.append(self.layShapes[-1].snapshot())

#			cShapeAll = [f"<svg width='{int(self.canvasVBox[2])}' height='{int(self.canvasVBox[3])}' xmlns='http://www.w3.org/2000/svg'>"]
#			for sh in self.shapesList:
#				cShapeAll += sh
#			cShapeAll += ["</svg>"]
##			self.layResult.setXml(' '.join(cShapeAll).encode())


			self.triggerDraw = 1
			self.moveto(self.lastSpot, True)


		coords = re.findall("X(-?[\d\.]+)Y(-?[\d\.]+)", _cmd)
		if coords:
			self.moveto((float(coords[0][0]), -float(coords[0][1])))


		if _res != True:
			self.osd[0].appendPlainText((f"{_res or 'Warning'}:\n ") + _cmd)

			cPoint = self.pointError if _res else self.pointWarning
			self.spot(self.lastSpot, cPoint)



	def final(self, _res):
		self.moveto(self.lastSpot, True)

		self.lenPoints -= 1 #last shape is park
		dt = datetime.now()-self.dtStart
		self.osd[1].setPlainText(f"time: {str(dt)[:-5]}\nsh/pt: {len(self.layShapes)-3}/{self.lenPoints}")
		self.osd[0].appendPlainText(f"Dispatch {'end' if _res else 'error'}")
		if not _res:
			self.spot(self.lastSpot, self.pointError)



	def spot(self, _xy, _xml):
		cSpot = self.svgGen(2)
		cSpot.show(self.visibleSpots)
		cSpot.ghost(True)
		cSpot.static(True)
		cSpot.setXml(_xml)
		cSpot.place(_xy)

		self.laySpots.append(cSpot)



	def moveto(self, _xy, _new=False):
		self.lastSpot = _xy


		if not self.layShapes or _new:
			self.layShapes and self.layShapes[-1].draw()

			cShape = TraceShape(lambda:self.svgGen(0), self.visibleShapes, self.canvasVBox)
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
