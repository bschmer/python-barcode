#! /usr/bin/env python

import numpy as np
import cv2
import os
import sys
import pprint
import glob

paper_size = (279, 216, 3)
image_size = (paper_size[0] - (2*25.4), paper_size[1] - (2*25.4), paper_size[2])

dotspermm = 300/25.4

image_size = (int(image_size[0] * dotspermm), int(image_size[1] * dotspermm), image_size[2])


paths = {}
image = None
for path in sorted(glob.glob('outfile_*.png')):
    index, size = [int(x) for x in path.replace('outfile_', '').replace('.png', '').split('_')]
    if size not in paths:
        paths[size] = {}
    paths[size][index] = path

outindex = 0
for size, v in sorted(paths.items()):
    if image is None:
        image = 255 * np.ones(image_size, dtype=np.uint8)
        yoff = 0
        xoff = 0
    for index, path in sorted(v.items()):
        barcode = cv2.imread(path)
        right = xoff + barcode.shape[1]
        if right > image_size[1]:
            xoff = 0
            yoff += barcode.shape[0]
        bottom = yoff + barcode.shape[0]
        if bottom > image.shape[0]:
            cv2.imwrite('labels%03d.png'% outindex, image)
            outindex += 1
            '''
            cv2.imshow('image', image)
            cv2.waitKey(0)
            cv2.destroyAllWindows()
            '''
            image = 255 * np.ones(image_size, dtype=np.uint8)
            yoff = 0
            xoff = 0
            right = xoff + barcode.shape[1]
            if right > image_size[1]:
                xoff = 0
                yoff += barcode.shape[0]
            bottom = yoff + barcode.shape[0]
            if bottom > image.shape[0]:
                sys.exit(0)
        print yoff, bottom, xoff, right, path, image.shape, barcode.shape
        image[yoff:yoff+barcode.shape[0], xoff:xoff+barcode.shape[1]] = barcode
        xoff += barcode.shape[1]

    

