+feature, file, graphics 1: +0 "src\Ui\AppWindow.py" kii 21/07/26 05:38:38
	load SVG

+feature, file 2: +0 "src\Ui\AppWindow.py" kii 21/07/25 16:29:21
	deal with recent files

 feature, file 3: +0 "src\Ui\Ui.py" kii 21/10/29 21:03:25
	geo library

+svg, feature 4: +0 "src\Ui\SvgViewport.py" kii 21/08/02 19:14:43
	zoom by wheel within center-mouse

=module-ui, feature 5: +0 "" kii 21/08/03 02:38:56
	pan by mouse

 module-ui, feature 6: -1 "src\Ui\SvgViewport.py" kii 21/10/24 04:43:28
	smooth animated zoom

+spec, module-data 7: +0 "src\__main__w.py" kii 21/07/31 02:59:50
	read svg

+spec, module-data 8: +0 "src\GGData\GGData.py" kii 21/07/31 16:30:49
	save gcode

!scene, spec, module-data 9: +1 "src\GGData\Scene.py" kii 21/10/18 18:33:32
	operate project data

!spec, module-data 10: +0 "" kii 21/09/08 21:55:55
	dup

+spec, module-data 11: +0 "src\GGData\Scene.py" kii 21/10/29 17:32:20
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

 API, module-dispatch, v2 18: +0 "src\Ui\DispatchLink.py" kii 21/12/05 04:55:41
	standalone dispatcher over *cloud*

!spec, module-dispatch 19: +0 "src\GGData\GGData.py" kii 21/11/15 01:00:55
	send to codegg

+module-dispatch, error 20: +0 "src\Ui\DispatchLink.py" kii 21/11/22 03:37:24
	handle errors, maybe status string

!module-ui, file 21: +0 "" kii 21/07/31 03:32:28
	dup

=module-dispatch, ux 22: +1 "src\Dispatch\DispatchManager.py" kii 21/11/26 04:06:12
	make dispatch interruptable and terminatable

-module-ui, ux 23: +0 "src\Ui\Ui.py" kii 21/11/22 15:16:12
	show progress for time consuming operations

!module-data, formats 24: +0 "" kii 21/07/31 16:33:32
	dup

 module-data, formats 25: +0 "src\GGData\GGData.py" kii 21/08/02 21:16:10
	load .nc gcode

!module-data, formats 26: +0 "src\GGData\GGData.py" kii 21/07/31 16:30:39
	

 module-data, module-ui, ux 27: +0 "src\Ui\Ui.py" kii 21/10/17 18:53:47
	allow append gcode from text buffer

+module-ui 28: +0 "src\Ui\AppWindow.py" kii 21/08/02 21:55:16
	add github link

+module-ui, tech 29: -1 "src\Ui\AppWindow.py" kii 21/07/31 19:34:09
	filter mouse events correctly

+module-ui, error 31: +1 "src\Ui\AppWindow.py" kii 21/07/31 19:26:37
	Filter __init__ dont work

+module-ui, spec, viewport 32: +1 "src\Ui\SvgViewport.py" kii 21/08/02 21:57:55
	make isolated viewport widget

 module-ui, widgets 33: +0 "src\Ui\AppWindow.py" kii 21/11/24 04:41:06
	zoom slider

 module-ui, widgets 34: +0 "src\Ui\AppWindow.py" kii 21/08/02 05:05:28
	transform reset

!module-ui, widgets 35: +0 "src\Ui\AppWindow.py" kii 21/08/02 05:10:07
	zoom factor 

+module-ui, API 36: +0 "src\Ui\SvgViewport.py" kii 21/10/31 00:39:45
	make viewport interaction callbacks

 module-ui, viewport 37: +0 "src\Ui\SvgViewport.py" kii 21/11/01 19:40:46
	make custom scrollbars for SvgViewport

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

 module-dispatch, module-ui, ux, unsure 47: +0 "src\Ui\AppWindow.py" kii 21/12/07 23:29:27
	change device list to button+list

