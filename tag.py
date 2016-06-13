"""
    Functions for music files tagging.
"""

from recognize import recognize
from database import getTags
import eyed3
import settings
import os


def tagFolder(path, status=None, aborted=[False]):
    """
        Tags all file in a given folder.
        Args:
            path: path to the folder.
        Returns:
            List of files which couldn't be tagged.
    """
    res = []

    nfiles = 0
    for root, dirs, files in os.walk(path):
      for filename in files:
        nfiles += 1
    prog = 0
 
    for root, dirs, files in os.walk(path):
        if aborted[0] == True:
            break
        for filename in files:
            if aborted[0] == True:
                break
            path2 = root+"/"+filename
            if tagFile (path2)== -1:
                res.append(path2[len(path)+1:])
            prog += 1
            if status is not None:
                status(float(prog) / nfiles)
    return res


def tagFile(path, returnFilePath=False):
    """
        Tags single file and renames it in format Artist - Song name.
        Args:
            path: path to the file.
            returnFilePath: if True function will return new fileName instead of -1
        Retruns:
            0 if tagging was successful.
            -1 if tagging failed.
    """
    # print("Tagging: "+path)
    song_id = recognize(path)
    if song_id == -1:
        return -1
    tags = getTags(song_id)
    af = eyed3.load(path)
    if not af.tag:
        af.initTag()
    af.tag.artist = tags['artist'].decode('utf-8')
    af.tag.title = tags['title'].decode('utf-8')
    if tags['album'] != None:
        af.tag.album = tags['album'].decode('utf-8')
    else:
        af.tag.album = u'';
    if tags['track'] != None:
        af.tag.track_num = tags['track']
    af.tag.save()

    filename, fileExtension = os.path.splitext(path)
    newFilename = settings.rename(path, af.tag.artist, af.tag.title, af.tag.album, fileExtension)
    if returnFilePath:
        return newFilename
    return 0


def tag(path):
    """
        Tags folder or a single music file.
        Args:
            path: path to file or folder.
        Returns:
            List of files for which tagging failed.
    """
    # TODO: implement it using
    pass
