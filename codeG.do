+feature, file, graphics 1: +0 "src\Ui\AppWindow.py" kii 21/07/26 05:38:38
	load SVG

+feature, file 2: +0 "src\Ui\AppWindow.py" kii 21/07/25 16:29:21
	deal with recent files

 feature, file 3: +0 "src\Ui\AppWindow.py" kii 21/09/02 00:47:26
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

=scene, spec, module-data 9: +1 "src\GGData\GGData.py" kii 21/09/08 21:11:30
	operate project data

!spec, module-data 10: +0 "" kii 21/09/08 21:55:55
	dup

=spec, module-data 11: +0 "src\GGData\GGData.py" kii 21/09/08 22:03:53
	read/save own format

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

 spec, module-dispatch 18: +0 "src\GGData\GGData.py" kii 21/08/02 21:19:55
	standalone dispatcher codegg

 spec, module-dispatch 19: +0 "src\GGData\GGData.py" kii 21/08/02 21:16:57
	send to codegg

 module-ui, error 20: +0 "src\Ui\AppWindow.py" kii 21/09/02 00:47:53
	handle errors, maybe status string

!module-ui, file 21: +0 "" kii 21/07/31 03:32:28
	dup

=module-dispatch, ux 22: +0 "src\GGData\GGData.py" kii 21/08/28 18:00:30
	make dispatch interruptable

-module-ui, ux 23: +0 "src\Ui\Ui.py" kii 21/09/09 21:27:51
	show progress for time consuming operations

!module-data, formats 24: +0 "" kii 21/07/31 16:33:32
	dup

 module-data, formats 25: +0 "src\GGData\GGData.py" kii 21/08/02 21:16:10
	load .nc gcode

!module-data, formats 26: +0 "src\GGData\GGData.py" kii 21/07/31 16:30:39
	

 module-data, module-ui, ux 27: +0 "src\Ui\Ui.py" kii 21/08/02 21:19:12
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

 fix, module-ui, viewport 77: +0 "src\Ui\Ui.py" kii 21/09/08 13:43:18
	duplicate hover element topmost

+module-ui, ux 78: +0 "src\Ui\Ui.py" kii 21/08/15 22:10:50
	store/restore window size

 module-ui, ux, fix 79: +0 "src\Ui\AppWindow.py" kii 21/09/08 22:00:28
	make size ignored on maximize

+module-ui, svg, feature 80: +0 "src\Ui\SvgViewport.py" kii 21/08/20 05:30:30
	make SvgCanvas multilayered

-module-ui, svg, feature 81: +0 "" kii 21/08/27 03:13:26
	show grid

 module-data, ux 82: +0 "src\GGData\GGData.py" kii 21/08/20 03:48:29
	parse groups

 ux, module-ui, fix 83: +0 "src\Ui\SvgViewport.py" kii 21/09/08 22:00:28
	fit at init dont work due to obsolete size 

-module-data 84: +0 "src\GGData\GGData.py" kii 21/09/09 17:42:29
	make file load (save) plugin system

+module-dispatch 85: +0 "src\GGData\GGData.py" kii 21/08/28 18:00:25
	Gcode generate in background

!fix, gcode 86: +1 "src\Ui\Ui.py" kii 21/08/22 20:19:01
	

+fix, gcode 87: +0 "src\Ui\Ui.py" kii 21/08/28 18:02:01
	place svg layers more generally

-fix, gcode 88: +0 "src\Ui\Ui.py" kii 21/09/03 02:02:12
	use dispatch both for file save

-ux, module-ui, fix 89: +0 "src\Ui\SvgViewport.py" kii 21/08/28 18:03:13
	place grid correctly

=ux, module-ui, fix 90: +0 "src\GGData\GGData.py" kii 21/09/08 22:03:51
	respect units - both svg and device

-viewport, API 91: +0 "src\Ui\SvgViewport.py" kii 21/09/02 04:16:45
	add class-level SVG runtime generator signal/slot

 feature 92: +0 "src\GGData\GGData.py" kii 21/09/08 21:11:27
	multiple sources scene

=scene, feature 93: +0 "src\__main__w.py" kii 21/09/08 19:01:42
	store scene layer and layout state

 viewport, fix 95: +0 "src\Ui\SvgViewport.py" kii 21/08/28 15:52:23
	clip max scale by render limit

!module-ui, ux, scene 96: +0 "src\Ui\AppWindow.py" kii 21/08/29 16:52:03
	

 viewport, fix, solve 97: +0 "src\Ui\SvgViewport.py" kii 21/09/01 21:59:23
	decide how to paint different layer sizes

 module-ui, optimize 98: -1 "src\Ui\Ui.py" kii 21/09/02 01:04:33
	prevent doubling by difference change

!module-ui, optimize 99: +0 "src\GGen\GGen.py" kii 21/09/02 03:40:33
	

 gcode, feature 100: +0 "src\GGData\GGData.py" kii 21/09/08 21:40:03
	allow flexible filters for gcode

+module-ui 101: +0 "src\Ui\Ui.py" kii 21/09/08 02:52:08
	styles for selected-hovered-visible matrix

+module-ui, fix 102: +0 "src\Ui\Ui.py" kii 21/09/02 04:05:16
	bulk update layer change

+module-ui, module-data, API 103: +0 "src\Ui\Ui.py" kii 21/09/08 02:52:25
	move geo decorators to data

-module-dispatch, decide 104: +0 "src\GGData\GGData.py" kii 21/09/09 23:33:23
	move to dispatch

 module-data, filter, API 105: +0 "src\GGData\GGData.py" kii 21/09/08 21:39:29
	add geo Filter class

!module-data, module-dispatch, device, API 106: +0 "" kii 21/09/05 21:54:01
	--

+decorator, module-data 108: +0 "src\GGData\GGData.py" kii 21/09/08 02:43:01
	get only affected since last request names

!decorator, optimize 109: +0 "" kii 21/09/08 21:13:58
	obsolete

+clean 110: +0 "src\GGData\GGData.py" kii 21/09/07 22:45:38
	use namedRef

-mark, optimize 111: +0 "src\GGData\Geoblock.py" ki 21/09/12 18:27:51
	dramatically slow apply

=mark, feature 112: +0 "src\GGData\GGData.py" ki 21/09/12 18:26:55
	complex mark

=scene, module-ui, ux 113: +0 "src\GGData\Scene.py" ki 21/09/12 18:21:41
	assignable layer marks holding control data

=module-ui, fix 114: +0 "src\Ui\AppWindow.py" kii 21/09/08 13:42:53
	change vis for select-all case

 ux 115: -1 "src\Ui\Ui.py" kii 21/09/08 18:41:16
	allow to choose style by commandline

=ux, module-ui 116: +0 "src\Ui\Ui.py" kii 21/09/08 18:41:48
	choose style in app settings

=ux, module-ui 117: +0 "src\Ui\Ui.py" kii 21/09/08 18:42:04
	add app settings

-refactor, module-ui, module-data 118: +0 "src\Ui\Ui.py" kii 21/09/09 21:26:33
	clean for minor import

-refactor, module-ui, module-data 119: +0 "src\Ui\Ui.py" kii 21/09/09 21:27:02
	clean for dispatch

 refactor, module-ui, module-data 120: +0 "src\Ui\Ui.py" kii 21/09/09 21:27:41
	clean, previous size

+module-data, fix 121: +0 "src\GGen\GGen.py" kii 21/09/09 22:20:25
	go to .items() for ElementTree

