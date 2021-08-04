+feature, file, graphics 1: +0 "src\Ui\AppWindow.py" kii 21/07/26 05:38:38
	load SVG

+feature, file 2: +0 "src\Ui\AppWindow.py" kii 21/07/25 16:29:21
	deal with recent files

 feature, file 3: +0 "src\Ui\AppWindow.py" kii 21/08/02 21:40:49
	allow picking from Recent files list

+svg, feature 4: +0 "src\Ui\SvgViewport.py" kii 21/08/02 19:14:43
	zoom by wheel within center-mouse

=module-ui, feature 5: +0 "" ki 21/08/03 02:38:56
	pan by mouse

 module-ui, feature 6: +0 "src\Ui\SvgViewport.py" kii 21/08/02 21:02:22
	smooth animated zoom

+spec, module-data 7: +0 "src\__main__w.py" kii 21/07/31 02:59:50
	read svg

+spec, module-data 8: +0 "src\GGData\GGData.py" kii 21/07/31 16:30:49
	save gcode

 spec, module-data 9: +0 "src\__main__w.py" kii 21/07/28 03:36:44
	operate project data

 spec, module-data 10: +0 "src\__main__w.py" kii 21/07/28 03:36:06
	operate scene data

-spec, module-data 11: +0 "src\GGData\GGData.py" ki 21/08/03 02:42:06
	read/save own format

+spec, module-ui 12: +1 "src\__main__w.py" kii 21/07/31 02:59:35
	show scene

+spec, module-ui, proto 13: +0 "src\__main__w.py" kii 21/07/31 02:59:34
	render from xml svg

+spec, module-ui 14: +0 "src\__main__w.py" kii 21/07/31 02:58:53
	render from module-data

+module-ui, viewport, ux 15: +0 "src\Ui\SvgViewport.py" ki 21/08/03 02:38:35
	basic mouse navigation

!module-ui, viewport 16: +0 "" ki 21/08/04 06:11:58
	dup

=spec, module-dispatch 17: +0 "src\Dispatch\Dispatch.py" ki 21/08/04 06:46:08
	send to serial-usb (arduino)

 spec, module-dispatch 18: +0 "src\GGData\GGData.py" kii 21/08/02 21:19:55
	standalone dispatcher codegg

 spec, module-dispatch 19: +0 "src\GGData\GGData.py" kii 21/08/02 21:16:57
	send to codegg

 module-ui, error 20: +0 "src\Ui\AppWindow.py" kii 21/07/31 02:32:41
	handle errors, maybe status string

!module-ui, file 21: +0 "" kii 21/07/31 03:32:28
	dup

-module-ui, ux 22: +0 "src\Ui\Ui.py" ki 21/08/04 06:16:04
	make time consuming functions, like saveload, interruptable

-module-ui, ux 23: +0 "src\Ui\Ui.py" kii 21/08/02 21:18:43
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

 module-ui, widgets 33: +0 "src\Ui\AppWindow.py" kii 21/08/02 05:05:03
	zoom slider

 module-ui, widgets 34: +0 "src\Ui\AppWindow.py" kii 21/08/02 05:05:28
	transform reset

!module-ui, widgets 35: +0 "src\Ui\AppWindow.py" kii 21/08/02 05:10:07
	zoom factor 

 module-ui, API 36: +0 "src\Ui\SvgViewport.py" kii 21/08/02 06:13:19
	make viewport interaction callbacks

-module-ui, viewport 37: +0 "src\Ui\SvgViewport.py" kii 21/08/02 21:57:59
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

+module-ui, viewport, ux 44: +0 "src\Ui\SvgViewport.py" ki 21/08/03 02:17:12
	react on window resize

+module-ui, ux 45: +0 "src\Ui\SvgViewport.py" kii 21/08/02 20:34:09
	stop scale-moving beyond limits

=module-ui 46: +0 "" ki 21/08/03 13:39:59
	fill connection port list

 module-dispatch, module-ui, ux 47: +0 "src\Ui\AppWindow.py" ki 21/08/03 19:25:49
	change device list to button+list

 module-ui 48: +0 "src\Dispatch\Dispatch.py" ki 21/08/03 13:12:51
	update device list

 module-ui, ux 49: +0 "" ki 21/08/04 06:11:17
	save/restore active device between sessions

 module-ui 50: +0 "src\Ui\AppWindow.py" ki 21/08/03 19:31:08
	add style

=module-ui, ux 51: +0 "" ki 21/08/04 06:13:01
	layer control

 fix 52: +0 "src\Ui\Ui.py" ki 21/08/04 06:08:23
	odd branching solution

+fix, module-ui 53: +0 "src\Ui\AppWindow.py" ki 21/08/04 06:40:29
	reset layers selection at reload

-module-ui, ux 54: +0 "src\Ui\AppWindow.py" ki 21/08/04 07:10:28
	mouse hover layers

