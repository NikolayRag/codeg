+feature, file, graphics 1: +0 "src\Ui\AppWindow.py" kii 21/07/26 05:38:38
	load SVG

+feature, file 2: +0 "src\Ui\AppWindow.py" kii 21/07/25 16:29:21
	deal with recent files

 feature, file 3: +0 "" kii 21/10/14 17:04:11
	allow picking from Recent files list

+svg, feature 4: +0 "src\Ui\SvgViewport.py" kii 21/08/02 19:14:43
	zoom by wheel within center-mouse

=module-ui, feature 5: +0 "" kii 21/08/03 02:38:56
	pan by mouse

 module-ui, feature 6: +0 "src\Ui\SvgViewport.py" kii 21/08/02 21:02:22
	smooth animated zoom

+spec, module-data 7: +0 "src\__main__w.py" kii 21/07/31 02:59:50
	read svg

+spec, module-data 8: +0 "src\GGData\GGData.py" kii 21/07/31 16:30:49
	save gcode

!scene, spec, module-data 9: +1 "src\GGData\Scene.py" ki 21/10/18 18:33:32
	operate project data

!spec, module-data 10: +0 "" kii 21/09/08 21:55:55
	dup

=spec, module-data 11: +0 "src\GGData\Scene.py" kii 21/09/27 02:38:56
	read/save scene data

+spec, module-ui 12: +1 "src\__main__w.py" kii 21/07/31 02:59:35
	show scene

+spec, module-ui, proto 13: +0 "src\__main__w.py" kii 21/07/31 02:59:34
	render from xml svg

+spec, module-ui 14: +0 "src\__main__w.py" kii 21/07/31 02:58:53
	render from module-data

+module-ui, viewport, ux 15: +0 "src\Ui\SvgViewport.py" kii 21/08/03 02:38:35
	basic mouse navigation

!module-ui, viewport 16: +0 "" kii 21/08/04 06:11:58
	dup

=spec, module-dispatch 17: +0 "" kii 21/08/10 05:55:57
	send to serial-usb (arduino)

 spec, module-dispatch 18: +0 "src\GGData\GGData.py" kii 21/09/25 22:37:20
	standalone dispatcher codegg

 spec, module-dispatch 19: +0 "src\GGData\GGData.py" kii 21/08/02 21:16:57
	send to codegg

 module-ui, error 20: +0 "src\Ui\AppWindow.py" kii 21/10/10 14:16:43
	handle errors, maybe status string

!module-ui, file 21: +0 "" kii 21/07/31 03:32:28
	dup

=module-dispatch, ux 22: +0 "src\Dispatch\Dispatch.py" ki 21/10/17 17:36:52
	make dispatch interruptable

-module-ui, ux 23: +0 "src\Ui\Ui.py" kii 21/09/09 21:27:51
	show progress for time consuming operations

!module-data, formats 24: +0 "" kii 21/07/31 16:33:32
	dup

 module-data, formats 25: +0 "src\GGData\GGData.py" kii 21/08/02 21:16:10
	load .nc gcode

!module-data, formats 26: +0 "src\GGData\GGData.py" kii 21/07/31 16:30:39
	

 module-data, module-ui, ux 27: +0 "src\Ui\Ui.py" ki 21/10/17 18:53:47
	allow append gcode from text buffer

+module-ui 28: +0 "src\Ui\AppWindow.py" kii 21/08/02 21:55:16
	add github link

+module-ui, tech 29: -1 "src\Ui\AppWindow.py" kii 21/07/31 19:34:09
	filter mouse events correctly

+module-ui, error 31: +1 "src\Ui\AppWindow.py" kii 21/07/31 19:26:37
	Filter __init__ dont work

+module-ui, spec, viewport 32: +1 "src\Ui\SvgViewport.py" kii 21/08/02 21:57:55
	make isolated viewport widget

 module-ui, widgets 33: +0 "src\Ui\AppWindow.py" kii 21/08/04 14:07:26
	zoom slider

 module-ui, widgets 34: +0 "src\Ui\AppWindow.py" kii 21/08/02 05:05:28
	transform reset

!module-ui, widgets 35: +0 "src\Ui\AppWindow.py" kii 21/08/02 05:10:07
	zoom factor 

 module-ui, API 36: +0 "src\Ui\SvgViewport.py" kii 21/08/02 06:13:19
	make viewport interaction callbacks

 module-ui, viewport 37: +0 "src\Ui\SvgViewport.py" kii 21/08/24 17:44:42
	make custom scrollbars out of SvgViewport