+module-ui 48: +0 "src\Ui\AppWindow.py" kii 21/12/07 23:29:03
	update device list

 module-ui, ux 49: +0 "src\Ui\AppWindow.py" kii 21/12/07 23:29:04
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

-module-ui, ux, clean 59: +0 "src\Ui\AppWindow.py" kii 21/11/04 04:09:46
	make updatable connections list

+module-dispatch 60: +0 "src\Dispatch\DispatchManager.py" kii 21/11/22 17:03:37
	show gcodes live proto

-module-dispatch 61: +0 "src\Dispatch\DispatchManager.py" ki 21/12/12 00:55:05
	CNC manual control

!module-dispatch 62: +0 "src\Dispatch\DispatchManager.py" kii 21/11/22 17:03:25
	live device control

+module-ui, ux 63: +0 "src\Ui\Ui.py" kii 21/09/02 03:50:54
	basic layer control, on-off

+module-dispatch 64: +0 "src\Dispatch\DispatchManager.py" ki 21/12/10 16:29:33
	dispatch queue

!module-dispatch 65: +0 "src\Dispatch\Dispatch.py" kii 21/08/07 05:38:19
	

 module-ui, module-dispatch 66: +0 "src\GGData\Scene.py" kii 21/11/02 14:31:22
	show dispatch progress

-API 67: +1 "src\__main__w.py" kii 21/09/08 21:59:33
	change callbacks to signals-slots

-module-dispatch 68: +0 "src\Dispatch\DispatchManager.py" ki 21/12/10 16:29:34
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

!module-data, ux 82: +0 "src\GGData\Geoblock.py" kii 21/11/03 05:27:21
	parse groups

 ux, module-ui, fix 83: +0 "src\Ui\SvgViewport.py" kii 21/11/01 19:48:46
	fit at init dont work due to obsolete size 

 module-data 84: +0 "src\GGData\Scene.py" kii 21/10/29 17:32:58
	make file load plugin system

+module-dispatch 85: +0 "src\GGData\GGData.py" kii 21/08/28 18:00:25
	Gcode generate in background

!fix, gcode 86: +1 "src\Ui\Ui.py" kii 21/08/22 20:19:01
	

+fix, gcode 87: +0 "src\Ui\Ui.py" kii 21/08/28 18:02:01
	place svg layers more generally

 fix, gcode, unsure 88: +0 "src\Ui\Ui.py" kii 21/11/15 02:17:12
	use dispatch both for file save

+ux, module-ui, fix 89: +0 "src\Ui\AppWindow.py" kii 21/11/08 14:31:39
	place grid correctly

-ux, module-ui, fix 90: +5 "src\GGData\GGData.py" ki 21/12/12 00:58:37
	respect units - both svg and device

+viewport, API 91: +0 "src\Ui\SvgViewport.py" kii 21/10/24 05:32:07
	add class-level SVG runtime generator signal/slot

+feature 92: +0 "src\GGData\Scene.py" kii 21/10/29 17:32:58
	multiple sources scene

!scene, feature 93: +0 "" kii 21/09/27 02:39:14
	redundant

 viewport, fix 95: +0 "src\Ui\SvgViewport.py" kii 21/10/31 21:10:08
	clip max scale by render limit

!module-ui, ux, scene 96: +0 "src\Ui\AppWindow.py" kii 21/08/29 16:52:03
	

+viewport, fix, solve 97: +0 "src\Ui\SvgViewport.py" kii 21/10/31 05:43:32
	respect layer offset and scale

 module-ui, optimize 98: -1 "src\Ui\Ui.py" kii 21/09/02 01:04:33
	prevent doubling by difference change

!module-ui, optimize 99: +0 "src\GGen\GGen.py" kii 21/09/02 03:40:33
	

 gcode, feature 100: +0 "" kii 21/11/02 14:43:19
	allow flexible filters for gcode

+module-ui 101: +0 "src\Ui\Ui.py" kii 21/09/08 02:52:08
	styles for selected-hovered-visible matrix

