'''
Also tracer is optimised to be *fast*,
it blocks dispatch by single-threaded svg update if on,
that can and will interfere with entire cut proccess
at late event when there's lot of painted feed present already.
'''
import re
from datetime import datetime



'''
Dispatch live tracer
'''
#  todo 273 (ux, clean) +0: rewindable trace history
#  todo 274 (ux, clean) +0: make paint nonblocking
class Tracer():
	pointTrace = 'resource\\point-trace.svg'
	pointWarning = 'resource\\point-warning.svg'
	pointError = 'resource\\point-error.svg'

	outHeadInter = "<polyline vector-effect='non-scaling-stroke' stroke-width='1px' stroke='#590' stroke-dasharray='3' fill='none' points='"
	outHeadShape = "<polyline vector-effect='non-scaling-stroke' stroke-width='1px' stroke='#3b0' fill='none' points='"

	drawTrigger = 1


	svgGen = None

	#layResult = None
	layShapes = None
	layFocus = None
	laySpots = None
	osd = None


	session = None

	canvasVBox = None
	canvasBody = []
	shapesList = []
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
		self.shapesList = []

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

			if shapes and self.canvasVBox:
				self.canvasBuild()

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
		self.layShapes = []	
		self.canvasBody = []
		self.shapesList = []

		for sp in self.laySpots:
			sp.remove()
		self.laySpots = []	

		self.show(self.visibleSpots, self.visibleShapes)


		if not _session:
			return


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
		self.lenShapes = 0

		self.dtStart = datetime.now()



	def feed(self, _res, _cmd):
		dt = datetime.now()-self.dtStart
		self.osd[1].setPlainText(f"time: {str(dt)[:-5]}\nsh/pt: {self.lenShapes}/{self.lenPoints}")
		self.lenFeed += 1
		self.osd[2].setValue(100*self.lenFeed/self.session.pathLen())


		edge = re.findall("S[\d]+", _cmd)
		if len(edge)==1 and float(edge[0][1:])==0:
#			self.shapesList.append(self.canvasBuild())

#			cShapeAll = [f"<svg width='{int(self.canvasVBox[2])}' height='{int(self.canvasVBox[3])}' xmlns='http://www.w3.org/2000/svg'>"]
#			for sh in self.shapesList:
#				cShapeAll += sh
#			cShapeAll += ["</svg>"]
##			self.layResult.setXml(' '.join(cShapeAll).encode())


			self.canvasBuild()

			self.drawTrigger = 1
			self.canvasBody = []
			self.moveto(self.lastSpot)


		coords = re.findall("[XY]-?[\d\.]+", _cmd)

		if len(coords)==2 and len(coords[0])>1 and len(coords[1])>1 and coords[0][0]=='X' and coords[1][0]=='Y':
			self.moveto((float(coords[0][1:]), -float(coords[1][1:])))


		if _res != True:
			self.osd[0].appendPlainText((f"{_res or 'Warning'}:\n ") + _cmd)

			cPoint = self.pointError if _res else self.pointWarning
			self.spot(self.lastSpot, cPoint)



	def final(self, _res):
		self.lenPoints -= 1 #last shape is park
		self.lenShapes -= 1
		dt = datetime.now()-self.dtStart
		self.osd[1].setPlainText(f"time: {str(dt)[:-5]}\nsh/pt: {self.lenShapes}/{self.lenPoints}")
		self.osd[0].appendPlainText(f"Dispatch {'end' if _res else 'error'}")
		if not _res:
			self.spot(self.lastSpot, self.pointError)

		self.canvasBuild()



	def spot(self, _xy, _xml):
		cSpot = self.svgGen(2)
		cSpot.show(self.visibleSpots)
		cSpot.ghost(True)
		cSpot.static(True)
		cSpot.setXml(_xml)
		cSpot.place(_xy)

		self.laySpots.append(cSpot)



	def moveto(self, _xy):
		self.lastSpot = _xy


		self.layFocus and self.layFocus.place(_xy)


		if not self.canvasBody:
# -todo 269 (module-ui, clean, fix) +1: make painting reasonable
##use with layResult
#			if self.layShapes:
#				self.layShapes[-1].remove()
#				self.layShapes = []
##
			cShape = self.svgGen(0)
			cShape.show(self.visibleShapes)
			cShape.ghost(True)
			cShape.place(self.canvasVBox[0:2])
			self.layShapes.append(cShape)

		else:
			self.lenPoints += 1

		if len(self.canvasBody)==1:
			self.lenShapes += 1

		self.canvasBody += [f"{_xy[0]-self.canvasVBox[0]},{_xy[1]-self.canvasVBox[1]}"]

		
		l = len(self.canvasBody)
		if self.visibleShapes and l>self.drawTrigger:
			self.drawTrigger = l*1.01+self.lenPoints*.01
			self.canvasBuild()




	def canvasBuild(self):
		outSh = [self.outHeadInter] + self.canvasBody[:2] + ["'/>"]
		if len(self.canvasBody)>1:
			outSh += [f"<path d='M{self.canvasBody[1]} h0.0000001' stroke='#0f0' stroke-linecap='round' vector-effect='non-scaling-stroke' stroke-width='6px'/>"]
		outSh += [self.outHeadShape] + self.canvasBody[1:] + ["'/>"]

		out = [f"<svg width='{int(self.canvasVBox[2])}' height='{int(self.canvasVBox[3])}' xmlns='http://www.w3.org/2000/svg'>"]
		out += outSh
		out += ["</svg>"]

		self.layShapes and self.layShapes[-1].setXml(' '.join(out).encode())

		return outSh