+module-ui, API 38: +0 "src\Ui\SvgViewport.py" kii 21/08/02 19:14:34
	add SVGCanvas.canvasPlace

+module-ui, viewport, fix 39: +0 "src\Ui\SvgViewport.py" kii 21/08/02 16:08:53
	update wrong size at first call

+module-ui, viewport 40: +0 "src\Ui\SvgViewport.py" kii 21/08/02 21:02:08
	limit scaling

+module-ui, viewport 41: +0 "src\Ui\SvgViewport.py" kii 21/08/02 19:16:59
	limit moving

+module-ui, viewport, ux 42: +0 "src\Ui\SvgViewport.py" kii 21/08/02 19:11:21
	fit Svg on load

+module-ui, viewport, ux 44: +0 "src\Ui\SvgViewport.py" kii 21/08/03 02:17:12
	react on window resize

+module-ui, ux 45: +0 "src\Ui\SvgViewport.py" kii 21/08/02 20:34:09
	stop scale-moving beyond limits

=module-ui 46: +0 "" kii 21/08/03 13:39:59
	fill connection port list

 module-dispatch, module-ui, ux 47: +0 "src\Ui\AppWindow.py" kii 21/08/03 19:25:49
	change device list to button+list

 module-ui 48: +0 "src\Dispatch\Dispatch.py" kii 21/08/03 13:12:51
	update device list

 module-ui, ux 49: +0 "" kii 21/08/04 06:11:17
	save/restore active device between sessions

+module-ui 50: +0 "src\Ui\AppWindow.py" kii 21/09/01 22:53:30
	add style

=module-ui, ux 51: +0 "" kii 21/08/04 06:13:01
	layer control

+fix 52: +0 "src\Ui\Ui.py" kii 21/08/06 17:05:36
	odd branching optimisation

+fix, module-ui 53: +0 "src\Ui\AppWindow.py" kii 21/08/04 06:40:29
	reset layers selection at reload

=module-ui, ux 54: +0 "" kii 21/08/07 00:20:03
	mouse hover layers

+fix, module-ui 55: +0 "src\Ui\AppWindow.py" kii 21/08/04 14:44:55
	generalize case

+module-ui, fix 57: +0 "src\Ui\AppWindow.py" kii 21/08/07 00:14:59
	catch out of hover on short layers

+fix 58: +0 "src\Ui\Ui.py" kii 21/08/06 17:23:41
	isolate

-module-ui, ux, clean 59: +0 "src\Ui\AppWindow.py" kii 21/08/06 17:22:09
	make updatable connections list

=module-dispatch 60: +0 "src\Dispatch\Dispatch.py" kii 21/08/28 18:03:33
	show gcodes live proto

=module-dispatch 61: +0 "src\Dispatch\Dispatch.py" kii 21/08/07 03:45:15
	CNC control

=module-dispatch 62: +0 "src\Dispatch\Dispatch.py" kii 21/08/15 22:52:53
	live device control

+module-ui, ux 63: +0 "src\Ui\Ui.py" kii 21/09/02 03:50:54
	basic layer control, on-off

-module-dispatch 64: +0 "src\Dispatch\Dispatch.py" kii 21/08/17 15:28:44
	dispatch queue

!module-dispatch 65: +0 "src\Dispatch\Dispatch.py" kii 21/08/07 05:38:19
	

 module-ui, module-dispatch 66: +0 "src\GGData\GGData.py" kii 21/09/05 21:16:18
	show dispatch progress

-API 67: +1 "src\__main__w.py" kii 21/09/08 21:59:33
	change callbacks to signals-slots

-module-dispatch 68: +0 "src\Dispatch\Dispatch.py" kii 21/08/20 02:57:25
	queue control

 gcode 69: +0 "src\GGen\GGen.py" kii 21/08/12 04:40:26
	check min tolerance

!general 70: +0 "src\GGen\GGen.py" kii 21/08/12 04:33:11
	

=gcode, fix 71: +0 "src\GGen\GGen.py" kii 21/08/12 04:44:40
	clean gcode scale

-gcode 72: +0 "src\GGen\GGen.py" kii 21/08/12 04:43:22
	use different inlines from SVG

