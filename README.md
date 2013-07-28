A new version of the already old fluffy spheres codebase. More to come!

# Some things to work on
* Screw the physics engine! Use [PyODE](http://pyode.sourceforge.net/) instead!
    - Make input affect the physics engine in a nice way
    - Convert all in-game objects to objects for the phys engine
    - (In progress, done?)
* Text on screen while the graphics engine is running (by PIL atm)
	- (In progress, done?)
* Menus!
* Tesselation of big planes (to get correct lightning)
* Shadows
* Smart culling (begin with normal vector checking)
* Work out the level file format, should be human readable (YAML?)
* Try to work on a world editor
    - Keyboard, mouse support? Use rays in that case
    - Maybe able to load textures and apply those
    - Set starting position
* The _meaning_? Goals, event system etc
* (Check up on the math code, maybe switch to NumPy)
* Music and sound effects (should be handled by pygame)
	- (In progress)
* Better error handling
	- Loading functions etc should have their own error handling,
	not just the big try/except for the entire game

# Plot
The world has been taken over by squares! It's now up to Mr Sphereston and his assistant to save the world and bring back the smooth corners.
