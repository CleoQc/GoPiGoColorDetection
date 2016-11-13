from __future__ import print_function
from __future__ import division
from builtins import input

from PIL import Image
import sys
import math
import pprint
import read_colors
from io import BytesIO
from subprocess import call
from time import sleep
from picamera import PiCamera

idealsize = (400,400)

def getrbg(channel):
	rgb=[]
	avgrgb=[] #average rgb
	for i in range(3):
		rgb.append(list(channel[i].getdata()))
		avgrgb.append(sum(rgb[i])/len(rgb[i]))
		print ("avg rgb:{}".format(avgrgb[i]))
	return (avgrgb[0],avgrgb[1],avgrgb[2])

def gethsv(channel):

	hsv=[]
	avghsv=[] #average rgb
	for i in range(3):
		hsv.append(list(channel[i].getdata()))
		avghsv.append(sum(hsv[i])/(255.0*len(hsv[i])))
		print ("avg hsv: {}".format(avghsv[i]))
	return ((avghsv[0],avghsv[1],avghsv[2]))


def get_colors_from_file():
	global im
	im = Image.open("./{}.jpg".format(imagename))

def extract_color(im):
	# make image smaller to avoid noise
	# also makes it faster to study
	# local_im = im.resize(idealsize)

	local_im = im
	# print("Image size is {}".format(im.size))

	# take the central part which avoids lots of noise
	local_im = local_im.crop((im.size[0]//4,
				im.size[1]//4,
				im.size[0]*3//4,
				im.size[1]*3//4))
	# print("local_im size is {}".format(local_im.size))

	local_im.save("small.jpg")
	channel = local_im.split()

	local_hsv = local_im.convert('HSV')
	# print("Bands are {}".format(local_hsv.getbands()))
	# # print("type of local_hsv: {}".format(type(local_hsv)))
	hsv_channel = local_hsv.split()
	# pprint.pprint("local_HSV just one pixel: {}".format(list(local_hsv.getdata()[200])))
	# hsv_channel = local_hsv.split()

	return(getrbg(channel),gethsv(hsv_channel))

def learn_color(im):

	go = input("Press the Enter key when ready:")
	newrgb,newhsv = extract_color(im)
	newcolor = input("I am seeing \n{} in rgb or \n{} in hsv. \nWhat name should go with that color? ".format(newrgb,newhsv))
	read_colors.addnewcolor([newcolor.upper(),newrgb,newhsv])
	read_colors.savecolors()
	print (newrgb,newhsv)
	return ("{}.jpeg".format(newcolor))


def identify_color(im):

	extractedrgb,extractedhsv = extract_color(im)

	# print("Getting HSV: {}".format(gethsv(local_hsv)))
	rgb_color = read_colors.identifycolor(extractedrgb)
	print("Color as identified by RGB is {}".format(rgb_color))
	hsv_color = read_colors.identifyhsv(extractedhsv)
	print("Color as identified by HSV is {}".format(hsv_color))
	return (rgb_color, hsv_color	)



if __name__ == '__main__':


	tmp_img_name = "tmp.jpg"
	stream = BytesIO()
	camera = PiCamera()
	camera.resolution=(1280,720)
	camera.start_preview()
	sleep(2)

	cmd_beg= 'espeak -ven+f1 '
	#cmd_end= ' | aplay /home/pi/Desktop/Text.wav  2>/dev/null' # To play back the stored .wav file and to dump the std errors to /dev/null
	cmd_end= ' 2>/dev/null' # To play back the stored .wav file and to dump the std errors to /dev/null
	last_color = ""

	i = 0
	if len(sys.argv) == 2 and sys.argv[1].upper() == "LEARN":
		while True:
			camera.capture(tmp_img_name)	
			im = Image.open(tmp_img_name)
			im_name = learn_color(im)
			im.save(im_name)
	elif len(sys.argv)==1:	
		while i==0:
			i+=1
			camera.capture(tmp_img_name)	
			im = Image.open(tmp_img_name)
			im.save("test.jpg")

			read_colors.read_colors_def()
			rgbstr,hsvstr = identify_color(im)
			print(rgbstr,hsvstr)
			if hsvstr != last_color:
				call([cmd_beg+"I_see_"+hsvstr+cmd_end], shell=True)
				last_color = hsvstr
	else:
		print("I don't understand")
	camera.close()