=gcode 73: +0 "src\GGen\GGen.py" kii 21/08/12 04:44:33
	decorate shapes begin/end

+fix, gcode 74: +0 "src\GGen\GGen.py" kii 21/08/15 04:01:51
	detect multishape

!fix, gcode 75: +0 "src\GGen\GGen.py" kii 21/08/14 20:12:11
	

=fix, gcode 76: +0 "" kii 21/08/25 22:58:28
	gcode move, scale and crop

 fix, module-ui, viewport, decide 77: -1 "src\Ui\Ui.py" kii 21/09/25 22:46:34
	duplicate hover element topmost

+module-ui, ux 78: +0 "src\Ui\Ui.py" kii 21/08/15 22:10:50
	store/restore window size

!module-ui, ux, fix 79: +0 "src\Ui\AppWindow.py" kii 21/10/09 16:43:12
	make size ignored on maximize

+module-ui, svg, feature 80: +0 "src\Ui\SvgViewport.py" kii 21/08/20 05:30:30
	make SvgCanvas multilayered

-module-ui, svg, feature 81: +0 "" kii 21/08/27 03:13:26
	show grid

 module-data, ux 82: +0 "src\GGData\GGData.py" kii 21/08/20 03:48:29
	parse groups

 ux, module-ui, fix 83: +0 "src\Ui\SvgViewport.py" kii 21/09/22 23:33:54
	fit at init dont work due to obsolete size 

 module-data 84: +0 "src\GGData\GGData.py" kii 21/09/29 03:36:45
	make file load plugin system

+module-dispatch 85: +0 "src\GGData\GGData.py" kii 21/08/28 18:00:25
	Gcode generate in background

!fix, gcode 86: +1 "src\Ui\Ui.py" kii 21/08/22 20:19:01
	

+fix, gcode 87: +0 "src\Ui\Ui.py" kii 21/08/28 18:02:01
	place svg layers more generally

-fix, gcode 88: +0 "src\Ui\Ui.py" kii 21/09/03 02:02:12
	use dispatch both for file save

-ux, module-ui, fix 89: +0 "src\Ui\SvgViewport.py" kii 21/09/25 22:54:19
	place grid correctly

=ux, module-ui, fix 90: +0 "src\GGData\GGData.py" kii 21/09/08 22:03:51
	respect units - both svg and device

-viewport, api 91: +0 "src\Ui\SvgViewport.py" ki 21/10/18 18:20:26
	add class-level SVG runtime generator signal/slot

 feature 92: +0 "src\GGData\Scene.py" ki 21/10/18 18:33:34
	multiple sources scene

!scene, feature 93: +0 "" kii 21/09/27 02:39:14
	redundant

 viewport, fix 95: +0 "src\Ui\SvgViewport.py" kii 21/08/28 15:52:23
	clip max scale by render limit

!module-ui, ux, scene 96: +0 "src\Ui\AppWindow.py" kii 21/08/29 16:52:03
	

 viewport, fix, solve 97: +0 "src\Ui\SvgViewport.py" kii 21/09/01 21:59:23
	decide how to paint different layer sizes

 module-ui, optimize 98: -1 "src\Ui\Ui.py" kii 21/09/02 01:04:33
	prevent doubling by difference change

!module-ui, optimize 99: +0 "src\GGen\GGen.py" kii 21/09/02 03:40:33
	

 gcode, feature 100: +0 "src\GGData\GGData.py" kii 21/09/27 02:22:22
	allow flexible filters for gcode

+module-ui 101: +0 "src\Ui\Ui.py" kii 21/09/08 02:52:08
	styles for selected-hovered-visible matrix

+module-ui, fix 102: +0 "src\Ui\Ui.py" kii 21/09/02 04:05:16
	bulk update layer change

+module-ui, module-data, API 103: +0 "src\Ui\Ui.py" kii 21/09/08 02:52:25
	move geo decorators to data

-module-data, decide 104: +0 "src\GGData\GGData.py" kii 21/09/29 04:39:03
	move to filter

+module-data, filter, API 105: +0 "src\GGData\GGData.py" kii 21/09/25 22:38:42
	add geo Filter class

!module-data, module-dispatch, device, API 106: +0 "" kii 21/09/05 21:54:01
	--

