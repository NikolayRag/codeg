
# CNC GCode layout and dispatch workshop


## *Purpose*


Layouter and CNC dispatcher

Basic entities:

...

## *Install & Requirements*

* No engraver setup routines
* Specific config
    GRBL 2D engraver



...

## *Parts*




### Scene

<<<<<<< Updated upstream
*New
*Load
*Save
*Import/Drag/Paste
-
=======
* New
* Load
* Save
* Import
* Paste
* ...
>>>>>>> Stashed changes



### Geometry


*Solo/Unsolo tbd
-



### Marks





<<<<<<< Updated upstream
*Pan/zoom
*Select
*Control mode tbd
-
=======
### Viewport

* Pan/zoom
* Select
* ...
>>>>>>> Stashed changes


Issues:
* SVG pixel-size jitter
* ...



~~~~~~~~~~~~~~~~~~~~~~~

### Dispatch

* duty cycle
* session queue tbd
* ...



#### Dispatch/Device

* scan/rescan
* recover
 * reset/home
 * guide
* ...




#### Dispatch/Session

* controls
 * disconnect
 * start-pause/unpause-stop
* Stats log
* Tracer Focus and Painting
* ...


## *Issues*:
* Device routines are far from being correct for any abnormal device behavior.
* Having Tracer switched Live/Shapes on can result in speed jitter at high speed,
which can be incompatible with specific cut requirements.
* ...
