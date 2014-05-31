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
parser.add_argument('-T', action="store", dest="newTitle", default=False,help="change title")
parser.add_argument('-D', action="store", dest="album", default=False,help="change album")
parser.add_argument('-A', action="store", dest="artist", default=False,help="change Artist")
parser.add_argument('-g', action="store", dest="genre", default=False,help="change genre")
parser.add_argument('-t', action="store", dest="newTags", default=False,help="change tags (one letter for each)")
parser.add_argument('-a', action="store_true", dest="printAll", default=False,help="show all tags")
parser.add_argument('file')

params = parser.parse_args()

rating=""
update=True

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

if params.printAll:
	update=False

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

if params.newTags:
    tags = "@%s@" %(params.newTags)
    # !!! put old tags in a set so as to not destroy them
    newTitle = re.sub("@.*@","", newTitle)
    newTitle = newTitle + tags
    update = True

if update:
    song["title"] = newTitle
    song["artist"]= params.artist
    song["album"]= params.album
    song["genre"]= params.genre
    song.save()
    print "Changed from '%s' to '%s'" %(oldTitle,newTitle)

elif params.printAll:
    for k,v in song.tags.items():
        print "'%s' %s" % (k,v)

