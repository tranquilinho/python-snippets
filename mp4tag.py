#!/usr/bin/env python2.7
from mutagen.mp4 import MP4
import argparse
import re

parser = argparse.ArgumentParser(description='Simple command-line MP4 tagger')
parser.add_argument('-5', action="store_true", dest="fiveStars", default=False,help="set rating to 5 star")
parser.add_argument('-4', action="store_true", dest="fourStars", default=False,help="set rating to 4 star")
parser.add_argument('-3', action="store_true", dest="threeStars", default=False,help="set rating to 3 star")
parser.add_argument('-0', action="store_true", dest="removeStars", default=False,help="remove rating")
parser.add_argument('-f', action="store_true", dest="printFields", default=False,help="show the fields used")
parser.add_argument('-t', action="store", dest="newTitle", default=False,help="change title")
parser.add_argument('-a', action="store_true", dest="printAll", default=False,help="show all MP4 info")
parser.add_argument('file')

params = parser.parse_args()

rating=-1
update=False
audio = MP4(params.file)
oldTitle=audio["\xa9nam"][0]
newTitle=oldTitle

if params.printFields:
    print audio.tags.keys()

newSortTitle=None
if "sonm" in audio.tags.keys():
    oldSortTitle=audio["sonm"][0]
    newSortTitle=oldSortTitle

artist=audio["\xa9ART"][0]

if "\xa9cmt" in audio.tags.keys():
    comments=audio["\xa9cmt"][0]

updateRating = True
if params.fiveStars:
    rating="5"
elif params.fourStars:
    rating="4"
elif params.threeStars:
    rating="3"
elif params.removeStars:
    rating=""
else:
    updateRating = False


if params.newTitle:
    newTitle=params.newTitle
    update=True

if updateRating:
    if rating != "":
        rating = " !!%s" %(rating)
    newTitle = re.sub(" !!\d", "", newTitle)
    newTitle = newTitle + rating
    if newSortTitle != None :
        newSortTitle=re.sub("!!\d","",newSortTitle)
        newSortTitle=newSortTitle + " !!%d" %(rating)
    update = True


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
    try:
        print comments
    except:
        pass
