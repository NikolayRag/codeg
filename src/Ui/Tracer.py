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

	__canvas = None
	focus = None
	layers = None
	osd = None


	session = None

	canvasVBox = None
	canvasBody = []
	feedLen = 0
	lastSpot = (0,0)

	visible = True


	def __init__(self, _svgGen, _osd=None):
		self.svgGen = _svgGen

		self.__canvas = _svgGen(0)
		self.__canvas.ghost(True)

		self.layers = []

		self.osd = _osd



	def show(self, _state):
		self.visible = _state
		if _state and self.canvasVBox:
			self.canvasBuild()


		self.__canvas.show(_state)
		self.focus and self.focus.show(_state)
		for sp in self.layers:
			sp.show(_state)



	def reset(self, _session=None):
		self.__canvas = self.svgGen(0)
		self.__canvas.ghost(True)
		if self.canvasVBox:
			self.__canvas.place(self.canvasVBox[0:2])

		self.focus and self.focus.remove()
		self.focus = self.svgGen(1)
		self.focus.setXml(self.pointTrace)
		self.focus.ghost(True)
		self.focus.static(True)

		for sp in self.layers:
			sp.remove()
		self.layers = []	

		self.show(self.visible)


		if not _session:
			return


		self.osd[0].appendPlainText("Dispatch begin")
		self.osd[1].setPlainText('')
		self.osd[2].setValue(0)


		self.session = _session

		self.canvasVBox = _session.viewBox()
		self.canvasBody = [[]]
		self.feedLen = 0
		self.lastSpot = (0,0)

		self.__canvas.place(self.canvasVBox[0:2])
		self.canvasBuild([0,0])



	def feed(self, _res, _cmd):
		self.osd[1].setPlainText(f"Shapes: {len(self.canvasBody)-1}\nPoints: {sum(len(x) for x in self.canvasBody)-1}")
		self.feedLen += 1
		self.osd[2].setValue(100*self.feedLen/self.session.pathLen())


		edge = re.findall("S[\d]+", _cmd)
		if len(edge)==1 and float(edge[0][1:])==0:
			self.canvasBuild()
			self.canvasBody.append([])


		coords = re.findall("[XY]-?[\d\.]+", _cmd)

		if len(coords)==2 and len(coords[0])>1 and len(coords[1])>1 and coords[0][0]=='X' and coords[1][0]=='Y':
			self.lastSpot = (float(coords[0][1:]), -float(coords[1][1:]))
			self.moveto(self.lastSpot)


		if _res != True:
			self.osd[0].appendPlainText((f"{_res or 'Warning'}:\n ") + _cmd)

			cPoint = self.pointError if _res else self.pointWarning
			self.spot(self.lastSpot, cPoint)



	def final(self, _res):
		self.osd[1].setPlainText(f"Shapes: {len(self.canvasBody)-2}\nPoints: {sum(len(x) for x in self.canvasBody)-1}")
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
		self.focus and self.focus.place(_xy)

		self.canvasBuild(_xy)



	def canvasBuild(self, _add=None):
		if _add:
			if not self.canvasBody[-1]:
				self.spot((float(_add[0]), float(_add[1])), self.pointShape)

			self.canvasBody[-1] += [f"{_add[0]-self.canvasVBox[0]},{_add[1]-self.canvasVBox[1]}"]

		l = sum(len(x) for x in self.canvasBody)
		if _add and (not self.visible or (l% (int(l/self.decayDraw)+1))):
			return


		last = None

#  todo 269 (module-ui, clean, fix) +1: make painting reasonable
		out = [f"<svg width='{int(self.canvasVBox[2])}' height='{int(self.canvasVBox[3])}' xmlns='http://www.w3.org/2000/svg'>"]
		for sh in self.canvasBody:
			if last:
				out += [self.outHeadInter] + last + [sh[0]] + ["'/>"]

			out += [self.outHeadShape] + sh + ["'/>"]

			last = [sh[-1]]

		out += ["</svg>"]

		self.__canvas.setXml(' '.join(out).encode())
