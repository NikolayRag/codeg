import re



'''
Dispatch live tracer
'''
#  todo 273 (ux, clean) +0: rewindable trace history
#  todo 274 (ux, clean) +0: make paint nonblocking
class Tracer():
	pointTrace = 'resource\\point-trace.svg'
	pointShape = 'resource\\point-shape.svg'
	pointWarning = 'resource\\point-warning.svg'
	pointError = 'resource\\point-error.svg'

	outHeadInter = "<polyline vector-effect='non-scaling-stroke' stroke-width='1px' stroke='#590' stroke-dasharray='3' fill='none' points='"
	outHeadShape = "<polyline vector-effect='non-scaling-stroke' stroke-width='1px' stroke='#3b0' fill='none' points='"

	decayDraw = 100.


	svgGen = None

	layShapes = None
	focus = None
	layers = None
	osd = None


	session = None

	canvasVBox = None
	canvasBody = []
	lenFeed = 0
	lenPoints = 0
	lenShapes = 0
	lastSpot = (0,0)

	visible = True
	visibleShapes = True


	def __init__(self, _svgGen, _osd=None):
		self.svgGen = _svgGen

		self.layers = []
		self.layShapes = []

		self.osd = _osd



# =todo 282 (ui, performance) +0: Tracer separate shapes visibility
	def show(self, main=None, shapes=None):
		if main != None:
			self.visible = main

			self.focus and self.focus.show(main)
			for sp in self.layers:
				sp.show(main)


		if shapes != None:
			self.visibleShapes = shapes

			if shapes and self.canvasVBox:
				self.canvasBuild()

			for sp in self.layShapes:
				sp.show(shapes)




	#called with no session after SvgViewport recreated
	def reset(self, _session=None):
		self.focus and self.focus.remove()
		self.focus = self.svgGen(1)
		self.focus.setXml(self.pointTrace)
		self.focus.ghost(True)
		self.focus.static(True)

		for sp in self.layShapes:
			sp.remove()
		self.layShapes = []	
		self.canvasBody = []

		for sp in self.layers:
			sp.remove()
		self.layers = []	

		self.show(self.visible, self.visibleShapes)


		if not _session:
			return


		self.osd[0].appendPlainText("Dispatch begin")
		self.osd[1].setPlainText('')
		self.osd[2].setValue(0)


		self.session = _session
		self.canvasVBox = _session.viewBox()

		self.lastSpot = (0,0)
		self.moveto((0,0))

		self.lenFeed = 0
		self.lenPoints = 0
		self.lenShapes = 0



	def feed(self, _res, _cmd):
		self.osd[1].setPlainText(f"Shapes: {self.lenShapes}\nPoints: {self.lenPoints}")
		self.lenFeed += 1
		self.osd[2].setValue(100*self.lenFeed/self.session.pathLen())


		edge = re.findall("S[\d]+", _cmd)
		if len(edge)==1 and float(edge[0][1:])==0:
			self.canvasBuild()
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
		self.osd[1].setPlainText(f"Shapes: {self.lenShapes}\nPoints: {self.lenPoints}")
		self.osd[0].appendPlainText(f"Dispatch {'end' if _res else 'error'}")
		if not _res:
			self.spot(self.lastSpot, self.pointError)

		self.canvasBuild()



	def spot(self, _xy, _xml):
		cSpot = self.svgGen(2)
		cSpot.show(self.visible)
		cSpot.ghost(True)
		cSpot.static(True)
		cSpot.setXml(_xml)
		cSpot.place(_xy)

		self.layers.append(cSpot)



	def moveto(self, _xy):
		self.lastSpot = _xy


		self.focus and self.focus.place(_xy)


		if not self.canvasBody:
			cShape = self.svgGen(0)
			cShape.show(self.visibleShapes)
			cShape.ghost(True)
			cShape.place(self.canvasVBox[0:2])
			self.layShapes.append(cShape)

		else:
			self.lenPoints += 1

		if len(self.canvasBody)==1:
			self.lenShapes += 1
			self.spot((float(_xy[0]), float(_xy[1])), self.pointShape)

		self.canvasBody += [f"{_xy[0]-self.canvasVBox[0]},{_xy[1]-self.canvasVBox[1]}"]

		
		l = len(self.canvasBody)
		if self.visibleShapes and not(l% (int(l/self.decayDraw)+1)):
			self.canvasBuild()



	def canvasBuild(self):
#		last = None

# =todo 269 (module-ui, clean, fix) +1: make painting reasonable
		out = [f"<svg width='{int(self.canvasVBox[2])}' height='{int(self.canvasVBox[3])}' xmlns='http://www.w3.org/2000/svg'>"]
		out += [self.outHeadInter] + self.canvasBody[:2] + ["'/>"]
		out += [self.outHeadShape] + self.canvasBody[1:] + ["'/>"]
		out += ["</svg>"]

		self.layShapes and self.layShapes[-1].setXml(' '.join(out).encode())