+decorator, module-data 108: +0 "src\GGData\GGData.py" kii 21/09/08 02:43:01
	get only affected since last request names

!decorator, optimize 109: +0 "" kii 21/09/08 21:13:58
	obsolete

+clean 110: +0 "src\GGData\GGData.py" kii 21/09/07 22:45:38
	use namedRef

-mark, optimize 111: +0 "src\GGData\Scene.py" kii 21/09/29 04:27:33
	dramatically slow mark reapply

+mark, feature 112: +0 "src\GGData\Geomark.py" kii 21/09/25 22:41:32
	complex mark

+scene, module-ui, ux 113: +0 "src\GGData\Scene.py" kii 21/09/25 22:40:14
	assignable layer marks holding control data

=module-ui, fix 114: +0 "src\Ui\AppWindow.py" kii 21/09/08 13:42:53
	change vis for select-all case

 ux 115: -1 "src\Ui\Ui.py" kii 21/09/08 18:41:16
	allow to choose style by commandline

=ux, module-ui 116: +0 "src\Ui\Ui.py" kii 21/09/08 18:41:48
	choose style in app settings

=ux, module-ui 117: +0 "src\Ui\Ui.py" kii 21/10/11 22:19:18
	add app settings

 refactor, module-ui, module-data 118: +0 "src\Ui\Ui.py" kii 21/10/09 21:40:56
	clean for minor import

-refactor, module-ui, module-data 119: +0 "src\Ui\Ui.py" kii 21/09/09 21:27:02
	clean for dispatch

+refactor, module-ui, module-data, fix 120: +0 "src\Ui\Ui.py" kii 21/10/09 20:33:56
	hold pre-maximize size

+module-data, fix 121: +0 "src\GGen\GGen.py" kii 21/09/09 22:20:25
	go to .items() for ElementTree

+filter, module-data 124: +0 "src\GGData\Geomark.py" kii 21/09/25 22:41:33
	make set svg tag as system filter

+mark, optimize 126: +0 "src\GGData\Geoblock.py" kii 21/09/26 23:59:12
	manage object-level attributes

+mark, optimize, decide 127: +10 "src\GGData\Geomark.py" kii 21/09/25 22:42:08
	Move marks assignment to Geoblock WTF?!

+mark, optimize, decide 128: +10 "src\GGData\Geoblock.py" kii 21/09/25 22:40:45
	Move marks assignment to geo dict WTF?!

+mark 129: +0 "src\GGData\Geomark.py" kii 21/09/26 23:57:45
	store custom fields data list

+mark 130: +0 "src\GGData\Geomark.py" kii 21/09/19 03:24:15
	move filter data to Geofilter

!app, refactor 131: +1 "src\Ui\Ui.py" kii 21/09/25 22:44:00
	move default Marks creation to App-level

=module-data, refactor 132: +0 "" kii 21/09/25 22:47:48
	unify Filter creation

 mark, optimize, decide 133: -1 "src\GGData\Geoblock.py" kii 21/09/26 23:50:36
	Need to cache data?

+module-data, api 134: -1 "src\GGData\GGData.py" ki 21/10/16 21:01:11
	Clean Scene and further classes to be used as a GGData API part

+module-data, API, filters 135: +0 "src\GGData\GGData.py" kii 21/09/28 13:42:23
	add fallback dummy filter on fly

-module-data, decide 136: +0 "src\GGData\Mark.py" ki 21/10/16 22:42:37
	step is ambiguous

+module-data, scene 137: +0 "src\GGData\GGData.py" kii 21/09/29 03:15:27
	multiscene

+module-data, clean 138: +0 "src\GGData\GGData.py" kii 21/10/14 15:10:58
	cleanup root scene functions

 clean 139: +0 "src\GGData\Scene.py" kii 21/09/29 13:34:57
	Clean mark to object appending

-module-ui, mark 140: +0 "src\Ui\MarkWidget.py" kii 21/10/04 13:14:09
	redesign

-module-ui, mark 141: +0 "src\Ui\AppWindow.py" kii 21/10/10 13:17:56
	update Geoitem widgets

+ui, mark 142: +0 "src\Ui\AppWindow.py" kii 21/10/10 19:28:48
	Select Marks by layers

=ui, widgets 143: +0 "src\Ui\Widgets.py" kii 21/10/10 02:27:15
	simplify color picker

