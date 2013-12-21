#!/usr/bin/env python2.7
import mutagen.oggvorbis
import argparse
import re
# from mutagen.mp3 import EasyMP3 as MP3


parser = argparse.ArgumentParser(description='Simple command-line OGG Vorbis tagger')
parser.add_argument('-5', action="store_true", dest="fiveStars", default=False,help="set rating to 5 star")
parser.add_argument('-4', action="store_true", dest="fourStars", default=False,help="set rating to 4 star")
parser.add_argument('-3', action="store_true", dest="threeStars", default=False,help="set rating to 3 star")
parser.add_argument('-0', action="store_true", dest="removeStars", default=False,help="remove rating")
parser.add_argument('-t', action="store", dest="newTitle", default=False,help="change title")
parser.add_argument('-a', action="store_true", dest="printAll", default=False,help="show all tags")
parser.add_argument('file')

params = parser.parse_args()

rating=""
update=False

# easyMP3 = MP3(params.file)
# easyMP3.pprint()
# exit(0)

song = mutagen.oggvorbis.Open(params.file)

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



oldTitle = song.tags['title'][0]
newTitle = oldTitle

if params.newTitle:
    newTitle = params.newTitle
    update = True

if updateRating:
    if rating != "":
        rating = " !!%s" %(rating)
    newTitle = re.sub(" !!\d", "", newTitle)
    newTitle = newTitle + rating
    update = True

if update:
    song["title"] = newTitle
    song.save()
    print "Changed from '%s' to '%s'" %(oldTitle,newTitle)

elif params.printAll:
    for k,v in song.tags.items():
        print "'%s' %s" % (k,v)

