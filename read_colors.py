from __future__ import print_function
from __future__ import division

import pprint
import math
import pprint
import csv

colors=[]

knowncolors="knowncolors.csv"

def savecolors(data=colors,path=knowncolors):
    """
    Write data to a CSV file path
    """
    with open(path, "w") as csv_file:
        writer = csv.writer(csv_file, delimiter=',')
        for line in data:
            writer.writerow(line)

def read_colors_def(data=colors,path=knowncolors):
	'''
	read color definition from CSV file
	'''
	with open(path,"r") as csv_file:
		reader = csv.reader(csv_file,delimiter=',')
		for row in reader:
			#print (row)
			#print(row[0])
			#print(eval(row[1]))
			colors.append([row[0],eval(row[1]),eval(row[2])])
			#print (colors[:1])

def addnewcolor(innewcolor):
	colors.append(innewcolor)

def distance2color(incolor,basecolor):
    return math.sqrt((incolor[0] - basecolor[0])**2 + (incolor[1] - basecolor[1])**2 + (incolor[2] - basecolor[2])**2)

def distance2hsv(incolor,basecolor):
	print("Comparing {} and {}".format(incolor[0],basecolor[0]))
	#diff = incolor[0]-basecolor[0]
	diff = math.sqrt( (incolor[0] - basecolor[0])**2 
					# + (incolor[1] - basecolor[1])**2 
					# + (incolor[2] - basecolor[2])**2
					)
	print ("difference is {}".format(abs(diff)))
	return (abs(diff))

def identifyhsv(inhsv):
	'''
	returns a string of the color based on HSV average
	'''
	# add_hsv()
	print("inhsv is {}".format(inhsv))
	studyhsv = []

	# do the average of the Hue band
	for hsv in colors:
		print("hsv {}".format(hsv))
		studyhsv.append(distance2hsv(inhsv,hsv[2]))
	print("Min hsv distance : {}".format(min(studyhsv)))
	print("Index of color:{}".format( studyhsv.index(min(studyhsv))))
	print ("Return statement is {}".format(colors[studyhsv.index(min(studyhsv))][0]))
	return colors[studyhsv.index(min(studyhsv))][0]

def identifycolor(incolor):
	'''
	return a string containing the name of the color, based on RGB average
	'''
	# read_colors()
	studycolor = []
	for color in colors:
		studycolor.append(distance2color(incolor,color[1]))
	print("min rgb distance is {}".format(min(studycolor)))
	print( studycolor.index(min(studycolor)))
	return colors[studycolor.index(min(studycolor))][0]

if __name__ == "__main__":
	read_colors_def()
	studycolor = []
	for color in colors:
		dist = distance2color((244,200,0),color[1])
		studycolor.append(dist)
	pprint.pprint(studycolor)
	minfound = min(studycolor)
	indexfound = studycolor.index(minfound)

	print(identifycolor((0,200,0)))


