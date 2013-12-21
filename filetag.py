#!/usr/bin/env python2.7

import argparse
import re
import os

parser = argparse.ArgumentParser(description='Simple command-line filename tagger')
parser.add_argument('-5', action="store_true", dest="fiveStars", default=False,help="set rating to 5 star")
parser.add_argument('-4', action="store_true", dest="fourStars", default=False,help="set rating to 4 star")
parser.add_argument('-3', action="store_true", dest="threeStars", default=False,help="set rating to 3 star")
parser.add_argument('-0', action="store_true", dest="removeStars", default=False,help="remove rating")
parser.add_argument('-t', action="store", dest="newTitle", default=False,help="change title")
parser.add_argument('file')

params = parser.parse_args()

rating=-1
update=False

if params.fiveStars:
    rating="5"
if params.fourStars:
    rating="4"
if params.threeStars:
    rating="3"
if params.removeStars:
    rating=""
else:
    rating= "_%ss" %(rating)


if params.newTitle:
    newTitle=params.newTitle
    update=True

if rating >= 0:
    match =  re.search("(.*)\.(.*)$", params.file)
    oldTitle = match.group(1)
    extension = match.group(2)
    newTitle=re.sub("[,!\[\]'\(\)]","",oldTitle)
    newTitle=re.sub(" ","_",newTitle)
    newTitle=re.sub("_[1-5]s$","",newTitle)
    
    newTitle="%s%s.%s" %(newTitle, rating, extension)

    update=True

if update:
    os.rename(params.file, newTitle)
    print "Changed from %s to %s" %(params.file, newTitle)