+module-ui, fix 102: +0 "src\Ui\Ui.py" kii 21/09/02 04:05:16
	bulk update layer change

+module-ui, module-data, API 103: +0 "src\Ui\Ui.py" kii 21/09/08 02:52:25
	move geo decorators to data

-module-data, decide 104: +0 "src\GGData\Scene.py" kii 21/11/02 14:31:27
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

+mark, optimize 111: +0 "src\GGData\Scene.py" kii 21/10/24 01:38:11
	dramatically slow mark reapply

+mark, feature 112: +0 "src\GGData\Geomark.py" kii 21/09/25 22:41:32
	complex mark

+scene, module-ui, ux 113: +0 "src\GGData\Scene.py" kii 21/09/25 22:40:14
	assignable layer marks holding control data

+module-ui, fix 114: +0 "src\Ui\GeoWidget.py" kii 21/10/29 21:36:39
	select-all case bug

!ux 115: -1 "src\Ui\Ui.py" kii 21/11/08 14:29:21
	allow to choose style by commandline

+ux, module-ui 116: +0 "src\Ui\Ui.py" kii 21/11/08 14:29:12
	choose style in app settings

+ux, module-ui 117: +0 "src\Ui\Ui.py" kii 21/11/22 05:50:40
	add app settings

!refactor, module-ui, module-data 118: +0 "src\Ui\Ui.py" kii 21/10/23 03:36:50
	clean for minor import

-refactor, module-ui, module-data 119: +0 "src\Ui\Ui.py" kii 21/11/15 02:17:52
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

 mark, optimize, decide 133: -1 "src\GGData\Geoblock.py" kii 21/10/24 03:09:44
	Need to cache data?

+module-data, API 134: -1 "src\GGData\GGData.py" kii 21/10/16 21:01:11
	Clean Scene and further classes to be used as a GGData API part

+module-data, API, filters 135: +0 "src\GGData\GGData.py" kii 21/09/28 13:42:23
	add fallback dummy filter on fly

-module-data, decide 136: +0 "src\GGData\Mark.py" kii 21/10/16 22:42:37
	step is ambiguous

+module-data, scene 137: +0 "src\GGData\GGData.py" kii 21/09/29 03:15:27
	multiscene

+module-data, clean 138: +0 "src\GGData\GGData.py" kii 21/10/14 15:10:58
	cleanup root scene functions

+clean 139: +0 "src\GGData\Scene.py" kii 21/10/24 01:38:02
	Clean mark to object appending

-module-ui, mark 140: +0 "src\Ui\MarkWidget.py" kii 21/10/04 13:14:09
	redesign

-module-ui, mark 141: +0 "src\Ui\AppWindow.py" kii 21/10/23 01:36:55
	update Geoitem widgets on Mark assign

+ui, mark 142: +0 "src\Ui\AppWindow.py" kii 21/10/10 19:28:48
	Select Marks by layers

+ui, widgets 143: +0 "src\Ui\Widgets\ColorPicker.py" kii 21/10/24 17:01:41
	simplify color picker

+module-ui, widgets 144: +0 "src\Ui\AppWindow.py" kii 21/10/22 22:12:55
	Use Geoitems directly in UI

 module-ui, widgets 145: +0 "src\Ui\AppWindow.py" kii 21/10/25 15:42:29
	make Marks arrangable with priority change (DragList)

=module-data, mark 146: +0 "src\Ui\Ui.py" kii 21/10/10 13:29:23
	auto-increment mark priorities at creation

-module-ui, fix 147: +0 "src\Ui\GeoWidget.py" kii 21/10/29 21:04:50
	use blank layer space to from-to hover mouse selection

+module-ui, fix 148: +0 "src\Ui\Ui.py" kii 21/11/10 13:46:22
	review scene life cycle

 module-ui, feature 149: +0 "src\Ui\Ui.py" kii 21/10/11 22:19:18
	multiscene

+ux, widgets 150: +0 "src\Ui\AppWindow.py" kii 21/10/22 22:12:51
	Make GeoWidget

