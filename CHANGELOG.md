# Change Log

## 1.2.0 - 6/21/22

### Features
- Added command line option to override terminal window colors. Use -O command line option to enable. If
your terminal supports 256 colors.
- Added option not the clear the screen. Use -W from the command line or `W` command.
- Added command to clear the whole screen wait 2 seconds and start again. Use command `w`.
- Added option to select a color number between 1 and 255 to use as the text color. Use command line option --color_number. If your terminal
supports 256 colors.
- Added option to use italic text. Use command line option -j or --italic or command `j` to
toggle italic text.

### Improvements
- Switching between 1 and 0 modes will not clear the screen. This is the matches the transition
between extended characters and standard characters.
- Fixed wakeup key presses. Key pressed during wakeup scene were buffered until the pymatrix rain continued
causing the undesirable results.
- Some internal code improvements and refactoring.

## 1.1.0 - 1/25/22

### Features
- Added freeze and unfreeze the matrix option by using `f`
- Added option to change the background color by using ctrl + `r, t, y, u, i, o, p, [` or 
by using command line option --background [color]. Colors: red, green, blue, cyan, yellow, magenta and white.
- Added option to change the direction of the matrix to scroll up. Use `v` to toggle scrolling up or -v --reverse from the command line.

### Improvements
- Added color black to the matrix letters

## 1.0.0 - 12/4/21

### Features
* Command line option to disable keys except for `q or Q` to quit.

##  0.5.0 - 11/1/21

### Features
* Added 1 and 0 option by using command line option -z or ```z```
* Added Easter egg to display the wakeup computer scene from The Matrix

### Improvements
* Improved small screen size handling

### Fixes
* Fixed crashes on double space lines option.

### Other
* Removed password option 

## 0.4.0 - 7/21/2020

### Features
* Toggle extended Characters by using ```e```
* Only extended characters if on by using ```E```

## 0.3.0 - 6/28/2020

### Features
* Option to use double space lines using -l or ```l```
* Use shift 0 - 9 to adjust color cycle delay time

## 0.2.0 - 6/8/2020

### Improvements
* Switching colors is faster
* ctrl-c exits more gracefully

### Feature
* Alternate characters by command line options -e or -E

## 0.1.0 - 05/22/2020

* Initial Release