=module-ui, widgets 144: +0 "src\Ui\AppWindow.py" kii 21/10/11 22:21:45
	Use Geoitems directly in UI

-module-ui, widgets 145: +0 "src\Ui\AppWindow.py" kii 21/10/12 03:54:15
	make Marks arrangable with priority change (DragList)

=module-data, mark 146: +0 "src\Ui\Ui.py" kii 21/10/10 13:29:23
	auto-increment mark priorities at creation

-module-ui, fix 147: +0 "src\Ui\AppWindow.py" kii 21/10/10 19:31:52
	use blank layer space to from-to hover mouse selection

=module-ui, fix 148: +0 "src\Ui\Ui.py" kii 21/10/14 01:17:26
	review scene life cycle

 module-ui, feature 149: +0 "src\Ui\Ui.py" kii 21/10/11 22:19:18
	multiscene

-ux, widgets 150: +0 "src\Ui\AppWindow.py" kii 21/10/11 22:25:56
	Make ItemWidget

 module-ui, mark 152: +0 "src\Ui\AppWindow.py" kii 21/10/12 01:49:30
	make select by mark

 module-ui, mark 153: +0 "src\Ui\AppWindow.py" kii 21/10/12 01:50:38
	manage mark fields list

+module-data, scene 155: +0 "src\GGData\GGData.py" kii 21/10/14 15:09:14
	store short scene name in scene

-fix, canvas 156: +0 "src\Ui\SvgViewport.py" kii 21/10/14 02:05:39
	canvas is wrong size at init

 fix, canvas 157: +0 "src\Ui\AppWindow.py" kii 21/10/14 04:48:24
	review SvgViewport fit routine

+module-data, fix 158: +0 "src\GGData\GGData.py" kii 21/10/14 17:43:48
	move to direct Scene definitions

+module-data, fix, scene 159: +0 "src\GGData\GGData.py" kii 21/10/14 17:44:06
	make Scene data cleanup

+module-ui 160: +0 "src\Ui\Ui.py" kii 21/10/14 23:46:55
	File Load Cancel case

+module-data, scene 161: +0 "src\GGData\Scene.py" ki 21/10/15 14:50:22
	collect Scene dirty state

 module-data, mark 162: +0 "src\GGData\Mark.py" kii 21/10/15 14:28:14
	Filter Success case

!feature, save 163: +0 "src\Ui\Ui.py" ki 21/10/17 18:28:32
	Scene save/load

=feature, module-ui 164: -1 "src\Ui\Ui.py" ki 21/10/17 18:51:23
	auto-apply new Mark to selection

=feature, dispatch 165: +0 "src\Ui\Ui.py" ki 21/10/18 18:41:17
	device definition

=module-ui, ux 166: +0 "src\Ui\Ui.py" ki 21/10/18 18:41:19
	icons

=module-ui, viewport 167: +0 "src\Ui\Ui.py" ki 21/10/18 18:41:38
	deselect geo by viewport

-module-ui, viewport 168: +0 "src\Ui\Ui.py" ki 21/10/18 18:41:50
	select by viewport

=module-ui, ux, mark 169: +0 "src\Ui\Ui.py" ki 21/10/18 18:42:31
	del mark

-module-ui, ux, mark 170: +0 "src\Ui\Ui.py" ki 21/10/18 18:42:33
	reorder mark

=module-ui, ux, mark 171: +0 "src\Ui\Ui.py" ki 21/10/18 18:42:40
	select by mark

=module-ui, ux, mark 172: +0 "src\Ui\Ui.py" ki 21/10/18 18:42:47
	unselect mark/close mark box

-module-ui, ux, mark 173: +0 "src\Ui\Ui.py" ki 21/10/18 18:42:55
	hover mark show toolbox

=module-ui, module-data, geo 174: +0 "src\Ui\Ui.py" ki 21/10/18 18:43:36
	add more geo

=module-ui, module-data, geo 175: +0 "src\Ui\Ui.py" ki 21/10/18 18:43:43
	clone geo

=module-ui, module-data, geo 176: +0 "src\Ui\Ui.py" ki 21/10/18 18:43:48
	del geo

=ux 177: +0 "src\Ui\Ui.py" ki 21/10/18 18:44:30
	check dirty at exit

=ux 178: +0 "src\Ui\Ui.py" ki 21/10/18 18:44:25
	suggest recent at load