!module-ui, mark 152: +0 "src\Ui\AppWindow.py" kii 21/11/10 13:47:39
	make select by mark

 module-ui, mark 153: +0 "src\Ui\AppWindow.py" kii 21/11/10 15:25:28
	manage mark fields list

+module-data, scene 155: +0 "src\GGData\GGData.py" kii 21/10/14 15:09:14
	store short scene name in scene

+fix, canvas 156: +0 "src\Ui\SvgViewport.py" kii 21/11/02 01:08:16
	canvas is wrong size at init

+fix, canvas 157: +0 "src\Ui\AppWindow.py" kii 21/11/02 15:59:47
	review SvgViewport fit routine

+module-data, fix 158: +0 "src\GGData\GGData.py" kii 21/10/14 17:43:48
	move to direct Scene definitions

+module-data, fix, scene 159: +0 "src\GGData\GGData.py" kii 21/10/14 17:44:06
	make Scene data cleanup

+module-ui 160: +0 "src\Ui\Ui.py" kii 21/10/14 23:46:55
	File Load Cancel case

+module-data, scene 161: +0 "src\GGData\Scene.py" kii 21/10/15 14:50:22
	collect Scene dirty state

 module-data, mark 162: +0 "src\GGData\Mark.py" kii 21/10/15 14:28:14
	Filter Success case

!feature, save 163: +0 "src\Ui\Ui.py" kii 21/10/17 18:28:32
	Scene save/load

-feature, module-ui, unsure 164: -1 "src\Ui\Ui.py" kii 21/11/22 17:05:12
	auto-apply new Mark to selection

-feature, dispatch 165: +1 "src\Dispatch\DispatchManager.py" ki 21/12/12 00:55:13
	device settings definition

=module-ui, ux 166: +0 "src\Ui\Ui.py" kii 21/11/22 17:01:53
	icons

+module-ui, viewport 167: +0 "src\Ui\Ui.py" kii 21/10/24 05:53:45
	deselect geo by viewport

+module-ui, viewport, v2 168: +0 "src\Ui\Ui.py" kii 21/11/23 00:27:58
	select by viewport

=module-ui, ux, mark 169: +0 "src\Ui\Ui.py" kii 21/10/18 18:42:31
	del mark

-module-ui, ux, mark 170: +0 "src\Ui\Ui.py" kii 21/10/23 05:36:48
	reorder mark

=module-ui, ux, mark 171: +0 "src\Ui\Ui.py" kii 21/10/18 18:42:40
	select by mark

=module-ui, ux, mark 172: +0 "src\Ui\Ui.py" kii 21/10/18 18:42:47
	unselect mark/close mark box

-module-ui, ux, mark 173: +0 "src\Ui\Ui.py" kii 21/10/18 18:42:55
	hover mark show toolbox

+module-ui, module-data, geo 174: +0 "src\Ui\Ui.py" kii 21/10/29 21:07:36
	add more geo

=module-ui, module-data, geo 175: +0 "src\Ui\Ui.py" kii 21/10/29 21:07:44
	clone geo

=module-ui, module-data, geo 176: +0 "src\Ui\Ui.py" kii 21/10/18 18:43:48
	del geo

+ux 177: +0 "src\Ui\Ui.py" kii 21/10/23 05:34:36
	check dirty at exit

=ux, feature 178: +0 "src\Ui\Ui.py" kii 21/11/10 13:44:57
	suggest recent at load

-clean 179: -1 "src\Ui\Ui.py" ki 21/12/12 00:56:35
	check names, order and var/function annotates

-module-ui, mark, wat 180: +0 "src\Ui\MarkWidget.py" kii 21/11/08 14:32:19
	allow to assign only with selected geo

-decide 181: +0 "src\GGData\Geoblock.py" kii 21/11/05 20:04:13
	geometry embed method

-ux 182: +0 "src\Ui\Ui.py" ki 21/12/12 00:57:06
	save saved project with increment

-ux, module-ui 183: +1 "src\Ui\Ui.py" kii 21/10/19 20:47:46
	brush Scene routines

