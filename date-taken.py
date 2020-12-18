#!/usr/bin/env python3
# print date taken of a picture using exif data.

import os
import time
import shutil
import sys
from PIL import Image, ExifTags

img = Image.open(sys.argv[1])
exif = img.getexif()
date_taken = exif.get(36867)
print('date taken: ',  date_taken)
