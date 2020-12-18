#!/usr/bin/env python3
# Move all files found in the current folder or subfolders into folders
# named <year>-<month>, e.g. 2019-05.
# The new subfolders become siblings to the current folder.

import os
import time
import shutil
import sys
from datetime import datetime
from PIL import Image, ExifTags

if len(sys.argv) > 1:
  src_folder = sys.argv[1]
else:
  src_folder = '.'

root_folder = os.path.join(src_folder, os.pardir)


def make_unique(existing_file):
  basename = os.path.basename(existing_file)
  head, tail = os.path.splitext(basename)
  dst_dir = os.path.dirname(existing_file)
  dst_file = os.path.join(dst_dir, basename)
  # rename if necessary
  count = 0
  while os.path.exists(dst_file):
      count += 1
      dst_file = os.path.join(dst_dir, '%s-%d%s' % (head, count, tail))
  return (dst_file)

def creation_date(foto_file):
  try:
    img = Image.open(foto_file)
    exif = img.getexif()
    date_taken_str = exif.get(36867)
    date_taken = datetime.strptime(date_taken_str, '%Y:%m:%d %H:%M:%S').date()
    return(date_taken)
  except:
    pass
  return(datetime.fromtimestamp(os.path.getmtime(foto_file)))

for root, directories, filenames in os.walk(src_folder):
  for filename in filenames:
    file = os.path.join(root, filename)
    time.gmtime(os.path.getmtime(file))

    foto_date = creation_date(file)
    year_month = foto_date.strftime("%Y-%m")

    target_folder = os.path.join(root_folder, year_month)
    target_file = os.path.join(target_folder, filename)
    while os.path.exists(target_file):
      print(target_file, ' exists')
      target_file = make_unique(target_file)
      print('using',  target_file)
    os.makedirs(target_folder, exist_ok=True)
    print('move "', file, '" to "', target_file, '"')
    shutil.move(file, target_file)