-ux, module-ui 184: +0 "src\Ui\Ui.py" kii 21/11/23 00:28:46
	save/load app settings with project

+feature, module-ui, module-dispatch, v2 186: +0 "src\Ui\Ui.py" kii 21/11/23 00:28:46
	live cut visualize

!dispatch, feature 187: +0 "src\Ui\Ui.py" kii 21/10/20 22:57:58
	

!module-data, API 188: +0 "src\Ui\Ui.py" kii 21/11/07 07:46:10
	move scene load to data

 module-data, API, decide 189: +0 "src\GGData\GGData.py" ki 21/12/12 00:58:32
	make all indirect (by id) controls

+feature, module-ui 190: +0 "src\Ui\Ui.py" kii 21/11/22 17:01:11
	live cut visualize from standalone dispatcher

 filter, feature 191: +2 "src\Ui\Ui.py" kii 21/10/20 23:58:14
	outline, fill and shape-intersect filters

+module-ui, fix 192: +0 "src\Ui\AppWindow.py" kii 21/11/05 04:13:41
	wrong fit at start

 ux, widgets, decide 193: +0 "src\Ui\GeoWidget.py" kii 21/10/22 18:21:35
	move to GeoItem widget

!issue, explore 194: +0 "src\Ui\GeoWidget.py" kii 21/10/22 18:35:40
	why does it remove selection before select-by-click?

+fix 195: +2 "src\Ui\Ui.py" kii 21/10/23 01:11:15
	fix sysytem marks assignment

 module-data, API 196: +0 "src\Ui\Ui.py" kii 21/12/05 22:54:41
	deal with Markfilter data fields within Mark

=data, fix 197: +0 "src\Ui\Ui.py" kii 21/11/04 04:06:17
	deal with missing svg link

-data, fix 198: +0 "src\Ui\Ui.py" kii 21/11/23 00:27:12
	move save/load routines to GGData

+module-data, module-ui, feature, API 199: +0 "src\Ui\AppWindow.py" kii 21/10/29 21:14:32
	multiple Geoblocks

+ux 200: +0 "src\Ui\Ui.py" kii 21/10/23 04:42:23
	suggest file ext at save

 geo, feature 201: +0 "src\GGData\Geoblock.py" kii 21/10/23 23:49:51
	update reference geometry 

+clean 202: +0 "src\__main__w.py" kii 21/11/07 05:55:28
	add app constants

=ux, clean 203: +0 "src\Ui\Ui.py" kii 21/10/24 01:21:13
	scene load/save error handling

+ux 204: +0 "src\Ui\Ui.py" kii 21/10/26 23:42:24
	group scene controls

+fix, module-data 205: +0 "src\GGData\Scene.py" kii 21/11/02 13:58:22
	check for multiobject case

+fix 206: +0 "src\Ui\MarkWidget.py" kii 21/10/24 03:15:59
	maybe unsafe for some threaded case

+viewport, v2 207: +0 "src\Ui\SvgViewport.py" kii 21/11/01 18:47:41
	onscreen controls

 viewport 208: +0 "src\Ui\SvgViewport.py" kii 21/10/24 04:29:16
	viewport controls

-fix, widgets 209: +0 "src\Ui\Widgets\ColorPicker.py" kii 21/10/24 17:03:37
	bound color picker by screen borders

 fix, widgets 210: -1 "src\Ui\Widgets\ColorPicker.py" kii 21/10/24 19:13:00
	popup ignores Alt+F4

+viewport, ux 211: +0 "src\Ui\AppWindow.py" kii 21/10/26 10:46:18
	cancel select by right click

 module-ui, clean, widget 212: +0 "src\Ui\AppWindow.py" kii 21/11/03 20:29:54
	MarkWidget collection class

 ux, viewport 213: +0 "src\Ui\AppWindow.py" kii 21/12/05 13:22:27
	geoblock overlay info

