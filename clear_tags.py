#!/usr/bin/python
##
#  Clear tags from given files and rename to random string.
#  Using: python clear_tags.py [paths to mp3 file...]
#     eg. python clear_tags.py song1.mp3 song2.mp3
##

import eyed3
import sys
import re
import random
import string

r = re.compile('^.*\.mp3$')
mp3_list = filter(r.match, sys.argv)

for path in mp3_list:
    try:
        af = eyed3.load(path)
        af.initTag()
        af.tag.save()
        rand_name = ''.join(random.choice(string.ascii_uppercase
            + string.digits) for _ in range(10))
        af.rename(rand_name)
        print "Clearing tags from path: ", path
        print "New file name: ", rand_name
    except:
        print "ERROR: Probably wrong path: ", path
