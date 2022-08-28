# CNC GCode layout and dispatch workshop


## Purpose


Layouter and CNC dispatcher





## Install & Requirements

* No engraver setup routines
* Specific config
	GRBL 2D engraver



## Layouting




### Scene

* New / Load / Save
* Import / Drag / Paste geometry




### Viewport

* Pan / zoom
* Select
* Transform
* Control mode tbd


Issues:
* SVG pixel-size jitter



### Geometry

* Solo/Unsolo tbd


### Marks



~~~~~~~~~~~~~~~~~~~~~~~

## Dispatch

* duty cycle
* session queue tbd



### Device

* scan/rescan
* recover
	* configure and preset
	* reset/home
	* guide


### Dispatch Session

* controls
	* disconnect
	* start-pause/unpause-stop
* Stats log
* Tracer Focus and Painting

---

## Issues for b version:
* Device routines are far from being correct for any abnormal device behavior.
* Having Tracer switched Live/Shapes on can result in speed jitter at high speed,
which can be incompatible with specific cut requirements.
-