+module-ui, viewport 214: +0 "src\Ui\AppWindow.py" kii 21/10/30 02:09:01
	display inactive block differently

 module-ui 215: +0 "src\Ui\AppWindow.py" kii 21/10/28 15:34:12
	cleanup GeoWidget ui collection

=module-data, clean 216: +0 "src\GGData\Geoblock.py" kii 21/10/29 17:28:30
	use relative paths

 module-data, ux 217: +0 "src\Ui\Ui.py" kii 21/10/29 17:29:46
	detect missing geometry file

!module-ui, ux 218: +0 "src\Ui\Ui.py" kii 21/10/29 21:14:54
	add inactive Geo visual style

=module-ui, module-data, geo 219: +0 "src\Ui\Ui.py" kii 21/11/04 03:56:45
	edit Geoblock transform

=ux, widget 220: +0 "src\Ui\GeoWidget.py" ki 21/12/12 00:59:07
	make Geoitems list view continuous

+viewport 221: +0 "src\Ui\SvgViewport.py" kii 21/10/29 21:22:24
	add viewport descriptor

 feature 222: +2 "src\Ui\Ui.py" kii 21/10/30 00:47:31
	independent undo/preset stack for any Geo and Mark

!feature 223: +1 "src\Ui\Ui.py" kii 21/10/30 00:47:33
	

 ux, widget, fix 224: +0 "src\Ui\GeoWidget.py" kii 21/10/30 04:08:39
	GeoWidget badly layout review

 ux 225: +0 "src\Ui\Ui.py" kii 21/10/31 01:52:29
	store viewport position/size within scene

!fix, check 226: +0 "" kii 21/11/02 01:09:28
	probably will fit wrong if canvas and widget orientation differs

-fix 227: +0 "src\Ui\SvgViewport.py" kii 21/11/05 04:41:27
	integer pos and size result in SvgCanvasLayer jitter

+ux, fix 228: +0 "src\Ui\AppWindow.py" kii 21/10/31 22:47:20
	pin viewport while transforming geo

 viewport, v2 229: +0 "src\Ui\SvgViewport.py" kii 21/11/01 18:47:52
	overview

!viewport, feature 230: +0 "src\Ui\SvgViewport.py" kii 21/11/01 19:29:54
	add keypress event passed to sigInteract

+fix, svg, data 231: +0 "src\GGData\Geoblock.py" kii 21/11/03 06:29:32
	proccess SVG responsibly

!fix, svg 232: +1 "src\GGData\Geoblock.py" kii 21/11/02 23:41:47
	compensate svg scale with wrap-all transform block

 performance, unsure 233: +0 "src\GGData\Geoblock.py" kii 21/11/04 00:21:29
	bBox maybe time consuming for complex geo

+ux, viewport 234: +0 "src\Ui\SvgViewport.py" kii 21/11/03 20:06:29
	show interaction box

+fix 235: +1 "src\GGData\Geoblock.py" kii 21/11/04 06:29:58
	very bad viewport parsing, find reasonable solution

 svg, fix, v2 236: +0 "src\GGData\Geoblock.py" kii 21/11/05 20:05:08
	parse svg more completely

 svg, fix, v2 237: +0 "src\Ui\SvgViewport.py" kii 21/11/05 00:18:00
	go OGL

+fix, viewport, svg 238: +0 "src\Ui\SvgViewport.py" kii 21/11/08 14:33:01
	correct SvgCanvasLayer xform for scaled/offset svg

-svg 239: +0 "src\Ui\SvgViewport.py" ki 21/12/12 00:58:50
	join SvgDescriptor and SvgCanvasLayer

+API 240: +0 "src\args.py" kii 21/11/07 07:23:15
	make global settings singletone

-API, app 243: +0 "src\Args.py" ki 21/12/12 00:57:55
	parse command line

 feature 244: +0 "src\Ui\AppWindow.py" kii 21/11/08 14:11:05
	add drop scene, svg files and tag text

!feature 245: +0 "src\Ui\AppWindow.py" kii 21/11/08 14:11:32
	drop svg

-widget, feature 246: +0 "src\Ui\PrefsWidget.py" kii 21/11/09 13:51:01
	add reset settings

