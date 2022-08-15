import cv2
import os
import numpy as np
import math
from PIL import Image


def rotation(image, angleInDegrees):
	# copied from https://stackoverflow.com/a/52477601
    h, w = image.shape[:2]
    img_c = (w / 2, h / 2)

    rot = cv2.getRotationMatrix2D(img_c, angleInDegrees, 1)

    rad = math.radians(angleInDegrees)
    sin = math.sin(rad)
    cos = math.cos(rad)
    b_w = int((h * abs(sin)) + (w * abs(cos)))
    b_h = int((h * abs(cos)) + (w * abs(sin)))

    rot[0, 2] += ((b_w / 2) - img_c[0])
    rot[1, 2] += ((b_h / 2) - img_c[1])

    outImg = cv2.warpAffine(image, rot, (b_w, b_h), flags=cv2.INTER_CUBIC)
    return outImg

def process(folder, out_folder, n_col=None, reverse=False, offset_begin=0, offset_end=0, angle=0):
	# folder: where the image sequence is stored.
	# out_folder: where to save the output image.
	# n_col: number of columns.
	# reverse: False -> from 1 to N; True -> from N to 1.
	# offset_{begin, end}: ignore the first X images and the last Y images.
	# angle: rotate X degrees.

	img_list = []
	for root, ds, fs in os.walk(folder):
		for f in fs:
			if f[0] != ".":
				img_list.append(f)
	img_list.sort()	
	n_img = len(img_list) - offset_end - offset_begin
	if n_col == None:
		n_col = n_img

	result = cv2.imread(os.path.join(folder, img_list[0]))
	w0 = result.shape[1]
	h0 = result.shape[0]
	result = rotation(result, angle)
	w = result.shape[1]
	h = result.shape[0]

	for i in range(n_col):
		idx = int(round((n_img - 1) * i / (n_col - 1)))
		if reverse:
			idx = n_img - idx - 1
		idx += offset_begin
		print("processing " + img_list[idx])
		img = cv2.imread(os.path.join(folder, img_list[idx]))
		img = rotation(img, angle)
		x1 = int(round(i*w/n_col))
		x2 = int(round((i+1)*w/n_col))
		result[0:h, x1:x2] = img[0:h, x1:x2]

	# restore rotation
	result = rotation(result, -angle)
	w = result.shape[1]
	h = result.shape[0]
	result = result[int(math.ceil(h/2-h0/2)):int(math.floor(h/2+h0/2)), int(math.ceil(w/2-w0/2)):int(math.floor(w/2+w0/2))]
		
	out_name = "_".join(["output", str(n_col), ("desc" if reverse else "asc"), str(offset_begin), str(offset_end), str(angle)]) + ".jpg"
	# cv2.imwrite(os.path.join(out_folder, out_name), result)

	# The image may have special color profile, e.g. ITU-R BT.2020 Reference Display
	# OpenCV supports sRGB only....
	# So PIL is used here
	result = Image.fromarray(cv2.cvtColor(result, cv2.COLOR_BGR2RGB))
	img = Image.open(os.path.join(folder, img_list[0]))
	result.save(os.path.join(out_folder, out_name), icc_profile=img.info.get('icc_profile'))


process('./timelapse/tokyo-tower', './timelapse', n_col=11, reverse=False, offset_begin=100, offset_end=0, angle=30)
print('done.')
