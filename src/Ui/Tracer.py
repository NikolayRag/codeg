import re



'''
Dispatch live tracer
'''
# =todo 271 (ux, clean) +0: Trace OSD
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

	canvas = None
	focus = None
	spots = None
	osd = None


	session = None

	canvasVBox = None
	canvasBody = []

	visible = True


	def __init__(self, _svgGen, _osd=None):
		self.svgGen = _svgGen

		self.canvas = _svgGen(0)
		self.canvas.ghost(True)

		self.focus = _svgGen(1)
		self.focus.setXml(self.pointTrace)
		self.focus.ghost(True)
		self.focus.static(True)

		self.spots = []

		self.osd = _osd



	def show(self, _state):
		self.visible = _state
		if _state and self.canvasVBox:
			self.canvasBuild()


		self.canvas.show(_state)
		self.focus.show(_state)
		for sp in self.spots:
			sp.show(_state)



	def reset(self, _session=None):
		if not _session:
			self.canvas = self.svgGen(0)
			self.canvas.ghost(True)
			if self.canvasVBox:
				self.canvas.place(self.canvasVBox[0:2])

			self.focus = self.svgGen(1)
			self.focus.setXml(self.pointTrace)
			self.focus.ghost(True)
			self.focus.static(True)

			self.show(self.visible)

			return


		self.session = _session

		self.canvasVBox = _session.viewBox()
		self.canvasBody = [[]]

		self.canvas.place(self.canvasVBox[0:2])
		self.canvasBuild([0,0])
		
		for sp in self.spots:
			sp.remove()
		self.spots = []	



	def feed(self, _res, _cmd):
		edge = re.findall("S[\d]+", _cmd)
		if len(edge)==1 and float(edge[0][1:])==0:
			print(f"Shape {len(self.canvasBody)}")

			self.canvasBuild()
			self.canvasBody.append([])


		coords = re.findall("[XY]-?[\d\.]+", _cmd)

		if len(coords)==2 and len(coords[0])>1 and len(coords[1])>1 and coords[0][0]=='X' and coords[1][0]=='Y':
			self.moveto(float(coords[0][1:]), -float(coords[1][1:]))


		l = sum(len(x) for x in self.canvasBody)
		progress = round(100.*l/self.session.pathLen(),2)
		step = int(l/self.decayDraw)+1

		if _res != True:
			cPoint = self.pointWarning if _res else self.pointError
			self.spot(float(coords[0][1:]), -float(coords[1][1:]), cPoint)

			print(f'Step {l}/{step}: {progress}% with {_res}')



	def final(self, _res):
		self.canvasBuild()



	def spot(self, _x, _y, _xml):
		cSpot = self.svgGen(2)
		cSpot.show(self.visible)
		cSpot.ghost(True)
		cSpot.static(True)
		cSpot.setXml(_xml)
		cSpot.place((_x, _y))

		self.spots.append(cSpot)



	def moveto(self, _x, _y):
		self.focus and self.focus.place((_x, _y))

		self.canvasBuild((_x,_y))



	def canvasBuild(self, _add=None):
		if _add:
			if not self.canvasBody[-1]:
				self.spot(float(_add[0]), float(_add[1]), self.pointShape)

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

		self.canvas.setXml(' '.join(out).encode())
