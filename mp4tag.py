#!/usr/bin/env python2.7
from mutagen.mp4 import MP4
import argparse
import re

parser = argparse.ArgumentParser(description='Simple command-line MP4 tagger')
parser.add_argument('-5', action="store_true", dest="fiveStars", default=False,help="set rating to 5 star")
parser.add_argument('-t', action="store", dest="newTitle", default=False,help="change title")
parser.add_argument('-a', action="store_true", dest="printAll", default=False,help="show all MP4 info")
parser.add_argument('file')

params = parser.parse_args()

rating=-1
update=False
audio = MP4(params.file)
oldTitle=audio["\xa9nam"][0]
newTitle=oldTitle

newSortTitle=None
if "sonm" in audio.tags.keys():
    oldSortTitle=audio["sonm"][0]
    newSortTitle=oldSortTitle
artist=audio["\xa9ART"][0]
comments=audio["\xa9cmt"][0]


if params.fiveStars:
    rating=5

if params.newTitle:
    newTitle=params.newTitle
    update=True

if rating >= 0:
    newTitle=re.sub("!!\d","",newTitle)
    newTitle=newTitle + " !!%d" %(rating)
    if newSortTitle != None :
        newSortTitle=re.sub("!!\d","",newSortTitle)
        newSortTitle=newSortTitle + " !!%d" %(rating)
    update=True

if update:
    audio["\xa9nam"][0]=newTitle
    if newSortTitle != None :
        audio["sonm"][0]=newSortTitle
    audio.save()
    print "Changed from %s to %s" %(oldTitle,newTitle)

elif params.printAll:
    print(audio.tags.keys())
    print(audio.tags.values())
else:
    print "%s - %s " %(artist,oldTitle)
    print comments
