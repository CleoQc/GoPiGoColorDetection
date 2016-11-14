# GoPiGoColorDetection
GoPiGo can react to colors as seen via the Pi Camera

Two modes to run in:

1. Learning mode
python colors.py learn
You can then put your color samples one by one in front of the camera, and the Pi will extract the dominant color and ask you for the name of that color. Once you've gone through all your samples, simply use Ctrl-C to exit. The colors are saved in a file names knowncolors.csv

2. Identifying mode
The GoPiGo will detect a color change and name the color in front of it. 