+fix, app 247: +0 "src\Ui\AppWindow.py" kii 21/11/10 03:27:45
	window pisition ruined if opened-closed maximized

-ux, feature 248: +0 "src\Ui\Ui.py" kii 21/11/14 23:40:28
	update default plate size

!module-dispatch, app, feature 249: +0 "src\Ui\DispatchLink.py" kii 21/11/15 01:01:08
	dis

+ux, module-dispatch 250: +0 "src\Ui\AppWindow.py" kii 21/11/23 00:24:20
	react on device changed

 module-dispatch, feature 251: +0 "src\Ui\Ui.py" kii 21/12/03 00:46:42
	make generation by iterator

+module-dispatch, feature 252: +0 "src\Ui\DispatchLink.py" kii 21/11/22 04:48:13
	dispatch async

+module-dispatch, ux 253: +0 "src\Dispatch\DispatchManager.py" kii 21/11/19 05:09:06
	find all suitable devices

+module-dispatch, ux 254: +0 "src\Dispatch\DispatchManager.py" kii 21/11/23 23:11:13
	scan devices parallel

+module-dispatch, fix 255: +0 "src\Ui\DispatchLink.py" kii 21/11/21 22:44:04
	use engines by reference only

+module-dispatch, ux 256: +0 "src\Ui\DispatchLink.py" kii 21/11/21 19:59:23
	list devices nonblocking

 ux 257: +0 "src\Ui\DispatchWidget.py" kii 21/12/08 01:44:45
	handle nonexistent device

 module-dispatch, error, ux 258: +0 "src\Ui\DispatchLink.py" kii 21/11/22 02:03:58
	handle retries

+fix, module-dispatch 259: +0 "src\Dispatch\engines\EngineArduinoGRBL.py" kii 21/11/28 21:55:23
	test device errors

-module-dispatch, fix 260: +5 "src\Dispatch\Engines\EngineArduinoGRBL.py" ki 21/12/12 00:53:33
	adopt full GRBL specification

-module-dispatch, feature 261: +1 "src\Ui\DispatchLink.py" ki 21/12/12 00:55:48
	add basic dispatch session manager

+feature, module-ui, module-dispatch 262: +0 "src\Ui\AppWindow.py" kii 21/11/23 00:25:46
	add functional cut feedback

+module-dispatch, feature 263: +0 "src\Ui\DispatchLink.py" kii 21/12/05 05:29:34
	add dispatch queue

+module-ui, module-dispatch, fix 264: +0 "src\Ui\Ui.py" kii 21/12/08 02:24:28
	use actual box

+feature, ux, module-dispatch 265: +0 "src\Ui\AppWindow.py" kii 21/11/24 04:06:22
	show live statistics

=module-dispatch, test 266: +0 "src\Dispatch\DispatchManager.py" ki 21/12/11 21:16:08
	handle device rescan interfere case

+module-dispatch, module-ui 267: +0 "src\Ui\AppWindow.py" kii 21/11/24 00:09:59
	instant update 

 module-dispatch, feature 268: +0 "src\Ui\DispatchLink.py" kii 21/11/27 03:41:18
	handle concurent sessions

+module-ui, clean, fix 269: +1 "src\Ui\Tracer.py" kii 21/12/03 00:30:37
	make painting reasonable

 module-dispatch, clean 270: +0 "src\Dispatch\DispatchEngine.py" kii 21/11/27 03:35:01
	add device queue control

+ux, clean 271: +0 "src\Ui\Tracer.py" kii 21/11/27 02:46:15
	Trace OSD

+ux, clean 272: +0 "src\Ui\Tracer.py" kii 21/11/26 22:30:09
	trace show error/warning position

 ux, clean 273: +0 "src\Ui\Tracer.py" kii 21/11/27 02:46:16
	rewindable trace history

-ux, fix 274: +1 "src\Ui\Tracer.py" kii 21/12/04 00:41:26
	make Tracer paint nonblocking

 module-dispatch, clean 275: +0 "src\Ui\DispatchLink.py" kii 21/11/26 02:45:55
	rescan device at stop state

