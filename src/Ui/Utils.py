class Counter():
	seeds = {}


	def next(_name, _inc):
		if _name not in Counter.seeds:
			Counter.seeds[_name] = 0

		out = Counter.seeds[_name]

		Counter.seeds[_name] += _inc

		return out

