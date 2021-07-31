+feature, file, graphics 1: +0 "src\Ui\AppWindow.py" ki 21/07/26 05:38:38
	load SVG

+feature, file 2: +0 "src\Ui\AppWindow.py" kii 21/07/25 16:29:21
	deal with recent files

 feature, file 3: +0 "src\Ui\AppWindow.py" ki 21/07/26 05:38:40
	allow picking from Recent files list

 svg, feature 4: +0 "src\Ui\AppWindow.py" ki 21/07/26 05:52:15
	zoom by wheel

 svg, feature 5: +0 "src\Ui\AppWindow.py" ki 21/07/26 05:52:31
	pan by mouse

 svg, feature 6: +0 "src\Ui\AppWindow.py" ki 21/07/26 05:53:10
	smooth animated zoom

+spec, module-data 7: +0 "src\__main__w.py" ki 21/07/31 02:59:50
	read svg

+spec, module-data 8: +0 "src\GGData\GGData.py" ki 21/07/31 16:30:49
	save gcode

 spec, module-data 9: +0 "src\__main__w.py" ki 21/07/28 03:36:44
	operate project data

 spec, module-data 10: +0 "src\__main__w.py" ki 21/07/28 03:36:06
	operate scene data

=spec, module-data 11: +0 "src\GGData\GGData.py" ki 21/07/31 16:33:39
	read/save own format

+spec, module-ui 12: +1 "src\__main__w.py" ki 21/07/31 02:59:35
	show scene

+spec, module-ui, proto 13: +0 "src\__main__w.py" ki 21/07/31 02:59:34
	render from xml svg

+spec, module-ui 14: +0 "src\__main__w.py" ki 21/07/31 02:58:53
	render from module-data

 spec, module-ui, viewport 15: +0 "src\__main__w.py" ki 21/07/31 02:59:36
	basic mouse zoom, pan and reset

 spec, module-ui 16: +0 "src\__main__w.py" ki 21/07/28 06:14:53
	layers

=spec, module-dispatch, proto 17: +0 "src\__main__w.py" ki 21/07/31 16:33:15
	send to serial-usb (arduino)

 spec, module-data 18: +0 "src\__main__w.py" ki 21/07/31 16:32:56
	standalone dispatcher codegg

 spec, module-data 19: +0 "src\__main__w.py" ki 21/07/28 06:20:08
	send to codegg

 module-ui, error 20: +0 "src\Ui\AppWindow.py" ki 21/07/31 02:32:41
	handle errors, maybe status string

!module-ui, file 21: +0 "" ki 21/07/31 03:32:28
	dup

=module-ui, ux 22: +0 "src\Ui\Ui.py" ki 21/07/31 16:32:30
	make time consuming functions, like saveload, interruptable

=module-ui, ux 23: +0 "src\Ui\Ui.py" ki 21/07/31 16:28:59
	show progress for time consuming operations

!module-data, formats 24: +0 "" ki 21/07/31 16:33:32
	dup

=module-data, formats 25: +0 "src\GGData\GGData.py" ki 21/07/31 16:30:23
	load .nc gcode

!module-data, formats 26: +0 "src\GGData\GGData.py" ki 21/07/31 16:30:39
	

=module-ui, ux 27: +0 "src\Ui\Ui.py" ki 21/07/31 16:32:14
	allow append gcode from text field (paste)

 module-ui 28: +0 "src\Ui\AppWindow.py" ki 21/07/31 16:35:02
	add credits: About, License, Github