-ux, clean 276: +0 "src\Ui\DispatchWidget.py" kii 21/12/08 05:10:01
	clean device rescan cycle

!! 277: +0 "src\Ui\DispatchLink.py" kii 21/11/26 14:56:19
	test

!! 278: +0 "src\Ui\DispatchLink.py" kii 21/11/26 14:56:17
	

 viewport, fix 279: +0 "src\Ui\SvgViewport.py" kii 21/11/26 18:11:17
	make removed SvgDescriptor safe

 ui, feature, idea 280: +0 "src\Ui\AppWindow.py" kii 21/12/07 23:30:10
	paint with Tracer into geometry layers

+ui, clean 281: +0 "src\Ui\AppWindow.py" kii 21/12/07 23:18:45
	make Tracer ui unweird

!ui, performance 282: +0 "src\Ui\Tracer.py" kii 21/12/05 03:18:18
	Tracer shapes separate visibility

=performance 283: +0 "" kii 21/12/02 15:56:34
	add shape into result layer

 module-dispatch, clean 284: +0 "src\Dispatch\DispatchManager.py" kii 21/11/30 00:27:32
	add deviceMeta

+ux, fix 285: +0 "src\Ui\Tracer.py" kii 21/12/03 23:50:03
	add TraceShape class

 viewport, optimize 286: +0 "src\Ui\SvgViewport.py" kii 21/12/03 00:48:44
	recompute viewport nonblocking

-test 287: +0 "src\Dispatch\DispatchManager.py" ki 21/12/12 00:54:32
	scan devices while busy

+tracer, ui 288: +0 "src\Ui\AppWindow.py" kii 21/12/05 17:19:35
	split shape/focus painting

-tracer, ux 289: +0 "src\Ui\Tracer.py" kii 21/12/05 12:55:00
	add clean/pin Tracer echo

=module-dispatch, feature 290: +0 "src\Ui\DispatchLink.py" kii 21/12/05 04:31:11
	dispatch end command

+module-ui, tracer 291: +0 "src\Ui\AppWindow.py" kii 21/12/05 22:36:23
	make Tracer an root ui for DispatchLink

 tracer, ui 292: +0 "src\Ui\Tracer.py" kii 21/12/05 12:54:01
	apply styles to Tracer

-Tracer, ux 293: +0 "src\Ui\Tracer.py" ki 21/12/11 21:00:14
	leave Traced spots after reset viewport

 Tracer, unsure 294: +0 "src\Ui\DispatchWidget.py" ki 21/12/10 17:50:16
	check memory leak on subsequent sessions

+ui, dispatch 295: +0 "src\Ui\AppWindow.py" kii 21/12/07 23:26:51
	dedicated DisppatchLink ui

 tracer, fix 296: +0 "src\Ui\Tracer.py" kii 21/12/07 20:52:32
	fix Tracer live viewbox

 tracer, fix 297: +0 "src\Ui\Tracer.py" kii 21/12/07 20:53:48
	fix Tracer shapes viewbox

-device, fix 298: +2 "src\Dispatch\Engines\EngineArduinoGRBL.py" ki 21/12/12 00:53:40
	operate device nonblocking

+device, fix 299: +0 "src\Dispatch\Engines\EngineArduinoGRBL.py" ki 21/12/12 00:51:23
	get GRBL actual metrics

-module-dispatch, device 300: +0 "src\Ui\DispatchLink.py" ki 21/12/12 00:55:29
	read device nonblocking from session

 trace 301: +0 "src\Ui\DispatchWidget.py" ki 21/12/10 17:39:44
	show computed feed, points rate

 trace 302: +0 "src\Ui\DispatchWidget.py" ki 21/12/10 17:41:33
	show path kpi and segments metrics

 module-dispatch, API, clean 303: +0 "src\Dispatch\DispatchEngine.py" ki 21/12/11 21:22:14
	clean up DeviceEngine property methods

