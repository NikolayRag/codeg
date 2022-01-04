# CNC GCode layout and dispatch workshop


Purpose
=======

Layouter and CNC dispatcher




Install & Requirements
======================

*No engraver setup routines
*Specific config
	GRBL 2D engraver
-




Layouting
=========




Scene
-----

*New
*Load
*Save
*Import
*Paste
-




Geometry
--------




Marks
-----




Viewport
--------

*Pan/zoom
*Select
-


Issues:
*SVG pixel-size jitter
-




Dispatch
========

*duty cycle
*session queue tbd
-



Dispatch/Device
--------

*scan/rescan
*recover
	reset/home/guide
*Jog guide tbd
-




Dispatch/Session
------

*controls
	disconnect
	start-pause/unpause-stop
*Stats log
*Tracer Focus and Painting
-


Issues:
*Device routines are far from being correct for any abnormal device behavior.
*Having Tracer switched Live/Shapes on can result in speed jitter at high speed,
which can be incompatible with specific cut requirements.
-
